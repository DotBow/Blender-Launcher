from PyQt5.QtWidgets import QAbstractItemView, QListWidget


class BaseListWidget(QListWidget):
    def __init__(self, parent=None, extended_selection=False):
        super().__init__()
        self.parent = parent
        self.widgets = set()

        self.setFrameShape(QListWidget.NoFrame)
        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)
        self.setProperty("HideBorder", True)

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

    def resize_labels(self, params):
        items = []

        for i in range(self.count()):
            item = self.itemWidget(self.item(i))

            if hasattr(item, 'subversionLabel'):
                items.append(item)

        for param in params:
            widths = [getattr(item, param).minimumSizeHint().width()
                      for item in items]
            widths.append(
                getattr(self.parent, param).minimumSizeHint().width())
            max_width = max(widths)

            for item in items:
                getattr(item, param).setFixedWidth(max_width)

            getattr(self.parent, param).setFixedWidth(max_width)

        if hasattr(item, 'launchButton'):
            b_width = getattr(item, 'launchButton').minimumWidth()
        else:
            b_width = getattr(item, 'downloadButton').minimumWidth()

        getattr(self.parent, 'fakeLabel').setMinimumWidth(b_width)
