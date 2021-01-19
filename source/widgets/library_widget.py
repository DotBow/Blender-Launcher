import os
import subprocess
from pathlib import Path

from items.base_list_widget_item import BaseListWidgetItem
from modules._platform import _call, _popen, get_platform
from modules.build_info import BuildInfoReader
from modules.settings import (get_bash_arguments,
                              get_blender_startup_arguments, get_favorite_path,
                              get_library_folder, get_mark_as_favorite,
                              set_favorite_path)
from modules.shortcut import create_shortcut
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QAction, QApplication, QHBoxLayout, QLabel,
                             QPushButton, QWidget)
from threads.observer import Observer
from threads.register import Register
from threads.remover import Remover
from threads.template_installer import TemplateInstaller
from windows.dialog_window import DialogWindow

from widgets.base_menu_widget import BaseMenuWidget
from widgets.build_state_widget import BuildStateWidget
from widgets.datetime_widget import DateTimeWidget
from widgets.elided_text_label import ElidedTextLabel
from widgets.left_icon_button_widget import LeftIconButtonWidget


class LibraryWidget(QWidget):
    def __init__(self, parent, item, link, list_widget,
                 show_branch=True, show_new=False, parent_widget=None):
        super().__init__()

        self.parent = parent
        self.item = item
        self.link = link
        self.list_widget = list_widget
        self.show_branch = show_branch
        self.show_new = show_new
        self.observer = None
        self.build_info = None
        self.child_widget = None
        self.parent_widget = parent_widget

        self.destroyed.connect(lambda: self._destroyed())

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(2, 2, 0, 2)
        self.setLayout(self.layout)

        if self.parent_widget is None:
            self.setEnabled(False)
            self.infoLabel = QLabel("Loading build information...")

            self.launchButton = QPushButton("Launch")
            self.launchButton.setFixedWidth(85)
            self.launchButton.setProperty("CancelButton", True)

            self.layout.addWidget(self.launchButton)
            self.layout.addWidget(self.infoLabel, stretch=1)

            self.build_info_reader = BuildInfoReader(link)
            self.build_info_reader.finished.connect(self.draw)
            self.build_info_reader.start()

            self.item.setSizeHint(self.sizeHint())
        else:
            self.draw(self.parent_widget.build_info)
            self.item.setSizeHint(self.sizeHint())

    def draw(self, build_info):
        if self.parent_widget is None:
            if self.parent.library_drawer is not None:
                self.parent.library_drawer.release_build()

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

        self.launchButton = LeftIconButtonWidget("Launch")
        self.launchButton.setFixedWidth(85)
        self.launchButton.setProperty("LaunchButton", True)

        self.subversionLabel = QLabel()
        self.subversionLabel.setFixedWidth(80)
        self.branchLabel = ElidedTextLabel()
        self.commitTimeLabel = DateTimeWidget(self.build_info.commit_time)

        self.build_state_widget = BuildStateWidget(self.parent)

        self.layout.addWidget(self.launchButton)
        self.layout.addWidget(self.subversionLabel)

        if self.show_branch:
            self.layout.addWidget(self.branchLabel, stretch=1)
        else:
            self.layout.addStretch()

        self.layout.addWidget(self.commitTimeLabel)
        self.layout.addWidget(self.build_state_widget)

        self.launchButton.clicked.connect(self.launch)
        self.launchButton.setCursor(Qt.PointingHandCursor)
        self.subversionLabel.setText(self.build_info.subversion)

        if self.branch == 'lts':
            branch_name = "LTS"
        else:
            branch_name = self.branch.replace('-', ' ').title()

        self.branchLabel._setText(branch_name)

        # Context menu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context_menu)

        self.menu = BaseMenuWidget()
        self.menu.setFont(self.parent.font)

        self.menu_extended = BaseMenuWidget()
        self.menu_extended.setFont(self.parent.font)

        self.deleteAction = QAction("Delete From Drive", self)
        self.deleteAction.setIcon(self.parent.icon_delete)
        self.deleteAction.triggered.connect(self.ask_remove_from_drive)

        self.addToQuickLaunchAction = QAction("Add To Quick Launch", self)
        self.addToQuickLaunchAction.setIcon(self.parent.icon_quick_launch)
        self.addToQuickLaunchAction.triggered.connect(self.add_to_quick_launch)

        self.addToFavoritesAction = QAction("Add To Favorites", self)
        self.addToFavoritesAction.setIcon(self.parent.icon_favorite)
        self.addToFavoritesAction.triggered.connect(self.add_to_favorites)

        self.removeFromFavoritesAction = QAction("Remove From Favorites", self)
        self.removeFromFavoritesAction.setIcon(self.parent.icon_favorite)
        self.removeFromFavoritesAction.triggered.connect(
            self.remove_from_favorites)

        if self.parent_widget is not None:
            self.addToFavoritesAction.setVisible(False)
        else:
            self.removeFromFavoritesAction.setVisible(False)

        self.registerExtentionAction = QAction("Register Extension")
        self.registerExtentionAction.triggered.connect(self.register_extension)

        self.createShortcutAction = QAction("Create Shortcut")
        self.createShortcutAction.triggered.connect(self.create_shortcut)

        self.showFolderAction = QAction("Show Folder")
        self.showFolderAction.triggered.connect(self.show_folder)

        self.createSymlinkAction = QAction("Create Symlink")
        self.createSymlinkAction.triggered.connect(self.create_symlink)

        self.installTemplateAction = QAction("Install Template")
        self.installTemplateAction.triggered.connect(self.install_template)

        self.menu.addAction(self.addToQuickLaunchAction)
        self.menu.addAction(self.addToFavoritesAction)
        self.menu.addAction(self.removeFromFavoritesAction)

        self.menu.addSeparator()

        if get_platform() == 'Windows':
            self.menu.addAction(self.registerExtentionAction)

        self.menu.addAction(self.createShortcutAction)
        self.menu.addAction(self.createSymlinkAction)
        self.menu.addAction(self.installTemplateAction)
        self.menu.addSeparator()
        self.menu.addAction(self.showFolderAction)
        self.menu.addAction(self.deleteAction)

        self.menu_extended.addAction(self.deleteAction)

        if self.show_new:
            self.build_state_widget.setNewBuild(True)

            if get_mark_as_favorite() == 0:
                pass
            elif (get_mark_as_favorite() == 1 and self.branch == "stable"):
                self.add_to_quick_launch()
            elif (get_mark_as_favorite() == 2 and self.branch == "daily"):
                self.add_to_quick_launch()
            elif get_mark_as_favorite() == 3:
                self.add_to_quick_launch()
        elif get_favorite_path() == self.link:
            self.add_to_quick_launch()

        self.setEnabled(True)
        self.list_widget.sortItems()
        self.list_widget.resize_labels(['branchLabel'])

    def context_menu(self):
        if len(self.list_widget.selectedItems()) > 1:
            self.menu_extended._show()
            return

        self.createSymlinkAction.setEnabled(True)
        link_path = Path(get_library_folder()) / "bl_symlink"
        link = link_path.as_posix()

        if os.path.exists(link):
            if (os.path.isdir(link) or os.path.islink(link)):
                if link_path.resolve() == self.link:
                    self.createSymlinkAction.setEnabled(False)

        self.menu._show()

    def mouseDoubleClickEvent(self, event):
        if self.build_info is not None:
            self.launch()

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            if self.show_new is True:
                self.build_state_widget.setNewBuild(False)
                self.show_new = False

            mod = QApplication.keyboardModifiers()
            if not (mod == Qt.ShiftModifier or mod == Qt.ControlModifier):
                self.list_widget.clearSelection()
                self.item.setSelected(True)

            event.accept()

        event.ignore()

    def install_template(self):
        self.launchButton.setText("Updating")
        self.launchButton.setEnabled(False)
        self.deleteAction.setEnabled(False)
        self.installTemplateAction.setEnabled(False)
        self.tempalte_installer = TemplateInstaller(
            self.parent.manager, self.link)
        self.tempalte_installer.finished.connect(
            self.install_template_finished)
        self.tempalte_installer.start()

    def install_template_finished(self):
        self.launchButton.setText("Launch")
        self.launchButton.setEnabled(True)
        self.deleteAction.setEnabled(True)
        self.installTemplateAction.setEnabled(True)

    @QtCore.pyqtSlot()
    def launch(self):
        self.item.setSelected(True)

        if self.show_new is True:
            self.build_state_widget.setNewBuild(False)
            self.show_new = False

        platform = get_platform()
        library_folder = Path(get_library_folder())
        blender_args = get_blender_startup_arguments()

        if platform == 'Windows':
            b3d_exe = library_folder / self.link / "blender.exe"

            if blender_args == "":
                proc = _popen(b3d_exe.as_posix())
            else:
                args = [b3d_exe.as_posix()]
                args.extend(blender_args.split(' '))
                proc = _popen(args)
        elif platform == 'Linux':
            bash_args = get_bash_arguments()

            if bash_args != '':
                bash_args = bash_args + " nohup"
            else:
                bash_args = "nohup"

            b3d_exe = library_folder / self.link / "blender"
            proc = _popen('{0} "{1}" {2}'.format(
                bash_args, b3d_exe.as_posix(), blender_args))

        if self.observer is None:
            self.observer = Observer(self)
            self.observer.count_changed.connect(self.proc_count_changed)
            self.observer.started.connect(self.observer_started)
            self.observer.finished.connect(self.observer_finished)
            self.observer.start()

        self.observer.append_proc(proc)

    def proc_count_changed(self, count):
        self.build_state_widget.setCount(count)

    def observer_started(self):
        self.deleteAction.setEnabled(False)
        self.installTemplateAction.setEnabled(False)

    def observer_finished(self):
        self.observer = None
        self.build_state_widget.setCount(0)
        self.deleteAction.setEnabled(True)
        self.installTemplateAction.setEnabled(True)

    @QtCore.pyqtSlot()
    def ask_remove_from_drive(self):
        self.item.setSelected(True)
        self.dlg = DialogWindow(
            self.parent, title="Warning",
            text="Are you sure you want to<br> \
                  delete selected builds?",
            accept_text="Yes", cancel_text="No")

        if len(self.list_widget.selectedItems()) > 1:
            self.dlg.accepted.connect(self.remove_from_drive_extended)
        else:
            self.dlg.accepted.connect(self.remove_from_drive)

    @QtCore.pyqtSlot()
    def remove_from_drive_extended(self):
        for item in self.list_widget.selectedItems():
            self.list_widget.itemWidget(item).remove_from_drive()

    @QtCore.pyqtSlot()
    def remove_from_drive(self):
        self.launchButton.setText("Deleting")
        self.setEnabled(False)
        self.item.setFlags(self.item.flags() & ~Qt.ItemIsSelectable)
        path = Path(get_library_folder()) / self.link
        self.remover = Remover(path)
        self.remover.finished.connect(self.remover_finished)
        self.remover.start()

    def remover_finished(self, code):
        if code == 0:
            self.list_widget.remove_item(self.item)
            self.parent.draw_from_cashed(self.build_info)
            return
        else:
            self.launchButton.setText("Launch")
            self.setEnabled(True)
            return

    @QtCore.pyqtSlot()
    def add_to_quick_launch(self):
        set_favorite_path(self.link)

        if self.parent.favorite is not None:
            self.parent.favorite.launchButton.setIcon(self.parent.icon_fake)
            self.parent.favorite.addToQuickLaunchAction.setEnabled(True)

        self.parent.favorite = self
        self.launchButton.setIcon(self.parent.icon_quick_launch)
        self.addToQuickLaunchAction.setEnabled(False)

    @QtCore.pyqtSlot()
    def add_to_favorites(self):
        item = BaseListWidgetItem()
        widget = LibraryWidget(self.parent, item, self.link,
                               self.list_widget, parent_widget=self)

        self.parent.UserFavoritesListWidget.insert_item(item, widget)
        self.child_widget = widget

        self.removeFromFavoritesAction.setVisible(True)
        self.addToFavoritesAction.setVisible(False)

    @QtCore.pyqtSlot()
    def remove_from_favorites(self):
        if self.parent_widget is None:
            widget = self
        else:
            widget = self.parent_widget

        self.parent.UserFavoritesListWidget.remove_item(
            widget.child_widget.item)

        widget.child_widget = None
        widget.removeFromFavoritesAction.setVisible(False)
        widget.addToFavoritesAction.setVisible(True)

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
        target = self.link.as_posix()
        link = (Path(get_library_folder()) / "bl_symlink").as_posix()
        platform = get_platform()

        if platform == 'Windows':
            if os.path.exists(link):
                if os.path.isdir(link):
                    os.rmdir(link)

            _call('mklink /J "{0}" "{1}"'.format(link, target))
        elif platform == 'Linux':
            if os.path.exists(link):
                if os.path.islink(link):
                    os.unlink(link)

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
