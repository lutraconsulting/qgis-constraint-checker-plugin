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
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from reference_number_dialog import ReferenceNumberDialog
from checker import Checker
from configuration_dialog import ConfigurationDialog
from freehand_polygon_maptool import *
import os.path
import traceback


class ConstraintChecker:

    
    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'constraintchecker_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        # self.dlg = ConstraintCheckerDialog()
        
        self.freeHandTool = FreehandPolygonMaptool(self.iface.mapCanvas())
        
    
    def initGui(self):
        # Create action that will start plugin configuration
        self.existingCheckAction = QAction(
            QIcon(":/plugins/constraintchecker/checker_select_32.png"),
            u"Check Constraints for Existing Polygon", self.iface.mainWindow())
        self.freehandCheckAction = QAction(
            QIcon(":/plugins/constraintchecker/checker_freehand_32.png"),
            u"Check Constraints for Free-hand Polygon", self.iface.mainWindow())
        self.openConfigurationAction = QAction(
            QIcon(":/plugins/constraintchecker/checker_config_32.png"),
            u"Edit Configuration", self.iface.mainWindow())
        # connect the action to the run method
        self.existingCheckAction.triggered.connect(self.checkExistingGeometry)
        self.freehandCheckAction.triggered.connect(self.checkFreehandGeometry)
        self.openConfigurationAction.triggered.connect(self.openConfiguration)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.existingCheckAction)
        self.iface.addToolBarIcon(self.freehandCheckAction)
        self.iface.addPluginToMenu(u"&Constraint Checker", self.existingCheckAction)
        self.iface.addPluginToMenu(u"&Constraint Checker", self.freehandCheckAction)
        self.iface.addPluginToMenu(u"&Constraint Checker", self.openConfigurationAction)
        QObject.connect(self.freeHandTool, SIGNAL("geometryReady(PyQt_PyObject)"), self.receiveFeature)

    
    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&Constraint Checker", self.existingCheckAction)
        self.iface.removePluginMenu(u"&Constraint Checker", self.freehandCheckAction)
        self.iface.removePluginMenu(u"&Constraint Checker", self.openConfigurationAction)
        self.iface.removeToolBarIcon(self.existingCheckAction)
        self.iface.removeToolBarIcon(self.freehandCheckAction)
        QObject.disconnect(self.freeHandTool, SIGNAL("geometryReady(PyQt_PyObject)"), self.receiveFeature)
        
    
    def receiveFeature(self, geom):
        crs = self.iface.mapCanvas().mapRenderer().destinationCrs()
        epsg = int( crs.authid().split('EPSG:')[1] )
        self.iface.mapCanvas().unsetMapTool( self.freeHandTool )
        self.constraintCheck(geom, epsg)

    
    def checkExistingGeometry(self):
        """ The user should already have a feature selected.  Ensure 
        this is the case and then send the geometry to the main 
        function. """
        
        erTitle = 'Select a feature'
        erMsg = 'Please select a single feature in a loaded vector layer.'
        
        if self.iface.mapCanvas().layerCount() < 1:
            QMessageBox.critical(self.iface.mainWindow(), erTitle, erMsg)
            return
        
        currentLayer = self.iface.mapCanvas().currentLayer()
        if currentLayer is None or currentLayer.type() != QgsMapLayer.VectorLayer:
            QMessageBox.critical(self.iface.mainWindow(), erTitle, erMsg)
            return
        
        if currentLayer.selectedFeatureCount() != 1:
            QMessageBox.critical(self.iface.mainWindow(), erTitle, erMsg)
            return
        
        # By this point the user has a single, existing feature selected
        # Now pass the geometry to the query
        
        # Due to an existing bug ? 777
        # We need to fetch the list first before taking off the feature we want
        selFeats = currentLayer.selectedFeatures()
        geom = QgsGeometry( selFeats[0].geometry() )
        authid = currentLayer.crs().authid()
        try:
            epsg = int(authid.split('EPSG:')[1])
        except:
            QMessageBox.critical(self.iface.mainWindow(), 'Failed to determine CRS', 'Please ensure the layer to which the query feature belongs has a CRS set.')
            return
        self.constraintCheck(geom, epsg)
        
    
    def checkFreehandGeometry(self):
        
        self.iface.messageBar().pushMessage("Constraint Checker", \
            "Please digitise your area of interest - Right-click to add last vertex.", \
            level=QgsMessageBar.INFO, duration=10)
        self.iface.mapCanvas().setMapTool(self.freeHandTool)
        
    
    def constraintCheck(self, queryGeom, epsg):
        
        # Prompt the user for a reference number
        refDlg = ReferenceNumberDialog()
        result = refDlg.exec_()
        if result == QDialog.Rejected:
            # User pressed cancel
            return
        
        refNumber = refDlg.getRefNumber()
        
        try:
            c = Checker(self.iface, refNumber)
            c.check(queryGeom, epsg)
            c.display()
        except:
            QMessageBox.critical(self.iface.mainWindow(), 'Query Failed', 'The query failed and the detailed error was:\n\n%s' % traceback.format_exc() )
        
    
    def openConfiguration(self):
        # Display the configuration editor dialog
        d = ConfigurationDialog()
        d.exec_()
        
        
    """
    # run method that performs all the real work
    def run(self):
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result == 1:
            # do something useful (delete the line containing pass and
            # substitute with your code)
            pass
    """
