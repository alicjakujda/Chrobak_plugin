# -*- coding: utf-8 -*-
from qgis.core import *
from qgis.utils import *
from math import sqrt

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
    
    #ok 237 metrów różnicy między funkcjami
    #przerobić!!!!!!
    def lineCentroid(self):
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
    
    def segmentDefinition(self, startPoint, endPoint):
        A = startPoint[1] - endPoint[1]
        B = endPoint[0] - startPoint[0]
        C = endPoint[1]*startPoint[0] - startPoint[1]*endPoint[0]
        
        return [A, B, C]

    #intersekcja musi być oparta na współczynnikach lini, ponieważ nie zawsze obiekty się przecinają geometrycznie ale w przestrzeni tak
    def segmentIntersection(self, firstLine, secondLine):

        if firstLine[0] == 0 and (firstLine[1] == 0 or secondLine[1] == 0) and (firstLine[2] != secondLine[2]):
            intersectionPointX = - secondLine[2] / secondLine[0]
            intersectionPointY = - firstLine[2] / firstLine[1]
            
        elif secondLine[0] == 0 and (firstLine[1] == 0 or secondLine[1] == 0) and (firstLine[2] != secondLine[2]):
            intersectionPointX = - firstLine[2] / firstLine[0]
            intersectionPointY = - secondLine[2] / secondLine[1]
            
        elif (firstLine[0], secondLine[0]) == (0, 0) or (firstLine[1], secondLine[1]) == (0, 0):
            intersectionPointX = None
            intersectionPointY = None
            print "Parallel lines"
            
        else:

            intersectionPointX = (firstLine[1]*secondLine[2]-secondLine[1]*firstLine[2])/(firstLine[0]*secondLine[1]-secondLine[0]*firstLine[1])
            intersectionPointY = - (secondLine[0]*firstLine[2]-firstLine[0]*secondLine[2])/(firstLine[1]*secondLine[0]-secondLine[1]*firstLine[0])
            
        intersectionPoint = [QgsPoint(intersectionPointX, intersectionPointY)]
        
        return intersectionPoint
    
    #stworzyć funkcję w klasie linia z numeracją punktów - jeżeli będzie pierscien to wtedy będzie inna kolejność
    
    #stworzyć funkcję w klasie linia dla pierscienia - jeżeli true to wtedy funkcja z numeracją będzie dla pierscienia


#nie testowany
def epsylon(scale, chosenType):
    if chosenType == 'angular':
        return (scale/1000) * 0.4
    else:
        return (scale/1000) * 0.6

#nie testpwany
def variablesForTriangle(scale, widthLineOnMap,chosenType):
    
    coeficiants = {}
    
    if chosenType == 'oval':
        coeficiants['triangleBase'] = 0.7
        coeficiants['traiangleHight'] = 0.3
        coeficiants['triangleS0'] = 0.1
        
    elif chosenType == 'oval2':
        coeficiants['triangleBase'] = 0.6
        coeficiants['traiangleHight'] = 0.3
        coeficiants['triangleS0'] = 0.1
        
    elif chosenType == 'angular':
        coeficiants['triangleBase'] = 0.4
        coeficiants['traiangleHight'] = 0.4
        coeficiants['triangleS0'] = 0.1
        
    hightOut = coeficiants['traiangleHight'] + coeficiants['triangleS0']
    d1 = coeficiants['triangleS0'] * ( coeficiants['traiangleHight'] / coeficiants['triangleBase'] )
    d2 = sqrt( d1**2 + (coeficiants['triangleS0']/2)**2 )
    hightIns = hightOut - d2 - (coeficiants['triangleS0']/2)
    baseIns = hightIns * (coeficiants['triangleBase'] / coeficiants['traiangleHight'])
    db = coeficiants['triangleBase'] - baseIns
    dbWithWidthLineOnMap = db * (widthLineOnMap/coeficiants['triangleS0'])
    d2WithWidthLineOnMap = d2 * (widthLineOnMap/coeficiants['triangleS0'])
    baseWithWidthLineOnMap = (baseIns + dbWithWidthLineOnMap) * (scale / 1000)
    hightOutWithWidthLineOnMap = (hightIns + d2WithWidthLineOnMap + (widthLineOnMap/2)) * (scale / 1000)
    armOutWithWidthLineOnMap = sqrt( hightOutWithWidthLineOnMap**2 + (baseWithWidthLineOnMap/2)**2 )
    valuables = [chosenType, baseWithWidthLineOnMap, hightOutWithWidthLineOnMap, armOutWithWidthLineOnMap]

    return valuables
    