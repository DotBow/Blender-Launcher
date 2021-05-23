import tarfile
import zipfile
from pathlib import Path

from modules._platform import _check_call
from PyQt5.QtCore import QThread, pyqtSignal


class Extractor(QThread):
    started = pyqtSignal()
    progress_changed = pyqtSignal('PyQt_PyObject', 'PyQt_PyObject')
    finished = pyqtSignal('PyQt_PyObject')

    def __init__(self, manager, source, dist):
        QThread.__init__(self)
        self.manager = manager
        self.source = Path(source)
        self.dist = Path(dist)

    def run(self):
        self.progress_changed.emit(0, "Extracting: %p%")
        suffixes = self.source.suffixes

        if suffixes[-1] == ".zip":
            zf = zipfile.ZipFile(self.source)
            folder = zf.infolist()[0].filename.split('/')[0]
            uncompress_size = sum((file.file_size for file in zf.infolist()))
            extracted_size = 0

            for file in zf.infolist():
                zf.extract(file, self.dist)
                extracted_size += file.file_size
                progress = extracted_size / uncompress_size
                self.progress_changed.emit(progress, "Extracting: %p%")

            zf.close()
            self.finished.emit(self.dist / folder)
        elif suffixes[-2] == '.tar':
            tar = tarfile.open(self.source)
            folder = tar.getnames()[0].split('/')[0]
            uncompress_size = sum((member.size for member in tar.getmembers()))
            extracted_size = 0

            for member in tar.getmembers():
                tar.extract(member, path=self.dist)
                extracted_size += member.size
                progress = extracted_size / uncompress_size
                self.progress_changed.emit(progress,  "Extracting: %p%")

            tar.close()
            self.finished.emit(self.dist / folder)
        elif suffixes[-1] == '.dmg':
            _check_call(["hdiutil", "mount", self.source.as_posix()])
            dist = self.dist / self.source.stem

            if not dist.is_dir():
                dist.mkdir()

            _check_call(["cp", "-R", "/Volumes/Blender", dist.as_posix()])
            _check_call(["hdiutil", "unmount", "/Volumes/Blender"])

            self.finished.emit(dist)

        return
