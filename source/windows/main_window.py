import threading
from pathlib import Path

from PyQt5.QtCore import QFile, QTextStream, QTimer
from PyQt5.QtGui import QFont, QFontDatabase, QIcon
from PyQt5.QtWidgets import (QAction, QApplication, QListWidgetItem,
                             QMainWindow, QMenu, QSystemTrayIcon)

from modules.settings import *
from threads.library_drawer import LibraryDrawer
from threads.scraper import Scraper
from ui.main_window_design import Ui_MainWindow
from widgets.download_widget import DownloadWidget
from widgets.library_widget import LibraryWidget
from windows.base_window import BaseWindow
from windows.settings_window import SettingsWindow


class BlenderLauncher(QMainWindow, BaseWindow, Ui_MainWindow):
    def __init__(self, app):
        super().__init__()
        self.setupUi(self)

        # Global Scope
        self.app = app
        self.favorite = None

        # Setup Window
        self.setWindowTitle("Blender Launcher")
        self.app.setWindowIcon(QIcon(":resources/icons/bl_tray.ico"))

        # Setup Font
        QFontDatabase.addApplicationFont(
            ":/resources/fonts/Inter-Regular.otf")
        font = QFont("Inter", 10)
        font.setHintingPreference(QFont.PreferNoHinting)
        self.app.setFont(font)

        # Setup Style
        file = QFile(":/resources/styles/global.qss")
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        self.app.setStyleSheet(stream.readAll())

        self.SettingsButton.setProperty("HeaderButton", True)
        self.MinimizeButton.setProperty("HeaderButton", True)
        self.CloseButton.setProperty("HeaderButton", True)
        self.CloseButton.setProperty("CloseButton", True)

        # Connect Buttons
        self.SettingsButton.clicked.connect(self.show_settings_window)
        self.MinimizeButton.clicked.connect(self.showMinimized)
        self.CloseButton.clicked.connect(self.close)

        self.LibraryToolBox.currentChanged.connect(self.page_changed)
        self.DownloadsToolBox.currentChanged.connect(self.page_changed)

        # Draw Library
        library_drawer = LibraryDrawer(self)
        library_drawer.build_found.connect(self.draw_to_library)
        library_drawer.start()

        # Draw Downloads
        self.update()

        # Setup Tray Icon Context Menu
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.quit)
        hide_action = QAction("Hide", self)
        hide_action.triggered.connect(self.hide)
        show_action = QAction("Show", self)
        show_action.triggered.connect(self._show)
        launch_favorite_action = QAction(
            QIcon(":resources/icons/favorite.svg"), "Blender", self)
        launch_favorite_action.triggered.connect(self.launch_favorite)

        tray_menu = QMenu()
        tray_menu.addAction(launch_favorite_action)
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)

        # Draw Tray Icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(":resources/icons/bl_tray.ico"))
        self.tray_icon.setToolTip("Blender Launcher")
        self.tray_icon.activated.connect(self.tray_icon_activated)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon_trigger = QTimer(self)
        self.tray_icon_trigger.setSingleShot(True)
        self.tray_icon_trigger.timeout.connect(self._show)

        self.show()
        self.tray_icon.show()

    def _show(self):
        self.activateWindow()
        self.show()

    def page_changed(self, index):
        tool_box = self.sender()
        icon_page_opened = QIcon(":resources/icons/page_opened.svg")
        icon_page_closed = QIcon(":resources/icons/page_closed.svg")

        for i in range(tool_box.count()):
            if i != index:
                tool_box.setItemIcon(i, icon_page_closed)

        tool_box.setItemIcon(index, icon_page_opened)

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

        old_links.extend(self.get_list_widget_items(
            self.LibraryStableListWidget, 'path'))
        old_links.extend(self.get_list_widget_items(
            self.LibraryDailyListWidget, 'path'))
        old_links.extend(self.get_list_widget_items(
            self.LibraryExperimentalListWidget, 'path'))

        old_links.extend(self.get_list_widget_items(
            self.DownloadsStableListWidget, 'link'))
        old_links.extend(self.get_list_widget_items(
            self.DownloadsDailyListWidget, 'link'))
        old_links.extend(self.get_list_widget_items(
            self.DownloadsExperimentalListWidget, 'link'))

        for link in links:
            if Path(link.link).stem not in old_links:
                new_links.append(link)

        for link in new_links:
            self.draw_to_downloads(link)

    def get_list_widget_items(self, list_widget, type):
        items = []

        for i in range(list_widget.count()):
            link = list_widget.itemWidget(list_widget.item(i)).build_info.link

            if type == 'link':
                name = Path(link).stem
            elif type == 'path':
                name = Path(link).name

            items.append(name)

        return items

    def draw_to_downloads(self, build_info):
        branch = build_info.branch

        if branch == 'stable':
            list_widget = self.DownloadsStableListWidget
        elif branch == 'daily':
            list_widget = self.DownloadsDailyListWidget
        else:
            list_widget = self.DownloadsExperimentalListWidget

        item = QListWidgetItem()
        widget = DownloadWidget(self, list_widget, item, build_info)
        item.setSizeHint(widget.sizeHint())
        list_widget.addItem(item)
        list_widget.setItemWidget(item, widget)

    def draw_to_library(self, dir):
        item = QListWidgetItem()
        widget = LibraryWidget(self, item, dir)
        item.setSizeHint(widget.sizeHint())

        if widget.branch == 'stable':
            list_widget = self.LibraryStableListWidget
        elif widget.branch == 'daily':
            list_widget = self.LibraryDailyListWidget
        else:
            list_widget = self.LibraryExperimentalListWidget

        widget.list_widget = list_widget
        list_widget.insertItem(0, item)
        list_widget.setItemWidget(item, widget)

    def show_settings_window(self):
        self.settings_window = SettingsWindow()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
