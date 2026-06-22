# Architektur-Dokumentation

## Überblick

Die HyGeNa HMI-Anwendung folgt einer **sauberen, modularen Architektur** mit klarer Trennung von Concerns:

```
┌─────────────────────────────────────────────────────────┐
│                   Presentation Layer                    │
│  (MainWindow, Screens, Widgets, SimulationWindow)       │
└─────────────────────────────────────────────────────────┘
                            ↕ (Signale)
┌─────────────────────────────────────────────────────────┐
│                    Business Logic Layer                 │
│  (StateManager, Navigation, Alarms, Maintenance)        │
└─────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────┐
│                     Data Model Layer                    │
│  (PlantState, AlarmModel, MaintenanceModel)             │
└─────────────────────────────────────────────────────────┘
```

## Schichten-Modell

### 1. Data Model Layer (Datenmodelle)
**Dateien**: `models/plant_state.py`, `models/alarm_model.py`, `models/maintenance_model.py`

**Verantwortung**:
- Speicherung von Zustandsdaten
- Validierung von Eingaben (Min/Max-Grenzen)
- Emission von Qt-Signalen bei Änderungen
- Keine UI-Logik

**Beispiel - PlantState**:
```python
class PlantState(QObject):
    temperature_changed = Signal(float)  # Signal
    
    @property
    def temperature(self) -> float:
        return self._temperature
    
    @temperature.setter
    def temperature(self, value: float):
        # Validierung
        value = max(-50.0, min(150.0, value))
        if self._temperature != value:
            self._temperature = value
            self.temperature_changed.emit(value)  # Signal
```

**Vorteile**:
- Können unabhängig von UI getestet werden
- Mehrere UIs können gleichzeitig darauf zugreifen
- Leicht zu mockchen für Tests

### 2. Business Logic Layer (Geschäftslogik)
**Dateien**: `core/state_manager.py`, `core/navigation.py`

**StateManager**:
- Orchestriert alle Sub-Models (PlantState, AlarmModel, MaintenanceModel)
- Reagiert auf State-Änderungen (z.B. kritischer Alarm → Notfall-Stopp)
- Bietet High-Level-API: `start_plant()`, `stop_plant()`, `trigger_emergency_stop()`

**Navigation**:
- Verwaltet verfügbare Screens
- Koordiniert Screen-Übergänge
- Bietet Mapping: Screen-Name → Screen-Klasse

```python
# StateManager-Beispiel
state_manager.plant_state.system_state_changed.connect(
    self._on_system_state_changed
)

def _on_system_state_changed(self, state):
    if state == "EMERGENCY_STOP":
        self.emergency_stop_triggered.emit()
```

### 3. Presentation Layer (Präsentation)
**Dateien**: `app/main_window.py`, `screens/`, `widgets/`

**Struktur**:
```
MainWindow
├── Sidebar (Navigation)
├── Header-Bar (Systeminformationen)
├── ContentContainer
│   └── Current Screen (Home, Alarms, etc.)
└── Footer-Bar (Status + STOP-Button)
```

**Screens** erben von BaseScreen:
```python
class HomeScreen(BaseScreen):
    def setup_ui(self):
        # UI aufbauen
        title = QLabel("System-Übersicht")
        self.layout.addWidget(title)
    
    def _on_state_changed(self):
        # Reagiert auf State-Änderungen
        self._update_all()
```

## Datenfluss

### 1. Simulation → HMI
```
SimulationWindow (User bewegt Slider)
    ↓
state_manager.plant_state.temperature = 25.0  (Setter)
    ↓
PlantState emittiert temperature_changed Signal
    ↓
HomeScreen verbunden auf temperature_changed
    ↓
HomeScreen aktualisiert UI
    ↓
Header und andere Screens aktualisieren auch
```

### 2. STOP-Button → Emergency Stop
```
FooterBar.stop_pressed Signal
    ↓
MainWindow._on_stop_pressed()
    ↓
StateManager.trigger_emergency_stop()
    ↓
plant_state.system_state = "EMERGENCY_STOP"
    ↓
Alarm hinzufügen
    ↓
Alle Screens aktualisieren
```

### 3. Screen-Navigation
```
Sidebar.screen_selected("monitoring")
    ↓
Navigation.navigate_to("monitoring")
    ↓
Navigation.screen_changed Signal emittiert
    ↓
MainWindow._on_screen_changed()
    ↓
MonitoringScreen wird erstellt
    ↓
ContentContainer zeigt neuen Screen
    ↓
Header-Titel wird aktualisiert
```

## Signal-Architektur (Qt Signals & Slots)

Alle Komponenten kommunizieren über Qt-Signale:

```
┌──────────────────┐     Temperature Changed     ┌──────────────┐
│  PlantState      │ ─────────────────────────→ │ HomeScreen   │
└──────────────────┘                            └──────────────┘

┌──────────────────┐     Alarm Added            ┌──────────────┐
│  AlarmModel      │ ─────────────────────────→ │ AlarmScreen  │
└──────────────────┘                            └──────────────┘

┌──────────────────┐     Screen Changed         ┌──────────────┐
│  Navigation      │ ─────────────────────────→ │ MainWindow   │
└──────────────────┘                            └──────────────┘
```

