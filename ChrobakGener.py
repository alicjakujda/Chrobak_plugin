class chrobak():
    
    def readVertex(self,qgsVectorLayer):
        feature = qgsVectorLayer.getFeatures().next()
        polyline = feature.geometry().asPolyline()
         
        n = len(polyline)
        vertex = []
         
        for i in range(n):
            vertex.append(polyline[i])
             
        return vertex
     
    def segmantation(self,qgsVectorLayer):
        segments = []
        
        features = qgsVectorLayer.getFeatures()
        for current, feature in enumerate(features):
            geom = feature.geometry()
            if geom.isMultipart(): #not tested yet
                lines = geom.asMultiPolyline()
                for line in lines:
                    for point in range(len(vertices)-1):
#                         segment = QgsFeature()
#                         segment.setGeometry(QgsGeometry.fromPolyline([vertices[point], vertices [point+1]]))
#                         segment.setAttributes(feature.attributes())
#                         segments.append(segment)
                        segments.append(vertices[point])


            else:
                vertices = geom.asPolyline()
                for point in range(len(vertices)):
                        segments.append(vertices[point])
                
        return segments                    