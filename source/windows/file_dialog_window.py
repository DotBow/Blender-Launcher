from PyQt5.QtWidgets import QFileDialog


class FileDialogWindow(QFileDialog):
    def __init__(self):
        super().__init__()

    def _getExistingDirectory(self, parent, title, dir):
        options = (
            QFileDialog.DontUseNativeDialog |
            QFileDialog.ShowDirsOnly |
            QFileDialog.HideNameFilterDetails)
        return self.getExistingDirectory(
            parent, title, dir, options)
