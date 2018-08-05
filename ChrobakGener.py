# -*- coding: utf-8 -*-
from qgis.core import *
from qgis.utils import *

class line():
    
    def __init__(self,geometria):
        self.geometria = geometria
    
    
    def segmantation(self):
        listOfSegments = []
        #for Polyline only
        vertices = self.geometria.asPolyline()
        for point in range(len(vertices)):
                listOfSegments.append(vertices[point])
                
        return listOfSegments
    
    #pewnie usunę bo nie jest identyczne jak od szombary
    def lineCentroid(self):
        centroid = []
        centroid.append(self.geometria.centroid().asPoint().x())
        centroid.append(self.geometria.centroid().asPoint().y())
        return centroid
    
    #ok 237 metrów różnicy między funkcjami
    #przerobić!!!!!!
    def SzmobiCentroid(self):
        A = 0.0
        sc = 0.0
        sc_sum = 0.0
        cx = 0.0
        cy = 0.0
        cx_sum = 0.0
        cy_sum = 0.0
        for i in range(len(self.segmantation())-1):        
            sc = ((self.segmantation()[i][0]*self.segmantation()[i+1][1]) - (self.segmantation()[i+1][0]*self.segmantation()[i][1]))
            cx = ( self.segmantation()[i][0] + self.segmantation()[i+1][0]) * sc
            cy = ( self.segmantation()[i][1] + self.segmantation()[i+1][1]) * sc
            sc_sum = sc_sum + sc
            cx_sum = cx_sum + cx
            cy_sum = cy_sum + cy
        A = sc_sum/2
        centr_x = cx_sum * ( 1/ (6*A))
        centr_y = cy_sum * ( 1/ (6*A))
    
        return [centr_x, centr_y]
    
    def geometryOfSegment(self, startPoint, endPoint):
        segment = QgsGeometry.fromPolyline([QgsPoint(startPoint), QgsPoint(endPoint)])
        
        return segment
    
    #muszę się zastanowić czy potrzebuję podziału na współczynniki
    def segmentDefinition(self, startPoint, endPoint):
        A = startPoint[1] - endPoint[1]
        B = endPoint[0] - startPoint[0]
        C = endPoint[1]*startPoint[0] - startPoint[1]*endPoint[0]
        
        return [A, B, C]

    def segmentIntersection(self, firstLine, secondLine):

        intersectionPoint = QgsGeometry.intersection(firstLine, secondLine).asPoint()
        return intersectionPoint
    
    