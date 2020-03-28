import os
import re
from pathlib import Path

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QAction, QLabel, QSizePolicy, QWidget

from modules.settings import *
from threads.downloader import Downloader


class DownloadWidget(QtWidgets.QWidget):
    def __init__(self, parent, list_widget, item, build_info):
        super(DownloadWidget, self).__init__(None)
        self.parent = parent
        self.list_widget = list_widget
        self.item = item
        self.build_info = build_info

        self.progressBar = QtWidgets.QProgressBar()
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.hide()

        label = build_info.subversion + ' ' + build_info.branch.replace('-', ' ').title(
        ) + ' ' + str(build_info.commit_time) + ' ' + str(build_info.build_hash)
        widgetText = QtWidgets.QLabel(label)
        widgetText.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        self.widgetButton = QtWidgets.QPushButton("Download")
        self.widgetButton.setProperty("LaunchButton", True)
        self.widgetButton.clicked.connect(self.init_download)
        self.cancelButton = QtWidgets.QPushButton("Cancel")
        self.cancelButton.setProperty("CancelButton", True)
        self.cancelButton.clicked.connect(self.download_cancelled)
        self.cancelButton.hide()
        widgetLayout = QtWidgets.QHBoxLayout()
        widgetLayout.addWidget(
            self.widgetButton, alignment=QtCore.Qt.AlignRight)
        widgetLayout.addWidget(
            self.cancelButton, alignment=QtCore.Qt.AlignRight)
        widgetLayout.addWidget(widgetText, stretch=1)
        widgetLayout.addWidget(self.progressBar)
        # widgetLayout.addStretch()

        # widgetLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        widgetLayout.setContentsMargins(2, 2, 2, 2)
        self.setLayout(widgetLayout)

    def init_download(self):
        print("init_download")
        self.thread = Downloader(self, self.build_info.link)
        self.thread.started.connect(self.download_started)
        self.thread.progress_changed.connect(self.set_progress_bar)
        self.thread.finished.connect(self.destroy)
        self.thread.start()

    def download_started(self):
        self.progressBar.show()
        self.cancelButton.show()
        self.widgetButton.hide()

    def download_cancelled(self):
        print("download_cancelled")
        self.progressBar.hide()
        self.cancelButton.hide()
        self.thread.terminate()
        self.thread.wait()
        self.widgetButton.show()

    def set_progress_bar(self, progress_bar_val, taskbar_val, format):
        self.progressBar.setFormat(format)
        self.progressBar.setValue(progress_bar_val * 100)

    def destroy(self, status):
        if status == 0:
            self.parent.draw_to_library(
                Path(get_library_folder()) / Path(self.build_info.link).stem)
            row = self.list_widget.row(self.item)
            self.list_widget.takeItem(row)
        else:
            pass
