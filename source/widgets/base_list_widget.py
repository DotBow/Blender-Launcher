from PyQt5.QtWidgets import QListWidget


class BaseListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.setFrameShape(QListWidget.NoFrame)
        self.setSortingEnabled(True)

    def remove_item(self, item):
        row = self.row(item)
        self.takeItem(row)

    def resize_labels(self, params):
        items = []

        for i in range(self.count()):
            item = self.itemWidget(self.item(i))

            if hasattr(item, 'subversionLabel'):
                items.append(item)
            else:
                return

        for param in params:
            item = max(
                items, key=lambda item: getattr(item, param).minimumSizeHint().width())
            width = getattr(item, param).minimumSizeHint().width()

            for item in items:
                getattr(item, param).setFixedWidth(width)
