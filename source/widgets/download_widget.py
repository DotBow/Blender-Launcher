import os
import re
from pathlib import Path

from PyQt5 import QtCore, QtWidgets

from modules.settings import *
from threads.downloader import Downloader


class DownloadWidget(QtWidgets.QWidget):
    def __init__(self, parent, list_widget, item, link):
        super(DownloadWidget, self).__init__(None)
        self.parent = parent
        self.list_widget = list_widget
        self.item = item
        self.link = link

        self.progressBar = QtWidgets.QProgressBar()
        self.progressBar.setAlignment(QtCore.Qt.AlignHCenter)
        self.progressBar.hide()

        label = Path(link).stem
        label = label.replace("blender-", "")
        label = label.replace("-windows64", "")
        label_parts = label.rsplit('-', 2)

        if len(label_parts) > 2:
            label = label_parts[1] + ' ' + \
                label_parts[0].replace('-', ' ').title() + \
                " [" + label_parts[2] + "]"
        elif len(label_parts) > 1:
            label = label_parts[0] + " Experimental [" + label_parts[1] + "]"
        else:
            label = label_parts[0] + " Stable"

        widgetText = QtWidgets.QLabel(label)
        self.widgetButton = QtWidgets.QPushButton("Download")
        self.widgetButton.setProperty("LaunchButton", True)
        self.widgetButton.clicked.connect(self.init_download)
        widgetLayout = QtWidgets.QHBoxLayout()
        widgetLayout.addWidget(
            self.widgetButton, alignment=QtCore.Qt.AlignRight)
        widgetLayout.addWidget(widgetText)
        widgetLayout.addWidget(self.progressBar)
        widgetLayout.addStretch()

        widgetLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        widgetLayout.setContentsMargins(2, 2, 2, 2)
        self.setLayout(widgetLayout)

    def init_download(self):
        self.thread = Downloader(self, self.link)
        self.thread.progress_changed.connect(self.set_progress_bar)
        self.progressBar.show()
        self.widgetButton.setDisabled(True)
        self.thread.finished.connect(self.destroy)
        self.thread.start()

    def set_progress_bar(self, progress_bar_val, taskbar_val, format):
        self.progressBar.setFormat(format)
        self.progressBar.setValue(progress_bar_val * 100)

    def destroy(self, status):
        if status == 0:
            self.parent.draw_to_library(
                Path(get_library_folder()) / Path(self.link).stem)
            row = self.list_widget.row(self.item)
            self.list_widget.takeItem(row)
        else:
            pass
