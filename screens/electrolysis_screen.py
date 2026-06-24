"""
Electrolysis overview screen.
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from screens.base_screen import BaseScreen
import config


ICON_PATHS = {
    # Paste local image paths here. Relative paths are resolved from the project root.
    # Example: "images/icons/electrolysis/water.png"
    "water": "images/icons/wasser.png",
    "electrical_energy": "images/icons/01_Energie.png",
    "electrolyzer": "images/icons/02_Elektrolyse.png",
    "membrane": "images/icons/membran.png",
    "products": "images/icons/Produkt.png",
}


class ElectrolysisProcessCard(QFrame):
    """Large process card used in the electrolysis flow."""

    clicked = Signal(str)

    def __init__(self, title, subtitle, placeholder, status, values, icon_path="", page_key=None, parent=None):
        super().__init__(parent)
        self.page_key = page_key
        self.setCursor(Qt.CursorShape.PointingHandCursor if page_key else Qt.CursorShape.ArrowCursor)
        self.setMinimumSize(180, 330)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setStyleSheet("""
            ElectrolysisProcessCard {
                background-color: #ffffff;
                border: 1px solid #d7dce3;
                border-radius: 8px;
            }
            QLabel {
                background-color: transparent;
                border: none;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 18, 16, 14)
        layout.setSpacing(8)

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setWordWrap(True)
        title_label.setStyleSheet("""
            color: #1f2937;
            font-size: 13pt;
            font-weight: 900;
        """)
        layout.addWidget(title_label)

        subtitle_label = QLabel(subtitle)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setWordWrap(True)
        subtitle_label.setStyleSheet("""
            color: #4b5563;
            font-size: 11pt;
            font-weight: 500;
        """)
        layout.addWidget(subtitle_label)

        layout.addStretch(1)

        icon_area = QLabel(placeholder)
        icon_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_area.setMinimumHeight(130)
        icon_area.setStyleSheet("""
            color: #111827;
            font-size: 30pt;
            font-weight: 900;
            border: 1px dashed #9ca3af;
            border-radius: 8px;
            background-color: #fbfcfe;
        """)
        self._set_icon(icon_area, icon_path)
        layout.addWidget(icon_area)

        layout.addStretch(1)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #e5e7eb; border: none;")
        layout.addWidget(separator)

        status_row = QHBoxLayout()
        status_row.setContentsMargins(0, 4, 0, 0)
        status_row.setSpacing(8)

        dot = QLabel()
        dot.setFixedSize(10, 10)
        dot.setStyleSheet("background-color: #2eaa38; border-radius: 5px;")
        status_row.addWidget(dot)

        status_label = QLabel(status)
        status_label.setStyleSheet("""
            color: #2e7d32;
            font-size: 10pt;
            font-weight: 900;
        """)
        status_row.addWidget(status_label)
        status_row.addStretch()
        layout.addLayout(status_row)

        for value in values:
            value_label = QLabel(value)
            value_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            value_label.setStyleSheet("""
                color: #111827;
                font-size: 11pt;
                font-weight: 800;
            """)
            layout.addWidget(value_label)

    def mousePressEvent(self, event):
        if self.page_key and event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.page_key)
        super().mousePressEvent(event)

    def _set_icon(self, label, icon_path):
        if not icon_path:
            return

        pixmap = QPixmap(icon_path)
        if pixmap.isNull():
            return

        label.setText("")
        label.setPixmap(
            pixmap.scaled(
                120,
                120,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        label.setStyleSheet("""
            border: 1px dashed #9ca3af;
            border-radius: 8px;
            background-color: #fbfcfe;
        """)


class FlowArrow(QLabel):
    """Simple right-facing process arrow."""

    def __init__(self, parent=None):
        super().__init__("→", parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedWidth(36)
        self.setStyleSheet("""
            color: #374151;
            font-size: 32pt;
            font-weight: 700;
            background-color: transparent;
            border: none;
        """)


class ElectrolysisScreen(BaseScreen):
    """High-level electrolysis process overview."""

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
        main_layout.setSpacing(22)

        top_row = QHBoxLayout()
        title = QLabel("Electrolysis Overview")
        title.setStyleSheet("""
            color: #1f2937;
            font-size: 24pt;
            font-weight: 900;
            background-color: transparent;
            border: none;
        """)
        top_row.addWidget(title)
        top_row.addStretch()

        back_button = QPushButton("Back to Overview")
        back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        back_button.clicked.connect(lambda: self.navigation.navigate_to("home"))
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

        flow_row = QHBoxLayout()
        flow_row.setSpacing(10)

        cards = [
            ElectrolysisProcessCard(
                "WATER (H₂O)",
                "Feed water",
                "H₂O",
                "AVAILABLE",
                ["437 m³/h"],
                icon_path=ICON_PATHS["water"],
                page_key="water_treatment",
            ),
            ElectrolysisProcessCard(
                "ELECTRICAL ENERGY",
                "Renewable sources",
                "☀ / W",
                "AVAILABLE",
                ["14.0 GW"],
                icon_path=ICON_PATHS["electrical_energy"],
            ),
            ElectrolysisProcessCard(
                "ELECTROLYZER",
                "Anode | Cathode",
                "EL",
                "RUNNING",
                ["1,050 t/day H₂"],
                icon_path=ICON_PATHS["electrolyzer"],
            ),
            ElectrolysisProcessCard(
                "MEMBRANE",
                "Ion conductor",
                "H⁺",
                "RUNNING",
                ["Conductivity: High"],
                icon_path=ICON_PATHS["membrane"],
            ),
            ElectrolysisProcessCard(
                "PRODUCTS",
                "Hydrogen & Oxygen",
                "H₂ / O₂",
                "PRODUCTION",
                ["1,050 t/day H₂", "8,400 t/day O₂"],
                icon_path=ICON_PATHS["products"],
            ),
        ]

        for index, card in enumerate(cards):
            if card.page_key == "water_treatment":
                card.clicked.connect(lambda: self.navigation.navigate_to("water_treatment"))
            flow_row.addWidget(card, 1)
            if index < len(cards) - 1:
                flow_row.addWidget(FlowArrow())

        main_layout.addLayout(flow_row, 1)
        self.layout.addWidget(container, 1)
