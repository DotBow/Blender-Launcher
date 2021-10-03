import os
import re
import threading
import webbrowser
from enum import Enum
from pathlib import Path
from shutil import copyfileobj
from time import localtime, strftime

from items.base_list_widget_item import BaseListWidgetItem
from modules._platform import (_popen, get_cwd, get_platform, is_frozen,
                               set_locale)
from modules.enums import MessageType
from modules.settings import (create_library_folders,
                              get_default_downloads_page,
                              get_default_library_page, get_default_tab,
                              get_enable_download_notifications,
                              get_enable_new_builds_notifications,
                              get_enable_quick_launch_key_seq,
                              get_launch_minimized_to_tray, get_library_folder,
                              get_quick_launch_key_seq, get_show_tray_icon,
                              get_sync_library_and_downloads_pages,
                              get_taskbar_icon_color, is_library_folder_valid,
                              set_library_folder, taskbar_icon_paths)
from pynput import keyboard
from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtNetwork import QLocalServer
from PyQt5.QtWidgets import (QAction, QHBoxLayout, QLabel, QMainWindow,
                             QPushButton, QSystemTrayIcon, QTabWidget,
                             QVBoxLayout, QWidget)
from threads.library_drawer import LibraryDrawer
from threads.remover import Remover
from threads.scraper import Scraper
from ui.main_window_ui import Ui_MainWindow
from widgets.base_menu_widget import BaseMenuWidget
from widgets.base_page_widget import BasePageWidget
from widgets.base_tool_box_widget import BaseToolBoxWidget
from widgets.download_widget import DownloadState, DownloadWidget
from widgets.library_widget import LibraryWidget

from windows.base_window import BaseWindow
from windows.dialog_window import DialogIcon, DialogWindow
from windows.file_dialog_window import FileDialogWindow
from windows.settings_window import SettingsWindow

if get_platform() == 'Windows':
    from PyQt5.QtWinExtras import QWinThumbnailToolBar, QWinThumbnailToolButton


class AppState(Enum):
    IDLE = 1
    CHECKINGBUILDS = 2


