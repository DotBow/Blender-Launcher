from PyQt5.QtWidgets import QFormLayout, QLabel


class SettingsFormLayoutRow():
    def __init__(self, label, widget):
        super().__init__()
        self.label = label
        self.widget = widget

    def setEnabled(self, enabled=True):
        self.label.setEnabled(enabled)
        self.widget.setEnabled(enabled)


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

        return SettingsFormLayoutRow(label, widget)
