"""
Water Treatment detail screen.
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from screens.base_screen import BaseScreen
import config


ICON_PATHS = {
    # Paste local image paths here. Relative paths are resolved from the project root.
    # Example: "images/icons/water_treatment/feed_water.png"
    "feed_water": "",
    "water_quality": "",
    "treatment_status": "",
    "hydrogen_demand": "",
    "buffer_level": "",
    "next_process": "",
}


class WaterTreatmentScreen(BaseScreen):
    """Compact water treatment process screen."""

    def __init__(self, state_manager, navigation, parent=None):
        super().__init__(state_manager, navigation, parent)
        self.setup_ui()

    def setup_ui(self):
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        container = QWidget()
        container.setStyleSheet("background-color: #f6f7f9;")
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(24, 22, 24, 24)
        main_layout.setSpacing(20)

        top_row = QHBoxLayout()
        title = QLabel("Water Treatment")
        title.setStyleSheet("""
            color: #1f2937;
            font-size: 24pt;
            font-weight: 900;
            background-color: transparent;
            border: none;
        """)
        top_row.addWidget(title)
        top_row.addStretch()

        back_button = QPushButton("Back to Electrolysis")
        back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        back_button.clicked.connect(lambda: self.navigation.navigate_to("electrolysis"))
        back_button.setStyleSheet(f"""
            QPushButton {{
                background-color: #ffffff;
                border: 1px solid #b8c2cc;
                border-radius: 6px;
                color: {config.TEXT_PRIMARY};
                font-weight: 800;
                padding: 8px 14px;
            }}
            QPushButton:hover {{
                background-color: #edf4fb;
            }}
        """)
        top_row.addWidget(back_button)
        main_layout.addLayout(top_row)

        grid = QGridLayout()
        grid.setSpacing(18)
        grid.addWidget(self._metric_card("FEED WATER", "437 m³/h", "Available for electrolysis", "H₂O", ICON_PATHS["feed_water"]), 0, 0)
        grid.addWidget(self._metric_card("WATER QUALITY", "Deionized", "Conductivity controlled", "DI", ICON_PATHS["water_quality"]), 0, 1)
        grid.addWidget(self._metric_card("TREATMENT STATUS", "RUNNING", "Filtration and polishing active", "OK", ICON_PATHS["treatment_status"]), 0, 2)
        grid.addWidget(self._metric_card("HYDROGEN DEMAND BASIS", "1,050 t/day H₂", "10 L water per kg H₂", "H₂", ICON_PATHS["hydrogen_demand"]), 1, 0)
        grid.addWidget(self._metric_card("BUFFER LEVEL", "Normal", "Stable feed-water supply", "BUF", ICON_PATHS["buffer_level"]), 1, 1)
        grid.addWidget(self._metric_card("NEXT PROCESS", "Electrolyzer", "Feed water to electrolysis stacks", "EL", ICON_PATHS["next_process"]), 1, 2)
        main_layout.addLayout(grid, 1)

        self.layout.addWidget(container, 1)

    def _metric_card(self, title, value, subtitle, placeholder, icon_path=""):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid #d7dce3;
                border-radius: 8px;
            }
            QLabel {
                background-color: transparent;
                border: none;
            }
        """)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(10)

        title_label = QLabel(title)
        title_label.setStyleSheet("""
            color: #1f2937;
            font-size: 12pt;
            font-weight: 900;
        """)
        layout.addWidget(title_label)

        icon = QLabel(placeholder)
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setMinimumHeight(72)
        icon.setStyleSheet("""
            color: #4b5563;
            font-size: 24pt;
            font-weight: 900;
            border: 1px dashed #9ca3af;
            border-radius: 7px;
            background-color: #fbfcfe;
        """)
        self._set_icon(icon, icon_path)
        layout.addWidget(icon)

        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            color: {config.PRIMARY_COLOR};
            font-size: 20pt;
            font-weight: 900;
        """)
        layout.addWidget(value_label)

        subtitle_label = QLabel(subtitle)
        subtitle_label.setWordWrap(True)
        subtitle_label.setStyleSheet("""
            color: #6b7280;
            font-size: 10pt;
            font-weight: 600;
        """)
        layout.addWidget(subtitle_label)
        layout.addStretch()
        return card

    def _set_icon(self, label, icon_path):
        if not icon_path:
            return

        pixmap = QPixmap(icon_path)
        if pixmap.isNull():
            return

        label.setText("")
        label.setPixmap(
            pixmap.scaled(
                96,
                72,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        label.setStyleSheet("""
            border: 1px dashed #9ca3af;
            border-radius: 7px;
            background-color: #fbfcfe;
        """)
