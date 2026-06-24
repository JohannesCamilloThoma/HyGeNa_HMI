"""
Maintenance Model - Verwaltung von Wartungsinformationen.
"""

from PySide6.QtCore import QObject, Signal
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict


class MaintenanceStatus(Enum):
    """Wartungsstatus."""
    OK = "OK"
    WARNING = "WARNING"
    DUE = "DUE"
    OVERDUE = "OVERDUE"


class MaintenanceTask:
    """Datenstruktur für Wartungsaufgaben."""
    
    def __init__(self, task_id: str, name: str, interval_days: int, last_performed: datetime = None):
        self.task_id = task_id
        self.name = name
        self.interval_days = interval_days
        self.last_performed = last_performed or datetime.now()
        self.next_due = self.last_performed + timedelta(days=interval_days)

    def get_status(self) -> MaintenanceStatus:
        """Bestimmt den Status der Wartungsaufgabe."""
        days_until_due = (self.next_due - datetime.now()).days
        
        if days_until_due < 0:
            return MaintenanceStatus.OVERDUE
        elif days_until_due <= 7:
            return MaintenanceStatus.DUE
        elif days_until_due <= 30:
            return MaintenanceStatus.WARNING
        else:
            return MaintenanceStatus.OK

    def __repr__(self):
        return f"MaintenanceTask({self.task_id}, {self.name}, Status: {self.get_status().value})"


class MaintenanceModel(QObject):
    """
    Verwaltung aller Wartungsaufgaben.
    """

    task_added = Signal(MaintenanceTask)
    task_completed = Signal(str)  # task_id
    task_status_changed = Signal(str, str)  # task_id, new_status

    def __init__(self):
        super().__init__()
        self._tasks: Dict[str, MaintenanceTask] = {}
        self._init_default_tasks()

    def _init_default_tasks(self):
        """Initialisiert Standard-Wartungsaufgaben."""
        default_tasks = [
            ("filter_change", "Filter Replacement", 90),
            ("pump_check", "Pump Inspection", 30),
            ("system_calibration", "System Calibration", 180),
            ("oil_change", "Oil Change", 365),
        ]
        
        for task_id, name, days in default_tasks:
            task = MaintenanceTask(task_id, name, days)
            self._tasks[task_id] = task
            self.task_added.emit(task)

    def complete_task(self, task_id: str):
        """Markiert eine Wartungsaufgabe als abgeschlossen."""
        if task_id in self._tasks:
            self._tasks[task_id].last_performed = datetime.now()
            self._tasks[task_id].next_due = (
                datetime.now() + timedelta(days=self._tasks[task_id].interval_days)
            )
            self.task_completed.emit(task_id)
            self._notify_status_change(task_id)

    def get_all_tasks(self) -> list:
        """Gibt alle Wartungsaufgaben zurück."""
        return list(self._tasks.values())

    def get_tasks_by_status(self, status: MaintenanceStatus) -> list:
        """Filtert Aufgaben nach Status."""
        return [t for t in self._tasks.values() if t.get_status() == status]

    def get_overdue_tasks(self) -> list:
        """Gibt überfällige Wartungsaufgaben zurück."""
        return self.get_tasks_by_status(MaintenanceStatus.OVERDUE)

    def _notify_status_change(self, task_id: str):
        """Benachrichtigt über Statusänderungen."""
        if task_id in self._tasks:
            status = self._tasks[task_id].get_status()
            self.task_status_changed.emit(task_id, status.value)
