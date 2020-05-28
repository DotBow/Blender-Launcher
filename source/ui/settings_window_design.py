# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings_window_design.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SettingsWindow(object):
    def setupUi(self, SettingsWindow):
        SettingsWindow.setObjectName("SettingsWindow")
        SettingsWindow.resize(320, 240)
        SettingsWindow.setMinimumSize(QtCore.QSize(320, 240))
        self.CentralWidget = QtWidgets.QWidget(SettingsWindow)
        self.CentralWidget.setObjectName("CentralWidget")
        self.CentralLayout = QtWidgets.QVBoxLayout(self.CentralWidget)
        self.CentralLayout.setContentsMargins(0, 0, 0, 0)
        self.CentralLayout.setObjectName("CentralLayout")
        SettingsWindow.setCentralWidget(self.CentralWidget)
        self.MenuBar = QtWidgets.QMenuBar(SettingsWindow)
        self.MenuBar.setGeometry(QtCore.QRect(0, 0, 320, 21))
        self.MenuBar.setObjectName("MenuBar")
        SettingsWindow.setMenuBar(self.MenuBar)
        self.StatusBar = QtWidgets.QStatusBar(SettingsWindow)
        self.StatusBar.setSizeGripEnabled(False)
        self.StatusBar.setObjectName("StatusBar")
        SettingsWindow.setStatusBar(self.StatusBar)

        self.retranslateUi(SettingsWindow)
        QtCore.QMetaObject.connectSlotsByName(SettingsWindow)

    def retranslateUi(self, SettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        SettingsWindow.setWindowTitle(_translate("SettingsWindow", "MainWindow"))
import resources.resources_rc
