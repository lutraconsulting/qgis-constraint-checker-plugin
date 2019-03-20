# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Constraint Checker
                                 A QGIS plugin
 Generate reports of constraints (e.g. planning constraints) applicable to an area of interest.
                              -------------------
        begin                : 2014-03-19
        copyright            : (C) 2014 by Lutra Consulting for Dartmoor National Park Authority
        email                : it@dnpa.gov.uk
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import configparser
import os
import traceback
from qgis.PyQt import uic
from qgis.PyQt.QtCore import Qt, QSettings
from qgis.PyQt.QtWidgets import QFileDialog, QDialog, QTableWidgetItem, QMessageBox, QAbstractItemView

from .utils import dbSafe

ui_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ui', 'ui_configuration.ui')


class ConfigurationDialog(QDialog):

    def __init__(self, iface):
        self.iface = iface
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = uic.loadUi(ui_file, self)

        self.configFilePath = os.path.join(os.path.dirname(__file__), 'config.cfg')
        self.defFlags = Qt.NoItemFlags | Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable
        
        # Populate the PostGIS connection combo with the available connections
        
        # Determine our current preference
        s = QSettings()
        selectedConnection = str(s.value("constraintchecker/postgisConnection", ''))
        
        s.beginGroup('PostgreSQL/connections')
        i = 0
        for connectionName in s.childGroups():
            self.postgisConnectionComboBox.addItem(connectionName)
            if connectionName == selectedConnection:
                # Select this preference in the combo if exists
                self.postgisConnectionComboBox.setCurrentIndex(i)
            i += 1
        s.endGroup()
        
        # Now read the configuration file (if it exists) into the table widget
        try:
            self.readConfiguration()
        except:
            pass

    def readConfiguration(self, filePath=None):
        
        if filePath is None:
            filePath = self.configFilePath
        
        # Clear the QTableWidget in case it contains any old data
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        
        # First set up the TableWidget
        self.tableWidget.setColumnCount(6)
        
        labels = ['Constraint',
                  'Schema',
                  'Table',
                  'Geometry Column',
                  'Search Distance',
                  'Columns For Reporting']
        self.tableWidget.setHorizontalHeaderLabels(labels)
        
        # Read the config
        
        config = configparser.ConfigParser()
        config.read(filePath)
        
        i = 0
        for section in config.sections():
            self.tableWidget.insertRow(i)
            
            editItem = QTableWidgetItem(section, 0)
            editItem.setFlags(self.defFlags | Qt.ItemIsUserCheckable)
            include = config.get(section, 'include')
            if include.lower() == 't':
                editItem.setCheckState(Qt.Checked)
            else:
                editItem.setCheckState(Qt.Unchecked)
            self.tableWidget.setItem(i, 0, editItem)
            
            schema = config.get(section, 'schema')
            editItem = QTableWidgetItem(schema, 0)
            editItem.setFlags(self.defFlags)
            self.tableWidget.setItem(i, 1, editItem)
            
            table = config.get(section, 'table')
            editItem = QTableWidgetItem(table, 0)
            editItem.setFlags(self.defFlags)
            self.tableWidget.setItem(i, 2, editItem)
            
            geom_col = config.get(section, 'geom_column')
            editItem = QTableWidgetItem(geom_col, 0)
            editItem.setFlags(self.defFlags)
            self.tableWidget.setItem(i, 3, editItem)
            
            buffer_distance = config.get(section, 'buffer_distance')
            editItem = QTableWidgetItem(buffer_distance, 0)
            editItem.setFlags(self.defFlags)
            self.tableWidget.setItem(i, 4, editItem)
            
            columns = config.get(section, 'columns')
            editItem = QTableWidgetItem(columns, 0)
            editItem.setFlags(self.defFlags)
            self.tableWidget.setItem(i, 5, editItem)
            
            i += 1
        
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

    def exportConfiguration(self):
        """ User has opted to save the current configuration to a file """
        
        # Determine where we saved last time
        settings = QSettings()
        lastFolder = str(settings.value('constraintchecker/lastExportFolder', os.sep))

        exportFileName, ext_selector = QFileDialog.getSaveFileName(self, 'Export Current Configuration', lastFolder,
                                                         'Constraint Checker Configuration Files (*.ini)')
        if len(exportFileName) == 0:
            # User cancelled
            return
        
        # Store the path we just looked in
        head, tail = os.path.split(exportFileName)
        if head != os.sep and head.lower() != 'c:\\' and head != '':
            settings.setValue('constraintchecker/lastExportFolder', head)
        
        # Export the configuration
        file_name = "{}.ini".format(exportFileName)
        try:
            self.saveConfiguration(file_name)
        except:
            QMessageBox.critical(self.iface.mainWindow(), 'Error', 'Failed to write configuration to %s' % file_name)

    def importConfiguration(self):
        """ User has opted to load a configuration from a file """
        
        # Determine where we saved last time
        settings = QSettings()
        lastFolder = str(settings.value('constraintchecker/lastImportFolder', os.sep))
        
        importFileName, ext_selector = QFileDialog.getOpenFileName(self, 'Import Configuration', lastFolder,
                                                         'Constraint Checker Configuration Files (*.ini)')
        if len(importFileName) == 0:
            # User cancelled
            return
        
        # Store the path we just looked in
        head, tail = os.path.split(importFileName)
        if head != os.sep and head.lower() != 'c:\\' and head != '':
            settings.setValue('constraintchecker/lastImportFolder', head)
        
        # Import the configuration
        try:
            self.readConfiguration(importFileName)
        except:
            QMessageBox.critical(self.iface.mainWindow(), 'Error', 'Failed to read configuration from %s' %
                                 importFileName)

    def saveConfiguration(self, filePath=None):
        """ Run through the configuration, do basic checks on each item 
        and save to the config file """
        
        if filePath is None:
            filePath = self.configFilePath
        
        config = configparser.RawConfigParser()
        for i in range(self.tableWidget.rowCount()):
            
            # Perform checks
            name = ''
            for j in range(6):
                valueString = self.tableWidget.item(i, j).text()
                if len(valueString) == 0:
                    raise Exception('An empty value was seen in column %d, row %d' % (j+1, i+1))
                # Check that the string is not blank
                if j in [1, 2, 3]:
                    # Check that the string is db safe
                    if not dbSafe(valueString):
                        raise Exception('The value in column %d, row %d contained illegal characters. '
                                        'Please ensure the value consists of only letters, numbers, spaces '
                                        'and underscores.' % (j+1, i+1))
                if j == 5:
                    # Split the string and check each component is db safe
                    for val in valueString.split(','):
                        if not dbSafe(val):
                            raise Exception('The value in column %d, row %d contained illegal characters. '
                                            'Please ensure the value consists of a comma separated list of only '
                                            'letters, numbers, spaces and underscores.' % (j+1, i+1))
                if j == 4:
                    # Check the string is a number
                    try:
                        dummy = float(valueString)
                    except:
                        raise Exception('The value in column %d, row %d (%s) does not appear to be a valid number.' %
                                        ((j+1), (i+1), valueString))
                
                if j == 0:
                    name = valueString
                    config.add_section(name)
                    if self.tableWidget.item(i, j).checkState() == Qt.Checked:
                        config.set(name, 'include', 't')
                    else:
                        config.set(name, 'include', 'f')
                elif j == 1:
                    config.set(name, 'schema', valueString)
                elif j == 2:
                    config.set(name, 'table', valueString)
                elif j == 3:
                    config.set(name, 'geom_column', valueString)
                elif j == 4:
                    config.set(name, 'buffer_distance', valueString)
                elif j == 5:
                    config.set(name, 'columns', valueString)
                    
            try:
                with open(filePath, 'w') as config_file:
                    config.write(config_file)
            except:
                raise Exception('Failed to write the configuration to %s' % filePath)

    def removeSelectedRows(self):
        selRanges = self.tableWidget.selectedRanges()
        rowsToRemove = []
        for selRange in selRanges:
            for i in range(selRange.bottomRow(), selRange.topRow()+1 ):
                rowsToRemove.append(i)
        rowsToRemove.sort()
        rowsToRemove.reverse()
        for row in rowsToRemove:
            self.tableWidget.removeRow(row)

    def insertNewRow(self):
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        for i in range(self.tableWidget.columnCount()):
            editItem = QTableWidgetItem('', 0)
            if i == 0:
                editItem.setFlags(self.defFlags | Qt.ItemIsUserCheckable)
                editItem.setCheckState(Qt.Checked)
            else:
                editItem.setFlags(self.defFlags)
            self.tableWidget.setItem(self.tableWidget.rowCount()-1, i, editItem)

    def accept(self):
        
        # Set our connection preference based on the combo-box
        s = QSettings()
        if self.postgisConnectionComboBox.count() > 0:
            connecionName = self.postgisConnectionComboBox.currentText()
            s.setValue("constraintchecker/postgisConnection", connecionName)
            
        try:
            self.saveConfiguration()
        except:
            msg = 'An error occurred when trying to save the configuration. ' \
                  'The details are:\n\n%s' % traceback.format_exc()
            QMessageBox.critical(self, 'Error Saving Configuration', msg)
            return
        
        QDialog.accept(self)
