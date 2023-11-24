import os

from modules._platform import _popen, get_cwd, get_platform
from PyQt5.QtWidgets import QMainWindow
from threads.downloader import Downloader
from threads.extractor import Extractor
from ui.update_window_ui import UpdateWindowUI

from windows.base_window import BaseWindow

link = "https://github.com/Victor-IX/Blender-Launcher/releases/download/{0}/Blender_Launcher_{0}_{1}_x64.zip"


class BlenderLauncherUpdater(QMainWindow, BaseWindow, UpdateWindowUI):
    def __init__(self, app, version, release_tag):
        super(BlenderLauncherUpdater, self).__init__(app=app, version=version)
        self.setupUi(self)

        self.release_tag = release_tag
        self.platform = get_platform()
        self.cwd = get_cwd()

        self.show()
        self.download()

    def download(self):
        # TODO
        # This function should not use proxy for downloading new builds!
        self.link = link.format(self.release_tag, self.platform)
        self.downloader = Downloader(self.manager, self.link)
        self.downloader.progress_changed.connect(self.ProgressBar.set_progress)
        self.downloader.finished.connect(self.extract)
        self.downloader.start()

    def extract(self, source):
        self.extractor = Extractor(self.manager, source, self.cwd)
        self.extractor.progress_changed.connect(self.ProgressBar.set_progress)
        self.extractor.finished.connect(self.finish)
        self.extractor.start()

    def finish(self, dist):
        # Launch 'Blender Launcher.exe' and exit
        if self.platform == 'Windows':
            _popen([dist])
        elif self.platform == 'Linux':
            os.chmod(dist, 0o744)
            _popen('nohup "' + dist + '"')

        self.app.quit()

    def closeEvent(self, event):
        event.ignore()
        self.showMinimized()
