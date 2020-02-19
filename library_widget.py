import subprocess
from pathlib import Path
from shutil import rmtree
from subprocess import Popen

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction, QWidget

from _platform import *
from blender_version import *
from settings import *

if get_platform() == 'Windows':
    from subprocess import CREATE_NO_WINDOW


class LibraryWidget(QWidget):
    def __init__(self, parent, item, link):
        super(LibraryWidget, self).__init__(None)
        self.parent = parent
        self.item = item
        self.link = link
        self.is_favorite = False

        layout = QtWidgets.QHBoxLayout()
        self.widgetFavorite = QtWidgets.QLabel("★")

        if not self.is_favorite:
            self.widgetFavorite.hide()

        layout.addWidget(self.widgetFavorite)

        info = read_blender_version(Path(link).name)
        label = info['subversion'] + ' ' + \
            info['branch'] + ' ' + info['commit_time']

        widgetText = QtWidgets.QLabel(label)

        self.widgetButton = QtWidgets.QPushButton("Launch")
        self.widgetButton.clicked.connect(self.launch)
        layout.addWidget(
            self.widgetButton, alignment=QtCore.Qt.AlignRight)
        layout.addWidget(widgetText)
        layout.addStretch()

        layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.setLayout(layout)

        # Context menu
        self.setContextMenuPolicy(Qt.ActionsContextMenu)

        deleteAction = QAction("Delete From Drive", self)
        deleteAction.triggered.connect(self.delete_from_drive)

        self.setAsFavoriteAction = QAction("Set As Favorite", self)
        self.setAsFavoriteAction.triggered.connect(self.set_favorite)

        self.addAction(self.setAsFavoriteAction)
        self.addAction(deleteAction)

    def mouseDoubleClickEvent(self, event):
        self.launch()

    def launch(self):
        platform = get_platform()
        library_folder = Path(get_library_folder())

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
        rmtree((Path(get_library_folder()) / self.link).as_posix())
        row = self.parent.LibraryListWidget.row(self.item)
        self.parent.LibraryListWidget.takeItem(row)

    def set_favorite(self):
        if self.parent.favorite is not None:
            self.parent.favorite.widgetFavorite.hide()

        self.parent.favorite = self
        self.widgetFavorite.show()
