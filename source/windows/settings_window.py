from layouts.settings_form_layout import SettingsFormLayout
from modules.settings import (downloads_pages, favorite_pages,
                              get_bash_arguments,
                              get_blender_startup_arguments,
                              get_default_downloads_page,
                              get_default_library_page, get_default_tab,
                              get_enable_download_notifications,
                              get_enable_high_dpi_scaling,
                              get_enable_new_builds_notifications,
                              get_install_template,
                              get_launch_minimized_to_tray,
                              get_launch_when_system_starts,
                              get_library_folder, get_mark_as_favorite,
                              get_platform, get_show_tray_icon,
                              get_sync_library_and_downloads_pages,
                              get_taskbar_icon_color, library_pages,
                              set_bash_arguments,
                              set_blender_startup_arguments,
                              set_default_downloads_page,
                              set_default_library_page, set_default_tab,
                              set_enable_download_notifications,
                              set_enable_high_dpi_scaling,
                              set_enable_new_builds_notifications,
                              set_install_template,
                              set_launch_minimized_to_tray,
                              set_launch_when_system_starts,
                              set_library_folder, set_mark_as_favorite,
                              set_show_tray_icon,
                              set_sync_library_and_downloads_pages,
                              set_taskbar_icon_color, tabs,
                              taskbar_icon_colors)
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (QCheckBox, QComboBox, QFileDialog, QFormLayout,
                             QHBoxLayout, QLabel, QLineEdit, QMainWindow,
                             QPushButton, QWidget)
from ui.settings_window_ui import Ui_SettingsWindow

from windows.base_window import BaseWindow
from windows.dialog_window import DialogWindow


class SettingsWindow(QMainWindow, BaseWindow, Ui_SettingsWindow):
    def __init__(self, parent):
        super(SettingsWindow, self).__init__(parent=parent)

        self.setWindowFlag(Qt.SubWindow)
        self.setupUi(self)
        platform = get_platform()

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
        self.CloseButton.clicked.connect(self.close)
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

        # Taskbar Icon Color
        self.TaskbarIconColorComboBox = QComboBox()
        self.TaskbarIconColorComboBox.addItems(taskbar_icon_colors.keys())
        self.TaskbarIconColorComboBox.setCurrentIndex(
            get_taskbar_icon_color())
        self.TaskbarIconColorComboBox.activated[str].connect(
            self.change_taskbar_icon_color)

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
        layout = SettingsFormLayout(220)
        layout._addRow(
            "Taskbar Icon Color", self.TaskbarIconColorComboBox)

        if platform == 'Windows':
            layout._addRow("Launch When System Starts",
                           self.LaunchWhenSystemStartsCheckBox)

        layout._addRow("Show Tray Icon",
                       self.ShowTrayIconCheckBox)
        self.LaunchMinimizedToTrayRow = \
            layout._addRow("Launch Minimized To Tray",
                           self.LaunchMinimizedToTrayCheckBox)
        self.LaunchMinimizedToTrayRow.setEnabled(get_show_tray_icon())
        SettingsLayout.addRow(layout)

        SettingsLayout.addRow(self._QLabel("Interface:"))
        layout = SettingsFormLayout(220)
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
        layout = SettingsFormLayout(220)
        layout._addRow("When New Builds Are Available",
                       self.EnableNewBuildsNotifications)
        layout._addRow("When Downloading Is Finished",
                       self.EnableDownloadNotifications)
        SettingsLayout.addRow(layout)

        SettingsLayout.addRow(self._QLabel("New Build Actions:"))
        layout = SettingsFormLayout(220)
        layout._addRow("Mark As Favorite", self.MarkAsFavorite)
        layout._addRow("Install Template", self.InstallTemplate)
        SettingsLayout.addRow(layout)

        SettingsLayout.addRow(self._QLabel("Blender Launching:"))
        layout = SettingsFormLayout(120)
        layout._addRow("Startup Arguments",
                       self.BlenderStartupArguments)

        if platform == 'Linux':
            layout._addRow("Bash Arguments",
                           self.BashArguments)

        SettingsLayout.addRow(layout)

        self.resize(self.sizeHint())
        self.show()

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
        new_library_folder = QFileDialog.getExistingDirectory(
            self, "Select Library Folder", library_folder,
            options=QFileDialog.DontUseNativeDialog | QFileDialog.ShowDirsOnly)

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

    def change_taskbar_icon_color(self, color):
        currentIndex = self.TaskbarIconColorComboBox.currentIndex()

        if get_taskbar_icon_color() != currentIndex:
            set_taskbar_icon_color(color)
            self.show_dlg_restart_bl()

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

    def toggle_show_tray_icon(self, is_checked):
        set_show_tray_icon(is_checked)
        self.LaunchMinimizedToTrayRow.setEnabled(is_checked)
        self.parent.tray_icon.setVisible(is_checked)
