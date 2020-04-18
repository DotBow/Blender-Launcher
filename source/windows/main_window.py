import threading
import webbrowser
from pathlib import Path
from time import gmtime, strftime

from PyQt5.QtCore import QFile, QTextStream, QTimer
from PyQt5.QtGui import QFont, QFontDatabase, QIcon
from PyQt5.QtWidgets import (QAction, QApplication, QListWidgetItem,
                             QMainWindow, QMenu, QSystemTrayIcon, QLabel)

from items.base_list_widget_item import BaseListWidgetItem
from modules.settings import *
from threads.library_drawer import LibraryDrawer
from threads.scraper import Scraper
from ui.main_window_design import Ui_MainWindow
from widgets.download_widget import DownloadState, DownloadWidget
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
        self.status = "Status: None"

        # Setup Window
        self.setWindowTitle("Blender Launcher")
        self.app.setWindowIcon(QIcon(":resources/icons/tray.ico"))

        # Setup Font
        QFontDatabase.addApplicationFont(
            ":/resources/fonts/OpenSans-SemiBold.ttf")
        self.font = QFont("Open Sans SemiBold", 10)
        self.font.setHintingPreference(QFont.PreferNoHinting)
        self.app.setFont(self.font)

        # Setup Style
        file = QFile(":/resources/styles/global.qss")
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        self.app.setStyleSheet(stream.readAll())

        self.SettingsButton.setProperty("HeaderButton", True)
        self.WikiButton.setProperty("HeaderButton", True)
        self.MinimizeButton.setProperty("HeaderButton", True)
        self.CloseButton.setProperty("HeaderButton", True)
        self.CloseButton.setProperty("CloseButton", True)

        # Connect Buttons
        self.SettingsButton.clicked.connect(self.show_settings_window)
        self.WikiButton.clicked.connect(lambda: webbrowser.open(
            "https://github.com/DotBow/Blender-Launcher/wiki"))
        self.MinimizeButton.clicked.connect(self.showMinimized)
        self.CloseButton.clicked.connect(self.close)

        self.LibraryToolBox.currentChanged.connect(self.page_changed)
        self.DownloadsToolBox.currentChanged.connect(self.page_changed)

        # Draw Library
        library_drawer = LibraryDrawer(self)
        library_drawer.build_found.connect(self.draw_to_library)
        library_drawer.start()

        self.statusbar.setFont(self.font)
        self.statusbarLabel = QLabel()
        self.statusbar.addPermanentWidget(self.statusbarLabel, 1)

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
        tray_menu.setFont(self.font)
        tray_menu.addAction(launch_favorite_action)
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)

        # Draw Tray Icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(":resources/icons/tray.ico"))
        self.tray_icon.setToolTip("Blender Launcher")
        self.tray_icon.activated.connect(self.tray_icon_activated)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon_trigger = QTimer(self)
        self.tray_icon_trigger.setSingleShot(True)
        self.tray_icon_trigger.timeout.connect(self._show)

        self.tray_icon.show()

        if get_launch_minimized_to_tray() == False:
            self._show()

    def _show(self):
        self.activateWindow()
        self.show()
        self.set_status()

    def page_changed(self, index):
        tool_box = self.sender()
        icon_page_opened = QIcon(":resources/icons/page_opened.svg")
        icon_page_closed = QIcon(":resources/icons/page_closed.svg")

        for i in range(tool_box.count()):
            if i != index:
                tool_box.setItemIcon(i, icon_page_closed)

        tool_box.setItemIcon(index, icon_page_opened)

    def launch_favorite(self):
        try:
            self.favorite.launch()
        except Exception as e:
            return

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
        self.set_status("Status: Checking for new builds")
        self.timer = threading.Timer(600.0, self.update)
        self.timer.start()
        self.scraper = Scraper(self)
        self.scraper.links.connect(self.draw_new_builds)
        self.scraper.start()

    def draw_new_builds(self, builds):
        library_widgets = []
        download_widgets = []

        library_widgets.extend(self.get_list_widget_items(
            self.LibraryStableListWidget))
        library_widgets.extend(self.get_list_widget_items(
            self.LibraryDailyListWidget))
        library_widgets.extend(self.get_list_widget_items(
            self.LibraryExperimentalListWidget))

        download_widgets.extend(self.get_list_widget_items(
            self.DownloadsStableListWidget))
        download_widgets.extend(self.get_list_widget_items(
            self.DownloadsDailyListWidget))
        download_widgets.extend(self.get_list_widget_items(
            self.DownloadsExperimentalListWidget))

        for widget in download_widgets:
            if widget.build_info in builds:
                builds.remove(widget.build_info)
            elif widget.state != DownloadState.DOWNLOADING:
                widget.destroy()

        for widget in library_widgets:
            if widget.build_info in builds:
                builds.remove(widget.build_info)

        for build_info in builds:
            self.draw_to_downloads(build_info)

        utcnow = strftime(('%H:%M:%S %d-%b-%Y'), gmtime())
        self.set_status("Status: Last check at " + utcnow)

    def get_list_widget_items(self, list_widget):
        items = []

        for i in range(list_widget.count()):
            item = list_widget.itemWidget(list_widget.item(i))
            items.append(item)

        return items

    def draw_to_downloads(self, build_info):
        branch = build_info.branch

        if branch == 'stable':
            list_widget = self.DownloadsStableListWidget
        elif branch == 'daily':
            list_widget = self.DownloadsDailyListWidget
        else:
            list_widget = self.DownloadsExperimentalListWidget

        item = BaseListWidgetItem(build_info.commit_time)
        widget = DownloadWidget(self, list_widget, item, build_info)
        item.setSizeHint(widget.sizeHint())
        list_widget.addItem(item)
        list_widget.setItemWidget(item, widget)

    def draw_to_library(self, dir, branch):
        if branch == 'stable':
            list_widget = self.LibraryStableListWidget
        elif branch == 'daily':
            list_widget = self.LibraryDailyListWidget
        else:
            list_widget = self.LibraryExperimentalListWidget

        item = BaseListWidgetItem()
        widget = LibraryWidget(self, item, dir, list_widget)
        list_widget.insertItem(0, item)
        list_widget.setItemWidget(item, widget)

    def set_status(self, status=None):
        if status is not None:
            self.status = status

        self.statusbarLabel.setText(self.status)

    def show_settings_window(self):
        self.settings_window = SettingsWindow()
        x = self.x() + (self.width() - self.settings_window.width()) * 0.5
        y = self.y() + (self.height() - self.settings_window.height()) * 0.5
        self.settings_window.move(x, y)

    def closeEvent(self, event):
        event.ignore()
        self.hide()
