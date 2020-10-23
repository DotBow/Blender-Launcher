import os
import subprocess
from pathlib import Path
from subprocess import DEVNULL, Popen, check_call

from modules._platform import get_environment, get_platform
from modules.build_info import BuildInfoReader
from modules.settings import (get_favorite_path, get_library_folder,
                              get_mark_as_favorite, set_favorite_path)
from modules.shortcut import create_shortcut
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import (QAction, QApplication, QHBoxLayout, QLabel, QMenu,
                             QPushButton, QWidget)
from threads.observer import Observer
from threads.register import Register
from threads.remover import Remover
from windows.dialog_window import DialogIcon, DialogWindow

if get_platform() == 'Windows':
    from subprocess import CREATE_NO_WINDOW


class LibraryWidget(QWidget):
    def __init__(self, parent, item, link, list_widget, show_new=False):
        super(LibraryWidget, self).__init__(None)

        self.parent = parent
        self.item = item
        self.link = link
        self.list_widget = list_widget
        self.show_new = show_new
        self.observer = None
        self.build_info = None

        self.destroyed.connect(lambda: self._destroyed())
        self.setEnabled(False)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(2, 2, 2, 2)
        self.setLayout(self.layout)

        self.infoLabel = QLabel("Loading build information...")

        self.launchButton = QPushButton("Launch")
        self.launchButton.setMinimumWidth(75)
        self.launchButton.setProperty("CancelButton", True)

        self.layout.addWidget(self.launchButton)
        self.layout.addWidget(self.infoLabel, stretch=1)

        self.thread = BuildInfoReader(link)
        self.thread.finished.connect(self.draw)
        self.thread.start()

        self.item.setSizeHint(self.sizeHint())

    def draw(self, build_info):
        if build_info is None:
            self.infoLabel.setText(
                ("Build *{0}* is damaged!").format(Path(self.link).name))
            self.launchButton.setText("Delete")
            self.launchButton.clicked.connect(self.ask_remove_from_drive)
            self.setEnabled(True)
            return

        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

        self.build_info = build_info
        self.branch = self.build_info.branch
        self.item.date = build_info.commit_time

        self.icon_favorite = QIcon(":resources/icons/favorite.svg")
        self.icon_fake = QIcon(":resources/icons/fake.svg")
        self.icon_delete = QIcon(":resources/icons/delete.svg")

        self.launchButton = QPushButton("Launch")
        self.launchButton.setMinimumWidth(75)
        self.launchButton.setProperty("LaunchButton", True)

        self.subversionLabel = QLabel()
        self.branchLabel = QLabel()
        self.commitTimeLabel = QLabel()
        self.buildHashLabel = QLabel()

        self.countButton = QPushButton("0")
        self.countButton.setEnabled(False)
        self.countButton.setProperty("Count", True)
        self.countButton.hide()
        self.countButton.setFixedSize(24, 24)

        self.widgetFavorite = QPushButton()
        self.widgetFavorite.setEnabled(False)
        self.widgetFavorite.setFixedSize(24, 24)
        self.widgetFavorite.setIcon(self.icon_fake)
        self.widgetFavorite.setProperty("Icon", True)

        self.layout.addWidget(self.launchButton)
        self.layout.addWidget(self.subversionLabel)
        self.layout.addWidget(self.branchLabel)
        self.layout.addWidget(self.commitTimeLabel)
        self.layout.addWidget(self.buildHashLabel)
        self.layout.addStretch()
        self.layout.addWidget(self.countButton)
        self.layout.addWidget(self.widgetFavorite)

        self.launchButton.clicked.connect(self.launch)
        self.subversionLabel.setText(self.build_info.subversion)
        self.branchLabel.setText(self.branch.replace('-', ' ').title())
        self.commitTimeLabel.setText(self.build_info.commit_time)
        self.buildHashLabel.setText(self.build_info.build_hash)

        # Context menu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context_menu)

        self.menu = QMenu()
        self.menu.setFont(self.parent.font)

        self.deleteAction = QAction("Delete From Drive", self)
        self.deleteAction.setIcon(self.icon_delete)
        self.deleteAction.triggered.connect(self.ask_remove_from_drive)

        self.setAsFavoriteAction = QAction("Mark As Favorite", self)
        self.setAsFavoriteAction.setIcon(self.icon_favorite)
        self.setAsFavoriteAction.triggered.connect(self.set_favorite)

        self.registerExtentionAction = QAction("Register Extension")
        self.registerExtentionAction.triggered.connect(self.register_extension)

        self.createShortcutAction = QAction("Create Shortcut")
        self.createShortcutAction.triggered.connect(self.create_shortcut)

        self.showFolderAction = QAction("Show Folder")
        self.showFolderAction.triggered.connect(self.show_folder)

        self.createSymlinkAction = QAction("Create Symlink")
        self.createSymlinkAction.triggered.connect(self.create_symlink)

        self.menu.addAction(self.setAsFavoriteAction)

        if get_platform() == 'Windows':
            self.menu.addAction(self.registerExtentionAction)

        self.menu.addAction(self.createShortcutAction)
        self.menu.addAction(self.createSymlinkAction)
        self.menu.addAction(self.showFolderAction)
        self.menu.addAction(self.deleteAction)

        if self.show_new:
            self.NewItemLabel = QLabel("New")
            self.NewItemLabel.setAlignment(Qt.AlignRight | Qt.AlignCenter)
            self.NewItemLabel.setIndent(6)
            self.layout.addWidget(self.NewItemLabel)

            if get_mark_as_favorite() == 0:
                pass
            elif (get_mark_as_favorite() == 1 and self.branch == "stable"):
                self.set_favorite()
            elif (get_mark_as_favorite() == 2 and self.branch == "daily"):
                self.set_favorite()
            elif get_mark_as_favorite() == 3:
                self.set_favorite()
        elif get_favorite_path() == self.link:
            self.set_favorite()

        self.setEnabled(True)
        self.list_widget.sortItems()
        self.list_widget.resize_labels(
            ('subversionLabel', 'branchLabel',
             'commitTimeLabel', 'buildHashLabel'))

    def context_menu(self):
        self.menu.exec_(QCursor.pos())

    def mouseDoubleClickEvent(self, event):
        if self.build_info is not None:
            self.launch()

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            if hasattr(self, "NewItemLabel"):
                self.NewItemLabel.hide()

            mod = QApplication.keyboardModifiers()
            if not (mod == Qt.ShiftModifier or mod == Qt.ControlModifier):
                self.list_widget.clearSelection()
                self.item.setSelected(True)

            event.accept()

        event.ignore()

    @QtCore.pyqtSlot()
    def launch(self):
        self.item.setSelected(True)

        if hasattr(self, "NewItemLabel"):
            self.NewItemLabel.hide()

        platform = get_platform()
        library_folder = Path(get_library_folder())

        if platform == 'Windows':
            DETACHED_PROCESS = 0x00000008
            b3d_exe = library_folder / self.link / "blender.exe"
            proc = Popen(b3d_exe.as_posix(), shell=True,
                         stdin=None, stdout=None,
                         stderr=None, close_fds=True,
                         creationflags=DETACHED_PROCESS)
        elif platform == 'Linux':
            b3d_exe = library_folder / self.link / "blender"
            proc = Popen('nohup "' + b3d_exe.as_posix() + '"',
                         shell=True, stdout=None,
                         stderr=None, close_fds=True,
                         preexec_fn=os.setpgrp, env=get_environment())

        if self.observer is None:
            self.observer = Observer(self)
            self.observer.count_changed.connect(self.proc_count_changed)
            self.observer.started.connect(self.observer_started)
            self.observer.finished.connect(self.observer_finished)
            self.observer.start()

        self.observer.append_proc(proc)

    def proc_count_changed(self, count):
        self.countButton.setText(str(count))

    def observer_started(self):
        self.countButton.show()
        self.deleteAction.setEnabled(False)

    def observer_finished(self):
        self.observer = None
        self.countButton.hide()
        self.deleteAction.setEnabled(True)

    @QtCore.pyqtSlot()
    def ask_remove_from_drive(self):
        self.item.setSelected(True)
        self.dlg = DialogWindow(
            self.parent, title="Warning",
            text="Are you sure you want to delete?",
            accept_text="Yes", cancel_text="No", icon=DialogIcon.WARNING)
        self.dlg.accepted.connect(self.remove_from_drive)

    @QtCore.pyqtSlot()
    def remove_from_drive(self):
        self.launchButton.setText("Deleting")
        self.setEnabled(False)
        path = Path(get_library_folder()) / self.link
        self.remover = Remover(path)
        self.remover.finished.connect(self.remover_finished)
        self.remover.start()

    def remover_finished(self, code):
        if code == 0:
            self.parent.draw_from_cashed(self.build_info)
            self.list_widget.remove_item(self.item)
            return
        else:
            self.launchButton.setText("Launch")
            self.setEnabled(True)
            return

    @QtCore.pyqtSlot()
    def set_favorite(self):
        set_favorite_path(self.link)

        if self.parent.favorite is not None:
            self.parent.favorite.widgetFavorite.setIcon(self.icon_fake)
            self.parent.favorite.setAsFavoriteAction.setVisible(True)

        self.parent.favorite = self
        self.widgetFavorite.setIcon(self.icon_favorite)
        self.setAsFavoriteAction.setVisible(False)

    @QtCore.pyqtSlot()
    def register_extension(self):
        path = Path(get_library_folder()) / self.link
        self.register = Register(path)
        self.register.start()

    @QtCore.pyqtSlot()
    def create_shortcut(self):
        name = "Blender {0} {1}".format(
            self.build_info.subversion.replace('(', '').replace(')', ''),
            self.build_info.branch.replace('-', ' ').title())

        create_shortcut(self.link, name)

    @QtCore.pyqtSlot()
    def create_symlink(self):
        platform = get_platform()
        target = self.link
        link = (Path(get_library_folder()) / "blender_symlink").as_posix()

        if platform == 'Windows':
            check_call('mklink /J "{0}" "{1}"'.format(link, target),
                       creationflags=CREATE_NO_WINDOW,
                       shell=True,
                       stderr=DEVNULL, stdin=DEVNULL)
        elif platform == 'Linux':
            os.symlink(target, link)

    @QtCore.pyqtSlot()
    def show_folder(self):
        platform = get_platform()
        library_folder = Path(get_library_folder())
        folder = library_folder / self.link

        if platform == 'Windows':
            os.startfile(folder.as_posix())
        elif platform == 'Linux':
            subprocess.call(["xdg-open", folder.as_posix()])

    def _destroyed(self):
        if self.parent.favorite == self:
            self.parent.favorite = None
