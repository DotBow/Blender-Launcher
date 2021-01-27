from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QAbstractItemView, QListWidget


class BaseListWidget(QListWidget):
    subversion_indent_changed = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent=None, extended_selection=False):
        super().__init__()
        self.parent = parent
        self.widgets = set()
        self.metrics = QFontMetrics(self.font())

        self.setFrameShape(QListWidget.NoFrame)
        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)
        self.setProperty("HideBorder", True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        if extended_selection is True:
            self.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def add_item(self, item, widget):
        item.setSizeHint(widget.sizeHint())
        self.addItem(item)
        self.setItemWidget(item, widget)
        self.count_changed()
        self.widgets.add(widget)

    def insert_item(self, item, widget, index=0):
        item.setSizeHint(widget.sizeHint())
        self.insertItem(index, item)
        self.setItemWidget(item, widget)
        self.count_changed()
        self.widgets.add(widget)

    def remove_item(self, item):
        self.widgets.remove(self.itemWidget(item))
        row = self.row(item)
        self.takeItem(row)
        self.count_changed()
        self.resize()

    def count_changed(self):
        if self.count() > 0:
            self.show()
            self.parent.HeaderWidget.show()
            self.parent.PlaceholderWidget.hide()
        else:
            self.hide()
            self.parent.HeaderWidget.hide()
            self.parent.PlaceholderWidget.show()

    def items(self):
        items = []

        for i in range(self.count()):
            item = self.itemWidget(self.item(i))
            items.append(item)

        return items

    def contains_build_info(self, build_info):
        for widget in self.widgets:
            if build_info == widget.build_info:
                return True

        return False

    def resize(self):
        widths = []

        for widget in self.widgets:
            if not hasattr(widget, 'subversionLabel'):
                return
            else:
                text = widget.subversionLabel.text()
                widths.append(self.metrics.width(text))

        if len(widths) > 0:
            indent = int((80 - max(widths)) * 0.5)
            self.subversion_indent_changed.emit(indent)

    def _clear(self):
        self.clear()
        self.widgets.clear()
        self.count_changed()
