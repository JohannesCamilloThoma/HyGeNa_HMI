"""
Main Window - Das Hauptfenster der HMI-Anwendung.
"""

from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt
from core.state_manager import StateManager
from core.navigation import Navigation
from widgets.sidebar import Sidebar
from widgets.header_bar import HeaderBar
from widgets.footer_bar import FooterBar
from widgets.content_container import ContentContainer
from screens.home_screen import HomeScreen
from screens.alarm_screen import AlarmScreen
from screens.monitoring_screen import MonitoringScreen
from screens.maintenance_screen import MaintenanceScreen
from screens.settings_screen import SettingsScreen
import config


class MainWindow(QMainWindow):
    """
    Hauptfenster der HMI-Anwendung.
    Zeigt die Übersicht über den Anlagenzustand.
    """

    def __init__(self, state_manager: StateManager):
        super().__init__()
        
        self.state_manager = state_manager
        self.navigation = Navigation()
        
        # Window Setup
        self.setWindowTitle(config.MAIN_WINDOW_TITLE)
        self.setGeometry(100, 100, config.MAIN_WINDOW_WIDTH, config.MAIN_WINDOW_HEIGHT)
        
        # Create UI
        self.setup_ui()
        
        # Register Screens
        self._register_screens()
        
        # Connect Signals
        self.navigation.screen_changed.connect(self._on_screen_changed)
        self.sidebar.screen_selected.connect(self.navigation.navigate_to)
        self.footer_bar.stop_pressed.connect(self._on_stop_pressed)
        
        # Connect State Updates
        self.state_manager.plant_state.system_state_changed.connect(self._update_header_status)
        
        # Initialize first screen
        self.navigation.navigate_to("home")

    def setup_ui(self):
        """Baut die UI auf."""
        # === Main Container ===
        main_container = QWidget()
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # === Sidebar (Left) ===
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)
        
        # === Right Container (Header + Content + Footer) ===
        right_container = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)
        
        # Header Bar
        self.header_bar = HeaderBar()
        right_layout.addWidget(self.header_bar)
        
        # Content Container
        self.content_container = ContentContainer()
        right_layout.addWidget(self.content_container, 1)
        
        # Footer Bar
        self.footer_bar = FooterBar()
        right_layout.addWidget(self.footer_bar)
        
        right_container.setLayout(right_layout)
        main_layout.addWidget(right_container, 1)
        
        main_container.setLayout(main_layout)
        self.setCentralWidget(main_container)

    def _register_screens(self):
        """Registriert alle verfügbaren Screens."""
        self.navigation.register_screen("home", HomeScreen)
        self.navigation.register_screen("alarms", AlarmScreen)
        self.navigation.register_screen("monitoring", MonitoringScreen)
        self.navigation.register_screen("maintenance", MaintenanceScreen)
        self.navigation.register_screen("settings", SettingsScreen)

    def _on_screen_changed(self, screen_name: str):
        """Handler für Screen-Wechsel."""
        screen_class = self.navigation.get_screen_class(screen_name)
        
        if screen_class:
            # Erstelle neue Screen-Instanz
            screen_widget = screen_class(self.state_manager, self.navigation)
            
            # Setze im Content Container
            self.content_container.set_screen_widget(screen_widget)
            
            # Update Header Title
            title = self.navigation.get_screen_title(screen_name)
            self.header_bar.set_screen_title(title)
            
            # Update Sidebar Active State
            self.sidebar.set_active_screen(screen_name)

    def _update_header_status(self, state: str):
        """Aktualisiert den Anlagenstatus im Header."""
        state_text = {
            "STOPPED": "Gestoppt",
            "RUNNING": "Läuft",
            "EMERGENCY_STOP": "NOTFALL-STOPP",
            "ERROR": "Fehler",
        }.get(state, state)
        self.header_bar.set_system_status(state_text)

    def _on_stop_pressed(self):
        """Handler für STOP-Button."""
        # Triggert Notfall-Stopp
        self.state_manager.trigger_emergency_stop()
        
        # Update Status Text
        alarm_count = len(self.state_manager.alarm_model.get_active_alarms())
        status_text = f"{alarm_count} Alarme aktiv" if alarm_count > 0 else "NOTFALL-STOPP aktiviert"
        self.footer_bar.set_status_text(status_text)

    def closeEvent(self, event):
        """Aufgerufen beim Schließen des Fensters."""
        # Hier können Cleanup-Operationen durchgeführt werden
        event.accept()
