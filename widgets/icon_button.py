"""
Icon Button - Spezialisierter Button für Sidebar-Icons.
"""

from PySide6.QtWidgets import QPushButton, QSizePolicy
from PySide6.QtCore import Qt, QSize


class IconButton(QPushButton):
    """
    Spezialisierter Button mit technischem Icon für die Sidebar.
    """

    def __init__(self, icon, tooltip: str = "", parent=None):
        super().__init__(parent)

        self.setIcon(icon)
        self.setIconSize(QSize(30, 30))
        self.setToolTip(tooltip)

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.setFixedHeight(72)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

        self.set_active(False)

    def set_active(self, active: bool):
        if active:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #3a4655;
                    border: none;
                    border-left: 5px solid #00bcd4;
                    border-radius: 0px;
                    padding: 0px;
                }

                QPushButton:hover {
                    background-color: #435266;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #2f3a46;
                    border: none;
                    border-left: 5px solid transparent;
                    border-radius: 0px;
                    padding: 0px;
                }

                QPushButton:hover {
                    background-color: #3a4655;
                }
            """)