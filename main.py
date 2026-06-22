"""
HyGeNa HMI - Professionelle Demonstrations-Anwendung

Hauptanwendung für industrielle HMI/SCADA-ähnliche Benutzeroberfläche
mit separatem Simulations-Control-Panel.
"""

import sys
from PySide6.QtWidgets import QApplication
from core.state_manager import StateManager
from app.main_window import MainWindow
from app.simulation_window import SimulationWindow
from app.styles import get_global_stylesheet


def main():
    """Hauptfunktion der Anwendung."""
    
    # Erstelle QApplication
    app = QApplication(sys.argv)
    
    # Setze globales Stylesheet
    app.setStyleSheet(get_global_stylesheet())
    
    # Erstelle zentralen StateManager
    state_manager = StateManager()
    
    # Erstelle HMI Hauptfenster
    main_window = MainWindow(state_manager)
    main_window.show()
    
    # Erstelle Simulations-Fenster
    simulation_window = SimulationWindow(state_manager)
    simulation_window.show()
    
    # Starte Anwendung
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
