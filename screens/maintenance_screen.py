"""
Maintenance Screen - Wartungsverwaltung.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from screens.base_screen import BaseScreen
from models.maintenance_model import MaintenanceStatus
import config


class MaintenanceScreen(BaseScreen):
    """
    Screen für Wartungsverwaltung und Wartungsplanung.
    """

    def __init__(self, state_manager, navigation, parent=None):
        super().__init__(state_manager, navigation, parent)
        self.setup_ui()

    def setup_ui(self):
        """Baut die UI auf."""
        # Titel
        title = QLabel("Wartungsverwaltung")
        title_font = QFont()
        title_font.setPointSize(config.FONT_SIZE_TITLE + 2)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet(f"color: {config.TEXT_PRIMARY};")
        self.layout.addWidget(title)
        
        self.layout.addSpacing(10)
        
        # === Maintenance Table ===
        self.maintenance_table = QTableWidget()
        self.maintenance_table.setColumnCount(5)
        self.maintenance_table.setHorizontalHeaderLabels(["Aufgabe", "Status", "Nächst fällig", "Intervall", "Aktion"])
        self.maintenance_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.maintenance_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: white;
                gridline-color: #ecf0f1;
                border: 1px solid #ecf0f1;
            }}
            QHeaderView::section {{
                background-color: #f8f9fa;
                padding: 5px;
                border: none;
                border-bottom: 1px solid #ecf0f1;
            }}
        """)
        self.layout.addWidget(self.maintenance_table)
        
        # Verbinde Signale
        self.state_manager.maintenance_model.task_completed.connect(self._populate_table)
        
        # Initial populate
        self._populate_table()

    def _populate_table(self):
        """Füllt die Tabelle mit Wartungsaufgaben."""
        self.maintenance_table.setRowCount(0)
        for task in self.state_manager.maintenance_model.get_all_tasks():
            row = self.maintenance_table.rowCount()
            self.maintenance_table.insertRow(row)
            
            status = task.get_status()
            status_color = {
                MaintenanceStatus.OK: "🟢",
                MaintenanceStatus.WARNING: "🟡",
                MaintenanceStatus.DUE: "🟠",
                MaintenanceStatus.OVERDUE: "🔴",
            }.get(status, "⚪")
            
            self.maintenance_table.setItem(row, 0, QTableWidgetItem(task.name))
            self.maintenance_table.setItem(row, 1, QTableWidgetItem(f"{status_color} {status.value}"))
            self.maintenance_table.setItem(row, 2, QTableWidgetItem(task.next_due.strftime("%d.%m.%Y")))
            self.maintenance_table.setItem(row, 3, QTableWidgetItem(f"{task.interval_days} Tage"))
            
            # Action Button
            btn_layout = QHBoxLayout()
            btn_layout.setContentsMargins(0, 0, 0, 0)
            btn = QPushButton("✓ Abgeschlossen")
            btn.setMaximumWidth(130)
            btn.clicked.connect(lambda checked, tid=task.task_id: self._complete_task(tid))
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {config.SUCCESS_COLOR};
                    color: white;
                    border: none;
                    border-radius: 3px;
                    padding: 5px;
                }}
                QPushButton:hover {{
                    background-color: #27ae60;
                }}
            """)
            btn_layout.addWidget(btn)
            
            btn_widget = QWidget()
            btn_widget.setLayout(btn_layout)
            self.maintenance_table.setCellWidget(row, 4, btn_widget)

    def _complete_task(self, task_id: str):
        """Markiert eine Aufgabe als abgeschlossen."""
        self.state_manager.maintenance_model.complete_task(task_id)
