import os
import sys
import threading
from pathlib import Path

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QSettings, QThread, pyqtSignal, QEvent, Qt
from PyQt5.QtWidgets import QStyle, QSystemTrayIcon

import main_window_design
from _platform import get_platform
from download_widget import DownloadWidget
from library_widget import LibraryWidget
from scraper import Scraper
from settings import *
from settings_window import SettingsWindow


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

        # Draw Library
        library_folder = get_library_folder()
        dirs = library_folder.iterdir()

        if get_platform() == 'Windows':
            blender_exe = "blender.exe"
        elif get_platform() == 'Linux':
            blender_exe = "blender"

        for dir in dirs:
            path = library_folder / dir / blender_exe

            if path.is_file():
                self.draw_to_library(dir)

        self.work()

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(
            self.style().standardIcon(QStyle.SP_TitleBarMenuButton))
        self.tray_icon.activated.connect(self.show)
        self.tray_icon.show()

    def work(self):
        print("Updating...")
        threading.Timer(60.0, self.work).start()
        self.thread = Scraper(self)
        self.thread.links.connect(self.test)
        self.thread.start()

    def test(self, links):
        old_links = []
        new_links = []

        for i in range(self.LibraryListWidget.count()):
            link = self.LibraryListWidget.itemWidget(
                self.LibraryListWidget.item(i)).link
            name = Path(link).name
            old_links.append(name)

        for i in range(self.DownloadsListWidget.count()):
            link = self.DownloadsListWidget.itemWidget(
                self.DownloadsListWidget.item(i)).link
            name = Path(link).stem
            old_links.append(name)

        for link in links:
            if Path(link).stem not in old_links:
                new_links.append(link)

        for link in new_links:
            self.draw_to_downloads(link)

    def draw_to_downloads(self, link):
        item = QtWidgets.QListWidgetItem()
        widget = DownloadWidget(self, item, link)
        item.setSizeHint(widget.sizeHint())
        self.DownloadsListWidget.addItem(item)
        self.DownloadsListWidget.setItemWidget(item, widget)

    def draw_to_library(self, dir):
        item = QtWidgets.QListWidgetItem()
        widget = LibraryWidget(self, item, dir)
        item.setSizeHint(widget.sizeHint())
        self.LibraryListWidget.insertItem(0, item)
        self.LibraryListWidget.setItemWidget(item, widget)

    def show_settings_window(self):
        self.settings_window = SettingsWindow()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
