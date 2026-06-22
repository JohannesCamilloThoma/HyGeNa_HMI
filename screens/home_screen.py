"""
Home Screen - Startseite/Übersicht.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from screens.base_screen import BaseScreen
from widgets.status_card import StatusCard
import config


class HomeScreen(BaseScreen):
    """
    Startseite mit Übersicht über die wichtigsten Anlagenwerte.
    """

    def __init__(self, state_manager, navigation, parent=None):
        super().__init__(state_manager, navigation, parent)
        self.setup_ui()

    def setup_ui(self):
        """Baut die UI auf."""
        # Titel
        title = QLabel("System-Übersicht")
        title_font = QFont()
        title_font.setPointSize(config.FONT_SIZE_TITLE + 2)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet(f"color: {config.TEXT_PRIMARY};")
        self.layout.addWidget(title)
        
        self.layout.addSpacing(10)
        
        # === Status Cards Grid ===
        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)
        
        # Temperatur
        self.temp_card = StatusCard("Temperatur", "20°C", "Normal", "🌡️")
        grid_layout.addWidget(self.temp_card, 0, 0)
        
        # Druck
        self.pressure_card = StatusCard("Druck", "1.0 bar", "OK", "⚙️")
        grid_layout.addWidget(self.pressure_card, 0, 1)
        
        # Füllstand
        self.fill_card = StatusCard("Füllstand", "50%", "Normal", "📦")
        grid_layout.addWidget(self.fill_card, 0, 2)
        
        # System State
        self.system_card = StatusCard("Systemstatus", "Gestoppt", "Bereit", "🟢")
        grid_layout.addWidget(self.system_card, 1, 0)
        
        # Pumpe
        self.pump_card = StatusCard("Pumpe", "AUS", "Inaktiv", "💧")
        grid_layout.addWidget(self.pump_card, 1, 1)
        
        # Alarme
        self.alarms_card = StatusCard("Aktive Alarme", "0", "Keine", "🔔")
        grid_layout.addWidget(self.alarms_card, 1, 2)
        
        self.layout.addLayout(grid_layout)
        
        # Spacer
        self.layout.addStretch()
        
        # Verbinde Signale
        self.state_manager.plant_state.temperature_changed.connect(self._update_temperature)
        self.state_manager.plant_state.pressure_changed.connect(self._update_pressure)
        self.state_manager.plant_state.fill_level_changed.connect(self._update_fill_level)
        self.state_manager.plant_state.system_state_changed.connect(self._update_system_state)
        self.state_manager.plant_state.pump_status_changed.connect(self._update_pump_status)
        self.state_manager.alarm_model.alarm_added.connect(self._update_alarms)
        
        # Initial update
        self._update_all()

    def _update_temperature(self, value):
        """Aktualisiert die Temperaturanzeige."""
        self.temp_card.set_value(f"{value:.1f}°C")
        
        # Farbiger Untertitel basierend auf Wert
        if value < 0:
            status = "Zu kalt"
        elif value > 60:
            status = "Warnung!"
        else:
            status = "Normal"
        self.temp_card.set_subtitle(status)

    def _update_pressure(self, value):
        """Aktualisiert die Druckanzeige."""
        self.pressure_card.set_value(f"{value:.1f} bar")
        
        if value < 0.5:
            status = "Niedrig"
        elif value > 8:
            status = "Zu hoch!"
        else:
            status = "OK"
        self.pressure_card.set_subtitle(status)

    def _update_fill_level(self, value):
        """Aktualisiert die Füllstandanzeige."""
        self.fill_card.set_value(f"{value:.0f}%")
        
        if value < 20:
            status = "Niedrig"
        elif value > 90:
            status = "Hoch"
        else:
            status = "Normal"
        self.fill_card.set_subtitle(status)

    def _update_system_state(self, state):
        """Aktualisiert den Systemstatus."""
        state_text = {
            "STOPPED": "Gestoppt",
            "RUNNING": "Läuft",
            "EMERGENCY_STOP": "NOTFALL-STOPP",
            "ERROR": "Fehler",
        }.get(state, state)
        
        icon = {
            "STOPPED": "🔴",
            "RUNNING": "🟢",
            "EMERGENCY_STOP": "🔴",
            "ERROR": "🔴",
        }.get(state, "⚪")
        
        self.system_card.set_value(state_text)
        # Aktualisiere auch Icon (einfache Variante ohne Rekonstruktion)
        self.system_card.set_subtitle("Status aktualisiert")

    def _update_pump_status(self, status):
        """Aktualisiert die Pumpenstatus."""
        text = "EIN" if status else "AUS"
        subtitle = "Läuft" if status else "Inaktiv"
        self.pump_card.set_value(text)
        self.pump_card.set_subtitle(subtitle)

    def _update_alarms(self, alarm):
        """Aktualisiert die Alarmanzahl."""
        count = len(self.state_manager.alarm_model.get_active_alarms())
        self.alarms_card.set_value(str(count))
        status = "Alarme!" if count > 0 else "Keine"
        self.alarms_card.set_subtitle(status)

    def _update_all(self):
        """Aktualisiert alle Anzeigen."""
        self._update_temperature(self.state_manager.plant_state.temperature)
        self._update_pressure(self.state_manager.plant_state.pressure)
        self._update_fill_level(self.state_manager.plant_state.fill_level)
        self._update_system_state(self.state_manager.plant_state.system_state)
        self._update_pump_status(self.state_manager.plant_state.pump_status)
        self._update_alarms(None)
