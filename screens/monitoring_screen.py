"""
Monitoring Screen - Erweiterte Überwachung und Trends.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QScrollArea
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from screens.base_screen import BaseScreen
from widgets.status_card import StatusCard
import config


class MonitoringScreen(BaseScreen):
    """
    Screen für erweiterte Überwachung, Trends und KPIs.
    """

    def __init__(self, state_manager, navigation, parent=None):
        super().__init__(state_manager, navigation, parent)
        self.setup_ui()

    def setup_ui(self):
        """Baut die UI auf."""
        # Titel
        title = QLabel("Advanced Monitoring & Trends")
        title_font = QFont()
        title_font.setPointSize(config.FONT_SIZE_TITLE + 2)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet(f"color: {config.TEXT_PRIMARY};")
        self.layout.addWidget(title)
        
        self.layout.addSpacing(10)
        
        # === Subtitle ===
        subtitle = QLabel("Echtzeit-Daten und erweiterte Systemmetriken")
        subtitle_font = QFont()
        subtitle_font.setPointSize(config.FONT_SIZE_BODY)
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet(f"color: {config.TEXT_SECONDARY};")
        self.layout.addWidget(subtitle)
        
        self.layout.addSpacing(15)
        
        # === KPI Cards ===
        grid_layout = QHBoxLayout()
        grid_layout.setSpacing(15)
        
        # Uptime
        uptime_card = StatusCard("System Uptime", "24h 32m", "Ohne Fehler", "⏱️")
        grid_layout.addWidget(uptime_card)
        
        # Efficiency
        efficiency_card = StatusCard("Effizienz", "94.5%", "Optimal", "📈")
        grid_layout.addWidget(efficiency_card)
        
        # Cycle Count
        cycle_card = StatusCard("Zyklusanzahl", "1,247", "Heute", "🔄")
        grid_layout.addWidget(cycle_card)
        
        self.layout.addLayout(grid_layout)
        
        self.layout.addSpacing(15)
        
        # === Detaillierte Metriken ===
        metrics_label = QLabel("Detaillierte Systemmetriken")
        metrics_font = QFont()
        metrics_font.setPointSize(config.FONT_SIZE_HEADER)
        metrics_font.setBold(True)
        metrics_label.setFont(metrics_font)
        metrics_label.setStyleSheet(f"color: {config.TEXT_PRIMARY};")
        self.layout.addWidget(metrics_label)
        
        self.layout.addSpacing(10)
        
        # Platzhalter für weitere Metriken
        metrics_info = QLabel(
            "Hier können später Graphen, Diagramme und Trend-Analysen eingefügt werden.\n"
            "Z.B.: Temperaturverlauf, Druckkurven, Effizienztrends, etc."
        )
        metrics_info.setStyleSheet(f"""
            background-color: #f8f9fa;
            border: 1px dashed #bdc3c7;
            border-radius: 5px;
            padding: 15px;
            color: {config.TEXT_SECONDARY};
        """)
        self.layout.addWidget(metrics_info)
        
        self.layout.addStretch()
