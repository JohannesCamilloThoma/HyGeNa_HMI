"""
Navigation Manager - Verwaltung der Screen-Navigation.
"""

from PySide6.QtCore import QObject, Signal
from typing import Dict, Type


class Navigation(QObject):
    """
    Verwaltet die Navigation zwischen verschiedenen Screens.
    """

    screen_changed = Signal(str)  # screen_name

    def __init__(self):
        super().__init__()
        self._screens: Dict[str, Type] = {}
        self._current_screen: str = "home"

    def register_screen(self, screen_name: str, screen_class: Type):
        """Registriert einen neuen Screen."""
        self._screens[screen_name] = screen_class

    def get_screen_class(self, screen_name: str) -> Type:
        """Gibt die Screen-Klasse zurück."""
        return self._screens.get(screen_name)

    def get_available_screens(self) -> list:
        """Gibt alle verfügbaren Screen-Namen zurück."""
        return list(self._screens.keys())

    def navigate_to(self, screen_name: str) -> bool:
        """Navigiert zu einem Screen."""
        if screen_name in self._screens:
            if self._current_screen != screen_name:
                self._current_screen = screen_name
                self.screen_changed.emit(screen_name)
            return True
        return False

    def get_current_screen(self) -> str:
        """Gibt den Namen des aktuellen Screens zurück."""
        return self._current_screen

    def get_screen_title(self, screen_name: str) -> str:
        """Gibt einen benutzerfreundlichen Titel für den Screen zurück."""
        titles = {
            "home": "Overview",
            "electrolysis": "Electrolysis",
            "water_treatment": "Water Treatment",
            "alarms": "Alarms",
            "monitoring": "Monitoring",
            "maintenance": "Maintenance",
            "settings": "Settings",
        }
        return titles.get(screen_name, screen_name.capitalize())
