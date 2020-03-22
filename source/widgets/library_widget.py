import subprocess
from pathlib import Path
from subprocess import Popen

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QWidget, QSizePolicy, QLabel

from modules._platform import *
from modules.build_info import *
from modules.settings import *
from threads.remover import Remover
from threads.observer import Observer

if get_platform() == 'Windows':
    from subprocess import CREATE_NO_WINDOW


class LibraryWidget(QWidget):
    def __init__(self, parent, item, link):
        super(LibraryWidget, self).__init__(None)
        self.parent = parent
        self.list_widget = None
        self.item = item
        self.link = link
        self.observer = None

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(2, 2, 2, 2)
        self.icon_favorite = QIcon(":resources/icons/favorite.svg")
        self.icon_fake = QIcon(":resources/icons/fake.svg")
        self.icon_delete = QIcon(":resources/icons/delete.svg")
        self.widgetFavorite = QtWidgets.QPushButton()
        self.widgetFavorite.setIcon(self.icon_favorite)
        self.widgetFavorite.setProperty("Icon", True)

        self.build_info = read_build_info(Path(link).name)
        self.branch = self.build_info.branch

        branch = self.branch.replace('-', ' ').title()
        label = self.build_info.subversion + ' ' + branch + ' ' + \
            self.build_info.commit_time + \
            ' [' + self.build_info.build_hash + ']'

        widgetText = QLabel(label)
        widgetText.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)

        self.countButton = QtWidgets.QPushButton("0")
        self.countButton.setProperty("Icon", True)
        self.countButton.hide()

        self.launchButton = QtWidgets.QPushButton("Launch")
        self.launchButton.clicked.connect(self.launch)
        self.launchButton.setProperty("LaunchButton", True)

        layout.addWidget(
            self.launchButton, alignment=QtCore.Qt.AlignRight)
        layout.addWidget(widgetText, stretch=1)
        layout.addWidget(self.countButton)
        layout.addWidget(self.widgetFavorite)
        self.setLayout(layout)

        # Context menu
        self.setContextMenuPolicy(Qt.ActionsContextMenu)

        self.deleteAction = QAction("Delete From Drive", self)
        self.deleteAction.setIcon(self.icon_delete)
        self.deleteAction.triggered.connect(self.remove_from_drive)

        self.setAsFavoriteAction = QAction("Set As Favorite", self)
        self.setAsFavoriteAction.setIcon(self.icon_favorite)
        self.setAsFavoriteAction.triggered.connect(self.set_favorite)

        self.registerExtentionAction = QAction("Register Extension")

        self.addAction(self.setAsFavoriteAction)
        self.addAction(self.registerExtentionAction)
        self.addAction(self.deleteAction)

        if get_favorite_path() == link:
            self.set_favorite()
        else:
            self.widgetFavorite.setIcon(self.icon_fake)

    def mouseDoubleClickEvent(self, event):
        self.launch()

    @QtCore.pyqtSlot()
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

        if (self.observer is None) or (self.observer.destroyed):
            self.observer = Observer(self)
            self.observer.count_changed.connect(self.proc_count_changed)
            self.observer.finished.connect(self.countButton.hide)
            self.observer.started.connect(self.countButton.show)
            self.observer.start()

        self.observer.append_proc(proc)

    def proc_count_changed(self, count):
        self.countButton.setText(str(count))

    @QtCore.pyqtSlot()
    def remove_from_drive(self):
        path = Path(get_library_folder()) / self.link
        self.remover = Remover(path)
        self.remover.finished.connect(self.remover_finished)
        self.remover.start()

    @QtCore.pyqtSlot()
    def remover_finished(self):
        row = self.list_widget.row(self.item)
        self.list_widget.takeItem(row)

    @QtCore.pyqtSlot()
    def set_favorite(self):
        set_favorite_path(self.link)

        if self.parent.favorite is not None:
            self.parent.favorite.widgetFavorite.setIcon(self.icon_fake)
            self.parent.favorite.setAsFavoriteAction.setVisible(True)

        self.parent.favorite = self
        self.widgetFavorite.setIcon(self.icon_favorite)
        self.setAsFavoriteAction.setVisible(False)
