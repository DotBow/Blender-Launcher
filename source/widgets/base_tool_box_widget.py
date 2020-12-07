from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QToolBox


class BaseToolBoxWidget(QToolBox):
    def __init__(self, parent=None):
        super().__init__()
        self.pages = []
        self.parent = parent
        self.list_widgets = set()

        self.setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self.currentChanged.connect(self.current_changed)

    def add_page_widget(self, page_widget, page_name):
        self.pages.append(page_widget)
        self.addItem(page_widget, QIcon(
            ":resources/icons/page_closed.svg"), page_name)
        self.list_widgets.add(page_widget.list_widget)
        return page_widget.list_widget

    def current_changed(self, index):
        icon_page_opened = QIcon(":resources/icons/page_opened.svg")
        icon_page_closed = QIcon(":resources/icons/page_closed.svg")

        for i in range(self.count()):
            if i != index:
                self.setItemIcon(i, icon_page_closed)

        self.setItemIcon(index, icon_page_opened)
