from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QProgressBar


class BaseProgressBarWidget(QProgressBar):
    progress_updated = pyqtSignal('PyQt_PyObject', 'PyQt_PyObject')

    def __init__(self, format="", parent=None) -> None:
        super().__init__(parent)

        self.setFormat(format)
        self.setMinimum(0)

        self.set_progress(0, 0)

    def set_progress(self, obtained, total):
        # Convert bytes to megabytes
        obtained = obtained / 1048576
        total = total / 1048576

        # Update appearance
        self.setMaximum(total)
        self.setValue(obtained)

        # Repaint and call signal
        self.repaint()
        self.progress_updated.emit(obtained, total)
