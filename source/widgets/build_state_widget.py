from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QWidget


class BuildStateWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 4, 0)
        self.layout.setSpacing(0)

        self.fakeIcon = self.IconButton()

        self.countIcon = self.IconButton(text="0", prop="Count")
        self.countIcon.hide()

        self.newBuildIcon = self.IconButton(self.parent.filled_circle)
        self.newBuildIcon.hide()

        self.layout.addWidget(self.fakeIcon)
        self.layout.addWidget(self.countIcon)
        self.layout.addWidget(self.newBuildIcon)

        self.active_icon = self.fakeIcon

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
            self.countIcon.setText(str(count))
            self.active_icon.hide()
            self.countIcon.show()
            self.active_icon = self.countIcon
        else:
            self.active_icon.hide()
            self.fakeIcon.show()
            self.active_icon = self.fakeIcon

    def setNewBuild(self, show=True):
        if show:
            self.active_icon.hide()
            self.newBuildIcon.show()
            self.active_icon = self.newBuildIcon
        else:
            self.active_icon.hide()
            self.fakeIcon.show()
            self.active_icon = self.fakeIcon
