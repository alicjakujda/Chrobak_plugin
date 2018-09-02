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
                listOfSegment = {
                                  "index" : point,
                                  "x" : vertices[point][0],
                                  "y" : vertices[point][1],
                                  "ifPointStayAfterGeneralization" : False
                                  }
                listOfSegments.append(listOfSegment)
                listOfSegment = []
                
        return listOfSegments
    
    #ok 237 metrów różnicy między funkcjami
    #przerobić!!!!!!
    def lineCentroid(self, pointsOfLine):
                
        sc_sum = 0.0
        cx_sum = 0.0
        cy_sum = 0.0
        for i in range(len(pointsOfLine)-1):        
            sc = ((pointsOfLine[i]["x"]*pointsOfLine[i+1]["y"]) - (pointsOfLine[i+1]["x"]*pointsOfLine[i]["y"]))
            cx = ( pointsOfLine[i]["x"] + pointsOfLine[i+1]["x"]) * sc
            cy = ( pointsOfLine[i]["y"] + pointsOfLine[i+1]["y"]) * sc
            sc_sum = sc_sum + sc
            cx_sum = cx_sum + cx
            cy_sum = cy_sum + cy
        A = sc_sum/2
        centroid = {
                    "x" : cx_sum * ( 1/ (6*A)),
                    "y" : cy_sum * ( 1/ (6*A))
                    }
    
        return centroid
    
    #chyba nieużywane i można wyłączyć
    def geometryOfSegment(self, startPoint, endPoint):
        segment = QgsGeometry.fromPolyline([QgsPoint(startPoint), QgsPoint(endPoint)])
        
        return segment
    
    def distanceOfPoints(self, startPoint, endPoint):
        distance = sqrt((startPoint["x"] - endPoint["x"])**2 + (startPoint["y"] - endPoint["y"])**2)
    
        return distance
    
    def segmentDefinition(self, startPoint, endPoint):
        A = startPoint["y"] - endPoint["y"]
        B = endPoint["x"] - startPoint["x"]
        C = endPoint["y"] * startPoint["x"] - startPoint["y"] * endPoint["x"]
        segmentDefinition = {
                             "A" : A,
                             "B" : B,
                             "C" : C
                             }
        
        return segmentDefinition
    
    def distancePointToLine(self, point, segmentDefinition):
        distance = abs(segmentDefinition["A"] * point["x"] + segmentDefinition["B"] * point["y"] + segmentDefinition["C"]) / sqrt(segmentDefinition["A"]**2 + segmentDefinition["B"]**2)
        return distance

    #intersekcja musi być oparta na współczynnikach lini, ponieważ nie zawsze obiekty się przecinają geometrycznie ale w przestrzeni tak
    def segmentIntersection(self, firstLine, secondLine):

        if firstLine["A"] == 0 and (firstLine["B"] == 0 or secondLine["B"] == 0) and (firstLine["C"] != secondLine["C"]):
            intersectionPoint = {
                                 "x" : - secondLine["C"] / secondLine["A"],
                                 "y" : - firstLine["C"] / firstLine["B"]
                                 }
            
        elif secondLine["A"] == 0 and (firstLine["B"] == 0 or secondLine["B"] == 0) and (firstLine["C"] != secondLine["C"]):
            intersectionPoint = {
                                 "x" : - firstLine["C"] / firstLine["A"],
                                 "y" : - secondLine["C"] / secondLine["B"]
                                 }
            
        elif (firstLine["A"], secondLine["A"]) == (0, 0) or (firstLine["B"], secondLine["B"]) == (0, 0):
            intersectionPoint = {
                                 "x" : None,
                                 "y" : None
                                 }

        else:

            intersectionPoint = {
                                 "x" : (firstLine["B"] * secondLine["C"] - secondLine["B"] * firstLine["C"]) / (firstLine["A"] * secondLine["B"] - secondLine["A"] * firstLine["B"]),
                                 "y" : - (secondLine["A"] * firstLine["C"] - firstLine["A"] * secondLine["C"]) / (firstLine["B"] * secondLine["A"] - secondLine["B"] * firstLine["A"])
                                 }

        return intersectionPoint

    def perpendicularLineToLine(self, segmentDefinition, pointToProjection):
        perpendicularLine = {
            "A" : - segmentDefinition["B"],
            "B" : segmentDefinition["A"],
            "C" : segmentDefinition["B"] * pointToProjection["x"] - segmentDefinition["A"] * pointToProjection["y"]
            }
        
        return perpendicularLine

    
    #stworzyć funkcję w klasie linia dla pierscienia - jeżeli true to wtedy funkcja z numeracją będzie dla pierscienia
    def ringData(self, pointsOfLine):
        pointOfCentroid = self.lineCentroid(pointsOfLine)
        print "pointOfCentroid: " + str(pointOfCentroid)
        distanceToCentroid = []
        for point in pointsOfLine:
            dist = self.distanceOfPoints(point, pointOfCentroid)
            distanceToCentroid.append(dist)
        maxDistance = max(distanceToCentroid)
        indexPoint = distanceToCentroid.index(maxDistance)
        
        #numeration of poinst
        if indexPoint != 0:
            pointsOfLine = pointsOfLine[indexPoint:] + pointsOfLine[1:indexPoint] + [pointsOfLine[indexPoint].copy()]
            
            reorderPointsOfLine = []
            counterIndex = 0
            for point in pointsOfLine:
                point["index"] = counterIndex
                reorderPointsOfLine.append(point)
                counterIndex += 1

            pointsOfLine = reorderPointsOfLine
            
        #check if don't include when s more than one extremum!
        #find extremum in ring
        distanceToFirstPoint = []
        for point in pointsOfLine[1:-2]:
            dist = self.distanceOfPoints(point, pointsOfLine[0])
            distanceToFirstPoint.append(dist)
        #max function returns only one values, even if there is more than one!
        maxDistanceExtremum = max(distanceToFirstPoint)
        # +1 is because of starting line from second point
        indexPointOfRingExtremum = distanceToFirstPoint.index(maxDistanceExtremum)+1
        lineFromExtremumToFirstPoint = self.segmentDefinition(pointsOfLine[indexPointOfRingExtremum], pointsOfLine[0])
        minDistanceFromCentrToLine = self.distancePointToLine(pointOfCentroid, lineFromExtremumToFirstPoint)
        ringData = {
                    "indexPoint": indexPoint, 
                    "maxDistance" : maxDistance, 
                    "pointsOfLine" : pointsOfLine, 
                    "pointOfRingExtremum" : pointsOfLine[indexPointOfRingExtremum],
                    "maxDistanceExtremum" : maxDistanceExtremum
                    }
        
        return ringData

        
