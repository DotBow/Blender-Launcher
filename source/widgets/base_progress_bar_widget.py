from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QProgressBar


class BaseProgressBarWidget(QProgressBar):
    progress_updated = pyqtSignal('PyQt_PyObject', 'PyQt_PyObject')

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setAlignment(Qt.AlignCenter)
        self.setMinimum(0)
        self.set_progress(0, 0)

    def set_progress(self, obtained, total, title=""):
        # Convert bytes to megabytes
        obtained = obtained / 1048576
        total = total / 1048576

        # Update appearance
        self.setMaximum(total)
        self.setValue(obtained)

        # Repaint and call signal
        self.repaint()
        self.setFormat(
            "{}: {:.1f} of {:.1f} MB".format(title, obtained, total))
        self.progress_updated.emit(obtained, total)
