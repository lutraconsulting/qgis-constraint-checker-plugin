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

import os
import csv
from qgis.PyQt import uic
from qgis.PyQt.QtCore import QSettings
from qgis.PyQt.QtWidgets import QDialog, QFileDialog, QMessageBox

ui_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ui', 'ui_constraint_results.ui')


class ConstraintResultsDialog(QDialog):
    
    def __init__(self, model):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = uic.loadUi(ui_file, self)
        self.resultModel = model
        self.constraintTableView.setModel(self.resultModel)
        self.constraintTableView.resizeColumnsToContents()
        
    def export(self):
        """ Export the results to a CSV file """
        
        # Remember the last location in which we saved
        settings = QSettings()
        lastFolder = str(settings.value("constraintchecker/lastSaveFolder", os.sep))
        
        outFileName, ext_selector = QFileDialog.getSaveFileName(self, 'Save Query Results', lastFolder,
                                                      'Comma Separated Variable Files (*.csv)')
        
        # Store the path we just looked in
        head, tail = os.path.split(outFileName)
        if head != os.sep and head.lower() != 'c:\\' and head != '':
            settings.setValue("constraintchecker/lastSaveFolder", head)
        
        if len(outFileName) == 0:
            # User hit cancel
            return
        
        # Export the file
        try:
            csvfile = open(outFileName+'.csv', 'w')
        except:
            msg = 'Failed to open %s for writing - perhaps it is open in another application?' % outFileName
            QMessageBox.critical(self, 'Failed to Open File', msg)
            return
        
        resWriter = csv.writer(csvfile)
        resWriter.writerow(self.resultModel.headerNames)
        for i in range(self.resultModel.rowCount()):
            resWriter.writerow(self.resultModel.fetchRow(i))
        csvfile.close()
