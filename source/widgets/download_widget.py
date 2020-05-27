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
        self.progressBar.setMinimumWidth(135)
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

        layout = QHBoxLayout()
        layout.setContentsMargins(2, 2, 2, 2)
        layout.addWidget(
            self.downloadButton, alignment=Qt.AlignRight)
        layout.addWidget(
            self.cancelButton, alignment=Qt.AlignRight)

        self.subversionLabel = QLabel(self.build_info.subversion)
        self.branchLabel = QLabel(
            self.build_info.branch.replace('-', ' ').title())
        self.commitTimeLabel = QLabel(self.build_info.commit_time)
        self.buildHashLabel = QLabel(self.build_info.build_hash)
        self.buildHashLabel.setSizePolicy(
            QSizePolicy.Ignored, QSizePolicy.Fixed)

        layout.addWidget(self.subversionLabel)
        layout.addWidget(self.branchLabel)
        layout.addWidget(self.commitTimeLabel)
        layout.addWidget(self.buildHashLabel, stretch=1)
        layout.addWidget(self.progressBar)

        self.setLayout(layout)

    def showEvent(self, event):
        self.list_widget.resize_labels(
            ('subversionLabel', 'branchLabel', 'commitTimeLabel'))

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
            self.destroy()

    def destroy(self):
        if self.state == DownloadState.WAITING:
            row = self.list_widget.row(self.item)
            self.list_widget.takeItem(row)
