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
from qgis.core import *
from qgis.gui import *

class FreehandPolygonMaptool(QgsMapTool):
    
    def __init__(self, canvas):
        
        QgsMapTool.__init__(self,canvas)
        self.canvas = canvas
        self.rb = QgsRubberBand(canvas, QGis.Polygon)
        self.rb.setColor(QColor(255, 0, 0, 50))
    
    def activate(self):
        self.rb.reset(QGis.Polygon)
        
    def deactivate(self):
        self.rb.reset(QGis.Polygon)
        
    def canvasMoveEvent(self, ev):
        
        worldPoint = QgsMapToPixel.toMapCoordinates(    self.canvas.getCoordinateTransform(), 
                                                        ev.pos().x(),
                                                        ev.pos().y() )
        self.rb.movePoint(worldPoint)
        
    def canvasPressEvent(self, ev):
        
        if ev.button() == Qt.LeftButton:
            """ Add a new point to the rubber band """
            worldPoint = QgsMapToPixel.toMapCoordinates(    self.canvas.getCoordinateTransform(), 
                                                            ev.pos().x(),
                                                            ev.pos().y() )
            self.rb.addPoint( worldPoint )
        
        elif ev.button() == Qt.RightButton:
            """ Send back the geomertry to the calling 
            class """
            
            self.emit( SIGNAL("geometryReady(PyQt_PyObject)"), self.rb.asGeometry() )
            
        
    def isZoomTool(self):
        return False
    
    def isTransient(self):
        return False
      
    def isEditTool(self):
        return False
