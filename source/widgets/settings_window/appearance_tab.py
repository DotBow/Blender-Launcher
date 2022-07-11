from modules.settings import (downloads_pages, get_default_downloads_page,
                              get_default_library_page, get_default_tab,
                              get_enable_download_notifications,
                              get_enable_new_builds_notifications,
                              get_sync_library_and_downloads_pages,
                              library_pages, set_default_downloads_page,
                              set_default_library_page, set_default_tab,
                              set_enable_download_notifications,
                              set_enable_new_builds_notifications,
                              set_sync_library_and_downloads_pages, tabs)
from PyQt5.QtWidgets import QCheckBox, QComboBox
from widgets.settings_form_widget import SettingsFormWidget


class AppearanceTabWidget(SettingsFormWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

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

        # Layout
        self._addRow(
            "Default Tab", self.DefaultTabComboBox)
        self._addRow(
            "Sync Library & Downloads Pages",
            self.SyncLibraryAndDownloadsPages)
        self._addRow(
            "Default Library Page", self.DefaultLibraryPageComboBox)
        self._addRow(
            "Default Downloads Page", self.DefaultDownloadsPageComboBox)
        self._addRow("When New Builds Are Available",
                     self.EnableNewBuildsNotifications)
        self._addRow("When Downloading Is Finished",
                     self.EnableDownloadNotifications)

    def change_default_tab(self, tab):
        set_default_tab(tab)

    def toggle_sync_library_and_downloads_pages(self, is_checked):
        set_sync_library_and_downloads_pages(is_checked)
        self.parent.toggle_sync_library_and_downloads_pages(is_checked)

        if is_checked:
            index = self.DefaultLibraryPageComboBox.currentIndex()
            self.DefaultDownloadsPageComboBox.setCurrentIndex(index)
            text = self.DefaultLibraryPageComboBox.currentText()
            set_default_downloads_page(text)

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

    def toggle_enable_download_notifications(self, is_checked):
        set_enable_download_notifications(is_checked)

    def toggle_enable_new_builds_notifications(self, is_checked):
        set_enable_new_builds_notifications(is_checked)
