from PyQt5.QtWidgets import QListWidget


class BaseListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.setFrameShape(QListWidget.NoFrame)

    def remove_item(self, item):
        row = self.row(item)
        self.takeItem(row)
