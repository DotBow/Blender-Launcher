from PyQt5.QtWidgets import QHBoxLayout, QWidget


class TabWidget(QWidget):
    def __init__(self, parent, label="New Tab"):
        super().__init__()

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        parent.addTab(self, label)
