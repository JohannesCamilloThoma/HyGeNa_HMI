"""
Sidebar Widget - Linke Navigationsleiste mit technischen Icons.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap

from widgets.icon_button import IconButton
import qtawesome as qta
import config


class Sidebar(QWidget):
    """
    Vertikale Sidebar mit Navigations-Icons auf der linken Seite.
    """

    screen_selected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedWidth(config.SIDEBAR_WIDTH)
        self.setStyleSheet("""
            background-color: #2c3542;
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # === Profile Avatar ===
        profile_label = QLabel()
        profile_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        profile_label.setFixedHeight(105)

        pixmap = QPixmap("resources/images/profilbild.png")

        if not pixmap.isNull():
            pixmap = pixmap.scaled(
                72,
                72,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            profile_label.setPixmap(pixmap)
        else:
            profile_label.setText("👤")
            profile_label.setStyleSheet("""
                color: #d5dce3;
                font-size: 34px;
            """)

        layout.addWidget(profile_label)

        # === Separator ===
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFixedHeight(1)
        separator.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.18);
            border: none;
        """)
        layout.addWidget(separator)

        # Abstand nach Profilbereich
        layout.addSpacing(18)

        # === Navigation Buttons ===
        self.buttons = {}

        icon_color = "#f5f5f5"

        menu_items = [
            ("home", qta.icon("mdi.home-outline", color=icon_color), "Overview"),
            ("alarms", qta.icon("mdi.bell-outline", color=icon_color), "Alarms"),
            ("monitoring", qta.icon("mdi.chart-line", color=icon_color), "Monitoring"),
            ("maintenance", qta.icon("mdi.wrench-outline", color=icon_color), "Maintenance"),
            ("settings", qta.icon("mdi.cog-outline", color=icon_color), "Settings"),
        ]

        for index, (screen_id, icon, tooltip) in enumerate(menu_items):
            btn = IconButton(icon, tooltip)

            btn.clicked.connect(
                lambda checked=False, sid=screen_id: self._on_button_clicked(sid)
            )

            layout.addWidget(btn)
            self.buttons[screen_id] = btn

            if index < len(menu_items) - 1:
                layout.addStretch(1)

        layout.addStretch(1)

        self.setLayout(layout)

        self.set_active_screen("home")

    def _on_button_clicked(self, screen_id: str):
        self.set_active_screen(screen_id)
        self.screen_selected.emit(screen_id)

    def set_active_screen(self, screen_id: str):
        for bid, btn in self.buttons.items():
            btn.set_active(bid == screen_id)
