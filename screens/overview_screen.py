"""
Overview Screen - HyGeNa process overview.
"""

from PySide6.QtCore import Qt, QRect, QPointF, Signal
from PySide6.QtGui import QColor, QPainter, QPen, QPixmap, QPolygonF
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from screens.base_screen import BaseScreen
import config


ICON_PATHS = {
    "renewable_energy": "images/icons/renewable_energy.png",
    "water_treatment": "images/icons/water_treatment.png",
    "electrolysis": "images/icons/electrolysis.png",
    "hydrogen_storage": "images/icons/hydrogen_storage.png",
    "battery_storage": "images/icons/battery_storage.png",
    "ammonia_synthesis": "images/icons/ammonia_synthesis.png",
    "export": "images/icons/export.png",
}

ICON_FALLBACK_PATHS = {
    "renewable_energy": "images/icons/01_Energie.png",
    "water_treatment": "images/icons/02_Wasseraufbereitung.png",
    "electrolysis": "images/icons/03_Elektrolyse.png",
    "hydrogen_storage": "images/icons/04_H2_Speicherung.png",
    "battery_storage": "images/icons/06_Akku_Speicher.png",
    "ammonia_synthesis": "images/icons/05_AmmoniakSynthese.png",
    "export": "images/icons/08_export.png",
}


