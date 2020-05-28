from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QCheckBox, QDialog, QFileDialog, QHBoxLayout,
                             QLabel, QLineEdit, QMainWindow, QPushButton,
                             QVBoxLayout)

from modules.settings import *
from ui.settings_window_design import Ui_SettingsWindow
from windows.base_window import BaseWindow


class SettingsWindow(QMainWindow, BaseWindow, Ui_SettingsWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setupUi(self)

        self.setWindowTitle("Settings")

        self.HeaderLayout = QHBoxLayout()
        self.HeaderLayout.setContentsMargins(36, 1, 1, 0)
        self.HeaderLayout.setSpacing(0)
        self.CentralLayout.addLayout(self.HeaderLayout)

        self.CloseButton = \
            QPushButton(QIcon(":resources/icons/close.svg"), "")
        self.CloseButton.setIconSize(QSize(20, 20))
        self.CloseButton.setFixedSize(36, 32)
        self.CloseButton.setProperty("HeaderButton", True)
        self.CloseButton.setProperty("CloseButton", True)
        self.CloseButton.clicked.connect(self.close)
        self.HeaderLabel = QLabel("Settings")
        self.HeaderLabel.setAlignment(Qt.AlignCenter)

        self.HeaderLayout.addWidget(self.HeaderLabel, 1)
        self.HeaderLayout.addWidget(self.CloseButton, 0, Qt.AlignRight)

        self.LibraryFolderLineEdit = QLineEdit()
        self.LibraryFolderLineEdit.setText(str(get_library_folder()))
        self.LibraryFolderLineEdit.setContextMenuPolicy(Qt.NoContextMenu)
        self.LibraryFolderLineEdit.setReadOnly(True)
        self.LibraryFolderLineEdit.setCursorPosition(0)
 
        self.SetLibraryFolderButton = \
            QPushButton(QIcon(":resources/icons/folder.svg"), "")
        self.SetLibraryFolderButton.clicked.connect(self.set_library_folder)

        self.LaunchWhenSystemStartsCheckBox = QCheckBox(
            "Launch When System Starts")
        self.LaunchWhenSystemStartsCheckBox.setChecked(
            get_launch_when_system_starts())
        self.LaunchWhenSystemStartsCheckBox.clicked.connect(
            self.toggle_launch_when_system_starts)

        self.LaunchMinimizedToTrayCheckBox = QCheckBox(
            "Launch Minimized To Tray")
        self.LaunchMinimizedToTrayCheckBox.setChecked(
            get_launch_minimized_to_tray())
        self.LaunchMinimizedToTrayCheckBox.clicked.connect(
            self.toggle_launch_minimized_to_tray)

        self.EnableHighDpiScalingCheckBox = \
            QCheckBox("Enable High DPI Scaling")
        self.EnableHighDpiScalingCheckBox.clicked.connect(
            self.toggle_enable_high_dpi_scaling)
        self.EnableHighDpiScalingCheckBox.setChecked(
            get_enable_high_dpi_scaling())

        self.SettingsLayout = QVBoxLayout()
        self.SettingsLayout.setContentsMargins(6, 6, 6, 6)
        self.SettingsLayout.setSpacing(6)
        self.CentralLayout.addLayout(self.SettingsLayout)

        self.LibraryFolderLayout = QHBoxLayout()
        self.LibraryFolderLayout.setContentsMargins(1, 1, 1, 1)
        self.LibraryFolderLayout.setSpacing(0)

        self.SettingsLayout.addWidget(QLabel("Library Folder:"))
        self.SettingsLayout.addLayout(self.LibraryFolderLayout)
        self.LibraryFolderLayout.addWidget(self.LibraryFolderLineEdit)
        self.LibraryFolderLayout.addWidget(self.SetLibraryFolderButton)

        self.SettingsLayout.addWidget(QLabel("System:"))

        if get_platform() == 'Windows':
            self.SettingsLayout.addWidget(self.LaunchWhenSystemStartsCheckBox)

        self.SettingsLayout.addWidget(self.LaunchMinimizedToTrayCheckBox)
        self.SettingsLayout.addWidget(self.EnableHighDpiScalingCheckBox)

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
