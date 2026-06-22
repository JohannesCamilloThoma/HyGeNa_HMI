"""
Alarm Screen - Professionelle Alarmverwaltung mit modernem Layout.
"""

from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QComboBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QFrame, QScrollArea
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QColor
from screens.base_screen import BaseScreen
from models.alarm_model import AlarmSeverity
import config


class AlarmScreen(BaseScreen):
    """
    Professioneller Alarm-Screen mit Tab-Navigation, Filterung, Tabelle und Detail-Bereich.
    """

    def __init__(self, state_manager, navigation, parent=None):
        super().__init__(state_manager, navigation, parent)
        self.current_tab = "active"
        self.selected_alarm = None
        self.setup_ui()
        self._populate_table()

    def setup_ui(self):
        """Baut die komplette UI auf."""
        
        # === TAB-LEISTE ===
        self._create_tab_bar()
        self.layout.addWidget(self.tab_bar_frame)
        
        # === FILTER- UND AKTIONSLEISTE ===
        self._create_filter_bar()
        self.layout.addWidget(self.filter_bar_frame)
        
        # === ALARMTABELLE ===
        self._create_alarm_table()
        self.layout.addWidget(self.table_frame, 1)  # Stretch table
        
        # === DETAILBEREICH (konstante Höhe) ===
        self._create_detail_area()
        self.layout.addWidget(self.detail_container)  # Keine Stretch - feste Höhe
        
        # === UNTERE AKTIONSLEISTE ===
        self._create_action_bar()
        self.layout.addWidget(self.action_bar_frame)
        
        # Signale verbinden
        self.state_manager.alarm_model.alarm_added.connect(self._on_alarm_change)
        self.state_manager.alarm_model.alarm_cleared.connect(self._on_alarm_change)

    def _create_tab_bar(self):
        """Erstellt die Tab-Leiste."""
        self.tab_bar_frame = QFrame()
        self.tab_bar_frame.setFixedHeight(60)
        self.tab_bar_frame.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-bottom: 1px solid #e0e0e0;
            }}
        """)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(25)
        
        # Tabs
        self.tab_buttons = {}
        for tab_id, tab_name in [("active", "Aktive Alarme"), ("history", "Historie"), ("stats", "Alarmstatistik")]:
            btn = QPushButton(tab_name)
            btn.setFixedHeight(40)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked, tid=tab_id: self._switch_tab(tid))
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    border: none;
                    color: #7f8c8d;
                    font-weight: normal;
                    font-size: 11pt;
                }
                QPushButton:hover {
                    color: #3498db;
                }
            """)
            layout.addWidget(btn)
            self.tab_buttons[tab_id] = btn
        
        # Badge mit Alarmanzahl
        self.alarm_badge = QLabel()
        self.alarm_badge.setFixedSize(35, 35)
        self.alarm_badge.setAlignment(Qt.AlignCenter)
        self.alarm_badge.setStyleSheet("""
            background-color: #e74c3c;
            color: white;
            border-radius: 17px;
            font-weight: bold;
            font-size: 11pt;
        """)
        layout.addWidget(self.alarm_badge)
        
        layout.addStretch()
        
        self.tab_bar_frame.setLayout(layout)
        self._update_badge()
        self._highlight_tab("active")

    def _create_filter_bar(self):
        """Erstellt die Filter- und Aktionsleiste."""
        self.filter_bar_frame = QFrame()
        self.filter_bar_frame.setFixedHeight(70)
        self.filter_bar_frame.setStyleSheet(f"""
            QFrame {{
                background-color: #f7f8fa;
                border-bottom: 1px solid #e0e0e0;
            }}
        """)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(10)
        
        # Filter Button
        filter_btn = QPushButton("⏳ Filter")
        filter_btn.setFixedSize(80, 40)
        filter_btn.setCursor(Qt.PointingHandCursor)
        filter_btn.setStyleSheet(self._button_style("light"))
        layout.addWidget(filter_btn)
        
        # Severity Dropdown
        self.severity_combo = QComboBox()
        self.severity_combo.addItems(["Alle Severity", "Kritisch", "Hoch", "Mittel", "Niedrig"])
        self.severity_combo.setFixedSize(150, 40)
        self.severity_combo.setStyleSheet(self._combobox_style())
        layout.addWidget(self.severity_combo)
        
        # Status Dropdown
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Alle Status", "Aktiv", "Quittiert"])
        self.status_combo.setFixedSize(150, 40)
        self.status_combo.setStyleSheet(self._combobox_style())
        layout.addWidget(self.status_combo)
        
        # Bereich Dropdown
        self.area_combo = QComboBox()
        self.area_combo.addItems(["Alle Bereiche", "System", "Pumpe", "Sensor"])
        self.area_combo.setFixedSize(150, 40)
        self.area_combo.setStyleSheet(self._combobox_style())
        layout.addWidget(self.area_combo)
        
        # Suchfeld
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("🔍 Suche...")
        self.search_field.setFixedSize(200, 40)
        self.search_field.setStyleSheet("""
            QLineEdit {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 5px;
                background-color: white;
            }
        """)
        layout.addWidget(self.search_field)
        
        layout.addStretch()
        
        # Quittieren Button
        ack_btn = QPushButton("✓ Quittieren")
        ack_btn.setFixedSize(100, 40)
        ack_btn.setCursor(Qt.PointingHandCursor)
        ack_btn.clicked.connect(self._acknowledge_selected)
        ack_btn.setStyleSheet(self._button_style("light_blue"))
        layout.addWidget(ack_btn)
        
        # Alle quittieren Button
        ack_all_btn = QPushButton("✓✓ Alle quittieren")
        ack_all_btn.setFixedSize(120, 40)
        ack_all_btn.setCursor(Qt.PointingHandCursor)
        ack_all_btn.clicked.connect(self._acknowledge_all)
        ack_all_btn.setStyleSheet(self._button_style("blue"))
        layout.addWidget(ack_all_btn)
        
        self.filter_bar_frame.setLayout(layout)

    def _create_alarm_table(self):
        """Erstellt die Alarmtabelle mit zentrierten Einträgen."""
        self.table_frame = QFrame()
        self.table_frame.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Tabelle
        self.alarm_table = QTableWidget()
        self.alarm_table.setColumnCount(8)
        self.alarm_table.setHorizontalHeaderLabels([
            "Icon", "Zeit", "Nachricht", "ID", "Beschreibung", "Severity", "Status", "Bereich"
        ])
        self.alarm_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.alarm_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.alarm_table.setSelectionMode(QTableWidget.SingleSelection)
        self.alarm_table.itemSelectionChanged.connect(self._on_table_selection_changed)
        self.alarm_table.setRowHeight(0, 30)  # Höhe für zentrierte Einträge
        
        # Header Styling
        header_stylesheet = """
            QHeaderView::section {
                background-color: #2c3e50;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """
        self.alarm_table.horizontalHeader().setStyleSheet(header_stylesheet)
        self.alarm_table.setStyleSheet(f"""
            QTableWidget {{
                gridline-color: #ecf0f1;
                border: none;
            }}
            QTableWidget::item {{
                padding: 5px;
                alignment: center;
            }}
            QTableWidget::item:selected {{
                background-color: #d6eaf8;
            }}
        """)
        
        layout.addWidget(self.alarm_table)
        self.table_frame.setLayout(layout)

    def _create_detail_area(self):
        """Erstellt den Detailbereich unten mit konstanter Höhe."""
        self.detail_container = QFrame()
        self.detail_container.setFixedHeight(200)  # Konstante Höhe
        self.detail_container.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
            }}
        """)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # === LINKER DETAIL-CONTAINER (45%) ===
        left_frame = QFrame()
        left_frame.setStyleSheet(f"""
            QFrame {{
                background-color: #f7f8fa;
                border-radius: 6px;
                border: 1px solid #e0e0e0;
            }}
        """)
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(15, 15, 15, 15)
        left_layout.setSpacing(10)
        
        # Titel
        details_title = QLabel("Alarmdetails")
        details_font = QFont()
        details_font.setPointSize(12)
        details_font.setBold(True)
        details_title.setFont(details_font)
        details_title.setStyleSheet(f"color: {config.TEXT_PRIMARY};")
        left_layout.addWidget(details_title)
        
        # Scrollable Detail-Anzeige
        detail_scroll = QScrollArea()
        detail_scroll.setWidgetResizable(True)
        detail_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #f7f8fa;
            }
            QScrollBar:vertical {
                width: 8px;
            }
            QScrollBar::handle:vertical {
                background-color: #bdc3c7;
                border-radius: 4px;
            }
        """)
        
        self.detail_display = QLabel("Kein Alarm ausgewählt")
        self.detail_display.setWordWrap(True)
        self.detail_display.setStyleSheet(f"color: {config.TEXT_SECONDARY}; padding: 5px;")
        detail_scroll.setWidget(self.detail_display)
        
        left_layout.addWidget(detail_scroll)
        left_frame.setLayout(left_layout)
        layout.addWidget(left_frame, 45)
        
        # === RECHTER DETAIL-CONTAINER (55%) - PLATZHALTER ===
        right_frame = QFrame()
        right_frame.setStyleSheet(f"""
            QFrame {{
                background-color: #f7f8fa;
                border-radius: 6px;
                border: 2px dashed #bdc3c7;
            }}
        """)
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignCenter)
        
        placeholder_text = QLabel("Anlagenvisualisierung wird später integriert")
        placeholder_text.setAlignment(Qt.AlignCenter)
        placeholder_text.setStyleSheet(f"color: {config.TEXT_SECONDARY}; font-size: 12pt;")
        right_layout.addWidget(placeholder_text)
        
        right_frame.setLayout(right_layout)
        layout.addWidget(right_frame, 55)
        
        self.detail_container.setLayout(layout)

    def _create_action_bar(self):
        """Erstellt die untere Aktionsleiste."""
        self.action_bar_frame = QFrame()
        self.action_bar_frame.setFixedHeight(60)
        self.action_bar_frame.setStyleSheet(f"""
            QFrame {{
                background-color: #f7f8fa;
                border-top: 1px solid #e0e0e0;
            }}
        """)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(10)
        
        # Linke Buttons
        hide_btn = QPushButton("👁 Details ausblenden")
        hide_btn.setFixedSize(130, 40)
        hide_btn.setStyleSheet(self._button_style("light"))
        layout.addWidget(hide_btn)
        
        print_btn = QPushButton("🖨 Drucken")
        print_btn.setFixedSize(100, 40)
        print_btn.setStyleSheet(self._button_style("light"))
        layout.addWidget(print_btn)
        
        export_btn = QPushButton("💾 Exportieren")
        export_btn.setFixedSize(110, 40)
        export_btn.setStyleSheet(self._button_style("light"))
        layout.addWidget(export_btn)
        
        refresh_btn = QPushButton("🔄 Aktualisieren")
        refresh_btn.setFixedSize(120, 40)
        refresh_btn.clicked.connect(self._populate_table)
        refresh_btn.setStyleSheet(self._button_style("light"))
        layout.addWidget(refresh_btn)
        
        layout.addStretch()
        
        # Rechts: Status
        self.status_label = QLabel()
        self.status_label.setStyleSheet(f"""
            color: {config.DANGER_COLOR};
            font-weight: bold;
            font-size: 11pt;
        """)
        layout.addWidget(self.status_label)
        
        self.action_bar_frame.setLayout(layout)
        self._update_status_label()

    def _populate_table(self):
        """Füllt die Tabelle mit Alarmen basierend auf aktuellem Tab."""
        self.alarm_table.setRowCount(0)
        
        # Bestimme welche Alarme angezeigt werden
        if self.current_tab == "active":
            alarms = self.state_manager.alarm_model.get_active_alarms()
        elif self.current_tab == "history":
            alarms = self.state_manager.alarm_model.get_acknowledged_alarms()
        else:  # stats
            alarms = []
        
        for alarm in alarms:
            row = self.alarm_table.rowCount()
            self.alarm_table.insertRow(row)
            self.alarm_table.setRowHeight(row, 30)  # Konsistente Zeilenhöhe
            
            # Icon basierend auf Severity
            icon_text = self._get_severity_icon(alarm.severity)
            icon_item = QTableWidgetItem(icon_text)
            icon_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.alarm_table.setItem(row, 0, icon_item)
            
            # Zeit
            time_item = QTableWidgetItem(alarm.timestamp.strftime("%H:%M:%S"))
            time_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.alarm_table.setItem(row, 1, time_item)
            
            # Nachricht (left-aligned für Lesbarkeit)
            msg_item = QTableWidgetItem(alarm.message)
            msg_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.alarm_table.setItem(row, 2, msg_item)
            
            # ID
            id_item = QTableWidgetItem(alarm.alarm_id)
            id_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.alarm_table.setItem(row, 3, id_item)
            
            # Beschreibung (left-aligned)
            desc_item = QTableWidgetItem("--")
            desc_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.alarm_table.setItem(row, 4, desc_item)
            
            # Severity Badge (centered)
            severity_badge = QTableWidgetItem(alarm.severity.value)
            severity_badge.setBackground(self._get_severity_color(alarm.severity))
            severity_badge.setForeground(QColor("white"))
            severity_badge.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.alarm_table.setItem(row, 5, severity_badge)
            
            # Status (centered)
            status_text = "Aktiv" if not alarm.acknowledged else "Quittiert"
            status_color = QColor("#e74c3c") if not alarm.acknowledged else QColor("#2ecc71")
            status_item = QTableWidgetItem(status_text)
            status_item.setBackground(status_color)
            status_item.setForeground(QColor("white"))
            status_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.alarm_table.setItem(row, 6, status_item)
            
            # Bereich (centered)
            area_item = QTableWidgetItem("System")
            area_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.alarm_table.setItem(row, 7, area_item)
            
            # Speichere Alarm-Referenz in Zeile
            self.alarm_table.item(row, 0).alarm = alarm

    def _on_table_selection_changed(self):
        """Wird aufgerufen, wenn ein Alarm in der Tabelle ausgewählt wird."""
        rows = self.alarm_table.selectedIndexes()
        if rows:
            row = rows[0].row()
            self.selected_alarm = self.alarm_table.item(row, 0).alarm
            self._display_alarm_details(self.selected_alarm)

    def _display_alarm_details(self, alarm):
        """Zeigt Details eines Alarms."""
        severity_icon = self._get_severity_icon(alarm.severity)
        details_html = f"""
        <b>{severity_icon} {alarm.message}</b><br/>
        <br/>
        <b>Alarm-ID:</b> {alarm.alarm_id}<br/>
        <b>Bereich:</b> System<br/>
        <b>Erst aufgetreten:</b> {alarm.timestamp.strftime("%d.%m.%Y %H:%M:%S")}<br/>
        <b>Zuletzt aufgetreten:</b> {alarm.timestamp.strftime("%d.%m.%Y %H:%M:%S")}<br/>
        <b>Anzahl Ereignisse:</b> 1<br/>
        <br/>
        <b>Beschreibung:</b><br/>
        {alarm.message}<br/>
        <br/>
        <b>Mögliche Ursache:</b><br/>
        Systemüberwachung erforderlich<br/>
        <br/>
        <b>Empfohlene Maßnahme:</b><br/>
        Bitte System überprüfen und Parameter validieren.
        """
        self.detail_display.setText(details_html)

    def _acknowledge_selected(self):
        """Quittiert den ausgewählten Alarm."""
        if self.selected_alarm:
            self.state_manager.alarm_model.acknowledge_alarm(self.selected_alarm.alarm_id)
            self._populate_table()

    def _acknowledge_all(self):
        """Quittiert alle aktiven Alarme."""
        for alarm in self.state_manager.alarm_model.get_active_alarms():
            self.state_manager.alarm_model.acknowledge_alarm(alarm.alarm_id)
        self._populate_table()

    def _switch_tab(self, tab_id):
        """Wechselt zwischen Tabs und zeigt entsprechende Alarme."""
        self.current_tab = tab_id
        self._highlight_tab(tab_id)
        self._populate_table()  # Zeige entsprechende Alarme basierend auf Tab
        self.selected_alarm = None  # Selektion zurücksetzen
        self.detail_display.setText("Kein Alarm ausgewählt")

    def _highlight_tab(self, tab_id):
        """Hebt einen Tab hervor."""
        for tid, btn in self.tab_buttons.items():
            if tid == tab_id:
                btn.setStyleSheet("""
                    QPushButton {
                        background: transparent;
                        border: none;
                        border-bottom: 3px solid #3498db;
                        color: #3498db;
                        font-weight: bold;
                        font-size: 11pt;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background: transparent;
                        border: none;
                        color: #7f8c8d;
                        font-weight: normal;
                        font-size: 11pt;
                    }
                    QPushButton:hover {
                        color: #3498db;
                    }
                """)

    def _update_badge(self):
        """Aktualisiert die Alarm-Badge."""
        count = len(self.state_manager.alarm_model.get_active_alarms())
        self.alarm_badge.setText(str(count))

    def _update_status_label(self):
        """Aktualisiert die Status-Zeile."""
        count = len(self.state_manager.alarm_model.get_active_alarms())
        self.status_label.setText(f"🔴 {count} aktive Alarme")

    def _on_alarm_change(self, *args):
        """Wird aufgerufen, wenn sich Alarme ändern."""
        self._populate_table()  # Zeige aktuelle Tab-Alarme
        self._update_badge()
        self._update_status_label()
        # Wenn aktueller Alarm gelöscht wurde, Details zurücksetzen
        if self.selected_alarm and self.current_tab == "active" and self.selected_alarm not in self.state_manager.alarm_model.get_active_alarms():
            self.selected_alarm = None
            self.detail_display.setText("Kein Alarm ausgewählt")

    def _get_severity_icon(self, severity: AlarmSeverity) -> str:
        """Gibt das Icon für eine Severity zurück."""
        icons = {
            AlarmSeverity.CRITICAL: "🔴",
            AlarmSeverity.ERROR: "🟠",
            AlarmSeverity.WARNING: "🟡",
            AlarmSeverity.INFO: "🔵",
        }
        return icons.get(severity, "⚪")

    def _get_severity_color(self, severity: AlarmSeverity) -> QColor:
        """Gibt die Farbe für eine Severity zurück."""
        colors = {
            AlarmSeverity.CRITICAL: QColor("#e74c3c"),
            AlarmSeverity.ERROR: QColor("#f39c12"),
            AlarmSeverity.WARNING: QColor("#f1c40f"),
            AlarmSeverity.INFO: QColor("#3498db"),
        }
        return colors.get(severity, QColor("#95a5a6"))

    def _button_style(self, style_type: str) -> str:
        """Gibt Button-Styling zurück."""
        styles = {
            "light": """
                QPushButton {
                    background-color: white;
                    border: 1px solid #bdc3c7;
                    border-radius: 5px;
                    padding: 5px;
                    color: #2c3e50;
                    cursor: pointer;
                }
                QPushButton:hover {
                    background-color: #f8f9fa;
                }
            """,
            "light_blue": """
                QPushButton {
                    background-color: #d6eaf8;
                    border: 1px solid #3498db;
                    border-radius: 5px;
                    padding: 5px;
                    color: #3498db;
                    font-weight: bold;
                    cursor: pointer;
                }
                QPushButton:hover {
                    background-color: #aed6f1;
                }
            """,
            "blue": """
                QPushButton {
                    background-color: #3498db;
                    border: none;
                    border-radius: 5px;
                    padding: 5px;
                    color: white;
                    font-weight: bold;
                    cursor: pointer;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """,
        }
        return styles.get(style_type, "")

    def _combobox_style(self) -> str:
        """Gibt Combobox-Styling mit lesbarem Selected State zurück."""
        return """
            QComboBox {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 5px;
                background-color: white;
                color: #2c3e50;
                font-size: 11pt;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
            }
            QComboBox:on {
                background-color: #ecf0f1;
                color: #2c3e50;
            }
            QComboBox:focus {
                border: 2px solid #3498db;
                padding: 4px;
            }
            QComboBox::item {
                padding: 5px;
                color: #2c3e50;
                background-color: white;
            }
            QComboBox::item:selected {
                background-color: #3498db;
                color: white;
                font-weight: bold;
            }
            QComboBox::item:hover {
                background-color: #d6eaf8;
                color: #2c3e50;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: #2c3e50;
                selection-background-color: #3498db;
                selection-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 3px;
            }
        """
