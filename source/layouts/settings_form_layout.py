from PyQt5.QtWidgets import QFormLayout, QLabel


class SettingsFormLayout(QFormLayout):
    def __init__(self, label_width):
        super().__init__()

        self.setContentsMargins(6, 0, 6, 0)
        self.setSpacing(6)
        self.label_width = label_width

    def _addRow(self, label_text, widget):
        label = QLabel(label_text)
        label.setFixedWidth(self.label_width)
        self.addRow(label, widget)
