# Quick Start Guide

## Installation

### Schritt 1: Python 3.8+ installiert?
```bash
python --version
```

### Schritt 2: Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```

Die einzige Abhängigkeit ist PySide6:
```
PySide6>=6.6.0
```

## Erste Schritte

### Anwendung starten
```bash
python main.py
```

Dadurch werden zwei Fenster geöffnet:
1. **HMI-Fenster** (1400×850px) - Das Hauptfenster
2. **Simulations-Fenster** (600×800px) - Control Panel

### Tipps zum Herumprobieren

1. **Im HMI-Fenster**:
   - Klicke auf die Icons in der linken Sidebar um zwischen Screens zu wechseln
   - Beobachte die Header-Bar mit Live-Uhrzeit und Anlagenstatus
   - Der Footer zeigt immer den roten STOP-Button

2. **Im Simulations-Fenster**:
   - Bewege die Slider oder gib Werte ein um Temperatur, Druck und Füllstand zu ändern
   - Klicke "Start" um die Anlage zu starten
   - Klicke "Warnung auslösen" oder "Fehler auslösen" um Alarme zu testen
   - Beobachte wie sich das HMI in Echtzeit aktualisiert

3. **Teste den STOP-Button**:
   - Klick auf den roten "🛑 STOP"-Button im HMI-Footer
   - Der Anlagenstatus ändert sich zu "NOTFALL-STOPP"
   - Im AlarmScreen wird ein kritischer Alarm angezeigt

## Dateistruktur verstehen

```
HyGeNa_HMI/
├── main.py                 ← Start hier!
├── config.py               ← Globale Einstellungen
├── requirements.txt        ← Abhängigkeiten
│
├── models/                 ← Datenmodelle
│   ├── plant_state.py     ← Prozessvariablen
│   ├── alarm_model.py     ← Alarme
│   └── maintenance_model.py ← Wartung
│
├── core/                   ← Geschäftslogik
│   ├── state_manager.py   ← Zentrale Verwaltung
│   └── navigation.py      ← Screen-Navigation
│
├── widgets/                ← UI-Komponenten
│   ├── sidebar.py         ← Navigations-Icons
│   ├── header_bar.py      ← Top-Bar
│   ├── footer_bar.py      ← Bottom-Bar + STOP
│   └── ...
│
├── screens/                ← Die verschiedenen Screens
│   ├── home_screen.py     ← Übersicht
│   ├── alarm_screen.py    ← Alarme
│   ├── monitoring_screen.py ← Trends
│   ├── maintenance_screen.py ← Wartung
│   └── settings_screen.py ← Einstellungen
│
└── app/                    ← Hauptfenster
    ├── main_window.py     ← HMI-Fenster
    ├── simulation_window.py ← Control Panel
    └── styles.py          ← Qt Stylesheets
```

## Neuen Screen erstellen (5 Minuten)

### 1. Neue Datei erstellen
```python
# screens/dashboard_screen.py

from screens.base_screen import BaseScreen
from PySide6.QtWidgets import QLabel, QVBoxLayout
from PySide6.QtGui import QFont
import config

class DashboardScreen(BaseScreen):
    def __init__(self, state_manager, navigation, parent=None):
        super().__init__(state_manager, navigation, parent)
        self.setup_ui()
    
    def setup_ui(self):
        title = QLabel("Mein Dashboard")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet(f"color: {config.TEXT_PRIMARY};")
        self.layout.addWidget(title)
        
        # Deine UI hier
        self.layout.addStretch()
```

### 2. Im MainWindow registrieren
```python
# app/main_window.py -> _register_screens()

from screens.dashboard_screen import DashboardScreen

def _register_screens(self):
    self.navigation.register_screen("home", HomeScreen)
    self.navigation.register_screen("alarms", AlarmScreen)
    # ... existing ...
    self.navigation.register_screen("dashboard", DashboardScreen)  # ← Neu
```

### 3. In der Sidebar hinzufügen
```python
# widgets/sidebar.py -> __init__

menu_items = [
    ("home", "🏠", "Startseite"),
    ("alarms", "🔔", "Alarme"),
    ("monitoring", "📊", "Monitoring"),
    ("maintenance", "🔧", "Wartung"),
    ("dashboard", "📈", "Dashboard"),  # ← Neu
    ("settings", "⚙️", "Einstellungen"),
]
```

Fertig! Der neue Screen sollte jetzt in der Navigation verfügbar sein.

## Prozessvariablen hinzufügen

