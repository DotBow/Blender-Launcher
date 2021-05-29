from enum import Enum
from pathlib import Path

from modules.enums import MessageType
from modules.settings import get_install_template, get_library_folder
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QProgressBar, QPushButton,
                             QVBoxLayout)
from threads.downloader import Downloader
from threads.extractor import Extractor
from threads.template_installer import TemplateInstaller

from widgets.base_build_widget import BaseBuildWidget
from widgets.build_state_widget import BuildStateWidget
from widgets.datetime_widget import DateTimeWidget
from widgets.elided_text_label import ElidedTextLabel


class DownloadState(Enum):
    WAITING = 1
    DOWNLOADING = 2


class DownloadWidget(BaseBuildWidget):
    def __init__(self, parent, list_widget, item, build_info,
                 show_new=False):
        super(DownloadWidget, self).__init__(parent=parent)
        self.parent = parent
        self.list_widget = list_widget
        self.item = item
        self.build_info = build_info
        self.show_new = show_new
        self.state = DownloadState.WAITING

        self.progress_start = 0
        self.progress_end = 1

        self.progressBar = QProgressBar()
        self.progressBar.setFixedHeight(4)
        self.progressBar.hide()

        self.downloadButton = QPushButton("Download")
        self.downloadButton.setFixedWidth(85)
        self.downloadButton.setProperty("LaunchButton", True)
        self.downloadButton.clicked.connect(self.init_downloader)
        self.downloadButton.setCursor(Qt.PointingHandCursor)

        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.setFixedWidth(85)
        self.cancelButton.setProperty("CancelButton", True)
        self.cancelButton.clicked.connect(self.download_cancelled)
        self.cancelButton.setCursor(Qt.PointingHandCursor)
        self.cancelButton.hide()

        self.h_layout = QHBoxLayout()
        self.h_layout.setContentsMargins(2, 2, 0, 2)

        self.v_layout = QVBoxLayout()
        self.v_layout.setContentsMargins(0, 0, 0, 0)

        self.h_layout1 = QHBoxLayout()
        self.h_layout1.setContentsMargins(0, 0, 0, 0)

        self.subversionLabel = QLabel(self.build_info.subversion)
        self.subversionLabel.setFixedWidth(85)
        self.list_widget.subversion_indent_changed.connect(self.set_indent)

        if self.build_info.branch == 'lts':
            branch_name = "LTS"
        else:
            branch_name = self.build_info.branch.replace('-', ' ').title()

        self.branchLabel = ElidedTextLabel(branch_name)
        self.commitTimeLabel = DateTimeWidget(
            self.build_info.commit_time, self.build_info.build_hash)
        self.build_state_widget = BuildStateWidget(
            self.parent, self.list_widget)

        self.h_layout1.addWidget(self.subversionLabel)
        self.h_layout1.addWidget(self.branchLabel, stretch=1)
        self.h_layout1.addWidget(self.commitTimeLabel)

        if self.show_new:
            self.build_state_widget.setNewBuild(True)

        self.v_layout.addLayout(self.h_layout1)
        self.v_layout.addWidget(self.progressBar)

        self.h_layout.addWidget(self.downloadButton)
        self.h_layout.addWidget(self.cancelButton)
        self.h_layout.addLayout(self.v_layout)
        self.h_layout.addWidget(self.build_state_widget)

        self.setLayout(self.h_layout)

        if self.build_info.branch in "stable lts":
            self.menu.addAction(self.showReleaseNotesAction)

    def context_menu(self):
        self.menu._show()

    def mouseDoubleClickEvent(self, event):
        if self.state != DownloadState.DOWNLOADING:
            self.init_downloader()

    def mouseReleaseEvent(self, event):
        if self.show_new is True:
            self.build_state_widget.setNewBuild(False)
            self.show_new = False

    def init_downloader(self):
        self.item.setSelected(True)

        if self.show_new is True:
            self.build_state_widget.setNewBuild(False)
            self.show_new = False

        self.state = DownloadState.DOWNLOADING
        self.downloader = Downloader(self.parent.manager, self.build_info.link)
        self.downloader.started.connect(self.download_started)
        self.downloader.progress_changed.connect(self.set_progress_bar)
        self.downloader.finished.connect(self.init_extractor)

        self.progress_start = 0
        self.progress_end = 0.5

        self.downloader.start()

    def init_extractor(self, source):
        self.cancelButton.setEnabled(False)
        library_folder = Path(get_library_folder())

        if (self.build_info.branch == 'stable') or \
                (self.build_info.branch == 'lts'):
            dist = library_folder / 'stable'
        elif self.build_info.branch == 'daily':
            dist = library_folder / 'daily'
        else:
            dist = library_folder / 'experimental'

        self.extractor = Extractor(self.parent.manager, source, dist)
        self.extractor.progress_changed.connect(self.set_progress_bar)
        self.extractor.finished.connect(self.init_template_installer)

        self.progress_start = 0.5
        self.progress_end = 1

        self.extractor.start()
        self.build_state_widget.setExtract()

    def init_template_installer(self, dist):
        self.build_state_widget.setExtract(False)

        if get_install_template():
            self.template_installer = TemplateInstaller(
                self.parent.manager, dist)
            self.template_installer.progress_changed.connect(
                self.set_progress_bar)
            self.template_installer.finished.connect(
                lambda: self.download_finished(dist))
            self.template_installer.start()
        else:
            self.download_finished(dist)

    def download_started(self):
        self.set_progress_bar(0, "Downloading: %p%")
        self.progressBar.show()
        self.cancelButton.show()
        self.downloadButton.hide()
        self.h_layout1.setContentsMargins(0, 10, 0, 0)
        self.build_state_widget.setDownload()

    def download_cancelled(self):
        self.item.setSelected(True)
        self.state = DownloadState.WAITING
        self.progressBar.hide()
        self.cancelButton.hide()
        self.downloader.terminate()
        self.downloader.wait()
        self.downloadButton.show()
        self.h_layout1.setContentsMargins(0, 0, 0, 0)
        self.build_state_widget.setDownload(False)

    def set_progress_bar(self, value, format):
        self.progressBar.setFormat("")
        value = (self.progress_end - self.progress_start) * \
            value + self.progress_start
        self.progressBar.setValue(value * 100)

    def download_finished(self, dist=None):
        self.state = DownloadState.WAITING

        if dist is not None:
            self.parent.draw_to_library(dist, True)
            self.parent.clear_temp()
            name = "{0} {1} {2}".format(
                self.subversionLabel.text(),
                self.branchLabel.text,
                self.build_info.commit_time)
            self.parent.show_message(
                "Blender {0} download finished!".format(name),
                type=MessageType.DOWNLOADFINISHED)
            self.destroy()

        self.build_state_widget.setExtract(False)

    def destroy(self):
        if self.state == DownloadState.WAITING:
            self.list_widget.subversion_indent_changed.disconnect(
                self.set_indent)
            self.list_widget.remove_item(self.item)
