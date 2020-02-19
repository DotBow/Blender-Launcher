from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QDialog

from ui.settings_window_design import Ui_Dialog
from settings import *


class SettingsWindow(Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

        self.LibraryFolderLineEdit.setText(str(get_library_folder()))
        self.LibraryFolderLineEdit.setCursorPosition(0)
        self.SetLibraryFolderButton.clicked.connect(self.set_library_folder)

    def set_library_folder(self):
        library_folder = str(get_library_folder())
        new_library_folder = QFileDialog.getExistingDirectory(
            self, "Select Library Folder", library_folder)

        if new_library_folder and (library_folder != new_library_folder):
            self.LibraryFolderLineEdit.setText(new_library_folder)
            set_library_folder(new_library_folder)
