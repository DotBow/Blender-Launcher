from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton


class BuildStateWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 4, 0)
        self.layout.setSpacing(0)

        self.widgetFake = QPushButton()
        self.widgetFake.setProperty("Icon", True)
        self.widgetFake.setFixedSize(24, 24)
        self.widgetFake.setEnabled(False)

        self.countButton = QPushButton("0")
        self.countButton.setProperty("Count", True)
        self.countButton.setFixedSize(24, 24)
        self.countButton.setEnabled(False)
        self.countButton.hide()

        self.widgetFavorite = QPushButton()
        self.widgetFavorite.setProperty("Icon", True)
        self.widgetFavorite.setFixedSize(24, 24)
        self.widgetFavorite.setEnabled(False)
        self.widgetFavorite.setIcon(self.parent.icon_fake)
        self.widgetFavorite.hide()

        self.layout.addWidget(self.widgetFake)
        self.layout.addWidget(self.countButton)
        self.layout.addWidget(self.widgetFavorite)

    def setCount(self, count):
        if count > 0:
            self.countButton.setText(str(count))
            self.widgetFake.hide()
            self.countButton.show()
        else:
            self.countButton.hide()
            self.widgetFake.show()
