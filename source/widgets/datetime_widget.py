from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton


class DateTimeWidget(QPushButton):
    def __init__(self, datetime, build_hash):
        super().__init__()
        self.setFixedWidth(120)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        datetime_parts = datetime.rsplit('-', 1)
        date_parts = datetime_parts[0].rsplit('-')

        self.DayLabel = QLabel(date_parts[0])
        self.MonthLabel = QLabel(date_parts[1])
        self.MonthLabel.setFixedWidth(32)
        self.MonthLabel.setAlignment(Qt.AlignCenter)
        self.YearLabel = QLabel(date_parts[2] + ", ")
        self.TimeLabel = QLabel(datetime_parts[1])

        self.BuildHashLabel = QLabel(build_hash)
        self.BuildHashLabel.hide()

        self.layout.addStretch()
        self.layout.addWidget(self.DayLabel)
        self.layout.addWidget(self.MonthLabel)
        self.layout.addWidget(self.YearLabel)
        self.layout.addWidget(self.TimeLabel)
        self.layout.addWidget(self.BuildHashLabel)
        self.layout.addStretch()

        self.setCursor(Qt.PointingHandCursor)
        self.setToolTip("Press to show build hash number")
        self.clicked.connect(self.toggle_visibility)

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