#     #stworzyć funkcję w klasie linia z numeracją punktów - jeżeli będzie pierscien to wtedy będzie inna kolejność
#     def numerationOfPoints(self, pointsOfLine, indexPointOfRing):
#         if indexPointOfRing is not None and indexPointOfRing != 0:
#             pointsOfLine = pointsOfLine[indexPointOfRing:] + pointsOfLine[1:indexPointOfRing+1]
#             return pointsOfLine
        
    #brak opcji z większą ilością punktów o tej samej odległości od centr, min odl od centr oraz max nie są używane później nigdzie - może później jakoś się usunie
    #stworzyć funkcję obliczającą index i wartość odl punktu najdalszego - może się przydać!
    #przetestowac!
#     def findLocalExtremumInRing(self, pointsOfRing, pointOfCentroid):
#         if pointsOfRing[0] == pointsOfRing[-1]:
#             distanceToFirstPoint = []
#             for point in pointsOfRing[1:-2]:
#                 dist = sqrt(point.sqrDist(*pointsOfRing[0]))
#                 distanceToFirstPoint.append(dist)
#             maxDistance = max(distanceToFirstPoint)
#             indexPoint = distanceToFirstPoint.index(maxDistance)+1
#             lineFromExtremumToFirstPoint = self.segmentDefinition(pointsOfRing[indexPoint], pointsOfRing[0])
#             minDistanceFromCentrToLine = self.distancePointToLine(pointOfCentroid, lineFromExtremumToFirstPoint)
#             return [indexPoint, pointsOfRing[indexPoint], maxDistance]
        
# 
# #nie testowany
# raczej nie potrzebne będzie
# def epsylon(scale, chosenType):
#     if chosenType == 'angular':
#         return (scale/1000) * 0.4
#     else:
#         return (scale/1000) * 0.6




def variablesForTriangle(scale, widthLineOnMap,chosenType):
    
    coeficiants = {}
    
    if chosenType == 'oval':
        coeficiants = {
                       "triangleBase" : 0.7,
                       "traiangleHight" : 0.3,
                       "triangleS0" : 0.1
                       }

    elif chosenType == 'oval2':
        coeficiants = {
                       "triangleBase" : 0.6,
                       "traiangleHight" : 0.3,
                       "triangleS0" : 0.1
                       }
        
    elif chosenType == 'angular':
        coeficiants = {
                       "triangleBase" : 0.4,
                       "traiangleHight" : 0.4,
                       "triangleS0" : 0.1
                       }
        
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
    variables = {
                 "chosenType" : chosenType,
                 "baseWithWidthLineOnMap" : baseWithWidthLineOnMap,
                 "hightOutWithWidthLineOnMap" : hightOutWithWidthLineOnMap,
                 "armOutWithWidthLineOnMap" : armOutWithWidthLineOnMap
                 }

    return variables

