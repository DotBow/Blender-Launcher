from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QAbstractItemView, QListWidget


class BaseListWidget(QListWidget):
    def __init__(self, parent=None, extended_selection=False):
        super().__init__()
        self.parent = parent
        self.widgets = set()
        self.metrics = QFontMetrics(self.font())
        self.subversion_indent = 0

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

    def resize(self, widget):
        if hasattr(widget, 'subversionLabel'):
            text = widget.subversionLabel.text()
            indent = int((80 - self.metrics.width(text)) * 0.5)

            if self.subversion_indent != indent:
                self.subversion_indent = indent

                for widget in self.widgets:
                    if hasattr(widget, 'subversionLabel'):
                        widget.subversionLabel.setIndent(
                            self.subversion_indent)
            else:
                widget.subversionLabel.setIndent(self.subversion_indent)

    def _clear(self):
        self.clear()
        self.widgets.clear()
        self.count_changed()
