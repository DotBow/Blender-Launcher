from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QFileDialog, QMainWindow, QCheckBox

from modules.settings import *
from ui.settings_window_design import Ui_SettingsWindow
from windows.base_window import BaseWindow


class SettingsWindow(QMainWindow, BaseWindow, Ui_SettingsWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setupUi(self)

        self.setWindowTitle("Settings")

        self.CloseButton.setProperty("HeaderButton", True)
        self.CloseButton.setProperty("CloseButton", True)
        self.CloseButton.clicked.connect(self.close)

        self.LibraryFolderLineEdit.setText(str(get_library_folder()))
        self.LibraryFolderLineEdit.setCursorPosition(0)
        self.SetLibraryFolderButton.clicked.connect(self.set_library_folder)

        self.LaunchWhenSystemStartsCheckBox.setChecked(
            get_launch_when_system_starts())
        self.LaunchMinimizedToTrayCheckBox.setChecked(
            get_launch_minimized_to_tray())
        self.LaunchWhenSystemStartsCheckBox.clicked.connect(
            self.toggle_launch_when_system_starts)
        self.LaunchMinimizedToTrayCheckBox.clicked.connect(
            self.toggle_launch_minimized_to_tray)

        if get_platform() == 'Linux':
            self.LaunchWhenSystemStartsCheckBox.hide()

        self.EnableHighDpiScalingCheckBox = \
            QCheckBox("Enable High DPI Scaling")
        self.EnableHighDpiScalingCheckBox.clicked.connect(
            self.toggle_enable_high_dpi_scaling)
        self.EnableHighDpiScalingCheckBox.setChecked(
            get_enable_high_dpi_scaling())
        self.verticalLayout_2.addWidget(self.EnableHighDpiScalingCheckBox)

        self.show()

    def set_library_folder(self):
        library_folder = str(get_library_folder())
        new_library_folder = QFileDialog.getExistingDirectory(
            self, "Select Library Folder", library_folder)

        if new_library_folder and (library_folder != new_library_folder):
            self.LibraryFolderLineEdit.setText(new_library_folder)
            set_library_folder(new_library_folder)
            self.parent.draw_library(clear=True)

    def toggle_launch_when_system_starts(self, is_checked):
        set_launch_when_system_starts(is_checked)

    def toggle_launch_minimized_to_tray(self, is_checked):
        set_launch_minimized_to_tray(is_checked)

    def toggle_enable_high_dpi_scaling(self, is_checked):
        set_enable_high_dpi_scaling(self.parent.app, is_checked)
