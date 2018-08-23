# -*- coding: utf-8 -*-
from qgis.core import *
from qgis.utils import *
from math import *

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
    def lineCentroid(self, pointsOfLine):
                
#         A = 0.0
#         sc = 0.0
#         cx = 0.0
#         cy = 0.0
        sc_sum = 0.0
        cx_sum = 0.0
        cy_sum = 0.0
        for i in range(len(pointsOfLine)-1):        
            sc = ((pointsOfLine[i][0]*pointsOfLine[i+1][1]) - (pointsOfLine[i+1][0]*pointsOfLine[i][1]))
            cx = ( pointsOfLine[i][0] + pointsOfLine[i+1][0]) * sc
            cy = ( pointsOfLine[i][1] + pointsOfLine[i+1][1]) * sc
            sc_sum = sc_sum + sc
            cx_sum = cx_sum + cx
            cy_sum = cy_sum + cy
        A = sc_sum/2
        centroidX = cx_sum * ( 1/ (6*A))
        centroidY = cy_sum * ( 1/ (6*A))
    
        return [centroidX, centroidY]
    
    def geometryOfSegment(self, startPoint, endPoint):
        segment = QgsGeometry.fromPolyline([QgsPoint(startPoint), QgsPoint(endPoint)])
        
        return segment
    
    def segmentDefinition(self, startPoint, endPoint):
        A = startPoint[1] - endPoint[1]
        B = endPoint[0] - startPoint[0]
        C = endPoint[1]*startPoint[0] - startPoint[1]*endPoint[0]
        
        return [A, B, C]
    
    def distancePointToLine(self, point, segmentDefinition):
        distance = abs(segmentDefinition[0]*point[0]+segmentDefinition[1]*point[1]+segmentDefinition[2]) / sqrt(segmentDefinition[0]**2+segmentDefinition[1]**2)
        return distance

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

    
    #stworzyć funkcję w klasie linia dla pierscienia - jeżeli true to wtedy funkcja z numeracją będzie dla pierscienia
    def ringData(self, pointsOfLine, pointOfCentroid):
        if pointsOfLine[0] == pointsOfLine[-1]:
            distanceToCentroid = []
            for point in pointsOfLine:
                dist = sqrt(point.sqrDist(*pointOfCentroid))
                distanceToCentroid.append(dist)
            maxDistance = max(distanceToCentroid)
            indexPoint = distanceToCentroid.index(maxDistance)
            return [indexPoint, maxDistance]
        
    #stworzyć funkcję w klasie linia z numeracją punktów - jeżeli będzie pierscien to wtedy będzie inna kolejność
    def numerationOfPoints(self, pointsOfLine, indexPointOfRing):
        if indexPointOfRing is not None and indexPointOfRing != 0:
            newPointsOfLine = pointsOfLine[indexPointOfRing:] + pointsOfLine[1:indexPointOfRing+1]
            return newPointsOfLine
        
    #brak opcji z większą ilością punktów o tej samej odległości od centr, min odl od centr oraz max nie są używane później nigdzie - może później jakoś się usunie
    #stworzyć funkcję obliczającą index i wartość odl punktu najdalszego - może się przydać!
    #przetestowac!
    def findLocalExtremumInRing(self, pointsOfRing, pointOfCentroid):
        if pointsOfRing[0] == pointsOfRing[-1]:
            distanceToFirstPoint = []
            for point in pointsOfRing[1:-2]:
                dist = sqrt(point.sqrDist(*pointsOfRing[0]))
                distanceToFirstPoint.append(dist)
            maxDistance = max(distanceToFirstPoint)
            indexPoint = distanceToFirstPoint.index(maxDistance)+1
            lineFromExtremumToFirstPoint = self.segmentDefinition(pointsOfRing[indexPoint], pointsOfRing[0])
            minDistanceFromCentrToLine = self.distancePointToLine(pointOfCentroid, lineFromExtremumToFirstPoint)
            return [indexPoint, pointsOfRing[indexPoint], maxDistance]
        
    
                
                
        

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
    variables = [chosenType, baseWithWidthLineOnMap, hightOutWithWidthLineOnMap, armOutWithWidthLineOnMap]

    return variables
    