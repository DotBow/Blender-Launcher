import os
import re
import subprocess
from pathlib import Path

from items.base_list_widget_item import BaseListWidgetItem
from modules._platform import _call, _popen, get_platform
from modules.build_info import BuildInfoReader
from modules.settings import (get_bash_arguments,
                              get_blender_startup_arguments, get_favorite_path,
                              get_launch_blender_no_console,
                              get_library_folder, get_mark_as_favorite,
                              set_favorite_path)
from modules.shortcut import create_shortcut
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QAction, QApplication, QHBoxLayout, QLabel,
                             QPushButton)
from threads.observer import Observer
from threads.register import Register
from threads.remover import Remover
from threads.template_installer import TemplateInstaller
from windows.dialog_window import DialogWindow

from widgets.base_build_widget import BaseBuildWidget
from widgets.base_line_edit import BaseLineEdit
from widgets.base_menu_widget import BaseMenuWidget
from widgets.build_state_widget import BuildStateWidget
from widgets.datetime_widget import DateTimeWidget
from widgets.elided_text_label import ElidedTextLabel
from widgets.left_icon_button_widget import LeftIconButtonWidget


class LibraryWidget(BaseBuildWidget):
    def __init__(self, parent, item, link, list_widget,
                 show_new=False, parent_widget=None):
        super(LibraryWidget, self).__init__(parent=parent)

        self.parent = parent
        self.item = item
        self.link = link
        self.list_widget = list_widget
        self.show_new = show_new
        self.observer = None
        self.build_info = None
        self.child_widget = None
        self.parent_widget = parent_widget
        self.build_info_writer = None
        self.is_damaged = False

        self.parent.quit_signal.connect(self.list_widget_deleted)
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
        else:
            self.draw(self.parent_widget.build_info)

    def draw(self, build_info):
        if self.parent_widget is None:
            if self.parent.library_drawer is not None:
                self.parent.library_drawer.build_released.emit()

            if build_info is None:
                self.infoLabel.setText(
                    ("Build *{0}* is damaged!").format(Path(self.link).name))
                self.launchButton.setText("Delete")
                self.launchButton.clicked.connect(self.ask_remove_from_drive)
                self.setEnabled(True)
                self.is_damaged = True
                return

            for i in reversed(range(self.layout.count())):
                self.layout.itemAt(i).widget().setParent(None)

        self.build_info = build_info
        self.branch = self.build_info.branch
        self.item.date = build_info.commit_time

        self.launchButton = LeftIconButtonWidget("Launch")
        self.launchButton.setFixedWidth(85)
        self.launchButton.setProperty("LaunchButton", True)

        if self.branch == 'lts':
            branch_name = "LTS"
        elif (self.parent_widget is not None) and self.build_info.custom_name:
            branch_name = self.build_info.custom_name
        elif self.branch == 'daily':
            branch_name = self.build_info.subversion.split(" ", 1)[1]
        else:
            branch_name = re.sub(
                r'(\-|\_)', ' ', self.build_info.branch).title()

        sub = self.build_info.subversion.split(" ", 1)
        self.subversionLabel = QLabel(sub[0])
        self.subversionLabel.setFixedWidth(85)
        self.subversionLabel.setIndent(21)
        self.branchLabel = ElidedTextLabel(branch_name)
        self.commitTimeLabel = DateTimeWidget(
            self.build_info.commit_time, self.build_info.build_hash)

        self.build_state_widget = BuildStateWidget(
            self.parent, self.list_widget)

        self.layout.addWidget(self.launchButton)
        self.layout.addWidget(self.subversionLabel)
        self.layout.addWidget(self.branchLabel, stretch=1)

        if self.parent_widget is not None:
            self.lineEdit = BaseLineEdit()
            self.lineEdit.setMaxLength(256)
            self.lineEdit.setContextMenuPolicy(Qt.NoContextMenu)
            self.lineEdit.escapePressed.connect(
                self.rename_branch_rejected)
            self.lineEdit.returnPressed.connect(
                self.rename_branch_accepted)
            self.layout.addWidget(self.lineEdit, stretch=1)
            self.lineEdit.hide()

        self.layout.addWidget(self.commitTimeLabel)
        self.layout.addWidget(self.build_state_widget)

        self.launchButton.clicked.connect(lambda: self.launch(True))
        self.launchButton.setCursor(Qt.PointingHandCursor)

        # Context menu
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

        if self.parent_widget is not None:
            self.renameBranchAction = QAction("Rename Branch")
            self.renameBranchAction.triggered.connect(self.rename_branch)
            self.menu.addAction(self.renameBranchAction)

        self.menu.addSeparator()

        if get_platform() == 'Windows':
            self.menu.addAction(self.registerExtentionAction)

        self.menu.addAction(self.createShortcutAction)
        self.menu.addAction(self.createSymlinkAction)
        self.menu.addAction(self.installTemplateAction)
        self.menu.addSeparator()

        if self.branch in "stable lts":
            self.menu.addAction(self.showReleaseNotesAction)

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

        if self.build_info.is_favorite and self.parent_widget is None:
            self.add_to_favorites()

    def context_menu(self):
        if self.is_damaged:
            return

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
        self.launchButton._setText("Updating")
        self.launchButton.setEnabled(False)
        self.deleteAction.setEnabled(False)
        self.installTemplateAction.setEnabled(False)
        self.tempalte_installer = TemplateInstaller(
            self.parent.manager, self.link)
        self.tempalte_installer.finished.connect(
            self.install_template_finished)
        self.tempalte_installer.start()

    def install_template_finished(self):
        self.launchButton._setText("Launch")
        self.launchButton.setEnabled(True)
        self.deleteAction.setEnabled(True)
        self.installTemplateAction.setEnabled(True)

    def launch(self, update_selection=False):
        if update_selection is True:
            self.list_widget.clearSelection()
            self.item.setSelected(True)

        if self.parent_widget is not None:
            self.parent_widget.launch()
            return

        if self.show_new is True:
            self.build_state_widget.setNewBuild(False)
            self.show_new = False

        platform = get_platform()
        library_folder = Path(get_library_folder())
        blender_args = get_blender_startup_arguments()

        if platform == 'Windows':
            if get_launch_blender_no_console():
                if Path.exists(library_folder / self.link / "blender-launcher.exe"):
                    b3d_exe = library_folder / self.link / "blender-launcher.exe"
                else:
                    b3d_exe = library_folder / self.link / "blender.exe"
            else:
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

        self.observer.append_proc.emit(proc)

    def proc_count_changed(self, count):
        self.build_state_widget.setCount(count)

        if self.child_widget is not None:
            self.child_widget.proc_count_changed(count)

    def observer_started(self):
        self.deleteAction.setEnabled(False)
        self.installTemplateAction.setEnabled(False)

        if self.child_widget is not None:
            self.child_widget.observer_started()

    def observer_finished(self):
        self.observer = None
        self.build_state_widget.setCount(0)
        self.deleteAction.setEnabled(True)
        self.installTemplateAction.setEnabled(True)

        if self.child_widget is not None:
            self.child_widget.observer_finished()

    @QtCore.pyqtSlot()
    def rename_branch(self):
        self.lineEdit.setText(self.branchLabel.text)
        self.lineEdit.selectAll()
        self.lineEdit.setFocus()
        self.lineEdit.show()
        self.branchLabel.hide()

    @QtCore.pyqtSlot()
    def rename_branch_accepted(self):
        self.lineEdit.hide()
        name = self.lineEdit.text().strip()

        if name:
            self.branchLabel._setText(name)
            self.build_info.custom_name = name
            self.write_build_info()

        self.branchLabel.show()

    @QtCore.pyqtSlot()
    def rename_branch_rejected(self):
        self.lineEdit.hide()
        self.branchLabel.show()

    def write_build_info(self):
        if self.build_info_writer is None:
            self.build_info_writer = BuildInfoReader(
                self.link, build_info=self.build_info,
                mode=BuildInfoReader.Mode.WRITE)
            self.build_info_writer.finished.connect(
                self.build_info_writer_finished)
            self.build_info_writer.start()

    def build_info_writer_finished(self):
        self.build_info_writer = None

    @QtCore.pyqtSlot()
    def ask_remove_from_drive(self):
        self.item.setSelected(True)
        self.dlg = DialogWindow(
            parent=self.parent, title="Warning",
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
        if self.parent_widget is not None:
            self.parent_widget.remove_from_drive()
            return

        path = Path(get_library_folder()) / self.link
        self.remover = Remover(path, self.parent)
        self.remover.started.connect(self.remover_started)
        self.remover.finished.connect(self.remover_finished)
        self.remover.start()

    # TODO Clear icon if build in quick launch
    def remover_started(self):
        self.launchButton._setText("Deleting")
        self.setEnabled(False)
        self.item.setFlags(self.item.flags() & ~Qt.ItemIsSelectable)

        if self.child_widget is not None:
            self.child_widget.remover_started()

    def remover_finished(self, code):
        if self.child_widget is not None:
            self.child_widget.remover_finished(code)

        if code == 0:
            self.list_widget.remove_item(self.item)

            if self.parent_widget is None:
                self.parent.draw_from_cashed(self.build_info)

            return
        # TODO Child synchronization and reverting selection flags
        else:
            self.launchButton._setText("Launch")
            self.setEnabled(True)
            return

    @QtCore.pyqtSlot()
    def add_to_quick_launch(self):
        if (self.parent.favorite is not None) and \
                (self.parent.favorite.link != self.link):
            self.parent.favorite.remove_from_quick_launch()

        set_favorite_path(self.link)
        self.parent.favorite = self

        self.launchButton.setIcon(self.parent.icon_quick_launch)
        self.addToQuickLaunchAction.setEnabled(False)

        # TODO Make more optimal and simpler synchronization
        if self.parent_widget is not None:
            self.parent_widget.launchButton.setIcon(
                self.parent.icon_quick_launch)
            self.parent_widget.addToQuickLaunchAction.setEnabled(False)

        if self.child_widget is not None:
            self.child_widget.launchButton.setIcon(
                self.parent.icon_quick_launch)
            self.child_widget.addToQuickLaunchAction.setEnabled(False)

    @QtCore.pyqtSlot()
    def remove_from_quick_launch(self):
        self.launchButton.setIcon(self.parent.icon_fake)
        self.addToQuickLaunchAction.setEnabled(True)

        # TODO Make more optimal and simpler synchronization
        if self.parent_widget is not None:
            self.parent_widget.launchButton.setIcon(self.parent.icon_fake)
            self.parent_widget.addToQuickLaunchAction.setEnabled(True)

        if self.child_widget is not None:
            self.child_widget.launchButton.setIcon(self.parent.icon_fake)
            self.child_widget.addToQuickLaunchAction.setEnabled(True)

    @QtCore.pyqtSlot()
    def add_to_favorites(self):
        item = BaseListWidgetItem()
        widget = LibraryWidget(self.parent, item, self.link,
                               self.parent.UserFavoritesListWidget,
                               parent_widget=self)

        self.parent.UserFavoritesListWidget.insert_item(item, widget)
        self.child_widget = widget

        self.removeFromFavoritesAction.setVisible(True)
        self.addToFavoritesAction.setVisible(False)

        if self.build_info.is_favorite is False:
            self.build_info.is_favorite = True
            self.write_build_info()

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

        self.build_info.is_favorite = False
        self.build_info_writer = BuildInfoReader(
            self.link, build_info=self.build_info,
            mode=BuildInfoReader.Mode.WRITE)
        self.build_info_writer.start()

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
            try:
                os.rmdir(link)
            except Exception:
                pass

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

    def list_widget_deleted(self):
        self.list_widget = None

    def _destroyed(self):
        if self.parent.favorite == self:
            self.parent.favorite = None
