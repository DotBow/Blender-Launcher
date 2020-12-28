from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget


class DateTimeWidget(QWidget):
    def __init__(self, datetime):
        super(DateTimeWidget, self).__init__(None)
        self.setFixedWidth(105)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        datetime_parts = datetime.rsplit('-', 1)
        date_parts = datetime_parts[0].rsplit('-')

        DayLabel = QLabel(date_parts[0])
        MonthLabel = QLabel(date_parts[1])
        MonthLabel.setFixedWidth(32)
        MonthLabel.setAlignment(Qt.AlignCenter)
        YearLabel = QLabel(date_parts[2] + ", ")
        TimeLabel = QLabel(datetime_parts[1])

        self.layout.addWidget(DayLabel)
        self.layout.addWidget(MonthLabel)
        self.layout.addWidget(YearLabel)
        self.layout.addWidget(TimeLabel)
