"""
Status Card Widget - Wiederverwendbares Card-Widget für Status-Anzeigen.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import config


class StatusCard(QWidget):
    """
    Wiederverwendbares Card-Widget für Statusanzeigen.
    Zeigt einen Titel, Icon/Wert und optional einen Untertitel.
    """

    def __init__(self, title: str, value: str = "", subtitle: str = "", icon: str = "", parent=None):
        super().__init__(parent)
        
        self.setStyleSheet(f"""
            QWidget {{
                background-color: #ffffff;
                border-radius: {config.CONTENT_CONTAINER_RADIUS}px;
                border: 1px solid #ecf0f1;
            }}
        """)
        
        self.setMinimumHeight(100)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # === Icon/Left Side ===
        if icon:
            icon_label = QLabel(icon)
            icon_label.setStyleSheet("font-size: 32px;")
            icon_label.setAlignment(Qt.AlignCenter)
            icon_label.setFixedWidth(60)
            layout.addWidget(icon_label)
        
        # === Right Side - Text Content ===
        text_layout = QVBoxLayout()
        text_layout.setSpacing(5)
        
        title_label = QLabel(title)
        title_font = QFont()
        title_font.setPointSize(config.FONT_SIZE_SMALL)
        title_font.setColor(config.TEXT_SECONDARY)
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {config.TEXT_SECONDARY};")
        text_layout.addWidget(title_label)
        
        if value:
            value_label = QLabel(value)
            value_font = QFont()
            value_font.setPointSize(config.FONT_SIZE_HEADER)
            value_font.setBold(True)
            value_label.setFont(value_font)
            value_label.setStyleSheet(f"color: {config.TEXT_PRIMARY};")
            text_layout.addWidget(value_label)
        
        if subtitle:
            subtitle_label = QLabel(subtitle)
            subtitle_font = QFont()
            subtitle_font.setPointSize(config.FONT_SIZE_SMALL - 1)
            subtitle_label.setFont(subtitle_font)
            subtitle_label.setStyleSheet(f"color: {config.TEXT_SECONDARY};")
            text_layout.addWidget(subtitle_label)
        
        layout.addLayout(text_layout)
        layout.addStretch()
        
        self.setLayout(layout)
        
        # Store references for dynamic updates
        self.value_label = value_label if value else None
        self.subtitle_label = subtitle_label if subtitle else None

    def set_value(self, value: str):
        """Aktualisiert den Wert."""
        if self.value_label:
            self.value_label.setText(value)

    def set_subtitle(self, subtitle: str):
        """Aktualisiert den Untertitel."""
        if self.subtitle_label:
            self.subtitle_label.setText(subtitle)
