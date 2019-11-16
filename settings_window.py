from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog

import settings_window_design
from settings import *


class SettingsWindow(QtWidgets.QDialog, settings_window_design.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

        self.LibraryFolderLineEdit.setText(get_library_folder().as_posix())
        self.LibraryFolderLineEdit.setCursorPosition(0)
        self.SetLibraryFolderButton.clicked.connect(self.set_library_folder)

    def set_library_folder(self):
        library_folder = get_library_folder().as_posix()
        new_library_folder = QFileDialog.getExistingDirectory(
            self, "Select Library Folder", library_folder)

        if new_library_folder and (library_folder != new_library_folder):
            self.LibraryFolderLineEdit.setText(new_library_folder)
            set_library_folder(new_library_folder)
