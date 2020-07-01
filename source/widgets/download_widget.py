from enum import Enum
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QProgressBar, QPushButton,
                             QSizePolicy, QWidget)

from modules.settings import *
from threads.downloader import Downloader


class DownloadState(Enum):
    WAITING = 1
    DOWNLOADING = 2


class DownloadWidget(QWidget):
    def __init__(self, parent, list_widget, item, build_info):
        super(DownloadWidget, self).__init__(None)
        self.parent = parent
        self.list_widget = list_widget
        self.item = item
        self.build_info = build_info
        self.state = DownloadState.WAITING

        self.progressBar = QProgressBar()
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.hide()

        self.downloadButton = QPushButton("Download")
        self.downloadButton.setMinimumWidth(85)
        self.downloadButton.setProperty("LaunchButton", True)
        self.downloadButton.clicked.connect(self.init_download)

        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.setMinimumWidth(85)
        self.cancelButton.setProperty("CancelButton", True)
        self.cancelButton.clicked.connect(self.download_cancelled)
        self.cancelButton.hide()

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(2, 2, 2, 2)

        self.subversionLabel = QLabel(self.build_info.subversion)
        self.branchLabel = QLabel(
            self.build_info.branch.replace('-', ' ').title())
        self.commitTimeLabel = QLabel(self.build_info.commit_time)
        self.buildHashLabel = QLabel(self.build_info.build_hash)
        self.progressBar.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)

        self.layout.addWidget(self.downloadButton)
        self.layout.addWidget(self.cancelButton)
        self.layout.addWidget(self.subversionLabel)
        self.layout.addWidget(self.branchLabel)
        self.layout.addWidget(self.commitTimeLabel)
        self.layout.addWidget(self.buildHashLabel)
        self.layout.addStretch()
        self.layout.addWidget(self.progressBar, stretch=1)

        self.setLayout(self.layout)

    def showEvent(self, event):
        self.list_widget.resize_labels(
            ('subversionLabel', 'branchLabel', 'commitTimeLabel', 'buildHashLabel'))

    def init_download(self):
        self.state = DownloadState.DOWNLOADING
        self.thread = Downloader(self.parent.manager, self.build_info)
        self.thread.started.connect(self.download_started)
        self.thread.progress_changed.connect(self.set_progress_bar)
        self.thread.finished.connect(self.download_finished)
        self.thread.start()

    def download_started(self):
        self.set_progress_bar(0, "Downloading: %p%")
        self.progressBar.show()
        self.cancelButton.show()
        self.downloadButton.hide()

    def download_cancelled(self):
        self.state = DownloadState.WAITING
        self.progressBar.hide()
        self.cancelButton.hide()
        self.thread.terminate()
        self.thread.wait()
        self.downloadButton.show()

    def set_progress_bar(self, value, format):
        self.progressBar.setFormat(format)
        self.progressBar.setValue(value * 100)

    def download_finished(self, dist=None):
        self.state = DownloadState.WAITING

        if dist is not None:
            self.parent.draw_to_library(dist)
            self.parent.clear_temp()
            name = "{0} {1} {2}".format(
                self.subversionLabel.text(),
                self.branchLabel.text(),
                self.commitTimeLabel.text())
            self.parent.show_message(
                "Blender {0} download finished!".format(name), dist.name)
            self.destroy()

    def destroy(self):
        if self.state == DownloadState.WAITING:
            self.list_widget.remove_item(self.item)
