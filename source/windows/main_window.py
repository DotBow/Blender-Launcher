import re
import threading
import webbrowser
from enum import Enum
from pathlib import Path
from time import localtime, strftime

from items.base_list_widget_item import BaseListWidgetItem
from modules._platform import get_platform, get_platform_full, set_locale
from modules.enums import MessageType
from modules.settings import (create_library_folders,
                              get_default_downloads_page,
                              get_default_library_page, get_default_tab,
                              get_enable_download_notifications,
                              get_enable_new_builds_notifications,
                              get_launch_minimized_to_tray, get_library_folder,
                              get_show_tray_icon, get_taskbar_icon_color,
                              is_library_folder_valid, set_library_folder,
                              taskbar_icon_paths)
from PyQt5.QtCore import QFile, QSize, Qt, QTextStream, pyqtSignal
from PyQt5.QtGui import QFont, QFontDatabase, QIcon
from PyQt5.QtNetwork import QLocalServer
from PyQt5.QtWidgets import (QAction, QFileDialog, QHBoxLayout, QLabel,
                             QMainWindow, QPushButton, QSystemTrayIcon,
                             QTabWidget, QVBoxLayout, QWidget)
from threads.library_drawer import LibraryDrawer
from threads.remover import Remover
from threads.scraper import Scraper
from ui.main_window_ui import Ui_MainWindow
from urllib3 import PoolManager
from widgets.base_menu_widget import BaseMenuWidget
from widgets.base_page_widget import BasePageWidget
from widgets.base_tool_box_widget import BaseToolBoxWidget
from widgets.download_widget import DownloadState, DownloadWidget
from widgets.library_widget import LibraryWidget

from windows.base_window import BaseWindow
from windows.dialog_window import DialogIcon, DialogWindow
from windows.settings_window import SettingsWindow
from windows.update_window import UpdateWindow


class AppState(Enum):
    IDLE = 1
    CHECKINGBUILDS = 2


