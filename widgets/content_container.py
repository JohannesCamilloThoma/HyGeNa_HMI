"""
Content Container Widget - Hauptbereich für Screen-Inhalte.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import config


class ContentContainer(QWidget):
    """
    Dynamischer Content-Container für Screens.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            background-color: {config.CONTENT_AREA_BG_COLOR};
            border: none;
        """)
        
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(0)
        
        # === Content Frame ===
        self.content_frame = QFrame()
        self.content_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {config.CONTENT_CONTAINER_BG_COLOR};
                border-radius: {config.CONTENT_CONTAINER_RADIUS}px;
                border: 1px solid #dfe6e9;
            }}
        """)
        
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(config.CONTENT_CONTAINER_PADDING, config.CONTENT_CONTAINER_PADDING, config.CONTENT_CONTAINER_PADDING, config.CONTENT_CONTAINER_PADDING)
        self.content_frame.setLayout(self.content_layout)
        
        self.main_layout.addWidget(self.content_frame)
        self.setLayout(self.main_layout)
        
        self._current_screen_widget = None

    def set_screen_widget(self, screen_widget: QWidget):
        """
        Setzt einen neuen Screen-Widget.
        Entfernt den alten und fügt den neuen ein.
        """
        # Entferne ALLE Layout-Items (Widgets UND Stretches/Spacings)
        while self.content_layout.count() > 0:
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Füge neuen Content ein
        self._current_screen_widget = screen_widget
        self.content_layout.addWidget(screen_widget)
        self.content_layout.addStretch()

    def clear(self):
        """Löscht den aktuellen Content."""
        if self._current_screen_widget is not None:
            self.content_layout.removeWidget(self._current_screen_widget)
            self._current_screen_widget.deleteLater()
            self._current_screen_widget = None