def conditionsForExtremum(variables, data, type):
    condition = False
    
    for dictVariables in variables:
        tableWithLogic = {}
        tableWithLogic["chosenType"] = dictVariables['chosenType']

        for nameVariable, valueVariable in dictVariables.items():
            for name, value in data.items():
                
                #names of keys in dictionary 'dataForConditions' can not be changed
                if nameVariable[:2] == name[:2]:
                    if value >= valueVariable:
                        logic = True
                    else:
                        logic = False

                    tableWithLogic[name] = logic
                    

        #logical condition for type
        if type == "armAsBase":
#             print tableWithLogic
            condition = condition or tableWithLogic['base'] and tableWithLogic['armBegin'] and tableWithLogic['armEnd']
        elif type == "hightAsBase":
#             print tableWithLogic
            condition = condition or tableWithLogic['base'] and tableWithLogic['hight']

    return condition

# główna funkcja, dane wejściowe to podstawowe dane - wszystko tu przerobimy na cycuś glancuś!
#dodać jeszcze wybór czy chcemy mieć zgodnie z jakim typem
#type: hightAsBase; armAsBase
def chrobakGeneralization(features, scale, widthLineOnMap, type):
    
    #epsylon counting
    typesOfTriangle = ["oval", "oval2", "angular"]
    variables = []
    armsValues = []
    for typeOfTriangle in typesOfTriangle:
        variables.append(variablesForTriangle(scale, widthLineOnMap, typeOfTriangle))
        
    print "variables"
    print variables
    
    
    for i in range(0,len(variables)):
        armsValues.append(variables[i]["armOutWithWidthLineOnMap"])
    
    epsylon = min(armsValues)
    print epsylon
    
    for current, feature in enumerate(features):
        geom = feature.geometry()
        print geom
        if geom.isEmpty() is False:
            
            listSegments = line(geom).segmantation()
            print "listSegments: " + str(listSegments)
            
       
#             for i in range(0,len(listSegments)-2):
#                 lineCoef = line(geom).segmentDefinition(listSegments[i], listSegments[9])
#                 print lineCoef
#                 distance = line(geom).distancePointToLine(listSegments[i],lineCoef)
#                 print distance

            listIndex = [[[0, len(listSegments)-1]]]
            
            #for ring data
            if listSegments[0]["x"] == listSegments[-1]["x"] and  listSegments[0]["y"] == listSegments[-1]["y"]:
                ring = line(geom).ringData(listSegments)
                listSegments = ring["pointsOfLine"]
                if ring["pointOfRingExtremum"]["index"] != 0:
                    listIndex = [[[0, ring["pointOfRingExtremum"]["index"]], [ring["pointOfRingExtremum"]["index"], len(listSegments)-1]]]
                
                print "ring: " + str(ring)
                print "listSegments: " + str(listSegments)
                print "listIndex: " + str(listIndex)

            stopIteration = False
            levelOfListIndex = 0
            
            while not stopIteration:

                for i in range(0,len(listIndex[levelOfListIndex])):
                    
                    maxArrow = 0
                    pointExtremum = {}
                    pointExtremumDuringDoubleMax = {}
                         
                    startPoint = listSegments[(listIndex[levelOfListIndex][i][0])]
                    endPoint = listSegments[(listIndex[levelOfListIndex][i][1])]
                    
                    #points of listIndex stay after generalization
                    listSegments[(listIndex[levelOfListIndex][i][0])]["ifPointStayAfterGeneralization"] = True
                    listSegments[(listIndex[levelOfListIndex][i][1])]["ifPointStayAfterGeneralization"] = True
                    
                    
                    print "startPoint: " + str(startPoint)
                    print "endPoint: " + str(endPoint)
                    
                    #data of base of the triangle
                    lengthBaseOfTriangle = line(geom).distanceOfPoints(startPoint, endPoint)
#                     print "lengthBaseOfTriangle" + str(lengthBaseOfTriangle)
                    
                    definitionBaseOfTriangle = line(geom).segmentDefinition(startPoint, endPoint)
                    
                    #start iteration from other points in segment
                    for point in listSegments[listIndex[levelOfListIndex][i][0]+1:listIndex[levelOfListIndex][i][1]]:
                        print point
                        
                        #values of each point of segment
                        armFromPointToBegin = line(geom).distanceOfPoints(startPoint, point)
                        armFromPointToEnd = line(geom).distanceOfPoints(endPoint, point)
                        arrow = line(geom).distancePointToLine(point, definitionBaseOfTriangle)
                        print "arrow: " + str(arrow)
                        
                        #projection points on triangle base
                        perpendicularLine = line(geom).perpendicularLineToLine(definitionBaseOfTriangle, point)
                        projectionPointOnTriangleBase = line(geom).segmentIntersection(perpendicularLine, definitionBaseOfTriangle)
                        
