from enum import Enum
from pathlib import Path

from modules.enums import MessageType
from modules.settings import get_install_template, get_library_folder
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QProgressBar, QPushButton,
                             QWidget)
from threads.downloader import Downloader
from threads.extractor import Extractor
from threads.template_installer import TemplateInstaller

from widgets.datetime_widget import DateTimeWidget


class DownloadState(Enum):
    WAITING = 1
    DOWNLOADING = 2


class DownloadWidget(QWidget):
    def __init__(self, parent, list_widget, item, build_info,
                 show_branch=True, show_new=False):
        super(DownloadWidget, self).__init__(None)
        self.parent = parent
        self.list_widget = list_widget
        self.item = item
        self.build_info = build_info
        self.show_new = show_new
        self.state = DownloadState.WAITING

        self.progressBar = QProgressBar()
        self.progressBar.setFixedWidth(150)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.hide()

        self.downloadButton = QPushButton("Download")
        self.downloadButton.setFixedWidth(85)
        self.downloadButton.setProperty("LaunchButton", True)
        self.downloadButton.clicked.connect(self.init_downloader)

        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.setFixedWidth(85)
        self.cancelButton.setProperty("CancelButton", True)
        self.cancelButton.clicked.connect(self.download_cancelled)
        self.cancelButton.hide()

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(2, 2, 2, 2)

        self.subversionLabel = QLabel(self.build_info.subversion)
        self.subversionLabel.setFixedWidth(80)

        if self.build_info.branch == 'lts':
            branch_name = "LTS"
        else:
            branch_name = self.build_info.branch.replace('-', ' ').title()

        self.branchLabel = QLabel(branch_name)

        self.commitTimeLabel = DateTimeWidget(self.build_info.commit_time)

        self.layout.addWidget(self.downloadButton)
        self.layout.addWidget(self.cancelButton)
        self.layout.addWidget(self.subversionLabel)

        if show_branch:
            self.layout.addWidget(self.branchLabel)

        self.layout.addWidget(self.commitTimeLabel)
        self.layout.addStretch()
        self.layout.addWidget(self.progressBar)

        if self.show_new:
            self.NewItemLabel = QLabel("New")
            self.NewItemLabel.setAlignment(Qt.AlignRight | Qt.AlignCenter)
            self.NewItemLabel.setIndent(6)
            self.layout.addWidget(self.NewItemLabel)

        self.setLayout(self.layout)

    def mouseDoubleClickEvent(self, event):
        if self.state != DownloadState.DOWNLOADING:
            self.init_downloader()

    def mouseReleaseEvent(self, event):
        if hasattr(self, "NewItemLabel"):
            self.NewItemLabel.hide()

    def showEvent(self, event):
        self.list_widget.resize_labels(('branchLabel', 'commitTimeLabel'))

    def init_downloader(self):
        self.item.setSelected(True)

        if hasattr(self, "NewItemLabel"):
            self.NewItemLabel.hide()

        self.state = DownloadState.DOWNLOADING
        self.downloader = Downloader(self.parent.manager, self.build_info.link)
        self.downloader.started.connect(self.download_started)
        self.downloader.progress_changed.connect(self.set_progress_bar)
        self.downloader.finished.connect(self.init_extractor)
        self.downloader.start()

    def init_extractor(self, source):
        self.cancelButton.setEnabled(False)
        library_folder = Path(get_library_folder())

        if (self.build_info.branch == 'stable') or (self.build_info.branch == 'lts'):
            dist = library_folder / 'stable'
        elif self.build_info.branch == 'daily':
            dist = library_folder / 'daily'
        else:
            dist = library_folder / 'experimental'

        self.extractor = Extractor(self.parent.manager, source, dist)
        self.extractor.progress_changed.connect(self.set_progress_bar)
        self.extractor.finished.connect(self.init_template_installer)
        self.extractor.start()

    def init_template_installer(self, dist):
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

    def download_cancelled(self):
        self.item.setSelected(True)
        self.state = DownloadState.WAITING
        self.progressBar.hide()
        self.cancelButton.hide()
        self.downloader.terminate()
        self.downloader.wait()
        self.downloadButton.show()

    def set_progress_bar(self, value, format):
        self.progressBar.setFormat(format)
        self.progressBar.setValue(value * 100)

    def download_finished(self, dist=None):
        self.state = DownloadState.WAITING

        if dist is not None:
            self.parent.draw_to_library(dist, True)
            self.parent.clear_temp()
            name = "{0} {1} {2}".format(
                self.subversionLabel.text(),
                self.branchLabel.text(),
                self.commitTimeLabel.text())
            self.parent.show_message(
                "Blender {0} download finished!".format(name),
                type=MessageType.DOWNLOADFINISHED)
            self.destroy()

    def destroy(self):
        if self.state == DownloadState.WAITING:
            self.list_widget.remove_item(self.item)
