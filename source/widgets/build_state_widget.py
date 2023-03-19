from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, QRect, QSize
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QWidget


class BuildStateWidget(QWidget):
    def __init__(self, parent, list_widget):
        super().__init__()
        self.parent = parent
        self.list_widget = list_widget
        self.anim = None

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 4, 0)
        self.layout.setSpacing(0)

        self.fakeIcon = self.IconButton()

        self.countIcon = self.IconButton(text="0", prop="Count")
        self.countIcon.hide()

        self.newBuildIcon = self.IconButton(self.parent.filled_circle)
        self.newBuildIcon.hide()

        self.downloadIcon = self.IconButton(self.parent.icon_download)
        self.downloadIcon.hide()

        self.extractIcon = self.IconButton(self.parent.icon_file)
        self.extractIcon.hide()

        self.layout.addWidget(self.fakeIcon)
        self.layout.addWidget(self.countIcon)
        self.layout.addWidget(self.newBuildIcon)
        self.layout.addWidget(self.downloadIcon)
        self.layout.addWidget(self.extractIcon)

        self.active_icon = self.fakeIcon

    def IconButton(self, icon=None, text="", prop="Icon"):
        button = QPushButton(text)

        if icon is not None:
            button.setIcon(icon)
            button.setIconSize(QSize(24, 24))

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

    def setDownload(self, show=True):
        if show:
            self.active_icon.hide()
            self.downloadIcon.show()
            self.active_icon = self.downloadIcon
            self.download_anim()
        else:
            self.active_icon.hide()
            self.fakeIcon.show()
            self.active_icon = self.fakeIcon

            if self.anim is not None:
                self.anim.deleteLater()
                self.anim = None

    def setExtract(self, show=True):
        if show:
            self.active_icon.hide()
            self.extractIcon.show()
            self.active_icon = self.extractIcon
            self.extract_anim()
        else:
            self.active_icon.hide()
            self.fakeIcon.show()
            self.active_icon = self.fakeIcon

            if self.anim is not None:
                self.anim.deleteLater()
                self.anim = None

    def download_anim(self):
        self.anim = QPropertyAnimation(self.downloadIcon, b"geometry")
        self.anim.setDuration(1000)
        self.anim.setLoopCount(-1)
        geometry = self.downloadIcon.geometry()
        self.anim.setStartValue(QRect(
            geometry.x(), geometry.y() - geometry.height(),
            geometry.width(), geometry.height()))
        self.anim.setEndValue(QRect(
            geometry.x(), geometry.height() * 1.25,
            geometry.width(), geometry.height()))

        self.start_anim()

    def extract_anim(self):
        self.anim = QPropertyAnimation(self.extractIcon, b"geometry")
        self.anim.setDuration(1000)
        self.anim.setLoopCount(-1)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        geometry = self.extractIcon.geometry()
        self.anim.setStartValue(QRect(
            geometry.x(), geometry.height() * 1.25,
            geometry.width(), geometry.height()))
        self.anim.setKeyValueAt(0.3, QRect(
            geometry.x(), geometry.y() + geometry.height() * 0.15,
            geometry.width(), geometry.height()))
        self.anim.setKeyValueAt(0.7, QRect(
            geometry.x(), geometry.y() + geometry.height() * 0.15,
            geometry.width(), geometry.height()))
        self.anim.setEndValue(QRect(
            geometry.x() + geometry.width() * 1.25,
            geometry.y() + geometry.height() * 0.15,
            geometry.width(), geometry.height()))

        self.start_anim()

    def start_anim(self):
        for widget in self.list_widget.widgets:
            build_state_widget = widget.build_state_widget

            if (build_state_widget.anim is not None) and \
                    (build_state_widget != self):
                self.anim.start()
                self.anim.setCurrentTime(build_state_widget.anim.currentTime())
                return

        self.anim.start()
