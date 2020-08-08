import subprocess
from pathlib import Path
from subprocess import DEVNULL, PIPE, STDOUT

from PyQt5.QtCore import QThread, pyqtSignal

from modules._platform import get_platform

if get_platform() == 'Windows':
    from subprocess import CREATE_NO_WINDOW


class Register(QThread):
    finished = pyqtSignal('PyQt_PyObject')

    def __init__(self, path):
        QThread.__init__(self)
        self.path = path

    def run(self):
        platform = get_platform()

        if platform == 'Windows':
            b3d_exe = Path(self.path) / "blender.exe"
            subprocess.call([str(b3d_exe), "-r"], creationflags=CREATE_NO_WINDOW,
                            shell=True, stdout=PIPE, stderr=STDOUT, stdin=DEVNULL)
        elif platform == 'Linux':
            b3d_exe = Path(self.path) / "blender"
            pass

        self.finished.emit(0)
        return
