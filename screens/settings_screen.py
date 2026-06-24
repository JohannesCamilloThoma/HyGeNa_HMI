"""
Settings Screen - Anwendungseinstellungen.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QFormLayout, QSpinBox, QCheckBox, QPushButton, QHBoxLayout
from PySide6.QtGui import QFont
from screens.base_screen import BaseScreen
import config


class SettingsScreen(BaseScreen):
    """
    Screen für Anwendungseinstellungen und Konfiguration.
    """

    def __init__(self, state_manager, navigation, parent=None):
        super().__init__(state_manager, navigation, parent)
        self.setup_ui()

    def setup_ui(self):
        """Baut die UI auf."""
        # Titel
        title = QLabel("Settings")
        title_font = QFont()
        title_font.setPointSize(config.FONT_SIZE_TITLE + 2)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet(f"color: {config.TEXT_PRIMARY};")
        self.layout.addWidget(title)
        
        self.layout.addSpacing(15)
        
        # === System Settings ===
        system_group = QGroupBox("System Settings")
        system_layout = QFormLayout()
        
        refresh_spinbox = QSpinBox()
        refresh_spinbox.setValue(1)
        refresh_spinbox.setMinimum(1)
        refresh_spinbox.setMaximum(10)
        refresh_spinbox.setSuffix(" second(s)")
        system_layout.addRow("Refresh interval:", refresh_spinbox)
        
        auto_start = QCheckBox("Enable system on startup")
        system_layout.addRow("Auto-Start:", auto_start)
        
        system_group.setLayout(system_layout)
        self.layout.addWidget(system_group)
        
        self.layout.addSpacing(10)
        
        # === Alarm Settings ===
        alarm_group = QGroupBox("Alarm Settings")
        alarm_layout = QFormLayout()
        
        email_alerts = QCheckBox("Enable e-mail notifications")
        alarm_layout.addRow("E-mail alerts:", email_alerts)
        
        critical_only = QCheckBox("Show critical alarms only")
        alarm_layout.addRow("Filter:", critical_only)
        
        alarm_group.setLayout(alarm_layout)
        self.layout.addWidget(alarm_group)
        
        self.layout.addSpacing(10)
        
        # === Maintenance Settings ===
        maint_group = QGroupBox("Maintenance Settings")
        maint_layout = QFormLayout()
        
        maint_warning = QSpinBox()
        maint_warning.setValue(30)
        maint_warning.setMinimum(1)
        maint_warning.setMaximum(365)
        maint_warning.setSuffix(" days")
        maint_layout.addRow("Warning period before due maintenance:", maint_warning)
        
        maint_group.setLayout(maint_layout)
        self.layout.addWidget(maint_group)
        
        self.layout.addSpacing(15)
        
        # === Action Buttons ===
        button_layout = QHBoxLayout()
        
        reset_btn = QPushButton("🔄 Reset to defaults")
        reset_btn.setMaximumWidth(250)
        reset_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {config.PRIMARY_COLOR};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }}
            QPushButton:hover {{
                background-color: #2980b9;
            }}
        """)
        button_layout.addWidget(reset_btn)
        
        save_btn = QPushButton("💾 Save")
        save_btn.setMaximumWidth(250)
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {config.SUCCESS_COLOR};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }}
            QPushButton:hover {{
                background-color: #27ae60;
            }}
        """)
        button_layout.addWidget(save_btn)
        
        button_layout.addStretch()
        
        self.layout.addLayout(button_layout)
        
        self.layout.addStretch()
