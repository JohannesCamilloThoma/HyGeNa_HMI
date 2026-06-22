"""
Header Bar Widget - Obere Leiste mit Systeminformationen.
"""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap
from datetime import datetime
import config


class HeaderBar(QWidget):
    """
    Header-Bar mit Systeminformationen, Uhrzeit und Logo.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedHeight(config.HEADER_FOOTER_HEIGHT)
        self.setStyleSheet("""
            background-color: #ffffff;
            border-bottom: 1px solid #ecf0f1;
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 0, 24, 0)
        layout.setSpacing(28)

        # === Screen Title (Links) ===
        self.screen_title = QLabel("Übersicht")
        self.screen_title.setMinimumWidth(260)
        self.screen_title.setStyleSheet("""
            background-color: transparent;
            font-size: 34pt;
            font-weight: 800;
            color: #1f2937;
        """)
        layout.addWidget(self.screen_title)

        layout.addStretch(1)

        # === Date and Time ===
        self.datetime_label = QLabel()
        self.datetime_label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        self.datetime_label.setStyleSheet("""
            background-color: transparent;
            font-size: 14pt;
            font-weight: 500;
            color: #4b5563;
        """)
        layout.addWidget(self.datetime_label)

        # === System Status ===
        self.status_label = QLabel("Anlage: Gestoppt")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        self.status_label.setMinimumWidth(180)
        self.status_label.setStyleSheet("""
            background-color: transparent;
            font-size: 14pt;
            font-weight: 600;
            color: #4b5563;
        """)
        layout.addWidget(self.status_label)

        # === Logo Area ===
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_label.setMinimumWidth(230)
        self.logo_label.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Expanding
        )
        self.logo_label.setStyleSheet("""
            background-color: transparent;
            border-left: 1px solid #ecf0f1;
            padding-left: 24px;
        """)

        self.set_logo_image("images/Hygena_logo.png", width=250, height=100)
        layout.addWidget(self.logo_label)

        # === Timer für Uhrzeit-Update ===
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_datetime)
        self.timer.start(1000)
        self._update_datetime()

    def _update_datetime(self):
        now = datetime.now()
        self.datetime_label.setText(now.strftime("%d.%m.%Y  %H:%M:%S"))

    def set_screen_title(self, title: str):
        self.screen_title.setText(title)

    def set_system_status(self, status: str):
        self.status_label.setText(f"Anlage: {status}")

    def set_logo_image(self, image_path: str, width: int = 220, height: int = 70):
        pixmap = QPixmap(image_path)

        if pixmap.isNull():
            self.logo_label.setText("HYGENA")
            self.logo_label.setStyleSheet("""
                background-color: transparent;
                border-left: 1px solid #ecf0f1;
                padding-left: 24px;
                font-size: 22pt;
                font-weight: 800;
                color: #1f2937;
            """)
            return

        scaled_pixmap = pixmap.scaled(
            width,
            height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        self.logo_label.setPixmap(scaled_pixmap)

    def set_logo_text(self, text: str):
        self.logo_label.clear()
        self.logo_label.setText(text)