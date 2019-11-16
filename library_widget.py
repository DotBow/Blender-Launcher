import subprocess
from pathlib import Path
from subprocess import Popen

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction

from _platform import *
from settings import *

if get_platform() == 'Windows':
    from subprocess import CREATE_NO_WINDOW


class LibraryWidget(QtWidgets.QWidget):
    def __init__(self, link):
        super(LibraryWidget, self).__init__(None)
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
        deleteAction.triggered.connect(lambda: print("Delete"))
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
