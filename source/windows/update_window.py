import os
import tempfile
from pathlib import Path
from shutil import copyfileobj

from modules._platform import _popen, get_environment, get_platform
from PyQt5.QtWidgets import QMainWindow
from threads.downloader import Downloader
from threads.extractor import Extractor
from ui.update_window_ui import UpdateWindowUI

from windows.base_window import BaseWindow


class UpdateWindow(QMainWindow, BaseWindow, UpdateWindowUI):
    def __init__(self, parent, tag):
        super().__init__()
        self.setWindowTitle("Update")
        self.setupUi(self)

        self.parent = parent
        self.tag = tag

        self.download()

    def download(self):
        self.link = "https://github.com/DotBow/Blender-Launcher/releases/download/{0}/Blender_Launcher_{0}_{1}_x64.zip".format(
            self.tag, get_platform())
        self.thread = Downloader(self.parent.manager, self.link)
        self.thread.progress_changed.connect(self.set_progress_bar)
        self.thread.finished.connect(self.extract)
        self.thread.start()

        self.show()

    def extract(self, source):
        dist = tempfile.gettempdir()
        self.thread = Extractor(self.parent.manager, source, dist)
        self.thread.progress_changed.connect(self.set_progress_bar)
        self.thread.finished.connect(self.run)
        self.thread.start()

    def run(self, dist):
        platform = get_platform()
        cwd = Path.cwd()

        if platform == 'Windows':
            bl_exe = "Blender Launcher.exe"
            blu_exe = "Blender Launcher Updater.exe"
        elif platform == 'Linux':
            bl_exe = "Blender Launcher"
            blu_exe = "Blender Launcher Updater"

        source = cwd / bl_exe
        dist = cwd / blu_exe

        with open(source.as_posix(), 'rb') as f1, open(dist.as_posix(), 'wb') as f2:
            copyfileobj(f1, f2)

        if platform == 'Windows':
            _popen([dist.as_posix(), "-update"])
        elif platform == 'Linux':
            os.chmod(dist.as_posix(), 0o744)
            _popen('nohup "' + dist.as_posix() + '" -update')

        self.parent.destroy()

    def closeEvent(self, event):
        event.ignore()
        self.showMinimized()
