import os
import sys
import threading
from pathlib import Path

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QEvent, QSettings, Qt, QThread, QTimer, pyqtSignal
from PyQt5.QtWidgets import (QAction, QApplication, QMenu, QStyle,
                             QSystemTrayIcon)

import main_window_design
from _platform import get_platform
from download_widget import DownloadWidget
from library_widget import LibraryWidget
from scraper import Scraper
from settings import *
from settings_window import SettingsWindow


class BlenderLauncher(QtWidgets.QMainWindow, main_window_design.Ui_MainWindow):
    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.app = app

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

        self.update()

        # Tray icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(
            self.style().standardIcon(QStyle.SP_TitleBarMenuButton))
        self.tray_icon.setToolTip("Blender Version Manager")
        self.tray_icon.activated.connect(self.tray_icon_activated)

        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.quit)
        self.tray_menu = QMenu()
        self.tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(self.tray_menu)

        self.tray_icon.show()

        self.tray_icon_trigger = QTimer(self)
        self.tray_icon_trigger.setSingleShot(True)
        self.tray_icon_trigger.timeout.connect(self._show)

    def _show(self):
        self.show()

    def launch_favorite(self):
        print("Launch Favorite")

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.tray_icon_trigger.start(QApplication.doubleClickInterval())
        elif reason == QSystemTrayIcon.DoubleClick:
            self.tray_icon_trigger.stop()
            self.launch_favorite()

    def quit(self):
        self.timer.cancel()
        self.tray_icon.hide()
        self.app.quit()

    def update(self):
        print("Updating...")
        self.timer = threading.Timer(60.0, self.update)
        self.timer.start()
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
