from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QWidget


class BuildStateWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 4, 0)
        self.layout.setSpacing(0)

        self.widgetFake = self.IconButton()

        self.countButton = self.IconButton(text="0", prop="Count")
        self.countButton.hide()

        self.widgetFavorite = self.IconButton(self.parent.icon_fake)
        self.widgetFavorite.hide()

        self.layout.addWidget(self.widgetFake)
        self.layout.addWidget(self.countButton)
        self.layout.addWidget(self.widgetFavorite)

    def IconButton(self, icon=None, text="", prop="Icon"):
        button = QPushButton(text)

        if icon is not None:
            button.setIcon(icon)

        button.setProperty(prop, True)
        button.setFixedSize(24, 24)
        button.setEnabled(False)
        return button

    def setCount(self, count):
        if count > 0:
            self.countButton.setText(str(count))
            self.widgetFake.hide()
            self.countButton.show()
        else:
            self.countButton.hide()
            self.widgetFake.show()
