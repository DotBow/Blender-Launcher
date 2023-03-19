from modules.settings import (favorite_pages, get_bash_arguments,
                              get_blender_startup_arguments,
                              get_enable_quick_launch_key_seq,
                              get_install_template,
                              get_launch_blender_no_console,
                              get_mark_as_favorite, get_platform,
                              get_quick_launch_key_seq, set_bash_arguments,
                              set_blender_startup_arguments,
                              set_enable_quick_launch_key_seq,
                              set_install_template,
                              set_launch_blender_no_console,
                              set_mark_as_favorite, set_quick_launch_key_seq)
from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QCheckBox, QComboBox, QHBoxLayout, QLineEdit
from widgets.settings_form_widget import SettingsFormWidget


class BlenderBuildsTabWidget(SettingsFormWidget):
    def __init__(self):
        super().__init__()

        # Mark As Favorite
        self.MarkAsFavorite = QComboBox()
        self.MarkAsFavorite.addItems(favorite_pages.keys())
        self.MarkAsFavorite.setCurrentIndex(
            get_mark_as_favorite())
        self.MarkAsFavorite.activated.connect(
            self.change_mark_as_favorite)

        # Blender Startup Arguments
        self.BlenderStartupArguments = QLineEdit()
        self.BlenderStartupArguments.setText(
            str(get_blender_startup_arguments()))
        self.BlenderStartupArguments.setContextMenuPolicy(
            Qt.ContextMenuPolicy.NoContextMenu)
        self.BlenderStartupArguments.setCursorPosition(0)
        self.BlenderStartupArguments.editingFinished.connect(
            self.update_blender_startup_arguments)

        # Command Line Arguments
        self.BashArguments = QLineEdit()
        self.BashArguments.setText(
            str(get_bash_arguments()))
        self.BashArguments.setContextMenuPolicy(
            Qt.ContextMenuPolicy.NoContextMenu)
        self.BashArguments.setCursorPosition(0)
        self.BashArguments.editingFinished.connect(
            self.update_bash_arguments)

        # Install Template
        self.InstallTemplate = QCheckBox()
        self.InstallTemplate.clicked.connect(self.toggle_install_template)
        self.InstallTemplate.setChecked(get_install_template())

        # Run Blender using blender-launcher.exe
        self.LaunchBlenderNoConsole = QCheckBox()
        self.LaunchBlenderNoConsole.clicked.connect(
            self.toggle_launch_blender_no_console)
        self.LaunchBlenderNoConsole.setChecked(get_launch_blender_no_console())

        # Quick Launch Key Sequence
        self.EnableQuickLaunchKeySeq = QCheckBox()
        self.EnableQuickLaunchKeySeq.clicked.connect(
            self.toggle_enable_quick_launch_key_seq)
        self.EnableQuickLaunchKeySeq.setChecked(
            get_enable_quick_launch_key_seq())

        self.QuickLaunchKeySeq = QLineEdit()
        self.QuickLaunchKeySeq.setEnabled(get_enable_quick_launch_key_seq())
        self.QuickLaunchKeySeq.keyPressEvent = self._keyPressEvent
        self.QuickLaunchKeySeq.setText(
            str(get_quick_launch_key_seq()))
        self.QuickLaunchKeySeq.setContextMenuPolicy(
            Qt.ContextMenuPolicy.NoContextMenu)
        self.QuickLaunchKeySeq.setCursorPosition(0)
        self.QuickLaunchKeySeq.editingFinished.connect(
            self.update_quick_launch_key_seq)

        # Layout
        self._addRow("Mark As Favorite", self.MarkAsFavorite)
        self._addRow("Install Template", self.InstallTemplate)

        sub_layout = QHBoxLayout()
        sub_layout.addWidget(self.EnableQuickLaunchKeySeq)
        sub_layout.addWidget(self.QuickLaunchKeySeq)
        self.QuickLaunchKeySeqRow = self._addRow(
            "Quick Launch Global Shortcut", sub_layout)

        if get_platform() == 'Windows':
            self._addRow("Hide Console On Startup",
                         self.LaunchBlenderNoConsole)

        self._addRow("Startup Arguments:",
                     self.BlenderStartupArguments, True)

        if get_platform() == 'Linux':
            self._addRow("Bash Arguments:", self.BashArguments, True)

    def change_mark_as_favorite(self, page):
        set_mark_as_favorite(page)

    def update_blender_startup_arguments(self):
        args = self.BlenderStartupArguments.text()
        set_blender_startup_arguments(args)

    def update_bash_arguments(self):
        args = self.BashArguments.text()
        set_bash_arguments(args)

    def toggle_install_template(self, is_checked):
        set_install_template(is_checked)

    def toggle_launch_blender_no_console(self, is_checked):
        set_launch_blender_no_console(is_checked)

    def update_quick_launch_key_seq(self):
        key_seq = self.QuickLaunchKeySeq.text()
        set_quick_launch_key_seq(key_seq)

    def toggle_enable_quick_launch_key_seq(self, is_checked):
        set_enable_quick_launch_key_seq(is_checked)
        self.QuickLaunchKeySeq.setEnabled(is_checked)

    def _keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        MOD_MASK = (Qt.CTRL | Qt.ALT | Qt.SHIFT)
        key_name = ''
        key = e.key()
        modifiers = int(e.modifiers())

        if (modifiers and modifiers & MOD_MASK == modifiers and
            key > 0 and key != Qt.Key_Shift and key != Qt.Key_Alt and
                key != Qt.Key_Control and key != Qt.Key_Meta):

            key_name = QtGui.QKeySequence(modifiers + key).toString()
        elif not modifiers and (key != Qt.Key_Meta):
            key_name = QtGui.QKeySequence(key).toString()

        if key_name != '':
            # Remap <Shift + *> keys sequences
            if 'Shift' in key_name:
                alt_chars = '~!@#$%^&*()_+|{}:"<>?'
                real_chars = r"`1234567890-=\[];',./"
                trans_table = str.maketrans(alt_chars, real_chars)
                trans = key_name[-1].translate(trans_table)
                key_name = key_name[:-1] + trans

            self.QuickLaunchKeySeq.setText(key_name.lower())

        return super().keyPressEvent(e)
