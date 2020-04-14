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

        label = build_info.subversion + ' ' + build_info.branch.replace('-', ' ').title(
        ) + ' ' + str(build_info.commit_time) + ' ' + str(build_info.build_hash)
        widgetText = QLabel(label)
        widgetText.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        self.downloadButton = QPushButton("Download")
        self.downloadButton.setMinimumWidth(80)
        self.downloadButton.setProperty("LaunchButton", True)
        self.downloadButton.clicked.connect(self.init_download)
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.setMinimumWidth(80)
        self.cancelButton.setProperty("CancelButton", True)
        self.cancelButton.clicked.connect(self.download_cancelled)
        self.cancelButton.hide()
        layout = QHBoxLayout()
        layout.setContentsMargins(2, 2, 2, 2)
        layout.addWidget(
            self.downloadButton, alignment=Qt.AlignRight)
        layout.addWidget(
            self.cancelButton, alignment=Qt.AlignRight)
        layout.addWidget(widgetText, stretch=1)
        layout.addWidget(self.progressBar)

        self.setLayout(layout)

    def init_download(self):
        self.state = DownloadState.DOWNLOADING
        self.thread = Downloader(self, self.build_info)
        self.thread.started.connect(self.download_started)
        self.thread.progress_changed.connect(self.set_progress_bar)
        self.thread.finished.connect(self.destroy)
        self.thread.start()

    def download_started(self):
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

    def set_progress_bar(self, progress_bar_val, taskbar_val, format):
        self.progressBar.setFormat(format)
        self.progressBar.setValue(progress_bar_val * 100)

    def destroy(self, status, dist):
        if status == 0:
            self.parent.draw_to_library(dist, self.build_info.branch)
            row = self.list_widget.row(self.item)
            self.list_widget.takeItem(row)
        else:
            pass
