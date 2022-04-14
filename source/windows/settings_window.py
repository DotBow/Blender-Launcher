from layouts.settings_form_layout import SettingsFormLayout
from modules.settings import (downloads_pages, favorite_pages,
                              get_bash_arguments,
                              get_blender_startup_arguments,
                              get_check_for_new_builds_automatically,
                              get_default_downloads_page,
                              get_default_library_page, get_default_tab,
                              get_enable_download_notifications,
                              get_enable_high_dpi_scaling,
                              get_enable_new_builds_notifications,
                              get_enable_quick_launch_key_seq,
                              get_install_template,
                              get_launch_blender_no_console,
                              get_launch_minimized_to_tray,
                              get_launch_when_system_starts,
                              get_library_folder, get_mark_as_favorite,
                              get_new_builds_check_frequency, get_platform,
                              get_proxy_host, get_proxy_password,
                              get_proxy_port, get_proxy_type, get_proxy_user,
                              get_quick_launch_key_seq, get_show_tray_icon,
                              get_sync_library_and_downloads_pages,
                              get_use_custom_tls_certificates, library_pages,
                              proxy_types, set_bash_arguments,
                              set_blender_startup_arguments,
                              set_check_for_new_builds_automatically,
                              set_default_downloads_page,
                              set_default_library_page, set_default_tab,
                              set_enable_download_notifications,
                              set_enable_high_dpi_scaling,
                              set_enable_new_builds_notifications,
                              set_enable_quick_launch_key_seq,
                              set_install_template,
                              set_launch_blender_no_console,
                              set_launch_minimized_to_tray,
                              set_launch_when_system_starts,
                              set_library_folder, set_mark_as_favorite,
                              set_new_builds_check_frequency, set_proxy_host,
                              set_proxy_password, set_proxy_port,
                              set_proxy_type, set_proxy_user,
                              set_quick_launch_key_seq, set_show_tray_icon,
                              set_sync_library_and_downloads_pages,
                              set_use_custom_tls_certificates, tabs)
from PyQt5 import QtGui
from PyQt5.QtCore import QRegExp, QSize, Qt, QTime
from PyQt5.QtWidgets import (QCheckBox, QComboBox, QFormLayout, QHBoxLayout,
                             QLabel, QLineEdit, QMainWindow, QPushButton,
                             QTimeEdit, QWidget)
from ui.settings_window_ui import Ui_SettingsWindow

from windows.base_window import BaseWindow
from windows.dialog_window import DialogWindow
from windows.file_dialog_window import FileDialogWindow


