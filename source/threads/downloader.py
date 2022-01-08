import os
import shutil
from pathlib import Path

from modules.settings import get_library_folder
from PyQt5.QtCore import QThread, pyqtSignal


class Downloader(QThread):
    started = pyqtSignal()
    progress_changed = pyqtSignal('PyQt_PyObject', 'PyQt_PyObject')
    finished = pyqtSignal('PyQt_PyObject')

    def __init__(self, manager, link):
        QThread.__init__(self)
        self.manager = manager
        self.link = link
        self.size = 0

    def run(self):
        self.started.emit()

        # request = self.manager.request(
        #     'GET', self.link, preload_content=False)
        temp_folder = Path(get_library_folder()) / ".temp"

        # Create temp directory
        if not temp_folder.is_dir():
            temp_folder.mkdir()

        dist = temp_folder / Path(self.link).name

        with self.manager.request('GET', self.link, preload_content=False) as r:
            with open(dist, 'wb') as f:
                self.size = int(r.headers['Content-Length'])
                copyfileobj(r, f, self.test)

        # Download
        # with open(dist, 'wb') as file:
        #     size = int(request.headers['Content-Length'])

        #     for chunk in request.stream(16 * 1024):
        #         file.write(chunk)
        #         progress = os.stat(dist).st_size / size
        #         self.progress_changed.emit(progress, "Downloading: %p%")

        r.release_conn()
        r.close()

        self.finished.emit(dist)
        return

    def test(self, p):
        progress = p / self.size
        print(progress)
        self.progress_changed.emit(progress, "Downloading: %p%")


def copyfileobj(fsrc, fdst, callback, length=0):
    try:
        # check for optimisation opportunity
        if "b" in fsrc.mode and "b" in fdst.mode and fsrc.readinto:
            return _copyfileobj_readinto(fsrc, fdst, callback, length)
    except AttributeError:
        # one or both file objects do not support a .mode or .readinto attribute
        pass

    if not length:
        length = shutil.COPY_BUFSIZE

    fsrc_read = fsrc.read
    fdst_write = fdst.write

    copied = 0
    while True:
        buf = fsrc_read(length)
        if not buf:
            break
        fdst_write(buf)
        copied += len(buf)
        callback(copied)


# differs from shutil.COPY_BUFSIZE on platforms != Windows
READINTO_BUFSIZE = 1024 * 1024


def _copyfileobj_readinto(fsrc, fdst, callback, length=0):
    """readinto()/memoryview() based variant of copyfileobj().
    *fsrc* must support readinto() method and both files must be
    open in binary mode.
    """
    fsrc_readinto = fsrc.readinto
    fdst_write = fdst.write

    if not length:
        try:
            file_size = os.stat(fsrc.fileno()).st_size
        except OSError:
            file_size = READINTO_BUFSIZE
        length = min(file_size, READINTO_BUFSIZE)

    copied = 0
    with memoryview(bytearray(length)) as mv:
        while True:
            n = fsrc_readinto(mv)
            if not n:
                break
            elif n < length:
                with mv[:n] as smv:
                    fdst.write(smv)
            else:
                fdst_write(mv)
            copied += n
            callback(copied)
