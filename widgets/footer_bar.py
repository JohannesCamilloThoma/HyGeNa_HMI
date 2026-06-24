"""
Footer Bar Widget - Untere Leiste mit Systemstatus und STOP-Button.
"""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal
import config


class FooterBar(QWidget):
    """
    Footer-Bar mit Statusbereich und STOP-Button.
    """

    stop_pressed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(config.HEADER_FOOTER_HEIGHT)
        self.setStyleSheet(f"""
            background-color: #ffffff;
            border-top: 1px solid #ecf0f1;
        """)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 0, 15, 0)
        layout.setSpacing(15)
        
        # === Status Text (Links) ===
        self.status_text = QLabel("No active alarms")
        self.status_text.setStyleSheet(f"""
            font-size: {config.FONT_SIZE_BODY}pt;
            color: {config.TEXT_SECONDARY};
        """)
        layout.addWidget(self.status_text)
        
        # === Spacer ===
        layout.addStretch()
        
        # === STOP Button (Rechts) ===
        self.stop_button = QPushButton("STOP")
        self.stop_button.setFixedSize(120, 50)
        self.stop_button.setCursor(Qt.PointingHandCursor)
        self.stop_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {config.DANGER_COLOR};
                color: white;
                border: none;
                border-radius: 5px;
                font-size: {config.FONT_SIZE_BODY}pt;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #c0392b;
            }}
            QPushButton:pressed {{
                background-color: #a93226;
            }}
        """)
        self.stop_button.clicked.connect(self._on_stop_clicked)
        layout.addWidget(self.stop_button)
        
        self.setLayout(layout)

    def _on_stop_clicked(self):
        """Handler für STOP-Button."""
        self.stop_pressed.emit()

    def set_status_text(self, text: str):
        """Setzt den Statustext."""
        self.status_text.setText(text)

    def set_stop_button_enabled(self, enabled: bool):
        """Aktiviert/Deaktiviert den STOP-Button."""
        self.stop_button.setEnabled(enabled)
