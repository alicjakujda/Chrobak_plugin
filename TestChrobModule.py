# -*- coding: utf-8 -*-
"""
/***************************************************************************
 TestChrob
                                 A QGIS plugin
 Testing plugin
                              -------------------
        begin                : 2018-05-01
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Alicja Kujda
        email                : alicjakujda@gmail.com
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon, QFileDialog
from qgis.core import *
from qgis.utils import *
from ChrobakGener import *
from math import sqrt
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from TestChrobModule_dialog import TestChrobDialog
import os.path


class TestChrob:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgisInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'TestChrob_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = TestChrobDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Test Chrobak')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'TestChrob')
        self.toolbar.setObjectName(u'TestChrob')
        
        self.dlg.lineEdit.clear()
        self.dlg.pushButton.clicked.connect(self.selectOutputFile)

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('TestChrob', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = TestChrobDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/TestChrob/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'TestChrob'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Test Chrobak'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar
        
    def selectOutputFile(self):
        outputDir = QFileDialog.getExistingDirectory(self.dlg, "Select output file")
        self.dlg.lineEdit.setText(outputDir)
        
    def updateBoxes(self):
        self.updateLayers()
        
    def updateLayers(self):
        self.dlg.comboBox.clear()
        for layer in self.iface.mapCanvas().layers():
            #self.dlg.ui.cbbInLayer.addItem(layer.name(), QVariant(layer))
            self.dlg.comboBox.addItem(layer.name(), layer.id())
            
#     def layerChanged(self):
#         registry = QgsMapLayerRegistry.instance()
#         identifier = str(self.dlg.comboBox.itemData(self.dlg.comboBox.currentIndex()))
#         self.indivLayer = registry.mapLayer(identifier)
        
        
    def trueActiveLayer(self):
        layer = self.iface.legendInterface().selectedLayers()[0]
        return layer
        
    # save shp
    #it doesnt save at all - type problem
    def saveShapefile(self):
        layer = self.trueActiveLayer()
#        outputDir = self.dlg.lineEdit.text() + "/Chrobak/"
        #temporary, during tests
        outputDir = '/home/alicja/Pulpit/Chrobak4/'
        print outputDir
         # create directory if it doesn't exist
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)
        #type = 0 -> VectorLayer
        print layer.type
        if layer.type() == 0:
            writer = QgsVectorFileWriter.writeAsVectorFormat( layer, outputDir + layer.name() + ".shp", "utf-8", layer.crs(), "ESRI Shapefile")
            if writer == QgsVectorFileWriter.NoError:
                self.iface.messageBar().pushMessage("Layer Saved", layer.name() + ".shp saved to " + outputDir, 0, 2)
            else:
                self.iface.messageBar().pushMessage("Error saving layer:", layer.name() + ".shp to " + outputDir, 1, 2)
        else:
            pass

    def run(self):
        """Run method that performs all the real work"""
        #adding dialog functions
        
        #it duplicated layers when their were saved
#         layers = self.iface.legendInterface().layers()
#         layerList = []
#         for layer in layers:
#             layerList.append(layer.name())
#         self.dlg.comboBox.addItems(layerList)
        
        self.updateBoxes()
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            # pass
            features = self.trueActiveLayer().getFeatures()
            for current, feature in enumerate(features):
                geom = feature.geometry()
                if geom.isEmpty() is False:
                    
                    listSegments = line(geom).segmantation()
                    #print listSegments
                    for i in range(0,len(listSegments)-2):
                        lineCoef = line(geom).segmentDefinition(listSegments[i], listSegments[i+1])
                        print lineCoef
    #                     geomSegment = line(geom).geometryOfSegment(listSegments[0], listSegments[1])
    #                     print geomSegment
    #                     geomSegment2 = line(geom).geometryOfSegment(listSegments[4], listSegments[5])
    #                     print geomSegment2
                        lineCoef2 = line(geom).segmentDefinition(listSegments[i+1], listSegments[i+2])
                        print lineCoef2
                        intersection = line(geom).segmentIntersection(lineCoef, lineCoef2)
                        print "line" + str(i) + ", " + str(i+1)
                        print intersection
                        chosenTypeOval = variablesForTriangle(1000000, 0.1 ,"oval")
                        print chosenTypeOval
                        chosenTypeOval2 = variablesForTriangle(1000000, 0.1 ,"oval2")
                        print chosenTypeOval2
                        chosenTypeAngle = variablesForTriangle(1000000, 0.1 ,"angular")
                        print chosenTypeAngle
            self.saveShapefile()
                                    

            