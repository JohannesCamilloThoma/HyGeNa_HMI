# HyGeNa HMI - Professionelle Demonstrations-Anwendung

Eine moderne, industrielle HMI/SCADA-ähnliche Benutzeroberfläche in Python mit flexibler, modularer Softwarearchitektur.

## 🎯 Übersicht

HyGeNa HMI ist eine professionelle Demo-Anwendung, die zwei separate Fenster zeigt:

1. **HMI-Fenster** - Benutzeroberfläche für den Anlagenoperator
2. **Simulations-/Control-Fenster** - Zur Manipulation von simulierten Prozessdaten

Die Architektur ist so gestaltet, dass sie später leicht um echte Prozessdatenquellen (OPC UA, Modbus, MQTT) erweitert werden kann.

## 🏗️ Projektstruktur

```
HyGeNa_HMI/
├── main.py                      # Einstiegspunkt
├── config.py                    # Globale Konfiguration
├── requirements.txt             # Python-Abhängigkeiten
│
├── app/                         # Hauptanwendung
│   ├── __init__.py
│   ├── main_window.py          # HMI-Hauptfenster
│   ├── simulation_window.py    # Simulations-Control-Panel
│   └── styles.py               # Qt Stylesheets
│
├── core/                        # Geschäftslogik & State Management
│   ├── __init__.py
│   ├── state_manager.py        # Zentrale Zustandsverwaltung
│   └── navigation.py           # Screen-Navigation
│
├── models/                      # Datenmodelle
│   ├── __init__.py
│   ├── plant_state.py          # Anlagenzustände
│   ├── alarm_model.py          # Alarmverwaltung
│   └── maintenance_model.py    # Wartungsverwaltung
│
├── widgets/                     # Wiederverwendbare UI-Komponenten
│   ├── __init__.py
│   ├── icon_button.py          # Icon-Button für Sidebar
│   ├── sidebar.py              # Navigations-Sidebar
│   ├── header_bar.py           # Header mit Systeminformationen
│   ├── footer_bar.py           # Footer mit STOP-Button
│   ├── content_container.py    # Dynamischer Content-Bereich
│   └── status_card.py          # Wiederverwendbare Status-Cards
│
└── screens/                     # HMI-Screens
    ├── __init__.py
    ├── base_screen.py          # Basis-Klasse für alle Screens
    ├── home_screen.py          # Startseite / Übersicht
    ├── alarm_screen.py         # Alarmverwaltung
    ├── monitoring_screen.py    # Advanced Monitoring & Trends
    ├── maintenance_screen.py   # Wartungsverwaltung
    └── settings_screen.py      # Einstellungen
```

## 🚀 Installation & Start

### 1. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 2. Anwendung starten

```bash
python main.py
```

Dies startet zwei Fenster:
- **HMI-Fenster** (1400×850px) - Die Benutzeroberfläche
- **Simulations-Fenster** (600×800px) - Control Panel für Tests

## 🎨 HMI-Layout

### Strukturaufbau

```
┌─────────────────────────────────────────────┐
│ SIDEBAR │        HEADER-BAR                 │
│         ├─────────────────────────────────────┤
│  🏠     │                                     │
│  🔔     │        CONTENT CONTAINER            │
│  📊     │    (Dynamischer Screen-Bereich)    │
│  🔧     │                                     │
│  ⚙️     ├─────────────────────────────────────┤
│         │  Status     ...     🛑 STOP-Button │
│         └─────────────────────────────────────┘
```

### Komponenten

#### Sidebar (links)
- **Breite**: 90px
- **Profile Avatar**: Oben (👤)
- **Menu Icons**: 
  - 🏠 Startseite (Home Screen)
  - 🔔 Alarme (Alarm Screen)
  - 📊 Monitoring (Monitoring Screen)
  - 🔧 Wartung (Maintenance Screen)
  - ⚙️ Einstellungen (Settings Screen)
- **Highlight**: Aktiver Screen wird blau hervorgehoben

