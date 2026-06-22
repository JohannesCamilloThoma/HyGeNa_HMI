"""
Simulation Window - Control Panel für die Simulation.
"""

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QGroupBox, QFormLayout, QSlider, QSpinBox, QDoubleSpinBox, QCheckBox, QPushButton, QLabel, QHBoxLayout
from PySide6.QtCore import Qt
from core.state_manager import StateManager
import config


class SimulationWindow(QMainWindow):
    """
    Simulations-/Control-Fenster für Testzwecke.
    Erlaubt die Manipulation von Anlagenwerten.
    """

    def __init__(self, state_manager: StateManager):
        super().__init__()
        
        self.state_manager = state_manager
        
        # Window Setup
        self.setWindowTitle(config.SIMULATION_WINDOW_TITLE)
        self.setGeometry(600, 100, config.SIMULATION_WINDOW_WIDTH, config.SIMULATION_WINDOW_HEIGHT)
        
        # Create UI
        self.setup_ui()

    def setup_ui(self):
        """Baut die UI auf."""
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # === Title ===
        title = QLabel("Simulation & Control Panel")
        title_style = """
            font-size: 16pt;
            font-weight: bold;
            color: #2c3e50;
        """
        title.setStyleSheet(title_style)
        main_layout.addWidget(title)
        
        # === Process Variables Group ===
        process_group = QGroupBox("Prozessvariablen")
        process_layout = QFormLayout()
        
        # Temperature
        temp_layout = QHBoxLayout()
        self.temp_slider = QSlider(Qt.Horizontal)
        self.temp_slider.setMinimum(-50)
        self.temp_slider.setMaximum(150)
        self.temp_slider.setValue(int(config.DEFAULT_TEMPERATURE))
        self.temp_slider.valueChanged.connect(self._on_temperature_changed)
        self.temp_spinbox = QDoubleSpinBox()
        self.temp_spinbox.setMinimum(-50)
        self.temp_spinbox.setMaximum(150)
        self.temp_spinbox.setValue(config.DEFAULT_TEMPERATURE)
        self.temp_spinbox.setSuffix(" °C")
        self.temp_spinbox.valueChanged.connect(lambda v: self.temp_slider.setValue(int(v)))
        temp_layout.addWidget(self.temp_slider)
        temp_layout.addWidget(self.temp_spinbox)
        process_layout.addRow("Temperatur:", temp_layout)
        
        # Pressure
        pressure_layout = QHBoxLayout()
        self.pressure_slider = QSlider(Qt.Horizontal)
        self.pressure_slider.setMinimum(0)
        self.pressure_slider.setMaximum(100)
        self.pressure_slider.setValue(int(config.DEFAULT_PRESSURE * 10))
        self.pressure_slider.valueChanged.connect(self._on_pressure_changed)
        self.pressure_spinbox = QDoubleSpinBox()
        self.pressure_spinbox.setMinimum(0)
        self.pressure_spinbox.setMaximum(10)
        self.pressure_spinbox.setValue(config.DEFAULT_PRESSURE)
        self.pressure_spinbox.setSingleStep(0.1)
        self.pressure_spinbox.setSuffix(" bar")
        self.pressure_spinbox.valueChanged.connect(lambda v: self.pressure_slider.setValue(int(v * 10)))
        pressure_layout.addWidget(self.pressure_slider)
        pressure_layout.addWidget(self.pressure_spinbox)
        process_layout.addRow("Druck:", pressure_layout)
        
        # Fill Level
        fill_layout = QHBoxLayout()
        self.fill_slider = QSlider(Qt.Horizontal)
        self.fill_slider.setMinimum(0)
        self.fill_slider.setMaximum(100)
        self.fill_slider.setValue(int(config.DEFAULT_FILL_LEVEL))
        self.fill_slider.valueChanged.connect(self._on_fill_level_changed)
        self.fill_spinbox = QSpinBox()
        self.fill_spinbox.setMinimum(0)
        self.fill_spinbox.setMaximum(100)
        self.fill_spinbox.setValue(int(config.DEFAULT_FILL_LEVEL))
        self.fill_spinbox.setSuffix(" %")
        self.fill_spinbox.valueChanged.connect(lambda v: self.fill_slider.setValue(v))
        fill_layout.addWidget(self.fill_slider)
        fill_layout.addWidget(self.fill_spinbox)
        process_layout.addRow("Füllstand:", fill_layout)
        
        process_group.setLayout(process_layout)
        main_layout.addWidget(process_group)
        
        # === Equipment Status Group ===
        equipment_group = QGroupBox("Ausrüstungsstatus")
        equipment_layout = QFormLayout()
        
        # Pump Status
        self.pump_checkbox = QCheckBox("Pumpe läuft")
        self.pump_checkbox.setChecked(config.DEFAULT_PUMP_STATUS)
        self.pump_checkbox.stateChanged.connect(self._on_pump_status_changed)
        equipment_layout.addRow("Pumpe:", self.pump_checkbox)
        
        # System State
        system_layout = QHBoxLayout()
        self.start_btn = QPushButton("▶ Start")
        self.start_btn.clicked.connect(lambda: self.state_manager.start_plant())
        system_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("⏹ Stop")
        self.stop_btn.clicked.connect(lambda: self.state_manager.stop_plant())
        system_layout.addWidget(self.stop_btn)
        
        self.estop_btn = QPushButton("🛑 NOTFALL-STOPP")
        self.estop_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {config.DANGER_COLOR};
                color: white;
                border: none;
                border-radius: 3px;
                padding: 5px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #c0392b;
            }}
        """)
        self.estop_btn.clicked.connect(lambda: self.state_manager.trigger_emergency_stop())
        system_layout.addWidget(self.estop_btn)
        
        equipment_layout.addRow("Systemsteuerung:", system_layout)
        
        equipment_group.setLayout(equipment_layout)
        main_layout.addWidget(equipment_group)
        
        # === Alarm Simulation Group ===
        alarm_group = QGroupBox("Alarm-Simulation")
        alarm_layout = QFormLayout()
        
        alarm_btn_layout = QHBoxLayout()
        
        warning_btn = QPushButton("⚠️ Warnung auslösen")
        warning_btn.clicked.connect(self._trigger_warning_alarm)
        alarm_btn_layout.addWidget(warning_btn)
        
        error_btn = QPushButton("❌ Fehler auslösen")
        error_btn.clicked.connect(self._trigger_error_alarm)
        alarm_btn_layout.addWidget(error_btn)
        
        clear_alarms_btn = QPushButton("✓ Alle Alarme löschen")
        clear_alarms_btn.clicked.connect(lambda: self.state_manager.alarm_model.clear_all())
        alarm_btn_layout.addWidget(clear_alarms_btn)
        
        alarm_layout.addRow("Alarme:", alarm_btn_layout)
        
        alarm_group.setLayout(alarm_layout)
        main_layout.addWidget(alarm_group)
        
        # === System Actions Group ===
        actions_group = QGroupBox("System-Aktionen")
        actions_layout = QFormLayout()
        
        actions_btn_layout = QHBoxLayout()
        
        reset_btn = QPushButton("🔄 Auf Standard zurücksetzen")
        reset_btn.clicked.connect(self._reset_all)
        actions_btn_layout.addWidget(reset_btn)
        
        actions_layout.addRow("Aktionen:", actions_btn_layout)
        
        actions_group.setLayout(actions_layout)
        main_layout.addWidget(actions_group)
        
        main_layout.addStretch()
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        # Style the window
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {config.BG_PRIMARY};
            }}
            QGroupBox {{
                color: {config.TEXT_PRIMARY};
                border: 2px solid #ecf0f1;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }}
        """)

    def _on_temperature_changed(self, value):
        """Handler für Temperaturänderung."""
        self.state_manager.plant_state.temperature = float(value)

    def _on_pressure_changed(self, value):
        """Handler für Druckänderung."""
        self.state_manager.plant_state.pressure = value / 10.0

    def _on_fill_level_changed(self, value):
        """Handler für Füllstandänderung."""
        self.state_manager.plant_state.fill_level = float(value)

    def _on_pump_status_changed(self, state):
        """Handler für Pumpenstatus."""
        self.state_manager.plant_state.pump_status = self.pump_checkbox.isChecked()

    def _trigger_warning_alarm(self):
        """Löst einen Warnung-Alarm aus."""
        from models.alarm_model import AlarmSeverity
        self.state_manager.alarm_model.add_alarm(
            f"WARNING_{self.state_manager.alarm_model.alarm_added.emit.__self__}",
            "Testalarm: Warnung - Bitte überprüfen Sie das System",
            AlarmSeverity.WARNING
        )

    def _trigger_error_alarm(self):
        """Löst einen Fehler-Alarm aus."""
        from models.alarm_model import AlarmSeverity
        self.state_manager.alarm_model.add_alarm(
            f"ERROR_{self.state_manager.alarm_model.alarm_added.emit.__self__}",
            "Testalarm: Fehler - Sofortige Aufmerksamkeit erforderlich",
            AlarmSeverity.ERROR
        )

    def _reset_all(self):
        """Setzt alle Werte auf Standard zurück."""
        self.state_manager.plant_state.reset_to_defaults()
        self.state_manager.alarm_model.clear_all()
        self.state_manager.stop_plant()
        
        # Update UI
        self.temp_slider.setValue(int(config.DEFAULT_TEMPERATURE))
        self.pressure_slider.setValue(int(config.DEFAULT_PRESSURE * 10))
        self.fill_slider.setValue(int(config.DEFAULT_FILL_LEVEL))
        self.pump_checkbox.setChecked(config.DEFAULT_PUMP_STATUS)
