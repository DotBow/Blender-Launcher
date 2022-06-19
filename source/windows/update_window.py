import os
import tempfile
from pathlib import Path
from shutil import copyfileobj

from modules._platform import _popen, get_cwd, get_platform
from PyQt5.QtWidgets import QMainWindow
from threads.downloader import Downloader
from threads.extractor import Extractor
from ui.update_window_ui import UpdateWindowUI

from windows.base_window import BaseWindow


class BlenderLauncherUpdater(QMainWindow, BaseWindow, UpdateWindowUI):
    def __init__(self, app, version, tag):
        super(BlenderLauncherUpdater, self).__init__(app=app, version=version)
        self.tag = tag
        self.setupUi(self)

        self.show()
        self.download()

    def download(self):
        # TODO
        # This function should not use proxy for downloading new builds!
        self.ProgressBar.setFormat("Downloading: %p%")
        self.link = "https://github.com/DotBow/Blender-Launcher/releases/download/{0}/Blender_Launcher_{0}_{1}_x64.zip".format(
            self.tag, get_platform())
        self.downloader = Downloader(self.manager, self.link)
        self.downloader.progress_changed.connect(self.set_progress_bar)
        self.downloader.finished.connect(self.extract)
        self.downloader.start()

        self.show()

    def extract(self, source):
        self.ProgressBar.setFormat("Extracting: %p%")
        dist = tempfile.gettempdir()
        self.extractor = Extractor(self.manager, source, dist)
        self.extractor.progress_changed.connect(self.set_progress_bar)
        self.extractor.finished.connect(self.run)
        self.extractor.start()

    def run(self, dist):
        platform = get_platform()
        temp = Path(tempfile.gettempdir())
        cwd = get_cwd()

        if platform == 'Windows':
            bl_exe = "Blender Launcher.exe"
        elif platform == 'Linux':
            bl_exe = "Blender Launcher"

        source = (temp / bl_exe).as_posix()
        dist = (cwd / bl_exe).as_posix()

        with open(source, 'rb') as f1, open(dist, 'wb') as f2:
            copyfileobj(f1, f2)

        if platform == 'Windows':
            _popen([dist])
        elif platform == 'Linux':
            os.chmod(dist, 0o744)
            _popen('nohup "' + dist + '"')

        self.app.quit()

    def closeEvent(self, event):
        event.ignore()
        self.showMinimized()