#                         print projectionPointOnTriangleBase
                        
                        partBaseFromPointToBegin = line(geom).distanceOfPoints(startPoint, projectionPointOnTriangleBase)
                        partBaseFromPointToEnd = line(geom).distanceOfPoints(endPoint, projectionPointOnTriangleBase)                                                    
                        
                        #including width of line on the map
                        arrowWithWidth = arrow + (widthLineOnMap * (scale / 1000))
#                         print "arrowWithWidth" + str(arrowWithWidth)
                        
                        armFromPointToBeginWithWidth = sqrt(armFromPointToBegin ** 2 + arrowWithWidth ** 2)
#                         print "armFromPointToBeginWithWidth" + str(armFromPointToBeginWithWidth)
                        
                        armFromPointToEndWithWidth = sqrt(armFromPointToEnd ** 2 + arrowWithWidth ** 2)
#                         print "armFromPointToEndWithWidth" + str(armFromPointToEndWithWidth)
                        
                        dataForConditions = {
                            "base" : lengthBaseOfTriangle,
                            "armBegin" : armFromPointToBeginWithWidth,
                            "armEnd" : armFromPointToEndWithWidth,
                            "hight" : arrowWithWidth
                        }
                        
                        if conditionsForExtremum(variables, dataForConditions, type):
                            if arrow > maxArrow:
                                maxArrow = arrow
                                pointExtremum = point
                                sumOfExtremumArms = armFromPointToBegin + armFromPointToEnd
                            
                            #double maximum values
                            elif arrow == maxArrow:
                                sumOfExtremumArmsDuringDoubleMax = armFromPointToBegin + armFromPointToEnd
                                distanceBetweenExtremums = line(geom).distanceOfPoints(pointExtremum, point)
                                
                                #to get the sum in one condition or not?
                                if distanceBetweenExtremums < widthLineOnMap and sumOfExtremumArms < sumOfExtremumArmsDuringDoubleMax:
                                    maxArrow = arrow
                                    pointExtremum = point
                                    sumOfExtremumArms = sumOfExtremumArmsDuringDoubleMax
                                    
                                else:
                                    maxArrow = arrow                                 
                                    pointExtremumDuringDoubleMax = pointExtremum
                                    pointExtremum = point
                                    sumOfExtremumArms = sumOfExtremumArmsDuringDoubleMax
                                
                if bool(pointExtremum):

                    if len(listIndex) == levelOfListIndex + 1:
                        listIndex.append([])
                    
                    if bool(pointExtremumDuringDoubleMax):
                        listIndex[(levelOfListIndex + 1)].append([startPoint["index"], pointExtremumDuringDoubleMax["index"]])
                        listIndex[(levelOfListIndex + 1)].append([pointExtremumDuringDoubleMax["index"], pointExtremum["index"]])
                        listIndex[(levelOfListIndex + 1)].append([pointExtremum["index"], endPoint["index"]])
                        pointExtremumDuringDoubleMax = {}
                        
                    else:
                        listIndex[(levelOfListIndex + 1)].append([startPoint["index"], pointExtremum["index"]])
                        listIndex[(levelOfListIndex + 1)].append([pointExtremum["index"], endPoint["index"]])
                        
                else:
                    point["ifPointStayAfterGeneralization"] = True
                
                print "new listIndex: " + str(listIndex)
                    
                if (i == len(listIndex[levelOfListIndex]) - 1) and (len(listIndex) == levelOfListIndex + 1):
                    stopIteration = True

                            

                levelOfListIndex +=1     


#                 stopIteration = True
                print "after all listSegments: " + str(listSegments)
            
#             if ring is not None:
#                 numeration = line(geom).numerationOfPoints(listSegments, ring[0])
#                 print numeration
#                 localExtremum = line(geom).findLocalExtremumInRing(numeration, centr)
#                 print "localExtremum " + str(localExtremum)
                

#                     geomSegment = line(geom).geometryOfSegment(listSegments[0], listSegments[1])
#                     print geomSegment
#                     geomSegment2 = line(geom).geometryOfSegment(listSegments[4], listSegments[5])
#                     print geomSegment2
#                         lineCoef2 = line(geom).segmentDefinition(listSegments[i+1], listSegments[i+2])
#                         print lineCoef2
#                         intersection = line(geom).segmentIntersection(lineCoef, lineCoef2)
#                         print "line" + str(i) + ", " + str(i+1)
#                         print intersection
#                         chosenTypeOval = variablesForTriangle(1000000, 0.1 ,"oval")
#                         print chosenTypeOval
#                         chosenTypeOval2 = variablesForTriangle(1000000, 0.1 ,"oval2")
#                         print chosenTypeOval2
#                         chosenTypeAngle = variablesForTriangle(1000000, 0.1 ,"angular")
#                         print chosenTypeAngle


    
    
    
    return "chrobak generalization"
    