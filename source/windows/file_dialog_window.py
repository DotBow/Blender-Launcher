from PyQt6.QtWidgets import QFileDialog


class FileDialogWindow(QFileDialog):
    def __init__(self):
        super().__init__()

    def _getExistingDirectory(self, parent, title, dir):
        options = (
            QFileDialog.Option.DontUseNativeDialog |
            QFileDialog.Option.ShowDirsOnly |
            QFileDialog.Option.HideNameFilterDetails |
            QFileDialog.Option.DontUseCustomDirectoryIcons)
        return self.getExistingDirectory(
            parent, title, dir, options)
