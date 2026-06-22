"""
Plant State Model - Hält alle Anlagenwerte und simulierte Prozessdaten.
"""

from PySide6.QtCore import QObject, Signal
from datetime import datetime
import config


class PlantState(QObject):
    """
    Zentrale Klasse für alle Anlagenzustände.
    Sendet Signale bei Änderungen, um die GUI zu aktualisieren.
    """

    # Signale für Datenänderungen
    temperature_changed = Signal(float)
    pressure_changed = Signal(float)
    fill_level_changed = Signal(float)
    pump_status_changed = Signal(bool)
    system_state_changed = Signal(str)
    timestamp_changed = Signal(str)

    def __init__(self):
        super().__init__()
        
        # Prozessvariablen
        self._temperature = config.DEFAULT_TEMPERATURE
        self._pressure = config.DEFAULT_PRESSURE
        self._fill_level = config.DEFAULT_FILL_LEVEL
        self._pump_status = config.DEFAULT_PUMP_STATUS
        self._system_state = config.DEFAULT_SYSTEM_STATE
        self._timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # === Temperature ===
    @property
    def temperature(self) -> float:
        return self._temperature

    @temperature.setter
    def temperature(self, value: float):
        if self._temperature != value:
            # Min/Max Constraints
            value = max(-50.0, min(150.0, value))
            self._temperature = value
            self.temperature_changed.emit(value)
            self._update_timestamp()

    # === Pressure ===
    @property
    def pressure(self) -> float:
        return self._pressure

    @pressure.setter
    def pressure(self, value: float):
        if self._pressure != value:
            # Min/Max Constraints
            value = max(0.0, min(10.0, value))
            self._pressure = value
            self.pressure_changed.emit(value)
            self._update_timestamp()

    # === Fill Level ===
    @property
    def fill_level(self) -> float:
        return self._fill_level

    @fill_level.setter
    def fill_level(self, value: float):
        if self._fill_level != value:
            # Min/Max Constraints: 0-100%
            value = max(0.0, min(100.0, value))
            self._fill_level = value
            self.fill_level_changed.emit(value)
            self._update_timestamp()

    # === Pump Status ===
    @property
    def pump_status(self) -> bool:
        return self._pump_status

    @pump_status.setter
    def pump_status(self, value: bool):
        if self._pump_status != value:
            self._pump_status = value
            self.pump_status_changed.emit(value)
            self._update_timestamp()

    # === System State ===
    @property
    def system_state(self) -> str:
        return self._system_state

    @system_state.setter
    def system_state(self, value: str):
        valid_states = ["STOPPED", "RUNNING", "EMERGENCY_STOP", "ERROR"]
        if value not in valid_states:
            raise ValueError(f"Invalid system state: {value}")
        
        if self._system_state != value:
            self._system_state = value
            self.system_state_changed.emit(value)
            self._update_timestamp()

    # === Timestamp ===
    @property
    def timestamp(self) -> str:
        return self._timestamp

    def _update_timestamp(self):
        self._timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.timestamp_changed.emit(self._timestamp)

    # === Helper Methods ===
    def reset_to_defaults(self):
        """Setzt alle Werte auf Standardwerte zurück."""
        self.temperature = config.DEFAULT_TEMPERATURE
        self.pressure = config.DEFAULT_PRESSURE
        self.fill_level = config.DEFAULT_FILL_LEVEL
        self.pump_status = config.DEFAULT_PUMP_STATUS
        self.system_state = config.DEFAULT_SYSTEM_STATE

    def get_state_dict(self) -> dict:
        """Gibt alle Anlagenwerte als Dictionary zurück."""
        return {
            "temperature": self.temperature,
            "pressure": self.pressure,
            "fill_level": self.fill_level,
            "pump_status": self.pump_status,
            "system_state": self.system_state,
            "timestamp": self.timestamp,
        }

    def system_healthy(self) -> bool:
        """Prüft, ob die Anlage in einem gesunden Zustand ist."""
        return (
            self.system_state != "ERROR"
            and self.system_state != "EMERGENCY_STOP"
        )
