import sys
import threading
from pathlib import Path

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QEvent, QSettings, Qt, QThread, QTimer, pyqtSignal
from PyQt5.QtWidgets import (
    QAction, QApplication, QMainWindow, QMenu, QStyle, QSystemTrayIcon)

from _platform import get_platform
from download_widget import DownloadWidget
from library_widget import LibraryWidget
from scraper import Scraper
from settings import *
from settings_window import SettingsWindow

from ui.main_window_design import Ui_MainWindow


class BlenderLauncher(QMainWindow, Ui_MainWindow):
    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.app = app
        self.favorite = None

        # Connect Buttons
        self.SettingsButton.clicked.connect(self.show_settings_window)

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

        self.update()

        # Draw Tray Icon
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

        self.tray_icon_trigger = QTimer(self)
        self.tray_icon_trigger.setSingleShot(True)
        self.tray_icon_trigger.timeout.connect(self._show)

        self.show()
        self.tray_icon.show()

    def _show(self):
        self.activateWindow()
        self.show()

    def launch_favorite(self):
        if self.favorite is not None:
            self.favorite.launch()

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
        self.timer = threading.Timer(600.0, self.update)
        self.timer.start()
        self.scraper = Scraper(self)
        self.scraper.links.connect(self.test)
        self.scraper.start()

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
