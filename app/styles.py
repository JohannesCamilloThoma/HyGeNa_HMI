"""
Style Sheets - Zentrale Styling für die Anwendung.
"""


def get_global_stylesheet() -> str:
    """
    Gibt das globale Stylesheet für die gesamte Anwendung zurück.
    """
    return """
    QMainWindow {
        background-color: #ecf0f1;
    }
    
    QWidget {
        font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
        font-size: 11pt;
    }
    
    QLabel {
        color: #2c3e50;
    }
    
    QPushButton {
        border-radius: 5px;
        padding: 5px 10px;
        font-weight: bold;
    }
    
    QTableWidget {
        border-radius: 5px;
        padding: 0px;
    }
    
    QHeaderView::section {
        background-color: #f8f9fa;
        padding: 5px;
        border: none;
        border-right: 1px solid #ecf0f1;
        border-bottom: 1px solid #ecf0f1;
    }
    
    QScrollBar:vertical {
        background-color: #ecf0f1;
        width: 12px;
        margin: 0px;
        padding: 0px;
    }
    
    QScrollBar::handle:vertical {
        background-color: #bdc3c7;
        border-radius: 6px;
        min-height: 20px;
    }
    
    QScrollBar::handle:vertical:hover {
        background-color: #95a5a6;
    }
    
    QScrollBar:horizontal {
        background-color: #ecf0f1;
        height: 12px;
        margin: 0px;
        padding: 0px;
    }
    
    QScrollBar::handle:horizontal {
        background-color: #bdc3c7;
        border-radius: 6px;
        min-width: 20px;
    }
    
    QScrollBar::handle:horizontal:hover {
        background-color: #95a5a6;
    }
    """