### 1. In PlantState definieren
```python
# models/plant_state.py

class PlantState(QObject):
    # ... existing signals ...
    humidity_changed = Signal(float)  # ← Neu
    
    def __init__(self):
        super().__init__()
        # ... existing ...
        self._humidity = 60.0  # ← Neu
    
    @property
    def humidity(self) -> float:
        return self._humidity
    
    @humidity.setter
    def humidity(self, value: float):
        if self._humidity != value:
            value = max(0.0, min(100.0, value))  # Grenzen: 0-100%
            self._humidity = value
            self.humidity_changed.emit(value)
            self._update_timestamp()
```

### 2. Im Simulations-Fenster kontrollen
```python
# app/simulation_window.py -> setup_ui()

# Humidity Slider
self.humidity_slider = QSlider(Qt.Horizontal)
self.humidity_slider.setMinimum(0)
self.humidity_slider.setMaximum(100)
self.humidity_slider.setValue(60)
self.humidity_slider.valueChanged.connect(self._on_humidity_changed)

process_layout.addRow("Luftfeuchtigkeit:", self.humidity_slider)

# Handler hinzufügen
def _on_humidity_changed(self, value):
    self.state_manager.plant_state.humidity = float(value)
```

### 3. Im Screen anzeigen
```python
# screens/home_screen.py

self.humidity_card = StatusCard("Luftfeuchtigkeit", "60%", "Normal", "💧")
grid_layout.addWidget(self.humidity_card, 2, 0)

# Signal verbinden
self.state_manager.plant_state.humidity_changed.connect(self._update_humidity)

def _update_humidity(self, value):
    self.humidity_card.set_value(f"{value:.0f}%")
```

## Häufig gestellte Fragen

### Q: Wie ändere ich die Fenstergrößen?
A: In `config.py`:
```python
MAIN_WINDOW_WIDTH = 1400  # ← hier ändern
MAIN_WINDOW_HEIGHT = 850  # ← hier ändern

SIMULATION_WINDOW_WIDTH = 600   # ← hier ändern
SIMULATION_WINDOW_HEIGHT = 800  # ← hier ändern
```

### Q: Wie ändere ich die Farben?
A: In `config.py`:
```python
PRIMARY_COLOR = "#3498db"       # Blau
DANGER_COLOR = "#e74c3c"        # Rot
SUCCESS_COLOR = "#2ecc71"       # Grün
# Alle verwendeten Farben sind dort definiert
```

### Q: Wie verbinde ich echte Daten (OPC UA, Modbus)?
A: Erstelle einen Data Source:

```python
# core/data_sources/opc_ua_source.py
from opcua import Client
import threading
import time

class OPCUASource:
    def __init__(self, state_manager, server_url):
        self.state_manager = state_manager
        self.client = Client(server_url)
        self.client.connect()
        
        # Starten eines Background-Threads
        self.running = True
        self.thread = threading.Thread(target=self._update_loop, daemon=True)
        self.thread.start()
    
    def _update_loop(self):
        while self.running:
            try:
                # Temperatur von OPC UA lesen
                temp_node = self.client.get_node("ns=2;i=5")
                temp = temp_node.get_value()
                self.state_manager.plant_state.temperature = temp
                
                time.sleep(1)  # Jede Sekunde aktualisieren
            except Exception as e:
                print(f"OPC UA Error: {e}")
```

Dann in `main.py`:
```python
# Nach StateManager-Erstellung
opc_source = OPCUASource(state_manager, "opc.tcp://localhost:4840")
```

### Q: Wie speichere ich Einstellungen persistent?
A: Nutze JSON:

```python
import json

def save_settings(config_dict, filename="config.json"):
    with open(filename, 'w') as f:
        json.dump(config_dict, f, indent=2)

def load_settings(filename="config.json"):
    with open(filename, 'r') as f:
        return json.load(f)

# In main.py
settings = load_settings()
state_manager.plant_state.temperature = settings.get("default_temp", 20.0)
```

## Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'PySide6'"
**Lösung**: 
```bash
pip install --upgrade PySide6
```

### Problem: Fenster werden nicht angezeigt
**Lösung**: 
- Stelle sicher, dass du `main.py` aus dem Projektverzeichnis startest
- Prüfe ob der absolute Pfad richtig ist

### Problem: UI ist sehr langsam
**Lösung**:
- Reduziere die Anzahl der Signal-Verbindungen
- Optimiere das Rendering (weniger Widgets)
- Nutze einen Timer um UI-Updates zu drosseln

```python
self.update_timer = QTimer()
self.update_timer.timeout.connect(self._update_ui)
self.update_timer.start(500)  # Alle 500ms updaten, nicht bei jedem Signal
```

## Nächste Schritte

1. **Lese ARCHITECTURE.md** für tieferes Verständnis
2. **Erstelle deinen ersten neuen Screen**
3. **Integriere echte Daten** über eine OPC UA, Modbus oder MQTT-Quelle
4. **Passe das Design an** deine Anforderungen
5. **Erweitere die Screens** mit mehr Funktionalität

Viel Spaß!
