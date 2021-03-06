# -*- coding: utf-8 -*-
"""
/***************************************************************************
 RequeteAttributaire
                                 A QGIS plugin
 geoinfo
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-06-02
        git sha              : $Format:%H$
        copyright            : (C) 2021 by safaa
        email                : safaa.dk.1999@gmail.com
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
from PyQt5.QtWidgets import QFileDialog
import processing
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.utils import iface

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .RequeteAttributaire_dialog import RequeteAttributaireDialog
import os.path
from qgis.core import (QgsProject, QgsVectorLayer)


class RequeteAttributaire:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
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
            'RequeteAttributaire_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Requete_attributaire')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

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
        return QCoreApplication.translate('RequeteAttributaire', message)

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

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/RequeteAttributaire/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Save Attributes as CSV'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Requete_attributaire'),
                action)
            self.iface.removeToolBarIcon(action)

    def layer_name(self, name: str):
        return QgsProject.instance().mapLayersByName(name)[0]

    def select_output_file(self):
        filename = QFileDialog.getSaveFileName(self.dlg, "Select output file ", "", '.txt')
        self.dlg.lineEdit.setText(str(filename))
    def select_output_file2(self):
        filename = QFileDialog.getSaveFileName(self.dlg, "Select output file ", "", '.txt')
        self.dlg.lineEdit_3.setText(str(filename))

    def close(self):
        self.dlg.close()

    def ok(self):
        Selectedlayer1 = self.dlg.comboBox.currentText()
        Selectedlayer2 = self.dlg.comboBox_2.currentText()

        a = processing.run("qgis:selectbylocation", {
            "INPUT": self.layer_name(Selectedlayer1),
            "PREDICATE": 0,
            "INTERSECT": self.layer_name(Selectedlayer2),
            "METHOD": 0
        })
        self.iface.actionZoomToSelected().trigger()
        print(a)

    def getAttribute(self):
        self.dlg.comboBox_4.clear()
        selectedLayer = QgsProject.instance().mapLayersByName(self.dlg.comboBox_3.currentText())[0]
        fields = selectedLayer.fields()
        self.dlg.comboBox_4.addItem("")
        for field in fields:
            self.dlg.comboBox_4.addItem(field.name())

    def request(self):
        self.dlg.lineEdit_2.setText(self.dlg.comboBox_4.currentText())

    def run_request(self):
        request = self.dlg.lineEdit_2.text()
        layer = QgsProject.instance().mapLayersByName(self.dlg.comboBox_3.currentText())[0]
        print(request)
        result = layer.selectByExpression(request)
        self.iface.actionZoomToSelected().trigger()
        print(result)

    # def test(self):
    # print("it works ;) ")

    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = RequeteAttributaireDialog()
            layers = [tree_layer.layer() for tree_layer in QgsProject.instance().layerTreeRoot().findLayers()]
            # mapcanvas = self.iface.mapCanvas()  # Put the map in a variable called mapcanvas
            # layers = mapcanvas.layers()  # Put the layers in a variable called layers
            layer_list = ["", ]
            layer_list2 = ["", ]
            for layer in layers:
                layer_list.append(layer.name())
            self.dlg.comboBox.clear()
            self.dlg.comboBox.addItems(layer_list)

            # Selectedlayer1 = QgsProject.instance().mapLayersByName(self.dlg.comboBox.currentText())[0]
            selectedLayerIndex = self.dlg.comboBox.currentIndex()
            selectedLayer1 = layers[selectedLayerIndex]

            for layer in layers:
                if layer != selectedLayer1:
                    layer_list2.append(layer.name())
            self.dlg.comboBox_2.clear()
            self.dlg.comboBox_2.addItems(layer_list2)

            self.dlg.pushButton.clicked.connect(self.select_output_file)
            self.dlg.pushButton_2.clicked.connect(self.ok)
            self.dlg.buttonBox.clicked.connect(self.close)
            # Attributes
            self.dlg.comboBox_3.addItems(layer_list)
            self.dlg.comboBox_3.setCurrentText("")
            self.dlg.comboBox_3.currentIndexChanged.connect(self.getAttribute)
            self.dlg.comboBox_4.currentIndexChanged.connect(self.request)
            self.dlg.pushButton_3.clicked.connect(self.run_request)
            self.dlg.buttonBox_2.clicked.connect(self.dlg.close)
            self.dlg.pushButton_4.clicked.connect(self.select_output_file2)

        # show the dialog
        self.dlg.show()

        # self.dlg.btn_run.clicked.connect(self.test)
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.

            # Atributtes
            filename = self.dlg.lineEdit_3.text()
            output_file2 = open(filename, 'w')

            selectedLayerIndex = self.dlg.comboBox_3.currentIndex()
            selectedLayer = layers[selectedLayerIndex]
            fields = selectedLayer.pendingFields()
            fieldnames = [field.name() for field in fields]

            for f in selectedLayer.getFeatures():
                line2 = ','.join(unicode(f[x]) for x in fieldnames) + '\n'
                unicode_line = line2.encode('utf-8')
                output_file2.write(unicode_line)
            output_file2.close()



            #Atributtes
            filename = self.dlg.lineEdit.text()
            output_file = open(filename, 'w')

            selectedLayerIndex = self.dlg.comboBox.currentIndex()
            selectedLayer = layers[selectedLayerIndex]
            fields = selectedLayer.pendingFields()
            fieldnames = [field.name() for field in fields]

            for f in selectedLayer.getFeatures():
                line = ','.join(unicode(f[x]) for x in fieldnames) + '\n'
                unicode_line = line.encode('utf-8')
                output_file.write(unicode_line)
            output_file.close()

            pass
