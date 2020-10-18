from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QToolBox

from widgets.base_page_widget import BasePageWidget


class BaseToolBoxWidget(QToolBox):
    def __init__(self, parent=None):
        super().__init__()
        self.pages = []

        self.setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self.currentChanged.connect(self.current_changed)

    def add_list_widget(self, name, custom_name, text,
                        _show_hash=True, extended_selection=False):
        page_widget = BasePageWidget(
            self, text, custom_name, show_hash=_show_hash,
            extended_selection=extended_selection)
        self.pages.append(page_widget)
        self.addItem(page_widget, QIcon(
            ":resources/icons/page_closed.svg"), name)

        return page_widget.list_widget

    def current_changed(self, index):
        icon_page_opened = QIcon(":resources/icons/page_opened.svg")
        icon_page_closed = QIcon(":resources/icons/page_closed.svg")

        for i in range(self.count()):
            if i != index:
                self.setItemIcon(i, icon_page_closed)

        self.setItemIcon(index, icon_page_opened)