class ProcessCard(QFrame):
    """Clickable process card with icon, status, and value."""

    clicked = Signal(str)

    def __init__(self, title, icon_path, placeholder, status, value, page_key, parent=None):
        super().__init__(parent)
        self.page_key = page_key
        self._title = title
        self._icon_path = icon_path
        self._placeholder = placeholder
        self._status = status
        self._value = value
        self._pixmap = QPixmap(icon_path)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(self)
        self._layout = layout

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label = title_label
        layout.addWidget(title_label)

        icon_label = QLabel()
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label = icon_label
        layout.addWidget(icon_label)

        status_row = QHBoxLayout()
        status_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_row = status_row

        dot = QLabel()
        self.dot = dot
        status_row.addWidget(dot)

        status_label = QLabel(status)
        self.status_label = status_label
        status_row.addWidget(status_label)
        layout.addLayout(status_row)

        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.value_label = value_label
        layout.addWidget(value_label)
        self.set_display_scale(1.0)

    def set_display_scale(self, scale):
        self.setStyleSheet(f"""
            ProcessCard {{
                background-color: #ffffff;
                border: 1px solid #d6dbe1;
                border-radius: {_px(8, scale)}px;
            }}
            QLabel {{
                background-color: transparent;
                border: none;
            }}
        """)
        self._layout.setContentsMargins(
            _px(14, scale),
            _px(12, scale),
            _px(14, scale),
            _px(12, scale),
        )
        self._layout.setSpacing(_px(6, scale))
        self.title_label.setStyleSheet(f"""
            color: #222831;
            font-size: {_px(15, scale, 11)}px;
            font-weight: 800;
        """)

        icon_size = _px(70, scale, 42)
        self.icon_label.setFixedHeight(_px(62, scale, 38))
        if self._pixmap.isNull():
            margin = _px(38, scale, 12)
            self.icon_label.setText(self._placeholder)
            self.icon_label.setPixmap(QPixmap())
            self.icon_label.setStyleSheet(f"""
                color: #4b5563;
                font-size: {_px(24, scale, 14)}px;
                font-weight: 800;
                border: 1px solid #aab2bd;
                border-radius: {_px(5, scale)}px;
                margin-left: {margin}px;
                margin-right: {margin}px;
            """)
        else:
            self.icon_label.setText("")
            self.icon_label.setStyleSheet("background-color: transparent; border: none;")
            self.icon_label.setPixmap(
                self._pixmap.scaled(
                    icon_size,
                    icon_size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )

        self.status_row.setSpacing(_px(6, scale))
        dot_size = _px(10, scale, 7)
        self.dot.setFixedSize(dot_size, dot_size)
        self.dot.setStyleSheet(f"""
            background-color: #24a148;
            border-radius: {dot_size // 2}px;
        """)
        self.status_label.setStyleSheet(f"""
            color: #1f7a3a;
            font-size: {_px(12, scale, 9)}px;
            font-weight: 800;
        """)
        self.value_label.setStyleSheet(f"""
            color: #4b5563;
            font-size: {_px(13, scale, 10)}px;
            font-weight: 700;
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            print(f"Overview process selected: {self.page_key}")
            self.clicked.emit(self.page_key)
        super().mousePressEvent(event)


class PlantSummaryCard(QFrame):
    """Plant summary panel."""

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        self._layout = layout
        layout.setContentsMargins(0, 0, 0, 12)
        layout.setSpacing(0)

        header = QLabel("PLANT SUMMARY")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header = header
        layout.addWidget(header)

        self.rows = [
            ("PLANT STATUS", "●  RUNNING", "#24a148"),
            ("PLANT AVAILABILITY", "99.9 %", "#222831"),
            ("ACTIVE ALARMS", "0", "#24a148"),
            ("WARNING ALARMS", "0", "#24a148"),
            ("TOTAL POWER DEMAND", "8.4 GW", "#222831"),
            ("BATTERY SOC", "78 %", "#222831"),
        ]

        body = QGridLayout()
        self.body = body
        self.row_labels = []
        self.value_labels = []
        for row, (label, value, color) in enumerate(self.rows):
            name = QLabel(label)
            body.addWidget(name, row, 0)
            self.row_labels.append(name)

            value_label = QLabel(value)
            value_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            body.addWidget(value_label, row, 1)
            self.value_labels.append((value_label, color))
        layout.addLayout(body)
        self.set_display_scale(1.0)

    def set_display_scale(self, scale):
        self.setStyleSheet(f"""
            PlantSummaryCard {{
                background-color: #ffffff;
                border: 1px solid #d6dbe1;
                border-radius: {_px(8, scale)}px;
            }}
            QLabel {{
                background-color: transparent;
                border: none;
            }}
        """)
        self._layout.setContentsMargins(0, 0, 0, _px(12, scale))
        self.header.setFixedHeight(_px(38, scale, 28))
        self.header.setStyleSheet(f"""
            background-color: #edf0f3;
            border-top-left-radius: {_px(8, scale)}px;
            border-top-right-radius: {_px(8, scale)}px;
            color: #222831;
            font-size: {_px(15, scale, 11)}px;
            font-weight: 900;
        """)
        self.body.setContentsMargins(
            _px(16, scale),
            _px(14, scale),
            _px(16, scale),
            0,
        )
        self.body.setHorizontalSpacing(_px(18, scale))
        self.body.setVerticalSpacing(_px(10, scale, 5))
        for label in self.row_labels:
            label.setStyleSheet(f"""
                color: #606975;
                font-size: {_px(12, scale, 8)}px;
                font-weight: 800;
            """)
        for value_label, color in self.value_labels:
            value_label.setStyleSheet(f"""
                color: {color};
                font-size: {_px(13, scale, 9)}px;
                font-weight: 900;
            """)


class KpiCard(QFrame):
    """Bottom KPI card with a main value and progress bar."""

    def __init__(self, title, main_value, rows, progress, parent=None):
        super().__init__(parent)
        self._progress = progress

        layout = QVBoxLayout(self)
        self._layout = layout

        title_label = QLabel(title)
        self.title_label = title_label
        layout.addWidget(title_label)

        value_label = QLabel(main_value)
        self.value_label = value_label
        layout.addWidget(value_label)

        self.row_labels = []
        for label, value in rows:
            row = QHBoxLayout()
            row.setSpacing(8)
            self.row_labels.append((row, None, None))
            left = QLabel(label)
            row.addWidget(left)
            row.addStretch()
            right = QLabel(value)
            row.addWidget(right)
            self.row_labels[-1] = (row, left, right)
            layout.addLayout(row)

        layout.addStretch()
        self.progress_bar = _progress_bar(progress)
        layout.addWidget(self.progress_bar)
        self.set_display_scale(1.0)

    def set_display_scale(self, scale):
        self.setStyleSheet(f"""
            KpiCard {{
                background-color: #ffffff;
                border: 1px solid #d6dbe1;
                border-radius: {_px(8, scale)}px;
            }}
            QLabel {{
                background-color: transparent;
                border: none;
            }}
        """)
        self._layout.setContentsMargins(
            _px(14, scale),
            _px(12, scale),
            _px(14, scale),
            _px(12, scale),
        )
        self._layout.setSpacing(_px(7, scale, 3))
        self.title_label.setStyleSheet(f"""
            color: #222831;
            font-size: {_px(13, scale, 9)}px;
            font-weight: 900;
        """)
        self.value_label.setStyleSheet(f"""
            color: #1677c8;
            font-size: {_px(27, scale, 17)}px;
            font-weight: 900;
        """)
        for row, left, right in self.row_labels:
            row.setSpacing(_px(8, scale))
            left.setStyleSheet(f"""
                color: #606975;
                font-size: {_px(12, scale, 8)}px;
                font-weight: 700;
            """)
            right.setStyleSheet(f"""
                color: #222831;
                font-size: {_px(12, scale, 8)}px;
                font-weight: 800;
            """)
        _style_progress_bar(self.progress_bar, scale)


class StorageLevelsCard(QFrame):
    """Bottom card with hydrogen and ammonia storage levels."""

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        self._layout = layout
        self.storage_rows = []

        title = QLabel("STORAGE LEVELS")
        self.title_label = title
        layout.addWidget(title)
        layout.addSpacing(7)
        self._add_storage_level(layout, "Battery", "1.56 GWh", 78)
        layout.addSpacing(8)
        self._add_storage_level(layout, "Ammonia", "48,600 t", 81)
        layout.addStretch()
        self.set_display_scale(1.0)

    def _add_storage_level(self, layout, label, value, progress):
        row = QHBoxLayout()
        name = QLabel(label)
        row.addWidget(name)
        row.addStretch()
        amount = QLabel(value)
        row.addWidget(amount)
        layout.addLayout(row)
        bar = _progress_bar(progress)
        layout.addWidget(bar)
        self.storage_rows.append((row, name, amount, bar))

    def set_display_scale(self, scale):
        self.setStyleSheet(f"""
            StorageLevelsCard {{
                background-color: #ffffff;
                border: 1px solid #d6dbe1;
                border-radius: {_px(8, scale)}px;
            }}
            QLabel {{
                background-color: transparent;
                border: none;
            }}
        """)
        self._layout.setContentsMargins(
            _px(14, scale),
            _px(12, scale),
            _px(14, scale),
            _px(12, scale),
        )
        self._layout.setSpacing(_px(8, scale, 3))
        self.title_label.setStyleSheet(f"""
            color: #222831;
            font-size: {_px(13, scale, 9)}px;
            font-weight: 900;
        """)
        for row, name, amount, bar in self.storage_rows:
            row.setSpacing(_px(8, scale))
            name.setStyleSheet(f"""
                color: #606975;
                font-size: {_px(12, scale, 8)}px;
                font-weight: 800;
            """)
            amount.setStyleSheet(f"""
                color: #222831;
                font-size: {_px(12, scale, 8)}px;
                font-weight: 900;
            """)
            _style_progress_bar(bar, scale)


class OverviewCanvas(QWidget):
    """Scalable canvas using a 1600 x 777 reference coordinate system."""

    process_selected = Signal(str)

    BASE_WIDTH = 1600
    BASE_HEIGHT = 777

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(1200, 583)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setStyleSheet("background-color: #f6f7f9;")

        self.items = []
        self._create_cards()

    def _create_cards(self):
        self._add_process_card(
            "renewable_energy", QRect(72, 82, 218, 166),
            "RENEWABLE ENERGY", "RE", "AVAILABLE", "14.0 GW",
        )
        self._add_process_card(
            "water_treatment", QRect(390, 82, 218, 166),
            "WATER TREATMENT", "WT", "RUNNING", "437 m³/h",
        )
        self._add_process_card(
            "electrolysis", QRect(708, 82, 218, 166),
            "ELECTROLYSIS", "EL", "RUNNING", "1,050 t/day H₂",
        )
        self._add_process_card(
            "hydrogen_storage", QRect(1026, 82, 218, 166),
            "HYDROGEN STORAGE", "H₂", "RUNNING", "101 t H₂ buffer",
        )
        self._add_process_card(
            "battery_storage", QRect(72, 336, 218, 166),
            "BATTERY STORAGE", "BAT", "CHARGING", "1.56 GWh | 78 %",
        )
        self._add_process_card(
            "ammonia_synthesis", QRect(708, 336, 218, 166),
            "AMMONIA SYNTHESIS", "NH₃", "RUNNING", "5,000 t/day NH₃",
        )
        self._add_process_card(
            "export", QRect(1026, 336, 218, 166),
            "EXPORT", "EXP", "READY", "Export System",
        )

        summary = PlantSummaryCard(self)
        self.items.append((summary, QRect(1280, 72, 290, 240)))

        kpis = [
            KpiCard(
                "HYDROGEN PRODUCTION",
                "1,050 t/day",
                [("Target", "1,050 t/day"), ("Utilization", "100 %")],
                100,
                self,
            ),
            KpiCard(
                "AMMONIA PRODUCTION",
                "5,000 t/day",
                [("Target", "5,000 t/day"), ("Utilization", "100 %")],
                100,
                self,
            ),
            KpiCard(
                "ENERGY DEMAND",
                "8.4 GW",
                [("Electrolysis Load", "7.0 GW"), ("BESS Backup", "8.0 GW")],
                100,
                self,
            ),
            KpiCard(
                "RENEWABLE ENERGY",
                "14.0 GW",
                [("Wind", "10.5 GW"), ("PV", "3.5 GW")],
                92,
                self,
            ),
            StorageLevelsCard(self),
        ]

        x = 72
        for card in kpis:
            self.items.append((card, QRect(x, 586, 282, 148)))
            x += 300

    def _add_process_card(self, page_key, rect, title, placeholder, status, value):
        card = ProcessCard(
            title,
            _icon_path(page_key),
            placeholder,
            status,
            value,
            page_key,
            self,
        )
        card.clicked.connect(self.process_selected)
        self.items.append((card, rect))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._layout_items()

    def _layout_items(self):
        scale, offset_x, offset_y = self._transform()
        for widget, rect in self.items:
            if hasattr(widget, "set_display_scale"):
                widget.set_display_scale(scale)
            widget.setGeometry(
                int(offset_x + rect.x() * scale),
                int(offset_y + rect.y() * scale),
                int(rect.width() * scale),
                int(rect.height() * scale),
            )

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor("#f6f7f9"))

        scale, offset_x, offset_y = self._transform()
        painter.translate(offset_x, offset_y)
        painter.scale(scale, scale)

        pen = QPen(QColor("#4b5563"), 4)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(QColor("#4b5563"))

        arrows = [
            ((290, 165), (390, 165)),
            ((608, 165), (708, 165)),
            ((926, 165), (1026, 165)),
            ((181, 248), (181, 336)),
            ((817, 248), (817, 336)),
            ((926, 419), (1026, 419)),
        ]
        for start, end in arrows:
            self._draw_arrow(painter, QPointF(*start), QPointF(*end))

    def _draw_arrow(self, painter, start, end):
        painter.drawLine(start, end)
        dx = end.x() - start.x()
        dy = end.y() - start.y()
        if abs(dx) >= abs(dy):
            points = [
                QPointF(end.x(), end.y()),
                QPointF(end.x() - 16 if dx > 0 else end.x() + 16, end.y() - 9),
                QPointF(end.x() - 16 if dx > 0 else end.x() + 16, end.y() + 9),
            ]
        else:
            points = [
                QPointF(end.x(), end.y()),
                QPointF(end.x() - 9, end.y() - 16 if dy > 0 else end.y() + 16),
                QPointF(end.x() + 9, end.y() - 16 if dy > 0 else end.y() + 16),
            ]
        painter.drawPolygon(QPolygonF(points))

    def _transform(self):
        scale = min(self.width() / self.BASE_WIDTH, self.height() / self.BASE_HEIGHT)
        offset_x = (self.width() - self.BASE_WIDTH * scale) / 2
        offset_y = (self.height() - self.BASE_HEIGHT * scale) / 2
        return scale, offset_x, offset_y


class OverviewScreen(BaseScreen):
    """HyGeNa overview screen."""

    process_selected = Signal(str)

    def __init__(self, state_manager, navigation, parent=None):
        super().__init__(state_manager, navigation, parent)
        self.setup_ui()

    def setup_ui(self):
        self.setMinimumHeight(620)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.canvas = OverviewCanvas()
        self.canvas.process_selected.connect(self.process_selected)
        self.layout.addWidget(self.canvas, 1)


def _progress_bar(value):
    bar = QProgressBar()
    bar.setRange(0, 100)
    bar.setValue(value)
    bar.setTextVisible(False)
    _style_progress_bar(bar, 1.0)
    return bar


def _style_progress_bar(bar, scale):
    bar.setFixedHeight(_px(9, scale, 6))
    bar.setStyleSheet(f"""
        QProgressBar {{
            background-color: #e5e9ef;
            border: none;
            border-radius: {_px(4, scale, 3)}px;
        }}
        QProgressBar::chunk {{
            background-color: {config.PRIMARY_COLOR};
            border-radius: {_px(4, scale, 3)}px;
        }}
    """)


def _px(value, scale, minimum=1):
    """Scale a reference pixel value while keeping small UI parts legible."""
    return max(minimum, int(round(value * scale)))


def _icon_path(page_key):
    primary = ICON_PATHS[page_key]
    if QPixmap(primary).isNull():
        return ICON_FALLBACK_PATHS.get(page_key, primary)
    return primary
