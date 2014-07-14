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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui_constraint_results import Ui_Dialog

import os
import csv

class ConstraintResultsDialog(QDialog, Ui_Dialog):
    
    def __init__(self, model):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.setupUi(self)
        self.resultModel = model
        self.constraintTableView.setModel(self.resultModel)
        self.constraintTableView.resizeColumnsToContents()
        
    def export(self):
        """ Export the results to a CSV file """
        
        # Remember the last location in which we saved
        settings = QSettings()
        lastFolder = str(settings.value("constraintchecker/lastSaveFolder", os.sep))
        
        outFileName = str( QFileDialog.getSaveFileName(self, 'Save Query Results', lastFolder, 'Comma Separated Variable Files (*.csv)') )
        
        # Store the path we just looked in
        head, tail = os.path.split(outFileName)
        if head <> os.sep and head.lower() <> 'c:\\' and head <> '':
            settings.setValue("constraintchecker/lastSaveFolder", head)
        
        if len(outFileName) == 0:
            # User hit cancel
            return
        
        # Export the file
        try:
            csvfile = open(outFileName, 'wb')
        except:
            QMessageBox.critical(self, 'Failed to Open File', 'Failed to open %s for writing - perhaps it is open in another application?' % outFileName )
            return
        
        resWriter = csv.writer(csvfile)
        resWriter.writerow( self.resultModel.headerNames )
        for i in range(self.resultModel.rowCount()):
            resWriter.writerow( self.resultModel.fetchRow(i) )
        csvfile.close()
        