class SettingsWindow(QMainWindow, BaseWindow, Ui_SettingsWindow):
    def __init__(self, parent):
        super(SettingsWindow, self).__init__(parent=parent)

        self.setupUi(self)
        platform = get_platform()
        self.con_settings_changed = False
        self.new_builds_check_settings_changed = False

        self.setWindowTitle("Settings")

        self.HeaderLayout = QHBoxLayout()
        self.HeaderLayout.setContentsMargins(36, 0, 0, 0)
        self.HeaderLayout.setSpacing(0)
        self.CentralLayout.addLayout(self.HeaderLayout)

        self.CloseButton = QPushButton(self.parent.icon_close, "")
        self.CloseButton.setIconSize(QSize(20, 20))
        self.CloseButton.setFixedSize(36, 32)
        self.CloseButton.setProperty("HeaderButton", True)
        self.CloseButton.setProperty("CloseButton", True)
        self.CloseButton.clicked.connect(self._close)
        self.HeaderLabel = QLabel("Settings")
        self.HeaderLabel.setAlignment(Qt.AlignCenter)

        self.HeaderLayout.addWidget(self.HeaderLabel, 1)
        self.HeaderLayout.addWidget(self.CloseButton, 0, Qt.AlignRight)

        # Library Folder
        self.LibraryFolderLineEdit = QLineEdit()
        self.LibraryFolderLineEdit.setText(str(get_library_folder()))
        self.LibraryFolderLineEdit.setContextMenuPolicy(Qt.NoContextMenu)
        self.LibraryFolderLineEdit.setReadOnly(True)
        self.LibraryFolderLineEdit.setCursorPosition(0)

        self.SetLibraryFolderButton = QPushButton(self.parent.icon_folder, "")
        self.SetLibraryFolderButton.clicked.connect(self.set_library_folder)

        self.LibraryFolderLayout = QHBoxLayout()
        self.LibraryFolderLayout.setContentsMargins(6, 0, 6, 0)
        self.LibraryFolderLayout.setSpacing(0)

        self.LibraryFolderLayout.addWidget(self.LibraryFolderLineEdit)
        self.LibraryFolderLayout.addWidget(self.SetLibraryFolderButton)

        # Launch When System Starts
        self.LaunchWhenSystemStartsCheckBox = QCheckBox()
        self.LaunchWhenSystemStartsCheckBox.setChecked(
            get_launch_when_system_starts())
        self.LaunchWhenSystemStartsCheckBox.clicked.connect(
            self.toggle_launch_when_system_starts)

        # Launch Minimized To Tray
        self.LaunchMinimizedToTrayCheckBox = QCheckBox()
        self.LaunchMinimizedToTrayCheckBox.setChecked(
            get_launch_minimized_to_tray())
        self.LaunchMinimizedToTrayCheckBox.clicked.connect(
            self.toggle_launch_minimized_to_tray)

        # Show Tray Icon
        self.ShowTrayIconCheckBox = QCheckBox()
        self.ShowTrayIconCheckBox.setChecked(get_show_tray_icon())
        self.ShowTrayIconCheckBox.clicked.connect(self.toggle_show_tray_icon)

        # High Dpi Scaling
        self.EnableHighDpiScalingCheckBox = QCheckBox()
        self.EnableHighDpiScalingCheckBox.clicked.connect(
            self.toggle_enable_high_dpi_scaling)
        self.EnableHighDpiScalingCheckBox.setChecked(
            get_enable_high_dpi_scaling())

        # New Builds Check Settings
        self.CheckForNewBuildsAutomatically = QCheckBox()
        self.CheckForNewBuildsAutomatically.setChecked(
            get_check_for_new_builds_automatically())
        self.CheckForNewBuildsAutomatically.clicked.connect(
            self.toggle_check_for_new_builds_automatically)

        self.NewBuildsCheckFrequency = QTimeEdit()
        self.NewBuildsCheckFrequency.setTime(
            QTime().fromMSecsSinceStartOfDay(
                get_new_builds_check_frequency() * 1000))
        self.NewBuildsCheckFrequency.editingFinished.connect(
            self.new_builds_check_frequency_changed)

        # Custom TLS certificates
        self.UseCustomCertificatesCheckBox = QCheckBox()
        self.UseCustomCertificatesCheckBox.clicked.connect(
            self.toggle_use_custom_tls_certificates)
        self.UseCustomCertificatesCheckBox.setChecked(
            get_use_custom_tls_certificates())

        # Proxy Type
        self.ProxyTypeComboBox = QComboBox()
        self.ProxyTypeComboBox.addItems(proxy_types.keys())
        self.ProxyTypeComboBox.setCurrentIndex(get_proxy_type())
        self.ProxyTypeComboBox.activated[str].connect(self.change_proxy_type)

        # Proxy URL
        self.ProxyHostLineEdit = QLineEdit()
        self.ProxyHostLineEdit.setText(str(get_proxy_host()))
        self.ProxyHostLineEdit.setContextMenuPolicy(Qt.NoContextMenu)
        rx = QRegExp(
            r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$")
        self.host_validator = QtGui.QRegExpValidator(rx, self)
        self.ProxyHostLineEdit.setValidator(self.host_validator)
        self.ProxyHostLineEdit.editingFinished.connect(self.update_proxy_host)

        self.ProxyPortLineEdit = QLineEdit()
        self.ProxyPortLineEdit.setText(str(get_proxy_port()))
        self.ProxyPortLineEdit.setContextMenuPolicy(Qt.NoContextMenu)
        rx = QRegExp(r"\d{2,5}")
        self.port_validator = QtGui.QRegExpValidator(rx, self)
        self.ProxyPortLineEdit.setValidator(self.port_validator)
        self.ProxyPortLineEdit.editingFinished.connect(self.update_proxy_port)

        # Proxy authentication
        self.ProxyUserLineEdit = QLineEdit()
        self.ProxyUserLineEdit.setText(str(get_proxy_user()))
        self.ProxyUserLineEdit.setContextMenuPolicy(Qt.NoContextMenu)
        self.ProxyUserLineEdit.editingFinished.connect(self.update_proxy_user)

        self.ProxyPasswordLineEdit = QLineEdit()
        self.ProxyPasswordLineEdit.setText(str(get_proxy_password()))
        self.ProxyPasswordLineEdit.setContextMenuPolicy(Qt.NoContextMenu)
        self.ProxyPasswordLineEdit.setEchoMode(QLineEdit.Password)
        self.ProxyPasswordLineEdit.editingFinished.connect(
            self.update_proxy_password)

        # Default Tab
        self.DefaultTabComboBox = QComboBox()
        self.DefaultTabComboBox.addItems(tabs.keys())
        self.DefaultTabComboBox.setCurrentIndex(get_default_tab())
        self.DefaultTabComboBox.activated[str].connect(self.change_default_tab)

        # Sync Library and Downloads pages
        self.SyncLibraryAndDownloadsPages = QCheckBox()
        self.SyncLibraryAndDownloadsPages.clicked.connect(
            self.toggle_sync_library_and_downloads_pages)
        self.SyncLibraryAndDownloadsPages.setChecked(
            get_sync_library_and_downloads_pages())

        # Default Library Page
        self.DefaultLibraryPageComboBox = QComboBox()
        self.DefaultLibraryPageComboBox.addItems(library_pages.keys())
        self.DefaultLibraryPageComboBox.setCurrentIndex(
            get_default_library_page())
        self.DefaultLibraryPageComboBox.activated[str].connect(
            self.change_default_library_page)

        # Default Downloads Page
        self.DefaultDownloadsPageComboBox = QComboBox()
        self.DefaultDownloadsPageComboBox.addItems(downloads_pages.keys())
        self.DefaultDownloadsPageComboBox.setCurrentIndex(
            get_default_downloads_page())
        self.DefaultDownloadsPageComboBox.activated[str].connect(
            self.change_default_downloads_page)

        # Notifications
        self.EnableNewBuildsNotifications = QCheckBox()
        self.EnableNewBuildsNotifications.clicked.connect(
            self.toggle_enable_new_builds_notifications)
        self.EnableNewBuildsNotifications.setChecked(
            get_enable_new_builds_notifications())

        self.EnableDownloadNotifications = QCheckBox()
        self.EnableDownloadNotifications.clicked.connect(
            self.toggle_enable_download_notifications)
        self.EnableDownloadNotifications.setChecked(
            get_enable_download_notifications())

        # Mark As Favorite
        self.MarkAsFavorite = QComboBox()
        self.MarkAsFavorite.addItems(favorite_pages.keys())
        self.MarkAsFavorite.setCurrentIndex(
            get_mark_as_favorite())
        self.MarkAsFavorite.activated[str].connect(
            self.change_mark_as_favorite)

        # Blender Startup Arguments
        self.BlenderStartupArguments = QLineEdit()
        self.BlenderStartupArguments.setText(
            str(get_blender_startup_arguments()))
        self.BlenderStartupArguments.setContextMenuPolicy(Qt.NoContextMenu)
        self.BlenderStartupArguments.setCursorPosition(0)
        self.BlenderStartupArguments.editingFinished.connect(
            self.update_blender_startup_arguments)

        # Command Line Arguments
        self.BashArguments = QLineEdit()
        self.BashArguments.setText(
            str(get_bash_arguments()))
        self.BashArguments.setContextMenuPolicy(Qt.NoContextMenu)
        self.BashArguments.setCursorPosition(0)
        self.BashArguments.editingFinished.connect(
            self.update_bash_arguments)

        # Install Template
        self.InstallTemplate = QCheckBox()
        self.InstallTemplate.clicked.connect(self.toggle_install_template)
        self.InstallTemplate.setChecked(get_install_template())

        # Run Blender using blender-launcher.exe
        self.LaunchBlenderNoConsole = QCheckBox()
        self.LaunchBlenderNoConsole.clicked.connect(
            self.toggle_launch_blender_no_console)
        self.LaunchBlenderNoConsole.setChecked(get_launch_blender_no_console())

        # Quick Launch Key Sequence
        self.EnableQuickLaunchKeySeq = QCheckBox()
        self.EnableQuickLaunchKeySeq.clicked.connect(
            self.toggle_enable_quick_launch_key_seq)
        self.EnableQuickLaunchKeySeq.setChecked(
            get_enable_quick_launch_key_seq())

        self.QuickLaunchKeySeq = QLineEdit()
        self.QuickLaunchKeySeq.setEnabled(get_enable_quick_launch_key_seq())
        self.QuickLaunchKeySeq.keyPressEvent = self._keyPressEvent
        self.QuickLaunchKeySeq.setText(
            str(get_quick_launch_key_seq()))
        self.QuickLaunchKeySeq.setContextMenuPolicy(Qt.NoContextMenu)
        self.QuickLaunchKeySeq.setCursorPosition(0)
        self.QuickLaunchKeySeq.editingFinished.connect(
            self.update_quick_launch_key_seq)

        # Layout
        SettingsLayoutContainer = QWidget(self)
        SettingsLayoutContainer.setProperty('FormLayout', True)
        SettingsLayout = QFormLayout(SettingsLayoutContainer)
        SettingsLayout.setContentsMargins(0, 0, 0, 6)
        SettingsLayout.setSpacing(6)
        SettingsLayout.setRowWrapPolicy(QFormLayout.DontWrapRows)
        SettingsLayout.setFieldGrowthPolicy(
            QFormLayout.AllNonFixedFieldsGrow)
        SettingsLayout.setLabelAlignment(Qt.AlignLeft)
        self.CentralLayout.addWidget(SettingsLayoutContainer)

        SettingsLayout.addRow(self._QLabel("Library Folder:"))
        SettingsLayout.addRow(self.LibraryFolderLayout)

        SettingsLayout.addRow(self._QLabel("System:"))
        layout = SettingsFormLayout(240)

        if platform == 'Windows':
            layout._addRow("Launch When System Starts",
                           self.LaunchWhenSystemStartsCheckBox)

        layout._addRow("Show Tray Icon",
                       self.ShowTrayIconCheckBox)
        self.LaunchMinimizedToTrayRow = \
            layout._addRow("Launch Minimized To Tray",
                           self.LaunchMinimizedToTrayCheckBox)
        self.LaunchMinimizedToTrayRow.setEnabled(get_show_tray_icon())

        sub_layout = QHBoxLayout()
        sub_layout.addWidget(self.CheckForNewBuildsAutomatically)
        sub_layout.addWidget(self.NewBuildsCheckFrequency)
        self.NewBuildsCheckRow = layout._addRow(
            "Check For New Builds Automatically", sub_layout)

        SettingsLayout.addRow(layout)

        SettingsLayout.addRow(self._QLabel("Connection:"))
        layout = SettingsFormLayout(240)
        layout._addRow("Use Custom TLS Certificates",
                       self.UseCustomCertificatesCheckBox)
        layout._addRow("Proxy Type", self.ProxyTypeComboBox)

        sub_layout = QHBoxLayout()
        sub_layout.addWidget(self.ProxyHostLineEdit)
        sub_layout.addWidget(QLabel(" : "))
        sub_layout.addWidget(self.ProxyPortLineEdit)
        layout._addRow("Proxy IP", sub_layout)

        layout._addRow("Proxy User", self.ProxyUserLineEdit)
        layout._addRow("Proxy Password", self.ProxyPasswordLineEdit)

        SettingsLayout.addRow(layout)

        SettingsLayout.addRow(self._QLabel("Interface:"))
        layout = SettingsFormLayout(240)
        layout._addRow(
            "Default Tab", self.DefaultTabComboBox)
        layout._addRow(
            "Sync Library & Downloads Pages",
            self.SyncLibraryAndDownloadsPages)
        layout._addRow(
            "Default Library Page", self.DefaultLibraryPageComboBox)
        layout._addRow(
            "Default Downloads Page", self.DefaultDownloadsPageComboBox)
        layout._addRow("Enable High DPI Scaling",
                       self.EnableHighDpiScalingCheckBox)
        SettingsLayout.addRow(layout)

        SettingsLayout.addRow(self._QLabel("Notifications:"))
        layout = SettingsFormLayout(240)
        layout._addRow("When New Builds Are Available",
                       self.EnableNewBuildsNotifications)
        layout._addRow("When Downloading Is Finished",
                       self.EnableDownloadNotifications)
        SettingsLayout.addRow(layout)

        SettingsLayout.addRow(self._QLabel("New Build Actions:"))
        layout = SettingsFormLayout(240)
        layout._addRow("Mark As Favorite", self.MarkAsFavorite)
        layout._addRow("Install Template", self.InstallTemplate)
        SettingsLayout.addRow(layout)

        SettingsLayout.addRow(self._QLabel("Blender Launching:"))
        layout = SettingsFormLayout(240)

        sub_layout = QHBoxLayout()
        sub_layout.addWidget(self.EnableQuickLaunchKeySeq)
        sub_layout.addWidget(self.QuickLaunchKeySeq)
        self.QuickLaunchKeySeqRow = layout._addRow(
            "Quick Launch Global Shortcut", sub_layout)

        if platform == 'Windows':
            layout._addRow("Hide Console On Startup",
                           self.LaunchBlenderNoConsole)

        layout.addRow(QLabel("Startup Arguments:"))
        layout.addRow(self.BlenderStartupArguments)

        if platform == 'Linux':
            layout.addRow(QLabel("Bash Arguments:"))
            layout.addRow(self.BashArguments)

        SettingsLayout.addRow(layout)

        self.resize(self.sizeHint())
        self.show()

    def _close(self):
        if get_enable_quick_launch_key_seq() is True:
            self.parent.setup_global_hotkeys_listener()
        elif self.parent.listener is not None:
            self.parent.listener.stop()

        if self.new_builds_check_settings_changed is True:
            self.new_builds_check_settings_changed = False
            new_builds_check_frequency = \
                self.NewBuildsCheckFrequency.time().msecsSinceStartOfDay() * 0.001

            if get_new_builds_check_frequency() != new_builds_check_frequency:
                set_new_builds_check_frequency(new_builds_check_frequency)
                self.new_builds_check_settings_changed = True

            if get_check_for_new_builds_automatically() != \
                    self.CheckForNewBuildsAutomatically.isChecked():
                set_check_for_new_builds_automatically(
                    self.CheckForNewBuildsAutomatically.isChecked())
                self.new_builds_check_settings_changed = True

        if self.con_settings_changed or self.new_builds_check_settings_changed:
            self.parent.draw_library(clear=True)

        self.parent.settings_window = None
        self.close()

    def _QLabel(self, text):
        label = QLabel(text)
        label.setIndent(6)
        label.setProperty('Header', True)
        return label

    def show_dlg_restart_bl(self):
        self.dlg = DialogWindow(
            parent=self.parent, title="Warning",
            text="Restart Blender Launcher in<br> \
                  order to apply this setting!",
            accept_text="OK", cancel_text=None)

    def set_library_folder(self):
        library_folder = str(get_library_folder())
        new_library_folder = FileDialogWindow()._getExistingDirectory(
            self, "Select Library Folder", library_folder)

        if new_library_folder and (library_folder != new_library_folder):
            if set_library_folder(new_library_folder) is True:
                self.LibraryFolderLineEdit.setText(new_library_folder)
                self.parent.draw_library(clear=True)
            else:
                self.dlg = DialogWindow(
                    parent=self.parent, title="Warning",
                    text="Selected folder doesn't have write permissions!",
                    accept_text="Retry", cancel_text=None)
                self.dlg.accepted.connect(self.set_library_folder)

    def toggle_launch_when_system_starts(self, is_checked):
        set_launch_when_system_starts(is_checked)

    def toggle_launch_minimized_to_tray(self, is_checked):
        set_launch_minimized_to_tray(is_checked)

    def toggle_enable_high_dpi_scaling(self, is_checked):
        set_enable_high_dpi_scaling(is_checked)
        self.show_dlg_restart_bl()

    def toggle_use_custom_tls_certificates(self, is_checked):
        set_use_custom_tls_certificates(is_checked)
        self.con_settings_changed = True

    def change_proxy_type(self, type):
        set_proxy_type(type)
        self.con_settings_changed = True

    def update_proxy_host(self):
        host = self.ProxyHostLineEdit.text()
        set_proxy_host(host)
        self.con_settings_changed = True

    def update_proxy_port(self):
        port = self.ProxyPortLineEdit.text()
        set_proxy_port(port)
        self.con_settings_changed = True

    def update_proxy_user(self):
        user = self.ProxyUserLineEdit.text()
        set_proxy_user(user)
        self.con_settings_changed = True

    def update_proxy_password(self):
        password = self.ProxyPasswordLineEdit.text()
        set_proxy_password(password)
        self.con_settings_changed = True

    def change_default_tab(self, tab):
        set_default_tab(tab)

    def change_default_library_page(self, page):
        set_default_library_page(page)

        if get_sync_library_and_downloads_pages():
            index = self.DefaultLibraryPageComboBox.currentIndex()
            self.DefaultDownloadsPageComboBox.setCurrentIndex(index)
            set_default_downloads_page(page)

    def change_default_downloads_page(self, page):
        set_default_downloads_page(page)

        if get_sync_library_and_downloads_pages():
            index = self.DefaultDownloadsPageComboBox.currentIndex()
            self.DefaultLibraryPageComboBox.setCurrentIndex(index)
            set_default_library_page(page)

    def change_mark_as_favorite(self, page):
        set_mark_as_favorite(page)

    def toggle_check_for_new_builds_automatically(self, is_checked):
        self.new_builds_check_settings_changed = True

    def new_builds_check_frequency_changed(self):
        self.new_builds_check_settings_changed = True

    def toggle_sync_library_and_downloads_pages(self, is_checked):
        set_sync_library_and_downloads_pages(is_checked)
        self.parent.toggle_sync_library_and_downloads_pages(is_checked)

        if is_checked:
            index = self.DefaultLibraryPageComboBox.currentIndex()
            self.DefaultDownloadsPageComboBox.setCurrentIndex(index)
            text = self.DefaultLibraryPageComboBox.currentText()
            set_default_downloads_page(text)

    def toggle_enable_download_notifications(self, is_checked):
        set_enable_download_notifications(is_checked)

    def toggle_enable_new_builds_notifications(self, is_checked):
        set_enable_new_builds_notifications(is_checked)

    def update_blender_startup_arguments(self):
        args = self.BlenderStartupArguments.text()
        set_blender_startup_arguments(args)

    def update_bash_arguments(self):
        args = self.BashArguments.text()
        set_bash_arguments(args)

    def toggle_install_template(self, is_checked):
        set_install_template(is_checked)

    def toggle_launch_blender_no_console(self, is_checked):
        set_launch_blender_no_console(is_checked)

    def toggle_show_tray_icon(self, is_checked):
        set_show_tray_icon(is_checked)
        self.LaunchMinimizedToTrayRow.setEnabled(is_checked)
        self.parent.tray_icon.setVisible(is_checked)

    def update_quick_launch_key_seq(self):
        key_seq = self.QuickLaunchKeySeq.text()
        set_quick_launch_key_seq(key_seq)

    def toggle_enable_quick_launch_key_seq(self, is_checked):
        set_enable_quick_launch_key_seq(is_checked)
        self.QuickLaunchKeySeq.setEnabled(is_checked)

    def _keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        MOD_MASK = (Qt.CTRL | Qt.ALT | Qt.SHIFT)
        keyname = ''
        key = e.key()
        modifiers = int(e.modifiers())

        if (modifiers and modifiers & MOD_MASK == modifiers and
            key > 0 and key != Qt.Key_Shift and key != Qt.Key_Alt and
                key != Qt.Key_Control and key != Qt.Key_Meta):

            keyname = QtGui.QKeySequence(modifiers + key).toString()
        elif not modifiers and (key != Qt.Key_Meta):
            keyname = QtGui.QKeySequence(key).toString()

        if keyname != '':
            # Remap <Shift + *> keys sequences
            if 'Shift' in keyname:
                alt_chars = '~!@#$%^&*()_+|{}:"<>?'
                real_chars = r"`1234567890-=\[];',./"
                trans_table = str.maketrans(alt_chars, real_chars)
                trans = keyname[-1].translate(trans_table)
                keyname = keyname[:-1] + trans

            self.QuickLaunchKeySeq.setText(keyname.lower())

        return super().keyPressEvent(e)