#### Header-Bar (oben)
- **Höhe**: 70px
- **Links**: Screen-Titel (z.B. "Übersicht", "Alarme")
- **Mitte**: Aktuelle Uhrzeit und Datum (live aktualisiert)
- **Rechts**: Anlagenstatus, Logo-Bereich

#### Content Container (Mitte)
- **Dynamischer Bereich**: Zeigt den aktuell ausgewählten Screen
- **Design**: Großer weißer Container mit Padding und abgerundeten Ecken
- **Hintergrund**: Helles Grau (#ecf0f1)

#### Footer-Bar (unten)
- **Höhe**: 70px
- **Links**: Statustext (z.B. "Keine aktiven Alarme", "NOTFALL-STOPP aktiviert")
- **Rechts**: Roter STOP-Button (🛑 STOP)

## 📱 Verfügbare Screens

### 1. Home Screen (Übersicht)
Zeigt die wichtigsten Anlagenwerte in Status-Cards:
- Temperatur (mit Warnstufen)
- Druck
- Füllstand
- Systemstatus
- Pumpenstatus
- Aktive Alarme

### 2. Alarm Screen
- Tabelle aller aktiven Alarme
- Spalten: Zeit, Alarm-ID, Nachricht, Schweregrad
- Live-Updates bei neuen Alarmen

### 3. Monitoring Screen
- KPI-Anzeige (Uptime, Effizienz, Zyklusanzahl)
- Platzhalter für Diagramme und Trends
- Vorbereitet für Echtzeit-Datenvisualisierung

### 4. Maintenance Screen
- Tabelle aller Wartungsaufgaben
- Anzeige des Status (OK, WARNING, DUE, OVERDUE)
- "Abgeschlossen"-Buttons für jede Aufgabe
- Automatische Berechnung der nächsten Fälligkeit

### 5. Settings Screen
- Systemeinstellungen (Refresh-Intervall, Auto-Start)
- Alarmeinstellungen (E-Mail-Warnungen, Filter)
- Wartungseinstellungen (Warnfrist)
- Reset- und Speicher-Buttons

## 🎮 Simulations-/Control-Panel

Das Simulations-Fenster ermöglicht die Manipulation aller Prozessvariablen:

### Prozessvariablen
- **Temperatur**: Slider (-50°C bis +150°C) + Eingabefeld
- **Druck**: Slider (0-10 bar) + Eingabefeld
- **Füllstand**: Slider (0-100%) + Eingabefeld

### Ausrüstungsstatus
- **Pumpe**: Checkbox zum Ein-/Ausschalten
- **Systemsteuerung**: Start, Stop, Notfall-Stopp Buttons

### Alarm-Simulation
- **Warnung auslösen**: Trigger für Test-Warnung
- **Fehler auslösen**: Trigger für Test-Fehler
- **Alle Alarme löschen**: Löscht alle aktiven Alarme

### System-Aktionen
- **Auf Standard zurücksetzen**: Setzt alle Werte zurück

## 🏗️ Architektur-Highlights

### State Management
```python
StateManager
├── PlantState          # Prozessvariablen + Signale
├── AlarmModel          # Alarmverwaltung
└── MaintenanceModel    # Wartungsaufgaben
```

Das `StateManager`-Objekt ist zentral und wird allen Screens übergeben. Changes werden über Qt-Signale propagiert.

### Observer Pattern
Alle Screens registrieren sich auf StateManager-Signale:
```python
state_manager.plant_state.temperature_changed.connect(self._update_temperature)
state_manager.alarm_model.alarm_added.connect(self._update_alarms)
```

### Navigation System
Das `Navigation`-Objekt verwaltet Screen-Übergänge:
```python
navigation.register_screen("home", HomeScreen)
navigation.navigate_to("home")  # Wechselt zu Home Screen
```

### Screen-Architektur
Alle Screens erben von `BaseScreen`:
```python
class MyScreen(BaseScreen):
    def __init__(self, state_manager, navigation, parent=None):
        super().__init__(state_manager, navigation, parent)
        self.setup_ui()
```

Dies garantiert konsistente Struktur und einfache Erweiterbarkeit.

## 🔧 Erweiterung - Neue Screens hinzufügen

### 1. Neue Screen-Klasse erstellen

```python
# screens/custom_screen.py
from screens.base_screen import BaseScreen
from PySide6.QtWidgets import QLabel, QVBoxLayout
from PySide6.QtGui import QFont

class CustomScreen(BaseScreen):
    def __init__(self, state_manager, navigation, parent=None):
        super().__init__(state_manager, navigation, parent)
        self.setup_ui()
    
    def setup_ui(self):
        title = QLabel("Mein Custom Screen")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        self.layout.addWidget(title)
        self.layout.addStretch()
```

### 2. Screen registrieren

```python
# In app/main_window.py -> _register_screens()
from screens.custom_screen import CustomScreen

def _register_screens(self):
    # ... existing screens ...
    self.navigation.register_screen("custom", CustomScreen)
```

### 3. Menu-Icon hinzufügen

```python
# In widgets/sidebar.py -> setup_ui()
menu_items = [
    ("home", "🏠", "Startseite"),
    ("alarms", "🔔", "Alarme"),
    # ... existing ...
    ("custom", "🎨", "Mein Screen"),  # Neu hinzufügen
]
```

## 🔌 Integration echten Prozessdaten

Die Architektur ist vorbereitet für echte Datenquellen.

### Beispiel: OPC UA Integration

```python
# core/data_sources/opc_ua_source.py
from opcua import Client

class OPCUADataSource:
    def __init__(self, state_manager, server_url):
        self.state_manager = state_manager
        self.client = Client(server_url)
        self.client.connect()
    
    def read_temperature(self):
        return self.client.get_node("ns=2;i=5").get_value()
    
    def update_from_server(self):
        temp = self.read_temperature()
        self.state_manager.plant_state.temperature = temp
```

Dann in `main.py`:
```python
from core.data_sources.opc_ua_source import OPCUADataSource

state_manager = StateManager()
opc_source = OPCUADataSource(state_manager, "opc.tcp://localhost:4840")
# Starten eines Daten-Update-Timers
```

## 🎨 Design & Styling

### Farben
```python
PRIMARY_COLOR = "#3498db"       # Blau
DANGER_COLOR = "#e74c3c"        # Rot
SUCCESS_COLOR = "#2ecc71"       # Grün
WARNING_COLOR = "#f39c12"       # Orange
TEXT_PRIMARY = "#2c3e50"        # Dunkelgrau
TEXT_SECONDARY = "#7f8c8d"      # Hellgrau
BG_PRIMARY = "#ecf0f1"          # Hellgrau (Background)
BG_SECONDARY = "#ffffff"        # Weiß (Cards)
```

### Schriftgrößen
- Titel: 16pt
- Header: 14pt
- Body: 11pt
- Small: 9pt

### Komponenten-Styling
Alle Qt Stylesheets sind zentral in `app/styles.py` definiert für konsistentes Design.

## 📊 Konfiguration

Alle Konstanten sind in `config.py` definiert:

```python
# Window Configuration
MAIN_WINDOW_WIDTH = 1400
MAIN_WINDOW_HEIGHT = 850

# Sidebar Configuration
SIDEBAR_WIDTH = 90

# Default Values
DEFAULT_TEMPERATURE = 20.0
DEFAULT_PRESSURE = 1.0
DEFAULT_FILL_LEVEL = 50.0
```

## 🔒 Sicherheitshinweise

Bei der Integration echten Prozessdaten beachten:

1. **Authentifizierung**: Verschlüsselte Verbindungen (TLS/SSL)
2. **Zugriffskontrolle**: Rollen-basierte Berechtigungen
3. **Audit-Logging**: Alle Änderungen protokollieren
4. **Emergency Stop**: Immer hardwire-sicher implementieren
5. **Fehlerbehandlung**: Graceful Degradation bei Verbindungsverlust

## 📝 Lizenz & Kontakt

Diese Demo-Anwendung ist für Lern- und Demonstrationszwecke gedacht.

---

**Version**: 1.0.0  
**Letztes Update**: Juni 2026  
**Framework**: PySide6 / Qt6
Human Machine Interface for the HyGeNa Project
