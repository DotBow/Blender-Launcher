from PyQt5.QtWidgets import QHBoxLayout, QWidget


class TabWidget(QWidget):
    def __init__(self, parent, label="New Tab"):
        super().__init__()

        layout = QHBoxLayout()
        layout.setContentsMargins(6, 6, 6, 6)
        self.setLayout(layout)
        parent.addTab(self, label)

    def _add_widget(self, widget):
        self.layout().addWidget(widget)
