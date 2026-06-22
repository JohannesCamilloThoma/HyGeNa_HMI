"""
Base Screen - Basis-Klasse für alle Screens.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout
from core.state_manager import StateManager
from core.navigation import Navigation


class BaseScreen(QWidget):
    """
    Basis-Klasse für alle HMI-Screens.
    Stellt gemeinsame Funktionalität bereit.
    """

    def __init__(self, state_manager: StateManager, navigation: Navigation, parent=None):
        super().__init__(parent)
        
        self.state_manager = state_manager
        self.navigation = navigation
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        
        # Subclasses können auf diese verbinden
        state_manager.state_changed.connect(self._on_state_changed)

    def _on_state_changed(self):
        """
        Wird aufgerufen, wenn sich der Systemzustand ändert.
        Kann in Subclasses überschrieben werden.
        """
        pass

    def setup_ui(self):
        """
        Setup-Methode für UI-Komponenten.
        Sollte von Subclasses überschrieben werden.
        """
        pass
