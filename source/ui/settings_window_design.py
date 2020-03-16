# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings_window_design.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowModality(QtCore.Qt.ApplicationModal)
        Form.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.LibraryFolderLineEdit = QtWidgets.QLineEdit(Form)
        self.LibraryFolderLineEdit.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.LibraryFolderLineEdit.setReadOnly(True)
        self.LibraryFolderLineEdit.setObjectName("LibraryFolderLineEdit")
        self.horizontalLayout.addWidget(self.LibraryFolderLineEdit)
        self.SetLibraryFolderButton = QtWidgets.QPushButton(Form)
        self.SetLibraryFolderButton.setObjectName("SetLibraryFolderButton")
        self.horizontalLayout.addWidget(self.SetLibraryFolderButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.LaunchWhenSystemStartsCheckBox = QtWidgets.QCheckBox(Form)
        self.LaunchWhenSystemStartsCheckBox.setObjectName("LaunchWhenSystemStartsCheckBox")
        self.verticalLayout.addWidget(self.LaunchWhenSystemStartsCheckBox)
        self.LaunchMinimizedToTrayCheckBox = QtWidgets.QCheckBox(Form)
        self.LaunchMinimizedToTrayCheckBox.setObjectName("LaunchMinimizedToTrayCheckBox")
        self.verticalLayout.addWidget(self.LaunchMinimizedToTrayCheckBox)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.SetLibraryFolderButton.setText(_translate("Form", "PushButton"))
        self.LaunchWhenSystemStartsCheckBox.setText(_translate("Form", "Launch When System Starts"))
        self.LaunchMinimizedToTrayCheckBox.setText(_translate("Form", "Launch Minimized To Tray"))