**Vorteil**: 
- Lose Kopplung zwischen Komponenten
- Listener können dynamisch hinzugefügt/entfernt werden
- Keine direkten Abhängigkeiten

## Dependency Injection

Alle Screens erhalten ihre Abhängigkeiten als Parameter:

```python
# MainWindow bei Screen-Erstellung
screen_widget = screen_class(
    self.state_manager,      # Dependency
    self.navigation,         # Dependency
    parent=self
)

# Screen kann damit arbeiten
class HomeScreen(BaseScreen):
    def __init__(self, state_manager, navigation, parent=None):
        super().__init__(state_manager, navigation, parent)
        # state_manager ist verfügbar
        self.state_manager.plant_state.temperature_changed.connect(...)
```

**Vorteile**:
- Screens können leicht mit Mock-Objekten getestet werden
- Keine globalen Variablen
- Explizite Abhängigkeiten

## Erweiterungspunkte

### 1. Neue Screens
```python
# 1. Neue Klasse erstellen
class ReportScreen(BaseScreen):
    def setup_ui(self):
        ...

# 2. Registrieren
navigation.register_screen("reports", ReportScreen)

# 3. Zur Sidebar hinzufügen
menu_items.append(("reports", "📄", "Reports"))
```

### 2. Neue Prozessvariablen
```python
# In models/plant_state.py
class PlantState(QObject):
    humidity_changed = Signal(float)
    
    @property
    def humidity(self) -> float:
        return self._humidity
    
    @humidity.setter
    def humidity(self, value: float):
        value = max(0.0, min(100.0, value))
        if self._humidity != value:
            self._humidity = value
            self.humidity_changed.emit(value)
```

### 3. Datenquellen (OPC UA, Modbus, etc.)
```python
# core/data_sources/modbus_source.py
from pymodbus.client import ModbusClient

class ModbusDataSource:
    def __init__(self, state_manager, host, port):
        self.state_manager = state_manager
        self.client = ModbusClient(host=host, port=port)
    
    def read_and_update(self):
        temp = self.client.read_holding_registers(100, 1)[0]
        self.state_manager.plant_state.temperature = temp / 100.0
```

Dann in `main.py`:
```python
from core.data_sources.modbus_source import ModbusDataSource
import threading

state_manager = StateManager()
modbus = ModbusDataSource(state_manager, "192.168.1.100", 502)

# Starten eines Update-Threads
def update_loop():
    while True:
        modbus.read_and_update()
        time.sleep(1)

thread = threading.Thread(target=update_loop, daemon=True)
thread.start()
```

### 4. Neue Alarme
```python
# In screens oder data sources
from models.alarm_model import AlarmSeverity

if temp > 100:
    state_manager.alarm_model.add_alarm(
        "TEMP_HIGH",
        "Temperatur überschreitet Grenzwert!",
        AlarmSeverity.WARNING
    )
```

### 5. Persistenz (Datenspeicherung)
```python
# core/persistence.py
import json

class ConfigManager:
    def save_state(self, state_manager, filename):
        data = state_manager.get_all_state()
        with open(filename, 'w') as f:
            json.dump(data, f)
    
    def load_state(self, state_manager, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        # Daten zurück in state_manager schreiben
```

## Error Handling

Die Anwendung sollte robust gegen Fehler sein:

```python
try:
    value = float(user_input)
    state_manager.plant_state.temperature = value
except ValueError:
    self.show_error("Ungültige Eingabe")
except Exception as e:
    logger.error(f"Fehler beim Setzen der Temperatur: {e}")
    state_manager.alarm_model.add_alarm(
        "SYSTEM_ERROR",
        f"Fehler: {str(e)}",
        AlarmSeverity.ERROR
    )
```

## Testing

Die modulare Architektur ermöglicht einfaches Testen:

```python
# test_plant_state.py
import pytest
from models.plant_state import PlantState

def test_temperature_setter():
    state = PlantState()
    
    # Signal-Test
    signal_emitted = []
    state.temperature_changed.connect(lambda v: signal_emitted.append(v))
    
    state.temperature = 25.0
    assert state.temperature == 25.0
    assert signal_emitted == [25.0]

def test_temperature_bounds():
    state = PlantState()
    
    # Grenzen-Test
    state.temperature = 200.0  # Über Maximum
    assert state.temperature == 150.0  # Gekürzt auf Maximum
```

## Performance-Überlegungen

1. **Screen-Rekonstruktion**: Screens werden bei jedem Wechsel neu erstellt
   - **Optimierung**: Screens cachen (bei Bedarf)
   
2. **Signal-Flut**: Zu viele Signale können Performance beeinträchtigen
   - **Optimierung**: Throttling von Update-Signalen

3. **UI-Updates**: Direktes Aktualisieren von vielen UI-Elementen
   - **Optimierung**: Batch-Updates nutzen

## Zusammenfassung

Die Architektur bietet:
- ✅ **Modulare Struktur**: Klare Trennung der Concerns
- ✅ **Erweiterbarkeit**: Neue Screens und Features einfach hinzufügbar
- ✅ **Testbarkeit**: Komponenten können isoliert getestet werden
- ✅ **Wartbarkeit**: Klare Datenflüsse und Abhängigkeiten
- ✅ **Skalierbarkeit**: Vorbereitet für echte Datenquellen