class BlenderLauncher(QMainWindow, BaseWindow, Ui_MainWindow):
    show_signal = pyqtSignal()
    close_signal = pyqtSignal()

    def __init__(self, app, version):
        super().__init__()
        self.setupUi(self)
        self.setAcceptDrops(True)

        # Server
        self.server = QLocalServer()
        self.server.listen("blender-launcher-server")
        self.server.newConnection.connect(self.new_connection)

        # Global scope
        self.app = app
        self.version = version
        self.favorite = None
        self.status = "Ready"
        self.text = "OK"
        self.app_state = AppState.IDLE
        self.cashed_builds = []
        self.notification_pool = []
        self.windows = [self]

        _headers = {
            'user-agent': 'Blender Launcher/{0} ({1})'.format(
                version, get_platform_full())}
        self.manager = PoolManager(
            num_pools=50, maxsize=10, headers=_headers)

        self.timer = None
        self.started = True
        self.latest_tag = ""
        self.new_downloads = False

        # Icon cache
        self.icon_settings = QIcon(":resources/icons/settings.svg")
        self.icon_wiki = QIcon(":resources/icons/wiki.svg")
        self.icon_minimize = QIcon(":resources/icons/minimize.svg")
        self.icon_close = QIcon(":resources/icons/close.svg")
        self.icon_folder = QIcon(":resources/icons/folder.svg")
        self.icon_favorite = QIcon(":resources/icons/favorite.svg")
        self.icon_fake = QIcon(":resources/icons/fake.svg")
        self.icon_delete = QIcon(":resources/icons/delete.svg")
        self.filled_circle = QIcon(":resources/icons/filled_circle.svg")
        self.icon_quick_launch = QIcon(":resources/icons/quick_launch.svg")
        self.icon_taskbar = QIcon(taskbar_icon_paths[get_taskbar_icon_color()])

        # Setup window
        self.setWindowTitle("Blender Launcher")
        self.app.setWindowIcon(self.icon_taskbar)

        # Setup font
        QFontDatabase.addApplicationFont(
            ":/resources/fonts/OpenSans-SemiBold.ttf")
        self.font = QFont("Open Sans SemiBold", 10)
        self.font.setHintingPreference(QFont.PreferNoHinting)
        self.app.setFont(self.font)

        # Setup style
        file = QFile(":/resources/styles/global.qss")
        file.open(QFile.ReadOnly | QFile.Text)
        self.style_sheet = QTextStream(file).readAll()
        self.app.setStyleSheet(self.style_sheet)

        # Check library folder
        if is_library_folder_valid() is False:
            self.dlg = DialogWindow(
                self, title="Information",
                text="First, choose where Blender<br>builds will be stored",
                accept_text="Continue", cancel_text=None, icon=DialogIcon.INFO)
            self.dlg.accepted.connect(self.set_library_folder)
        else:
            create_library_folders(get_library_folder())
            self.draw()

    def set_library_folder(self):
        library_folder = Path.cwd().as_posix()
        new_library_folder = QFileDialog.getExistingDirectory(
            self, "Select Library Folder", library_folder,
            options=QFileDialog.DontUseNativeDialog | QFileDialog.ShowDirsOnly)

        if (new_library_folder):
            if set_library_folder(new_library_folder) is True:
                self.draw(True)
            else:
                self.dlg = DialogWindow(
                    self, title="Warning",
                    text="Selected folder doesn't have write permissions!",
                    accept_text="Retry", cancel_text=None)
                self.dlg.accepted.connect(self.set_library_folder)
        else:
            self.app.quit()

    def draw(self, polish=False):
        self.HeaderLayout = QHBoxLayout()
        self.HeaderLayout.setContentsMargins(0, 0, 0, 0)
        self.HeaderLayout.setSpacing(0)
        self.CentralLayout.addLayout(self.HeaderLayout)

        self.SettingsButton = QPushButton(self.icon_settings, "")
        self.SettingsButton.setIconSize(QSize(20, 20))
        self.SettingsButton.setFixedSize(36, 32)
        self.SettingsButton.setToolTip("Show settings window")
        self.WikiButton = QPushButton(self.icon_wiki, "")
        self.WikiButton.setIconSize(QSize(20, 20))
        self.WikiButton.setFixedSize(36, 32)
        self.WikiButton.setToolTip("Open documentation")
        self.MinimizeButton = QPushButton(self.icon_minimize, "")
        self.MinimizeButton.setIconSize(QSize(20, 20))
        self.MinimizeButton.setFixedSize(36, 32)
        self.CloseButton = QPushButton(self.icon_close, "")
        self.CloseButton.setIconSize(QSize(20, 20))
        self.CloseButton.setFixedSize(36, 32)
        self.HeaderLabel = QLabel("Blender Launcher")
        self.HeaderLabel.setAlignment(Qt.AlignCenter)

        self.HeaderLayout.addWidget(self.SettingsButton, 0, Qt.AlignLeft)
        self.HeaderLayout.addWidget(self.WikiButton, 0, Qt.AlignLeft)
        self.HeaderLayout.addWidget(self.HeaderLabel, 1)
        self.HeaderLayout.addWidget(self.MinimizeButton, 0, Qt.AlignRight)
        self.HeaderLayout.addWidget(self.CloseButton, 0, Qt.AlignRight)

        self.SettingsButton.setProperty("HeaderButton", True)
        self.WikiButton.setProperty("HeaderButton", True)
        self.MinimizeButton.setProperty("HeaderButton", True)
        self.CloseButton.setProperty("HeaderButton", True)
        self.CloseButton.setProperty("CloseButton", True)

        # Tab layout
        self.TabWidget = QTabWidget()
        self.TabWidget.setProperty('North', True)
        self.CentralLayout.addWidget(self.TabWidget)

        self.LibraryTab = QWidget()
        self.LibraryTabLayout = QVBoxLayout()
        self.LibraryTabLayout.setContentsMargins(0, 0, 0, 0)
        self.LibraryTab.setLayout(self.LibraryTabLayout)
        self.TabWidget.addTab(self.LibraryTab, "Library")

        self.DownloadsTab = QWidget()
        self.DownloadsTabLayout = QVBoxLayout()
        self.DownloadsTabLayout.setContentsMargins(0, 0, 0, 0)
        self.DownloadsTab.setLayout(self.DownloadsTabLayout)
        self.TabWidget.addTab(self.DownloadsTab, "Downloads")

        self.UserTab = QWidget()
        self.UserTabLayout = QVBoxLayout()
        self.UserTabLayout.setContentsMargins(0, 0, 0, 0)
        self.UserTab.setLayout(self.UserTabLayout)
        self.TabWidget.addTab(self.UserTab, "User")

        self.LibraryToolBox = BaseToolBoxWidget(self)
        self.DownloadsToolBox = BaseToolBoxWidget(self)
        self.UserToolBox = BaseToolBoxWidget(self)

        self.LibraryToolBox.tab_changed.connect(
            lambda i: self.DownloadsToolBox.setCurrentIndex(i))
        self.DownloadsToolBox.tab_changed.connect(
            lambda i: self.LibraryToolBox.setCurrentIndex(i))

        self.LibraryTab.layout().addWidget(self.LibraryToolBox)
        self.DownloadsTab.layout().addWidget(self.DownloadsToolBox)
        self.UserTab.layout().addWidget(self.UserToolBox)

        page = BasePageWidget(
            parent=self,
            page_name="LibraryStableListWidget",
            time_label="Commit Time",
            info_text="Nothing to show yet",
            extended_selection=True)
        self.LibraryStableListWidget = \
            self.LibraryToolBox.add_page_widget(page, "Stable")

        page = BasePageWidget(
            parent=self,
            page_name="LibraryDailyListWidget",
            time_label="Commit Time",
            info_text="Nothing to show yet",
            show_branch=False,
            extended_selection=True)
        self.LibraryDailyListWidget = \
            self.LibraryToolBox.add_page_widget(page, "Daily")

        page = BasePageWidget(
            parent=self,
            page_name="LibraryExperimentalListWidget",
            time_label="Commit Time",
            info_text="Nothing to show yet",
            extended_selection=True)
        self.LibraryExperimentalListWidget = \
            self.LibraryToolBox.add_page_widget(page, "Experimental")

        page = BasePageWidget(
            parent=self,
            page_name="DownloadsStableListWidget",
            time_label="Upload Time",
            info_text="No new builds available")
        self.DownloadsStableListWidget = \
            self.DownloadsToolBox.add_page_widget(page, "Stable")

        page = BasePageWidget(
            parent=self,
            page_name="DownloadsDailyListWidget",
            time_label="Upload Time",
            info_text="No new builds available",
            show_branch=False)
        self.DownloadsDailyListWidget = \
            self.DownloadsToolBox.add_page_widget(page, "Daily")

        page = BasePageWidget(
            parent=self,
            page_name="DownloadsExperimentalListWidget",
            time_label="Upload Time",
            info_text="No new builds available")
        self.DownloadsExperimentalListWidget = \
            self.DownloadsToolBox.add_page_widget(
                page, "Experimental")

        page = BasePageWidget(
            parent=self,
            page_name="UserFavoritesListWidget",
            time_label="Commit Time",
            info_text="Nothing to show yet")
        self.UserFavoritesListWidget = \
            self.UserToolBox.add_page_widget(
                page, "Favorites")

        page = BasePageWidget(
            parent=self,
            page_name="UserCustomListWidget",
            time_label="Commit Time",
            info_text="Nothing to show yet",
            show_reload=True,
            extended_selection=True)
        self.UserCustomListWidget = \
            self.UserToolBox.add_page_widget(page, "Custom")

        self.TabWidget.setCurrentIndex(get_default_tab())
        self.LibraryToolBox.setCurrentIndex(get_default_library_page())
        self.DownloadsToolBox.setCurrentIndex(get_default_downloads_page())

        # Connect buttons
        self.SettingsButton.clicked.connect(self.show_settings_window)
        self.WikiButton.clicked.connect(lambda: webbrowser.open(
            "https://github.com/DotBow/Blender-Launcher/wiki"))
        self.MinimizeButton.clicked.connect(self.showMinimized)
        self.CloseButton.clicked.connect(self.close)

        self.StatusBar.setContentsMargins(0, 0, 0, 2)
        self.StatusBar.setFont(self.font)
        self.statusbarLabel = QLabel()
        self.statusbarLabel.setIndent(8)
        self.NewVersionButton = QPushButton()
        self.NewVersionButton.hide()
        self.NewVersionButton.clicked.connect(self.show_update_window)
        self.statusbarVersion = QLabel(self.version)
        self.statusbarVersion.setToolTip(
            "The version of Blender Launcher that is currently run")
        self.StatusBar.addPermanentWidget(self.statusbarLabel, 1)
        self.StatusBar.addPermanentWidget(self.NewVersionButton)
        self.StatusBar.addPermanentWidget(self.statusbarVersion)

        # Draw library
        self.draw_library()

        # Setup tray icon context Menu
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.quit)
        hide_action = QAction("Hide", self)
        hide_action.triggered.connect(self.close)
        show_action = QAction("Show", self)
        show_action.triggered.connect(self._show)
        show_favorites_action = QAction(self.icon_favorite, "Favorites", self)
        show_favorites_action.triggered.connect(self.show_favorites)
        quick_launch_action = QAction(self.icon_quick_launch, "Blender", self)
        quick_launch_action.triggered.connect(self.quick_launch)

        self.tray_menu = BaseMenuWidget()
        self.tray_menu.setFont(self.font)
        self.tray_menu.addAction(quick_launch_action)
        self.tray_menu.addAction(show_favorites_action)
        self.tray_menu.addAction(show_action)
        self.tray_menu.addAction(hide_action)
        self.tray_menu.addAction(quit_action)

        # Setup tray icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.icon_taskbar)
        self.tray_icon.setToolTip("Blender Launcher")
        self.tray_icon.activated.connect(self.tray_icon_activated)
        self.tray_icon.messageClicked.connect(self._show)

        # Forse style update
        if polish is True:
            self.style().unpolish(self.app)
            self.style().polish(self.app)

        # Show window
        if get_show_tray_icon():
            self.tray_icon.show()

            if get_launch_minimized_to_tray() is False:
                self._show()
        else:
            self._show()

    def show_update_window(self):
        download_widgets = []

        download_widgets.extend(self.DownloadsStableListWidget.items())
        download_widgets.extend(self.DownloadsDailyListWidget.items())
        download_widgets.extend(self.DownloadsExperimentalListWidget.items())

        for widget in download_widgets:
            if widget.state == DownloadState.DOWNLOADING:
                self.dlg = DialogWindow(
                    self, title="Warning",
                    text="In order to update Blender Launcher<br> \
                          complete all active downloads!",
                    accept_text="OK", cancel_text=None)

                return

        self.tray_icon.hide()
        self.close()
        self.update_window = UpdateWindow(self, self.latest_tag)

    def _show(self):
        platform = get_platform()

        if self.isMinimized():
            self.showNormal()

        if platform == "Windows":
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            self.show()
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
            self.show()
        elif platform == "Linux":
            self.show()
            self.activateWindow()

        self.set_status()
        self.show_signal.emit()

    def show_message(self, message, value=None, type=None):
        if (type == MessageType.DOWNLOADFINISHED and
                get_enable_download_notifications() is False):
            return
        elif (type == MessageType.NEWBUILDS and
              get_enable_new_builds_notifications() is False):
            return

        if value not in self.notification_pool:
            if value is not None:
                self.notification_pool.append(value)
            self.tray_icon.showMessage(
                "Blender Launcher", message,
                self.icon_taskbar, 10000)

    def show_favorites(self):
        self.TabWidget.setCurrentWidget(self.UserTab)
        self.UserToolBox.setCurrentWidget(self.UserFavoritesListWidget)
        self._show()

    def quick_launch(self):
        try:
            self.favorite.launch()
        except Exception:
            self.dlg = DialogWindow(
                self, text="Add build to Quick Launch via<br>\
                            context menu to run it from tray",
                accept_text="OK", cancel_text=None, icon=DialogIcon.INFO)

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self._show()
        elif reason == QSystemTrayIcon.MiddleClick:
            self.quick_launch()
        elif reason == QSystemTrayIcon.Context:
            self.tray_menu._show()

    def quit(self):
        download_widgets = []

        download_widgets.extend(self.DownloadsStableListWidget.items())
        download_widgets.extend(self.DownloadsDailyListWidget.items())
        download_widgets.extend(self.DownloadsExperimentalListWidget.items())

        for widget in download_widgets:
            if widget.state == DownloadState.DOWNLOADING:
                self.dlg = DialogWindow(
                    self, title="Warning",
                    text="Active downloads in progress!<br>\
                          Are you sure you want to quit?",
                    accept_text="Yes", cancel_text="No")

                self.dlg.accepted.connect(self.destroy)
                return

        self.destroy()

    def destroy(self):
        if self.timer is not None:
            self.timer.cancel()

        self.tray_icon.hide()
        self.app.quit()

    def draw_library(self, clear=False):
        self.set_status("Updating", "Reading local builds")

        if clear:
            self.timer.cancel()
            self.scraper.quit()
            self.DownloadsStableListWidget._clear()
            self.DownloadsDailyListWidget._clear()
            self.DownloadsExperimentalListWidget._clear()
            self.started = True

        self.favorite = None

        self.LibraryStableListWidget._clear()
        self.LibraryDailyListWidget._clear()
        self.LibraryExperimentalListWidget._clear()
        self.UserCustomListWidget._clear()

        self.library_drawer = LibraryDrawer()
        self.library_drawer.build_found.connect(self.draw_to_library)
        self.library_drawer.finished.connect(self.draw_downloads)
        self.library_drawer.start()

    def reload_custom_builds(self):
        self.UserCustomListWidget._clear()
        self.library_drawer = LibraryDrawer()
        self.library_drawer.build_found.connect(self.draw_to_library)
        self.library_drawer.start()

    def draw_downloads(self):
        for page in self.DownloadsToolBox.pages:
            page.set_info_label_text("Checking for new builds")

        self.cashed_builds.clear()
        self.new_downloads = False
        self.app_state = AppState.CHECKINGBUILDS
        self.set_status("Updating", "Checking for new builds")
        self.scraper = Scraper(self, self.manager)
        self.scraper.links.connect(self.draw_to_downloads)
        self.scraper.new_bl_version.connect(self.set_version)
        self.scraper.error.connect(self.connection_error)
        self.scraper.finished.connect(self.scraper_finished)
        self.scraper.start()

    def connection_error(self):
        set_locale()
        utcnow = strftime(('%H:%M'), localtime())
        self.set_status("Error", "Connection failed at " + utcnow)
        self.app_state = AppState.IDLE

        self.timer = threading.Timer(600.0, self.draw_downloads)
        self.timer.start()

    def scraper_finished(self):
        if self.new_downloads and not self.started:
            self.show_message(
                "New builds of Blender are available!",
                type=MessageType.NEWBUILDS)

        for list_widget in self.DownloadsToolBox.list_widgets:
            for widget in list_widget.widgets.copy():
                if widget.build_info not in self.cashed_builds:
                    widget.destroy()

        set_locale()
        utcnow = strftime(('%H:%M'), localtime())
        self.set_status("Ready", "Last check at " + utcnow)
        self.app_state = AppState.IDLE

        for page in self.DownloadsToolBox.pages:
            page.set_info_label_text("No new builds available")

        self.timer = threading.Timer(600.0, self.draw_downloads)
        self.timer.start()
        self.started = False

    def draw_from_cashed(self, build_info):
        if self.app_state == AppState.IDLE:
            for cashed_build in self.cashed_builds:
                if build_info == cashed_build:
                    self.draw_to_downloads(cashed_build, False)
                    return

    def draw_to_downloads(self, build_info, show_new=True):
        show_branch = True

        if self.started:
            show_new = False

        if build_info not in self.cashed_builds:
            self.cashed_builds.append(build_info)

        branch = build_info.branch

        if (branch == 'stable') or (branch == 'lts'):
            downloads_list_widget = self.DownloadsStableListWidget
            library_list_widget = self.LibraryStableListWidget
        elif branch == 'daily':
            downloads_list_widget = self.DownloadsDailyListWidget
            library_list_widget = self.LibraryDailyListWidget
            show_branch = False
        else:
            downloads_list_widget = self.DownloadsExperimentalListWidget
            library_list_widget = self.LibraryExperimentalListWidget

        if not library_list_widget.contains_build_info(build_info) and \
                not downloads_list_widget.contains_build_info(build_info):
            item = BaseListWidgetItem(build_info.commit_time)
            widget = DownloadWidget(
                self, downloads_list_widget, item,
                build_info, show_branch, show_new)
            downloads_list_widget.add_item(item, widget)
            self.new_downloads = True

    def draw_to_library(self, path, show_new=False):
        branch = Path(path).parent.name
        show_branch = True

        if (branch == 'stable') or (branch == 'lts'):
            list_widget = self.LibraryStableListWidget
        elif branch == 'daily':
            list_widget = self.LibraryDailyListWidget
            show_branch = False
        elif branch == 'experimental':
            list_widget = self.LibraryExperimentalListWidget
        elif branch == 'custom':
            list_widget = self.UserCustomListWidget
        else:
            return

        item = BaseListWidgetItem()
        widget = LibraryWidget(self, item, path, list_widget,
                               show_branch, show_new)
        list_widget.insert_item(item, widget)

    def set_status(self, status=None, text=None):
        if status is not None:
            self.status = status

        if text is not None:
            self.text = text

        self.statusbarLabel.setText("{0} | {1}".format(self.status, self.text))

    def set_version(self, latest_tag):
        latest_ver = re.sub(r'\D', '', latest_tag)
        current_ver = re.sub(r'\D', '', self.version)

        if int(latest_ver) > int(current_ver):
            if latest_tag not in self.notification_pool:
                self.NewVersionButton.setText(
                    "Update to version {0}".
                    format(latest_tag.replace('v', '')))
                self.NewVersionButton.show()
                self.show_message(
                    "New version of Blender Launcher is available!",
                    latest_tag)

            self.latest_tag = latest_tag

    def show_settings_window(self):
        self.settings_window = SettingsWindow(self)

    def clear_temp(self):
        temp_folder = Path(get_library_folder()) / ".temp"
        self.remover = Remover(temp_folder)
        self.remover.start()

    def closeEvent(self, event):
        if get_show_tray_icon():
            event.ignore()
            self.hide()
            self.close_signal.emit()
        else:
            self.destroy()

    def new_connection(self):
        self._show()

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        print(e.mimeData().text())
