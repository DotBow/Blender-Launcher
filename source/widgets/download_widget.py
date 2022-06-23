import re
from enum import Enum
from pathlib import Path

from modules.build_info import BuildInfoReader
from modules.enums import MessageType
from modules.settings import get_install_template, get_library_folder
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout
from threads.downloader import Downloader
from threads.extractor import Extractor
from threads.renamer import Renamer
from threads.template_installer import TemplateInstaller

from widgets.base_build_widget import BaseBuildWidget
from widgets.base_progress_bar_widget import BaseProgressBarWidget
from widgets.build_state_widget import BuildStateWidget
from widgets.datetime_widget import DateTimeWidget
from widgets.elided_text_label import ElidedTextLabel


class DownloadState(Enum):
    WAITING = 1
    DOWNLOADING = 2


class DownloadWidget(BaseBuildWidget):
    def __init__(self, parent, list_widget, item, build_info,
                 show_new=False):
        super(DownloadWidget, self).__init__(parent=parent)
        self.parent = parent
        self.list_widget = list_widget
        self.item = item
        self.build_info = build_info
        self.show_new = show_new
        self.state = DownloadState.WAITING
        self.build_dir = None

        self.progressBar = BaseProgressBarWidget()
        font = self.parent.font
        font.setPointSize(8)
        self.progressBar.setFont(font)
        self.progressBar.setFixedHeight(18)
        self.progressBar.hide()

        self.downloadButton = QPushButton("Download")
        self.downloadButton.setFixedWidth(85)
        self.downloadButton.setProperty("LaunchButton", True)
        self.downloadButton.clicked.connect(self.init_downloader)
        self.downloadButton.setCursor(Qt.PointingHandCursor)

        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.setFixedWidth(85)
        self.cancelButton.setProperty("CancelButton", True)
        self.cancelButton.clicked.connect(self.download_cancelled)
        self.cancelButton.setCursor(Qt.PointingHandCursor)
        self.cancelButton.hide()

        self.main_hl = QHBoxLayout()
        self.main_hl.setContentsMargins(2, 2, 0, 2)
        self.main_hl.setSpacing(0)

        self.sub_vl = QVBoxLayout()
        self.sub_vl.setContentsMargins(0, 0, 0, 0)
        self.main_hl.setSpacing(0)

        self.build_info_hl = QHBoxLayout()
        self.build_info_hl.setContentsMargins(0, 0, 0, 0)
        self.main_hl.setSpacing(0)

        self.progress_bar_hl = QHBoxLayout()
        self.progress_bar_hl.setContentsMargins(16, 0, 8, 0)
        self.main_hl.setSpacing(0)

        if self.build_info.branch == 'lts':
            branch_name = "LTS"
        elif self.build_info.branch == 'daily':
            branch_name = self.build_info.subversion.split(" ", 1)[1]
        else:
            branch_name = re.sub(
                r'(\-|\_)', ' ', self.build_info.branch).title()

        self.subversionLabel = QLabel(
            self.build_info.subversion.split(" ", 1)[0])
        self.subversionLabel.setFixedWidth(85)
        self.subversionLabel.setIndent(20)
        self.branchLabel = ElidedTextLabel(branch_name)
        self.commitTimeLabel = DateTimeWidget(
            self.build_info.commit_time, self.build_info.build_hash)
        self.build_state_widget = BuildStateWidget(
            self.parent, self.list_widget)

        self.build_info_hl.addWidget(self.subversionLabel)
        self.build_info_hl.addWidget(self.branchLabel, stretch=1)
        self.build_info_hl.addWidget(self.commitTimeLabel)

        if self.show_new:
            self.build_state_widget.setNewBuild(True)

        self.progress_bar_hl.addWidget(self.progressBar)

        self.sub_vl.addLayout(self.build_info_hl)
        self.sub_vl.addLayout(self.progress_bar_hl)

        self.main_hl.addWidget(self.downloadButton)
        self.main_hl.addWidget(self.cancelButton)
        self.main_hl.addLayout(self.sub_vl)
        self.main_hl.addWidget(self.build_state_widget)

        self.setLayout(self.main_hl)

        if self.build_info.branch in "stable lts":
            self.menu.addAction(self.showReleaseNotesAction)
        else:
            regexp = re.compile(r'D\d{5}')

            if regexp.search(self.build_info.branch):
                self.showReleaseNotesAction.setText("Show Patch Details")
                self.menu.addAction(self.showReleaseNotesAction)

    def context_menu(self):
        self.menu._show()

    def mouseDoubleClickEvent(self, event):
        if self.state != DownloadState.DOWNLOADING:
            self.init_downloader()

    def mouseReleaseEvent(self, event):
        if self.show_new is True:
            self.build_state_widget.setNewBuild(False)
            self.show_new = False

    def init_downloader(self):
        self.item.setSelected(True)

        if self.show_new is True:
            self.build_state_widget.setNewBuild(False)
            self.show_new = False

        self.state = DownloadState.DOWNLOADING
        self.downloader = Downloader(self.parent.manager, self.build_info.link)
        self.downloader.started.connect(self.download_started)
        self.downloader.progress_changed.connect(self.progressBar.set_progress)
        self.downloader.finished.connect(self.init_extractor)

        self.progress_start = 0
        self.progress_end = 0.5

        self.downloader.start()

    def init_extractor(self, source):
        self.cancelButton.setEnabled(False)
        library_folder = Path(get_library_folder())

        if (self.build_info.branch == 'stable') or \
                (self.build_info.branch == 'lts'):
            dist = library_folder / 'stable'
        elif self.build_info.branch == 'daily':
            dist = library_folder / 'daily'
        else:
            dist = library_folder / 'experimental'

        self.extractor = Extractor(self.parent.manager, source, dist)
        self.extractor.progress_changed.connect(self.progressBar.set_progress)
        self.extractor.finished.connect(self.init_template_installer)
        self.extractor.start()
        self.build_state_widget.setExtract()

    def init_template_installer(self, dist):
        self.build_state_widget.setExtract(False)
        self.build_dir = dist

        if get_install_template():
            self.template_installer = TemplateInstaller(
                self.parent.manager, self.build_dir)
            self.template_installer.progress_changed.connect(
                self.progressBar.set_progress)
            self.template_installer.finished.connect(
                lambda: self.download_get_info())
            self.template_installer.start()
        else:
            self.download_get_info()

    def download_started(self):
        self.progressBar.show()
        self.cancelButton.show()
        self.downloadButton.hide()
        self.build_state_widget.setDownload()

    def download_cancelled(self):
        self.item.setSelected(True)
        self.state = DownloadState.WAITING
        self.progressBar.hide()
        self.cancelButton.hide()
        self.downloader.terminate()
        self.downloader.wait()
        self.downloadButton.show()
        self.build_state_widget.setDownload(False)

    def download_get_info(self):
        if self.parent.platform == 'Linux':
            archive_name = Path(self.build_info.link).with_suffix('').stem
        elif self.parent.platform in {'Windows', 'macOS'}:
            archive_name = Path(self.build_info.link).stem

        self.build_info_reader = BuildInfoReader(
            self.build_dir, archive_name=archive_name)
        self.build_info_reader.finished.connect(self.download_rename)
        self.build_info_reader.start()

    def download_rename(self, build_info):
        new_name = 'blender-{}+{}.{}'.format(
            build_info.subversion,
            build_info.branch,
            build_info.build_hash
        )

        self.build_renamer = Renamer(self.build_dir, new_name)
        self.build_renamer.finished.connect(self.download_finished)
        self.build_renamer.start()

    def download_finished(self, path):
        self.state = DownloadState.WAITING

        if path is None:
            path = self.build_dir

        if path is not None:
            self.parent.draw_to_library(path, True)
            self.parent.clear_temp()
            name = "{0} {1} {2}".format(
                self.subversionLabel.text(),
                self.branchLabel.text,
                self.build_info.commit_time)
            self.parent.show_message(
                "Blender {0} download finished!".format(name),
                type=MessageType.DOWNLOADFINISHED)
            self.destroy()

        self.build_state_widget.setExtract(False)

    def destroy(self):
        if self.state == DownloadState.WAITING:
            self.list_widget.remove_item(self.item)