class BlenderLauncher(QMainWindow, BaseWindow, Ui_MainWindow):
    show_signal = pyqtSignal()
    close_signal = pyqtSignal()
    quit_signal = pyqtSignal()
    quick_launch_fail_signal = pyqtSignal()

    def __init__(self, app, version, logger, argv):
        super(BlenderLauncher, self).__init__(
            app=app, version=version)
        self.setupUi(self)
        self.setAcceptDrops(True)

        # Server
        self.server = QLocalServer()
        self.server.listen("blender-launcher-server")
        self.quick_launch_fail_signal.connect(self.quick_launch_fail)
        self.server.newConnection.connect(self.new_connection)

        # Global scope
        self.app = app
        self.version = version
        self.logger = logger
        self.argv = argv
        self.favorite = None
        self.status = "Ready"
        self.text = "OK"
        self.app_state = AppState.IDLE
        self.cashed_builds = []
        self.notification_pool = []
        self.windows = [self]
        self.timer = None
        self.started = True
        self.latest_tag = ""
        self.new_downloads = False
        self.platform = get_platform()
        self.remover_count = 0
        self.renamer_count = 0
        self.settings_window = None
        self.listener = None

        if self.platform == "macOS":
            self.app.aboutToQuit.connect(self._aboutToQuit)

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
        self.icon_download = QIcon(":resources/icons/download.svg")
        self.icon_file = QIcon(":resources/icons/file.svg")
        self.icon_taskbar = QIcon(taskbar_icon_paths[get_taskbar_icon_color()])

        # Setup window
        self.setWindowTitle("Blender Launcher")
        self.app.setWindowIcon(self.icon_taskbar)

        # Set library folder from command line arguments
        if "-set-library-folder" in self.argv:
            library_folder = self.argv[-1]

            if set_library_folder(library_folder) is True:
                create_library_folders(get_library_folder())
                self.draw(True)
            else:
                self.dlg = DialogWindow(
                    parent=self, title="Warning",
                    text="Passed path is not a valid folder or<br>\
                    it doesn't have write permissions!",
                    accept_text="Quit", cancel_text=None)
                self.dlg.accepted.connect(lambda: self.app.quit())

            return

        # Check library folder
        if is_library_folder_valid() is False:
            self.dlg = DialogWindow(
                parent=self, title="Information",
                text="First, choose where Blender<br>builds will be stored",
                accept_text="Continue", cancel_text=None, icon=DialogIcon.INFO)
            self.dlg.accepted.connect(self.set_library_folder)
        else:
            create_library_folders(get_library_folder())
            self.draw()

    def set_library_folder(self):
        library_folder = get_cwd().as_posix()
        new_library_folder = FileDialogWindow()._getExistingDirectory(
            self, "Select Library Folder", library_folder)

        if (new_library_folder):
            if set_library_folder(new_library_folder) is True:
                self.draw(True)
            else:
                self.dlg = DialogWindow(
                    parent=self, title="Warning",
                    text="Selected folder is not valid or<br>\
                    doesn't have write permissions!",
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
        self.DocsButton = QPushButton(self.icon_wiki, "")
        self.DocsButton.setIconSize(QSize(20, 20))
        self.DocsButton.setFixedSize(36, 32)
        self.DocsButton.setToolTip("Open documentation")
        self.MinimizeButton = QPushButton(self.icon_minimize, "")
        self.MinimizeButton.setIconSize(QSize(20, 20))
        self.MinimizeButton.setFixedSize(36, 32)
        self.CloseButton = QPushButton(self.icon_close, "")
        self.CloseButton.setIconSize(QSize(20, 20))
        self.CloseButton.setFixedSize(36, 32)
        self.HeaderLabel = QLabel("Blender Launcher")
        self.HeaderLabel.setAlignment(Qt.AlignCenter)

        self.HeaderLayout.addWidget(self.SettingsButton, 0, Qt.AlignLeft)
        self.HeaderLayout.addWidget(self.DocsButton, 0, Qt.AlignLeft)
        self.HeaderLayout.addWidget(self.HeaderLabel, 1)
        self.HeaderLayout.addWidget(self.MinimizeButton, 0, Qt.AlignRight)
        self.HeaderLayout.addWidget(self.CloseButton, 0, Qt.AlignRight)

        self.SettingsButton.setProperty("HeaderButton", True)
        self.DocsButton.setProperty("HeaderButton", True)
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

        self.toggle_sync_library_and_downloads_pages(
            get_sync_library_and_downloads_pages())

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
            info_text="No new builds available")
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
        self.DocsButton.clicked.connect(lambda: webbrowser.open(
            "https://dotbow.github.io/Blender-Launcher"))
        self.MinimizeButton.clicked.connect(self.showMinimized)
        self.CloseButton.clicked.connect(self.close)

        self.StatusBar.setContentsMargins(0, 0, 0, 2)
        self.StatusBar.setFont(self.font)
        self.statusbarLabel = QLabel()
        self.statusbarLabel.setIndent(8)
        self.NewVersionButton = QPushButton()
        self.NewVersionButton.hide()
        self.NewVersionButton.clicked.connect(self.show_update_window)
        self.statusbarVersion = QPushButton(self.version)
        self.statusbarVersion.clicked.connect(self.show_changelog)
        self.statusbarVersion.setToolTip(
            "The version of Blender Launcher that is currently run. "
            "Press to check changelog.")
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

        # Linux doesn't handle QSystemTrayIcon.Context activation reason,
        # so add context menu as regular one
        if self.platform == "Linux":
            self.tray_icon.setContextMenu(self.tray_menu)

        # Forse style update
        if polish is True:
            self.style().unpolish(self.app)
            self.style().polish(self.app)

        # Show window
        if is_frozen():
            if get_show_tray_icon():
                self.tray_icon.show()

                if get_launch_minimized_to_tray() is False:
                    self._show()
            else:
                self._show()
        else:
            self.tray_icon.show()
            self._show()

        if get_enable_quick_launch_key_seq() is True:
            self.setup_global_hotkeys_listener()

    def setup_global_hotkeys_listener(self):
        if self.listener is not None:
            self.listener.stop()

        key_seq = get_quick_launch_key_seq()
        keys = key_seq.split('+')

        for key in keys:
            if len(key) > 1:
                key_seq = key_seq.replace(key, '<' + key + '>')

        try:
            self.listener = keyboard.GlobalHotKeys({
                key_seq: self.on_activate_quick_launch})
        except Exception:
            self.dlg = DialogWindow(
                parent=self, title="Warning",
                text="Global hotkey sequence was not recognized!<br> \
                      Try to use another combination of keys",
                accept_text="OK", cancel_text=None)
            return

        self.listener.start()

    def on_activate_quick_launch(self):
        if self.settings_window is None:
            self.quick_launch()

    def show_changelog(self):
        current_ver = re.sub(r'\D', '', self.version)
        url = "https://dotbow.github.io/Blender-Launcher/changelog.html#{0}".format(
            current_ver)
        webbrowser.open(url)

    def toggle_sync_library_and_downloads_pages(self, is_sync):
        if is_sync:
            self.LibraryToolBox.tab_changed.connect(
                lambda i: self.DownloadsToolBox.setCurrentIndex(i))
            self.DownloadsToolBox.tab_changed.connect(
                lambda i: self.LibraryToolBox.setCurrentIndex(i))
        else:
            if self.isSignalConnected(self.LibraryToolBox, 'tab_changed()'):
                self.LibraryToolBox.tab_changed.disconnect()

            if self.isSignalConnected(self.DownloadsToolBox, 'tab_changed()'):
                self.DownloadsToolBox.tab_changed.disconnect()

    def isSignalConnected(self, obj, name):
        index = obj.metaObject().indexOfMethod(name)

        if index > -1:
            method = obj.metaObject().method(index)

            if method:
                return obj.isSignalConnected(method)

        return False

    def show_update_window(self):
        download_widgets = []

        download_widgets.extend(self.DownloadsStableListWidget.items())
        download_widgets.extend(self.DownloadsDailyListWidget.items())
        download_widgets.extend(self.DownloadsExperimentalListWidget.items())

        for widget in download_widgets:
            if widget.state == DownloadState.DOWNLOADING:
                self.dlg = DialogWindow(
                    parent=self, title="Warning",
                    text="In order to update Blender Launcher<br> \
                          complete all active downloads!",
                    accept_text="OK", cancel_text=None)

                return

        cwd = get_cwd()

        if self.platform == 'Windows':
            bl_exe = "Blender Launcher.exe"
            blu_exe = "Blender Launcher Updater.exe"
        elif self.platform == 'Linux':
            bl_exe = "Blender Launcher"
            blu_exe = "Blender Launcher Updater"

        source = cwd / bl_exe
        dist = cwd / blu_exe

        with open(source.as_posix(), 'rb') as f1, \
                open(dist.as_posix(), 'wb') as f2:
            copyfileobj(f1, f2)

        if self.platform == 'Windows':
            _popen([dist.as_posix(), '-update', self.latest_tag])
        elif self.platform == 'Linux':
            os.chmod(dist.as_posix(), 0o744)
            _popen('nohup "{0}" -update {1}'.format(dist.as_posix(),
                                                    self.latest_tag))

        self.destroy()

    def _show(self):
        if self.isMinimized():
            self.showNormal()

        if self.platform == "Windows":
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            self.show()
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
            self.show()
        elif self.platform in {"Linux", "macOS"}:
            self.show()
            self.activateWindow()

        self.set_status()
        self.show_signal.emit()

        # Add custom toolbar icons
        if self.platform == 'Windows':
            self.thumbnail_toolbar = QWinThumbnailToolBar(self)
            self.thumbnail_toolbar.setWindow(self.windowHandle())

            self.toolbar_quick_launch_btn = QWinThumbnailToolButton(
                self.thumbnail_toolbar)
            self.toolbar_quick_launch_btn.setIcon(self.icon_quick_launch)
            self.toolbar_quick_launch_btn.setToolTip("Quick Launch")
            self.toolbar_quick_launch_btn.clicked.connect(self.quick_launch)
            self.thumbnail_toolbar.addButton(self.toolbar_quick_launch_btn)

            self.toolbar_quit_btn = QWinThumbnailToolButton(
                self.thumbnail_toolbar)
            self.toolbar_quit_btn.setIcon(self.icon_close)
            self.toolbar_quit_btn.setToolTip("Quit")
            self.toolbar_quit_btn.clicked.connect(self.quit)
            self.thumbnail_toolbar.addButton(self.toolbar_quit_btn)

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
            self.quick_launch_fail_signal.emit()

    def quick_launch_fail(self):
        self.dlg = DialogWindow(
            parent=self, text="Add build to Quick Launch via<br>\
                        context menu to run it from tray",
            accept_text="OK", cancel_text=None, icon=DialogIcon.INFO)

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self._show()
        elif reason == QSystemTrayIcon.MiddleClick:
            self.quick_launch()
        elif reason == QSystemTrayIcon.Context:
            self.tray_menu._show()

    def _aboutToQuit(self):
        self.quit()

    def quit(self):
        download_widgets = []

        download_widgets.extend(self.DownloadsStableListWidget.items())
        download_widgets.extend(self.DownloadsDailyListWidget.items())
        download_widgets.extend(self.DownloadsExperimentalListWidget.items())

        for widget in download_widgets:
            if widget.state == DownloadState.DOWNLOADING:
                self.dlg = DialogWindow(
                    parent=self, title="Warning",
                    text="Active downloads in progress!<br>\
                          Are you sure you want to quit?",
                    accept_text="Yes", cancel_text="No")

                self.dlg.accepted.connect(self.destroy)
                return

        self.destroy()

    def destroy(self):
        self.quit_signal.emit()

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

        if "-offline" not in self.argv:
            self.library_drawer.finished.connect(self.draw_downloads)

        self.library_drawer.start()

    def reload_custom_builds(self):
        self.UserCustomListWidget._clear()
        self.library_drawer = LibraryDrawer(folders=['custom'])
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
        else:
            downloads_list_widget = self.DownloadsExperimentalListWidget
            library_list_widget = self.LibraryExperimentalListWidget

        if not library_list_widget.contains_build_info(build_info) and \
                not downloads_list_widget.contains_build_info(build_info):
            item = BaseListWidgetItem(build_info.commit_time)
            widget = DownloadWidget(
                self, downloads_list_widget, item,
                build_info, show_new)
            downloads_list_widget.add_item(item, widget)
            self.new_downloads = True

    def draw_to_library(self, path, show_new=False):
        branch = Path(path).parent.name

        if (branch == 'stable') or (branch == 'lts'):
            list_widget = self.LibraryStableListWidget
        elif branch == 'daily':
            list_widget = self.LibraryDailyListWidget
        elif branch == 'experimental':
            list_widget = self.LibraryExperimentalListWidget
        elif branch == 'custom':
            list_widget = self.UserCustomListWidget
        else:
            return

        item = BaseListWidgetItem()
        widget = LibraryWidget(self, item, path, list_widget,
                               show_new)
        list_widget.insert_item(item, widget)

    def set_status(self, status=None, text=None):
        if status is not None:
            self.status = status

        if text is not None:
            self.text = text

        self.statusbarLabel.setText("{0} │ {1}".format(self.status, self.text))

    def set_version(self, latest_tag):
        if "dev" in self.version:
            return

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
        self.settings_window = SettingsWindow(parent=self)

    def clear_temp(self):
        temp_folder = Path(get_library_folder()) / ".temp"
        self.remover = Remover(temp_folder, self.parent)
        self.remover.start()

    def closeEvent(self, event):
        if get_show_tray_icon():
            event.ignore()
            self.hide()
            self.close_signal.emit()
        else:
            self.destroy()

    def new_connection(self):
        self.socket = self.server.nextPendingConnection()
        self.socket.readyRead.connect(self.read_socket_data)
        self._show()

    def read_socket_data(self):
        data = self.socket.readAll()

        if str(data, encoding='ascii') != self.version:
            self.dlg = DialogWindow(
                parent=self, title="Warning",
                text="An attempt to launch a different version<br>\
                      of Blender Launcher was detected!<br>\
                      Please, terminate currently running<br>\
                      version to proceed this action!",
                accept_text="OK", cancel_text=None, icon=DialogIcon.WARNING)

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        print(e.mimeData().text())
