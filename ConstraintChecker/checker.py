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

# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

from constraint_results_dialog import ConstraintResultsDialog
import psycopg2
import ConfigParser
import os

class ResultModel(QAbstractTableModel):
    
    def __init__(self, colCount, headerNames, parent=None, *args):
        QAbstractTableModel.__init__(self)
        self.colCount = colCount
        # data is a list of rows
        # each row contains the columns
        self.data = []
        self.headerNames = headerNames
        
    def appendRow(self, row):
        if len(row) > self.colCount:
            raise Exception('Row had length of %d which is more than the expected length of %d' % (len(row), self.colCount))
        if len(row) < self.colCount:
            paddingCount = self.colCount - len(row)
            for i in range(paddingCount):
                row.append('')
        self.data.append(row)
    
    def rowCount(self, parent=QModelIndex()):
        return len(self.data)
    
    def columnCount(self, parent=QModelIndex()):
        return self.colCount
    
    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            i = index.row()
            j = index.column()
            
            return self.data[i][j]
        else:
            return None
            
    def fetchRow(self, rowNumber):
        return self.data[rowNumber]
    
    def headerData(self, section, orientation, role = Qt.DisplayRole):
        
        if role != Qt.DisplayRole:
            # We are being asked for something else, do the default implementation
            return QAbstractItemModel.headerData(self, section, orientation, role)
            
        if orientation == Qt.Vertical:
            return section + 1
        else:
            return self.headerNames[section]
    
    

class Checker:
    
    
    def __init__(self, iface, refNumber):
        
        self.iface = iface
        self.refNumber = refNumber
        
        # Read the config
        config = ConfigParser.ConfigParser()
        configFilePath = os.path.join(os.path.dirname(__file__), 'config.cfg')
        config.read(configFilePath)
        
        self.config = []
        for section in config.sections():
            c = {}
            c['name'] = section
            c['schema'] = config.get(section, 'schema')
            c['table'] = config.get(section, 'table')
            c['geom_column'] = config.get(section, 'geom_column')
            c['buffer_distance'] = float( config.get(section, 'buffer_distance') )
            c['columns'] = config.get(section, 'columns').split(',')
            include = config.get(section, 'include')
            if include.lower() == 't':
                c['include'] = True
            else:
                c['include'] = False
            self.config.append(c)
            
        # Determine the largest number of columns requested
        maxColsRequested = 0
        headerNames = ['Site', 'Layer_name']
        for conf in self.config:
            if len(conf['columns']) > maxColsRequested:
                maxColsRequested = len(conf['columns'])
        for i in range(maxColsRequested):
            headerNames.append('Column%d' % (i+1))
        self.resModel = ResultModel(maxColsRequested + 2, headerNames)
        
    
    def display(self):
        # Only display the results if some constraints were detected
        if self.resModel.rowCount() == 0:
            QMessageBox.information(self.iface.mainWindow(), 'No constraints found', 'The query did not locate any constraints.')
            return
        crd = ConstraintResultsDialog(self.resModel)
        crd.exec_()

    
    def getDbCursor(self):
        """
            Creates a psycopg2 connection based on the selected 
            connection and returns a cursor.
            
        """
        
        # Determine our current preference
        s = QSettings()
        selectedConnection = str(s.value("constraintchecker/postgisConnection", ''))
        if len(selectedConnection) == 0:
            # We have not yet specified a connection
            raise Exception('No PostGIS connection has been nominated for performing constraints queries. \n\nPlease select a PostGIS connection using Plugins > Constraint Checker > Edit Configuration \n\nPostGIS connections can be created in the Add PostGIS Table(s) dialog.')
            
        host = str( s.value("PostgreSQL/connections/%s/host" % selectedConnection, '') )
        if len(host) == 0:
            # Looks like the preferred connection could not be found
            raise Exception('The preferred PostGIS connection, %s could not be found, please check your Constrain Checker settings')
        database = str( s.value("PostgreSQL/connections/%s/database" % selectedConnection, '') )
        user = str( s.value("PostgreSQL/connections/%s/username" % selectedConnection, '') )
        password = str( s.value("PostgreSQL/connections/%s/password" % selectedConnection, '') )
        port = int( s.value("PostgreSQL/connections/%s/port" % selectedConnection, 5432) )
        
        dbConn = psycopg2.connect( database = database,
                                   user = user,
                                   password = password,
                                   host = host,
                                   port = port)
        dbConn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        return dbConn.cursor()
    
    
    def check(self, queryGeom, epsg_code):
        
        # Extract QKT from geometry
        wkt = queryGeom.exportToWkt()
        
        cur = self.getDbCursor()
        
        for configItem in self.config:
            if not configItem['include']:
                continue
            queryString = """SELECT """
            for col in configItem['columns']:
                queryString += col + ', '
            # Remove last two chars
            queryString = queryString[:-2]
            queryString += """ FROM "%s"."%s" WHERE ST_Intersects(%s, ST_Buffer(ST_GeomFromText('%s', %d), %f))""" % (configItem['schema'], configItem['table'], configItem['geom_column'], wkt, epsg_code, configItem['buffer_distance'])
            cur.execute(queryString)
            
            # FIXME
            # msg = 'Query on %s returned %d results' % (configItem['name'], cur.rowcount)
            if cur.rowcount > 0:
                
                # Add a title row to the results
                dataRow = ['', '']
                
                # msg += ':\n\n'
                for colName in configItem['columns']:
                    dataRow.append(colName)
                    # msg += colName + '\t'
                self.resModel.appendRow(dataRow)
                for row in cur.fetchall():
                    dataRow = [self.refNumber, configItem['name']]
                    for val in row:
                        dataRow.append(str(val))
                        # msg += val + '\t'
                    self.resModel.appendRow(dataRow)
            # QMessageBox.information(self.iface.mainWindow(), 'DEBUG', msg)
