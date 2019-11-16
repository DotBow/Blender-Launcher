import subprocess
from pathlib import Path
from shutil import rmtree
from subprocess import Popen

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction

from _platform import *
from settings import *

if get_platform() == 'Windows':
    from subprocess import CREATE_NO_WINDOW


class LibraryWidget(QtWidgets.QWidget):
    def __init__(self, parent, item, link):
        super(LibraryWidget, self).__init__(None)
        self.parent = parent
        self.item = item
        self.link = link

        widgetText = QtWidgets.QLabel(os.path.basename(link))
        self.widgetButton = QtWidgets.QPushButton("Launch")
        self.widgetButton.clicked.connect(self.launch)
        widgetLayout = QtWidgets.QHBoxLayout()
        widgetLayout.addWidget(widgetText)
        widgetLayout.addWidget(
            self.widgetButton, alignment=QtCore.Qt.AlignRight)
        widgetLayout.addStretch()

        widgetLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.setLayout(widgetLayout)

        # Context menu
        self.setContextMenuPolicy(Qt.ActionsContextMenu)

        deleteAction = QAction("Delete From Drive", self)
        deleteAction.triggered.connect(self.delete_from_drive)

        setAsFavoriteAction = QAction("Set As Favorite", self)
        setAsFavoriteAction.triggered.connect(lambda: print("Set As Favorite"))

        self.addAction(setAsFavoriteAction)
        self.addAction(deleteAction)

    def mouseDoubleClickEvent(self, event):
        self.launch()

    def launch(self):
        platform = get_platform()
        library_folder = get_library_folder()

        if platform == 'Windows':
            DETACHED_PROCESS = 0x00000008
            b3d_exe = library_folder / self.link / "blender.exe"
            proc = Popen(b3d_exe.as_posix(), shell=True, stdin=None, stdout=None,
                         stderr=None, close_fds=True, creationflags=DETACHED_PROCESS)
        elif platform == 'Linux':
            b3d_exe = library_folder / self.link / "blender"
            proc = Popen('nohup "' + b3d_exe + '"', shell=True, stdout=None,
                         stderr=None, close_fds=True, preexec_fn=os.setpgrp)

    def delete_from_drive(self):
        rmtree((get_library_folder() / self.link).as_posix())
        row = self.parent.LibraryListWidget.row(self.item)
        self.parent.LibraryListWidget.takeItem(row)
