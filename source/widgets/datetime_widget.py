from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton


class DateTimeWidget(QPushButton):
    def __init__(self, datetime, build_hash):
        super().__init__()
        self.build_hash = build_hash

        self.setFixedWidth(120)
        self.setProperty("TextOnly", True)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        datetime_parts = datetime.rsplit('-', 1)
        date_parts = datetime_parts[0].rsplit('-')

        self.DayLabel = QLabel(date_parts[0])
        self.MonthLabel = QLabel(date_parts[1])
        self.MonthLabel.setFixedWidth(32)
        self.MonthLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.YearLabel = QLabel(date_parts[2] + ", ")
        self.TimeLabel = QLabel(datetime_parts[1])

        if self.build_hash is not None:
            self.LeftArrowLabel = QLabel("◂")
            self.LeftArrowLabel.setVisible(False)
            self.RightArrowLabel = QLabel("▸")
            self.RightArrowLabel.setVisible(False)

            self.BuildHashLabel = QLabel(self.build_hash)
            self.BuildHashLabel.hide()

            self.layout.addWidget(self.LeftArrowLabel)
            self.layout.addStretch()
            self.layout.addWidget(self.DayLabel)
            self.layout.addWidget(self.MonthLabel)
            self.layout.addWidget(self.YearLabel)
            self.layout.addWidget(self.TimeLabel)
            self.layout.addWidget(self.BuildHashLabel)
            self.layout.addStretch()
            self.layout.addWidget(self.RightArrowLabel)

            self.setCursor(Qt.CursorShape.PointingHandCursor)
            self.setToolTip("Press to show build hash number")
            self.clicked.connect(self.toggle_visibility)
        else:
            self.layout.addStretch()
            self.layout.addWidget(self.DayLabel)
            self.layout.addWidget(self.MonthLabel)
            self.layout.addWidget(self.YearLabel)
            self.layout.addWidget(self.TimeLabel)
            self.layout.addStretch()

    def toggle_visibility(self):
        self.DayLabel.setVisible(not self.DayLabel.isVisible())
        self.MonthLabel.setVisible(not self.MonthLabel.isVisible())
        self.YearLabel.setVisible(not self.YearLabel.isVisible())
        self.TimeLabel.setVisible(not self.TimeLabel.isVisible())
        self.BuildHashLabel.setVisible(not self.BuildHashLabel.isVisible())

        if self.BuildHashLabel.isVisible():
            self.setToolTip("Press to show date and time")
        else:
            self.setToolTip("Press to show build hash number")

    def enterEvent(self, event: QtCore.QEvent) -> None:
        if self.build_hash is not None:
            self.LeftArrowLabel.setVisible(True)
            self.RightArrowLabel.setVisible(True)

        return super().enterEvent(event)

    def leaveEvent(self, event: QtCore.QEvent) -> None:
        if self.build_hash is not None:
            self.LeftArrowLabel.setVisible(False)
            self.RightArrowLabel.setVisible(False)

        return super().leaveEvent(event)
