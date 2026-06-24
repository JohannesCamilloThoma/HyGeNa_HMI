"""
State Manager - Zentrale Verwaltung aller Anlagenzustände und Alarme.
"""

from PySide6.QtCore import QObject, Signal
from models.plant_state import PlantState
from models.alarm_model import AlarmModel, AlarmSeverity
from models.maintenance_model import MaintenanceModel
import config


class StateManager(QObject):
    """
    Zentrale Verwaltung aller Anlagenzustände.
    Koordiniert PlantState, AlarmModel und MaintenanceModel.
    """

    # Signale
    state_changed = Signal()
    emergency_stop_triggered = Signal()

    def __init__(self):
        super().__init__()
        
        # Sub-Models
        self.plant_state = PlantState()
        self.alarm_model = AlarmModel()
        self.maintenance_model = MaintenanceModel()
        
        # Verbinde Signale
        self.plant_state.system_state_changed.connect(self._on_system_state_changed)
        self.alarm_model.alarm_added.connect(self._on_alarm_added)

    def _on_system_state_changed(self, state: str):
        """Reagiert auf Systemzustandsänderungen."""
        if state == "EMERGENCY_STOP":
            self.emergency_stop_triggered.emit()
        self.state_changed.emit()

    def _on_alarm_added(self, alarm):
        """Reagiert auf neue Alarme."""
        # Falls kritischer Alarm, automatisch Notfall-Stopp
        if alarm.severity == AlarmSeverity.CRITICAL:
            self.trigger_emergency_stop()
        self.state_changed.emit()

    def trigger_emergency_stop(self):
        """Aktiviert den Notfall-Stopp."""
        self.plant_state.system_state = "EMERGENCY_STOP"
        self.alarm_model.add_alarm(
            "EMERGENCY_STOP",
            "Emergency stop has been activated!",
            AlarmSeverity.CRITICAL
        )

    def reset_emergency_stop(self):
        """Setzt den Notfall-Stopp zurück."""
        if self.plant_state.system_state == "EMERGENCY_STOP":
            self.plant_state.system_state = "STOPPED"
            self.alarm_model.clear_alarm("EMERGENCY_STOP")

    def start_plant(self):
        """Startet die Anlage."""
        if self.plant_state.system_state == "STOPPED":
            if not self.alarm_model.has_critical_alarms():
                self.plant_state.system_state = "RUNNING"
            else:
                self.alarm_model.add_alarm(
                    "START_FAILED",
                    "System start failed - critical alarms present",
                    AlarmSeverity.ERROR
                )

    def stop_plant(self):
        """Stoppt die Anlage."""
        self.plant_state.system_state = "STOPPED"
        self.plant_state.pump_status = False

    def get_all_state(self) -> dict:
        """Gibt den kompletten Systemzustand als Dict zurück."""
        return {
            "plant_state": self.plant_state.get_state_dict(),
            "active_alarms": [
                {
                    "id": a.alarm_id,
                    "message": a.message,
                    "severity": a.severity.value,
                    "timestamp": a.timestamp.isoformat(),
                }
                for a in self.alarm_model.get_active_alarms()
            ],
            "maintenance_tasks": [
                {
                    "id": t.task_id,
                    "name": t.name,
                    "status": t.get_status().value,
                    "next_due": t.next_due.isoformat(),
                }
                for t in self.maintenance_model.get_all_tasks()
            ],
        }
