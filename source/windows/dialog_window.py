from enum import Enum

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QMainWindow, QPushButton
from ui.dialog_window_ui import Ui_DialogWindow

from windows.base_window import BaseWindow

from darkdetect import isLight

class DialogIcon(Enum):
    WARNING = 1
    INFO = 2


class DialogWindow(QMainWindow, BaseWindow, Ui_DialogWindow):
    accepted = pyqtSignal()
    cancelled = pyqtSignal()

    def __init__(self, parent, title="Warning", text="Dialog Window",
                 accept_text="Accept", cancel_text="Cancel",
                 icon=DialogIcon.WARNING):
        super(DialogWindow, self).__init__(parent=parent)

        self.setupUi(self)
        self.setWindowTitle(title)

        self.IconLabel = QLabel()
        self.IconLabel.setScaledContents(True)
        self.IconLabel.setFixedSize(48, 48)

        if icon == DialogIcon.WARNING:
            if isLight():
                self.IconLabel.setPixmap(
                    QPixmap(":resources/icons/black/exclamation.svg"))
            else:
                self.IconLabel.setPixmap(
                    QPixmap(":resources/icons/white/exclamation.svg"))
        elif icon == DialogIcon.INFO:
            if isLight():
                self.IconLabel.setPixmap(QPixmap(":resources/icons/black/info.svg"))
            else:
                self.IconLabel.setPixmap(QPixmap(":resources/icons/white/info.svg"))

        self.TextLabel = QLabel(text)
        self.TextLabel.setTextFormat(Qt.RichText)
        self.TextLabel.setTextInteractionFlags(Qt.NoTextInteraction)
        self.AcceptButton = QPushButton(accept_text)
        self.CancelButton = QPushButton(cancel_text)

        self.TextLayout = QHBoxLayout()
        self.TextLayout.setContentsMargins(4, 4, 6, 0)
        self.ButtonsLayout = QHBoxLayout()
        self.ButtonsLayout.setContentsMargins(0, 0, 0, 0)

        if cancel_text is None:
            self.CancelButton.hide()
        else:
            self.CancelButton.setText(cancel_text)

        if self.AcceptButton.sizeHint().width() > self.CancelButton.sizeHint().width():
            width = self.AcceptButton.sizeHint().width()
        else:
            width = self.CancelButton.sizeHint().width()

        self.AcceptButton.setFixedWidth(width + 16)
        self.CancelButton.setFixedWidth(width + 16)

        self.AcceptButton.clicked.connect(self.accept)
        self.CancelButton.clicked.connect(self.cancel)

        self.TextLayout.addWidget(self.IconLabel)
        self.TextLayout.addSpacing(12)
        self.TextLayout.addWidget(self.TextLabel)
        self.ButtonsLayout.addWidget(
            self.AcceptButton, alignment=Qt.AlignRight, stretch=1)
        self.ButtonsLayout.addWidget(self.CancelButton)

        self.CentralLayout.addLayout(self.TextLayout)
        self.CentralLayout.addLayout(self.ButtonsLayout)

        self.show()

    def accept(self):
        self.accepted.emit()
        self.close()

    def cancel(self):
        self.cancelled.emit()
        self.close()
