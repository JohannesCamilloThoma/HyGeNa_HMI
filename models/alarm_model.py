"""
Alarm Model - Verwaltung von Alarmen und Warnmeldungen.
"""

from PySide6.QtCore import QObject, Signal
from datetime import datetime
from enum import Enum
from typing import List, Dict


class AlarmSeverity(Enum):
    """Alarmseveritätsstufen."""
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Alarm:
    """Datenstruktur für einzelne Alarme."""
    
    def __init__(self, alarm_id: str, message: str, severity: AlarmSeverity):
        self.alarm_id = alarm_id
        self.message = message
        self.severity = severity
        self.timestamp = datetime.now()
        self.acknowledged = False

    def __repr__(self):
        return f"Alarm({self.alarm_id}, {self.message}, {self.severity.value})"


class AlarmModel(QObject):
    """
    Verwaltung aller Alarme der Anlage.
    """

    alarm_added = Signal(Alarm)
    alarm_cleared = Signal(str)  # alarm_id
    alarm_acknowledged = Signal(str)  # alarm_id

    def __init__(self):
        super().__init__()
        self._alarms: Dict[str, Alarm] = {}

    def add_alarm(self, alarm_id: str, message: str, severity: AlarmSeverity = AlarmSeverity.WARNING):
        """Fügt einen neuen Alarm hinzu."""
        if alarm_id not in self._alarms:
            alarm = Alarm(alarm_id, message, severity)
            self._alarms[alarm_id] = alarm
            self.alarm_added.emit(alarm)

    def clear_alarm(self, alarm_id: str):
        """Entfernt einen Alarm."""
        if alarm_id in self._alarms:
            del self._alarms[alarm_id]
            self.alarm_cleared.emit(alarm_id)

    def acknowledge_alarm(self, alarm_id: str):
        """Bestätigt einen Alarm."""
        if alarm_id in self._alarms:
            self._alarms[alarm_id].acknowledged = True
            self.alarm_acknowledged.emit(alarm_id)

    def get_active_alarms(self) -> List[Alarm]:
        """Gibt alle aktiven (nicht quittierten) Alarme zurück."""
        return [a for a in self._alarms.values() if not a.acknowledged]

    def get_acknowledged_alarms(self) -> List[Alarm]:
        """Gibt alle quittierten Alarme zurück."""
        return [a for a in self._alarms.values() if a.acknowledged]

    def get_all_alarms(self) -> List[Alarm]:
        """Gibt alle Alarme (aktiv und quittiert) zurück."""
        return list(self._alarms.values())

    def get_alarms_by_severity(self, severity: AlarmSeverity) -> List[Alarm]:
        """Filtert Alarme nach Severity."""
        return [a for a in self._alarms.values() if a.severity == severity]

    def has_critical_alarms(self) -> bool:
        """Prüft, ob es kritische Alarme gibt."""
        return any(a.severity == AlarmSeverity.CRITICAL and not a.acknowledged for a in self._alarms.values())

    def clear_all(self):
        """Löscht alle Alarme."""
        alarm_ids = list(self._alarms.keys())
        for alarm_id in alarm_ids:
            self.clear_alarm(alarm_id)
