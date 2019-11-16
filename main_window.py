import os
import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QSettings, QThread, pyqtSignal

import main_window_design
from _platform import get_platform
from download_widget import DownloadWidget
from scraper import Scraper
from library_widget import LibraryWidget
from settings import *
from settings_window import SettingsWindow
from pathlib import Path


class BlenderLauncher(QtWidgets.QMainWindow, main_window_design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

        # Connect buttons
        self.SettingsButton.clicked.connect(self.show_settings_window)

        # Read settings
        self.settings = QSettings('blender_launcher', 'settings')

        self.settings.setValue('version', [0, 1, 0])

        library_folder = self.settings.value('library_folder')
        if (not library_folder) or (not os.path.isdir(library_folder)):
            exe_path = os.path.dirname(sys.executable)
            self.settings.setValue('library_folder', exe_path)

        print(os.path.dirname(sys.executable))

        # Draw downloads
        self.thread = Scraper(self)
        self.thread.download_row.connect(self.draw_to_downloads)
        self.thread.start()

        # Draw Library
        library_folder = Path(get_library_folder())
        dirs = library_folder.iterdir()

        if get_platform() == 'Windows':
            blender_exe = "blender.exe"
        elif get_platform() == 'Linux':
            blender_exe = "blender"

        for dir in dirs:
            path = library_folder / dir / blender_exe

            if path.is_file():
                self.draw_to_library(dir)

    def draw_to_downloads(self, link):
        item = QtWidgets.QListWidgetItem()
        widget = DownloadWidget(self, item, link)
        item.setSizeHint(widget.sizeHint())
        self.DownloadsListWidget.addItem(item)
        self.DownloadsListWidget.setItemWidget(item, widget)

    def draw_to_library(self, dir):
        item = QtWidgets.QListWidgetItem()
        widget = LibraryWidget(dir)
        item.setSizeHint(widget.sizeHint())
        self.LibraryListWidget.addItem(item)
        self.LibraryListWidget.setItemWidget(item, widget)

    def show_settings_window(self):
        self.settings_window = SettingsWindow()
