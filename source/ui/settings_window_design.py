# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings_window_design.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SettingsWindow(object):
    def setupUi(self, SettingsWindow):
        SettingsWindow.setObjectName("SettingsWindow")
        SettingsWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        SettingsWindow.resize(320, 240)
        self.centralwidget = QtWidgets.QWidget(SettingsWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.TitleLabel = QtWidgets.QLabel(self.centralwidget)
        self.TitleLabel.setObjectName("TitleLabel")
        self.horizontalLayout_2.addWidget(self.TitleLabel)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.CloseButton = QtWidgets.QPushButton(self.centralwidget)
        self.CloseButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/resources/icons/close.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.CloseButton.setIcon(icon)
        self.CloseButton.setIconSize(QtCore.QSize(32, 32))
        self.CloseButton.setObjectName("CloseButton")
        self.horizontalLayout_2.addWidget(self.CloseButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(9, 0, 9, 9)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.LibraryFolderLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.LibraryFolderLineEdit.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.LibraryFolderLineEdit.setReadOnly(True)
        self.LibraryFolderLineEdit.setObjectName("LibraryFolderLineEdit")
        self.horizontalLayout.addWidget(self.LibraryFolderLineEdit)
        self.SetLibraryFolderButton = QtWidgets.QPushButton(self.centralwidget)
        self.SetLibraryFolderButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/resources/icons/folder.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.SetLibraryFolderButton.setIcon(icon1)
        self.SetLibraryFolderButton.setObjectName("SetLibraryFolderButton")
        self.horizontalLayout.addWidget(self.SetLibraryFolderButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.LaunchWhenSystemStartsCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.LaunchWhenSystemStartsCheckBox.setObjectName("LaunchWhenSystemStartsCheckBox")
        self.verticalLayout_2.addWidget(self.LaunchWhenSystemStartsCheckBox)
        self.LaunchMinimizedToTrayCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.LaunchMinimizedToTrayCheckBox.setObjectName("LaunchMinimizedToTrayCheckBox")
        self.verticalLayout_2.addWidget(self.LaunchMinimizedToTrayCheckBox)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        SettingsWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(SettingsWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 320, 21))
        self.menubar.setObjectName("menubar")
        SettingsWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(SettingsWindow)
        self.statusbar.setSizeGripEnabled(False)
        self.statusbar.setObjectName("statusbar")
        SettingsWindow.setStatusBar(self.statusbar)

        self.retranslateUi(SettingsWindow)
        QtCore.QMetaObject.connectSlotsByName(SettingsWindow)

    def retranslateUi(self, SettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        SettingsWindow.setWindowTitle(_translate("SettingsWindow", "MainWindow"))
        self.TitleLabel.setText(_translate("SettingsWindow", "Settings"))
        self.label.setText(_translate("SettingsWindow", "Library Folder"))
        self.label_2.setText(_translate("SettingsWindow", "System"))
        self.LaunchWhenSystemStartsCheckBox.setText(_translate("SettingsWindow", "Launch When System Starts"))
        self.LaunchMinimizedToTrayCheckBox.setText(_translate("SettingsWindow", "Launch Minimized To Tray"))
import resources.resources_rc
