from PyQt5.QtWidgets import QTabWidget


class BaseToolBoxWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.pages = []
        self.parent = parent
        self.list_widgets = set()

        self.setContentsMargins(0, 0, 0, 0)
        self.setTabPosition(QTabWidget.West)

    def add_page_widget(self, page_widget, page_name):
        self.pages.append(page_widget)
        self.addTab(page_widget, page_name)
        self.list_widgets.add(page_widget.list_widget)
        return page_widget.list_widget
