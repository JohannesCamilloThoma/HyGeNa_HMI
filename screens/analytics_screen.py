"""
Analytics screen for energy, production and equipment performance.
"""

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPainterPath, QPen, QPolygonF
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from screens.base_screen import BaseScreen
import config


H2_TARGET_TPD = 1050
H2_AVG_TPH = 43.8
NH3_TARGET_TPD = 5000
NH3_AVG_TPH = 208.3
TOTAL_POWER_DEMAND_GW = 8.4
ELECTROLYSIS_LOAD_GW = 7.0
RENEWABLE_INSTALLED_GW = 14.0
RENEWABLE_AVAILABLE_GW = 9.1
BESS_CAPACITY_GWH = 2.0
BESS_DISCHARGE_GW = 8.0
BESS_SOC_PERCENT = 78
SPECIFIC_ENERGY_KWH_PER_KG = 56

TIMES = ["00:00", "03:00", "06:00", "09:00", "12:00", "15:00", "18:00", "21:00", "24:00"]
H2_TPH = [41, 42, 44, 45, 43, 44, 46, 44, 43]
NH3_TPH = [198, 202, 208, 211, 205, 209, 214, 210, 207]
POWER_GW = [8.1, 8.2, 8.4, 8.5, 8.3, 8.4, 8.6, 8.4, 8.3]
RENEWABLE_GW = [8.8, 9.5, 11.2, 12.6, 10.4, 11.8, 13.2, 10.7, 9.1]

BLUE = QColor("#1f77b4")
TEAL = QColor("#159895")
GREEN = QColor("#2ca02c")
PURPLE = QColor("#7f52d9")
ORANGE = QColor("#f0a202")
RED = QColor("#d94f3d")
TEXT = QColor("#1f2937")
MUTED = QColor("#6b7280")
GRID = QColor("#dfe5ec")


class CardFrame(QFrame):
    """White rounded dashboard card."""

    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            CardFrame {
                background-color: #ffffff;
                border: 1px solid #d7dce3;
                border-radius: 8px;
            }
            QLabel {
                background-color: transparent;
                border: none;
            }
        """)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(14, 12, 14, 12)
        self.layout.setSpacing(10)

        title_label = QLabel(title)
        title_label.setStyleSheet("""
            color: #111827;
            font-size: 12pt;
            font-weight: 900;
            border: none;
        """)
        self.layout.addWidget(title_label)


class TrendChartWidget(QWidget):
    """Two stacked lightweight trend charts."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(330)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor("#ffffff"))

        top = QRectF(46, 12, self.width() - 70, (self.height() - 74) * 0.52)
        bottom = QRectF(46, top.bottom() + 44, self.width() - 70, (self.height() - 74) * 0.36)

        self._draw_chart(
            painter,
            top,
            "Production (t/h)",
            [(H2_TPH, BLUE, "H₂ Production (t/h)"), (NH3_TPH, GREEN, "NH₃ Production (t/h)")],
            35,
            220,
        )
        self._draw_chart(
            painter,
            bottom,
            "Power / availability (GW)",
            [(POWER_GW, PURPLE, "Total Power Demand (GW)"), (RENEWABLE_GW, ORANGE, "Renewable Availability (GW)")],
            7.5,
            14.0,
        )
        self._draw_legend(painter)

    def _draw_chart(self, painter, rect, label, series, min_v, max_v):
        painter.setPen(QPen(GRID, 1))
        for i in range(5):
            y = rect.top() + rect.height() * i / 4
            painter.drawLine(QPointF(rect.left(), y), QPointF(rect.right(), y))

        painter.setPen(QPen(QColor("#9aa6b2"), 1))
        painter.drawRect(rect)
        self._font(painter, 10, True)
        painter.setPen(MUTED)
        painter.drawText(QRectF(rect.left(), rect.top() - 18, 230, 16), Qt.AlignmentFlag.AlignLeft, label)

        for data, color, _ in series:
            path = QPainterPath()
            for i, value in enumerate(data):
                x = rect.left() + rect.width() * i / (len(data) - 1)
                y = rect.bottom() - ((value - min_v) / (max_v - min_v)) * rect.height()
                if i == 0:
                    path.moveTo(x, y)
                else:
                    path.lineTo(x, y)
            painter.setPen(QPen(color, 2.4))
            painter.drawPath(path)

        self._font(painter, 9)
        painter.setPen(MUTED)
        for i, time in enumerate(TIMES):
            x = rect.left() + rect.width() * i / (len(TIMES) - 1)
            if i % 2 == 0 or i == len(TIMES) - 1:
                painter.drawText(QRectF(x - 22, rect.bottom() + 4, 44, 16), Qt.AlignmentFlag.AlignCenter, time)

    def _draw_legend(self, painter):
        items = [
            (BLUE, "H₂ Production (t/h)"),
            (GREEN, "NH₃ Production (t/h)"),
            (PURPLE, "Total Power Demand (GW)"),
            (ORANGE, "Renewable Availability (GW)"),
        ]
        self._font(painter, 9, True)
        positions = [
            (46, self.height() - 34),
            (280, self.height() - 34),
            (46, self.height() - 16),
            (280, self.height() - 16),
        ]
        for (color, label), (x, y) in zip(items, positions):
            painter.setPen(QPen(color, 2.5))
            painter.drawLine(QPointF(x, y - 5), QPointF(x + 22, y - 5))
            painter.setPen(TEXT)
            painter.drawText(QRectF(x + 28, y - 14, 230, 18), Qt.AlignmentFlag.AlignLeft, label)

    def _font(self, painter, size, bold=False):
        font = QFont("Segoe UI")
        font.setPixelSize(size)
        font.setBold(bold)
        painter.setFont(font)


class EnergyBalanceWidget(QWidget):
    """Simple energy-flow and demand breakdown widget."""

    rows = [
        ("Electrolysis", 7.00, "83.3 %", BLUE),
        ("Utilities / BOP", 0.75, "8.9 %", TEAL),
        ("Compression", 0.35, "4.2 %", PURPLE),
        ("BESS Smoothing", 0.12, "1.4 %", ORANGE),
        ("Cooling Auxiliaries", 0.08, "1.0 %", GREEN),
        ("Control & HMI", 0.10, "1.2 %", QColor("#64748b")),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(230)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor("#ffffff"))
        w = self.width()

        left = QRectF(12, 48, 98, 72)
        mid = QRectF(142, 48, 106, 72)
        surplus = QRectF(142, 148, 106, 46)

        self._box(painter, left, QColor("#e8f5ee"), GREEN, ["Renewable", "Available", "9.1 GW", "of 14.0 GW installed"])
        self._box(painter, mid, QColor("#e8f2fb"), BLUE, ["Plant Demand", "8.4 GW"])
        self._box(painter, surplus, QColor("#fff8e7"), ORANGE, ["Surplus / Charging", "0.7 GW"])
        self._arrow(painter, QPointF(left.right(), left.center().y()), QPointF(mid.left(), mid.center().y()), BLUE)
        self._arrow(painter, QPointF(left.center().x(), left.bottom()), QPointF(surplus.left(), surplus.center().y()), ORANGE)

        x0 = 266
        y = 18
        for label, gw, percent, color in self.rows:
            row_rect = QRectF(x0, y, max(150, w - x0 - 10), 28)
            painter.setPen(QPen(QColor("#e5e7eb"), 1))
            painter.setBrush(QColor("#f8fafc"))
            painter.drawRoundedRect(row_rect, 5, 5)
            painter.setBrush(color)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(QRectF(row_rect.left(), row_rect.top(), row_rect.width() * gw / TOTAL_POWER_DEMAND_GW, row_rect.height()), 5, 5)
            self._font(painter, 7, True)
            painter.setPen(TEXT)
            painter.drawText(row_rect.adjusted(6, 0, -58, 0), Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, label)
            painter.drawText(row_rect.adjusted(6, 0, -6, 0), Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight, f"{gw:.2f} GW  {percent}")
            y += 31

    def _box(self, painter, rect, fill, border, lines):
        painter.setPen(QPen(border, 1.5))
        painter.setBrush(fill)
        painter.drawRoundedRect(rect, 6, 6)
        self._font(painter, 9, True)
        painter.setPen(TEXT)
        line_h = 15
        start = rect.center().y() - (len(lines) * line_h) / 2
        for i, line in enumerate(lines):
            painter.drawText(QRectF(rect.left() + 6, start + i * line_h, rect.width() - 12, line_h), Qt.AlignmentFlag.AlignCenter, line)

    def _arrow(self, painter, start, end, color):
        painter.setPen(QPen(color, 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.setBrush(color)
        painter.drawLine(start, end)
        painter.drawPolygon(QPolygonF([end, QPointF(end.x() - 10, end.y() - 6), QPointF(end.x() - 10, end.y() + 6)]))

    def _font(self, painter, size, bold=False):
        font = QFont("Segoe UI")
        font.setPixelSize(size)
        font.setBold(bold)
        painter.setFont(font)


class ProductionLossWidget(QWidget):
    """Horizontal loss bars."""

    rows = [
        ("Renewable limitation", 5.0, "40 %", BLUE),
        ("Planned maintenance", 3.2, "26 %", TEAL),
        ("Cooling derating", 2.4, "19 %", ORANGE),
        ("Alarm-related slowdown", 1.2, "10 %", QColor("#7aa6d9")),
        ("Quality hold", 0.7, "5 %", QColor("#94a3b8")),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(190)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor("#ffffff"))
        self._font(painter, 9, True)
        y = 16
        max_loss = 5.0
        for label, value, pct, color in self.rows:
            painter.setPen(TEXT)
            painter.drawText(QRectF(10, y, 160, 18), Qt.AlignmentFlag.AlignLeft, label)
            bar = QRectF(178, y + 3, self.width() - 288, 12)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor("#edf2f7"))
            painter.drawRoundedRect(bar, 6, 6)
            painter.setBrush(color)
            painter.drawRoundedRect(QRectF(bar.left(), bar.top(), bar.width() * value / max_loss, bar.height()), 6, 6)
            painter.setPen(TEXT)
            painter.drawText(QRectF(bar.right() + 10, y, 62, 18), Qt.AlignmentFlag.AlignLeft, f"{value:.1f} t")
            painter.drawText(QRectF(self.width() - 50, y, 44, 18), Qt.AlignmentFlag.AlignRight, pct)
            y += 28
        painter.setPen(QPen(QColor("#e5e7eb"), 1))
        painter.drawLine(QPointF(10, y + 4), QPointF(self.width() - 10, y + 4))
        painter.setPen(TEXT)
        painter.drawText(QRectF(10, y + 16, self.width() - 20, 18), Qt.AlignmentFlag.AlignLeft, "Total estimated loss (24 h): 12.5 t H₂")
        painter.setPen(MUTED)
        painter.drawText(QRectF(10, y + 38, self.width() - 20, 18), Qt.AlignmentFlag.AlignLeft, "≈ 1.2 % of daily H₂ production")

    def _font(self, painter, size, bold=False):
        font = QFont("Segoe UI")
        font.setPixelSize(size)
        font.setBold(bold)
        painter.setFont(font)


class EquipmentHealthTable(QWidget):
    """Predictive maintenance table."""

    rows = [
        ("Electrolyzer Stacks", 91, "Normal", "230 days", "↗", "Inspect in 30 days"),
        ("Cooling System", 84, "Normal", "160 days", "→", "Clean filters in 14 days"),
        ("Power Converter", 88, "Normal", "190 days", "↗", "Thermal check in 30 days"),
        ("Feedwater Pump", 76, "Watch", "95 days", "↘", "Check seals in 7 days"),
        ("Compressor", 72, "Watch", "80 days", "↘", "Vibration inspection in 14 days"),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(220)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor("#ffffff"))
        cols = [12, 190, 360, 470, 600, 690]
        headers = ["Asset", "Health", "Status", "RUL", "Trend", "Next Recommendation"]
        self._font(painter, 9, True)
        painter.setPen(MUTED)
        for x, header in zip(cols, headers):
            painter.drawText(QRectF(x, 4, 170, 18), Qt.AlignmentFlag.AlignLeft, header)
        y = 32
        for asset, health, status, rul, trend, rec in self.rows:
            painter.setPen(QPen(QColor("#e5e7eb"), 1))
            painter.drawLine(QPointF(8, y - 7), QPointF(self.width() - 8, y - 7))
            self._font(painter, 10, True)
            painter.setPen(TEXT)
            painter.drawText(QRectF(cols[0], y, 170, 20), Qt.AlignmentFlag.AlignLeft, asset)
            self._health_bar(painter, QRectF(cols[1], y + 4, 100, 10), health)
            painter.drawText(QRectF(cols[1] + 110, y, 44, 20), Qt.AlignmentFlag.AlignLeft, f"{health} %")
            color = GREEN if status == "Normal" else ORANGE
            painter.setPen(color)
            painter.drawText(QRectF(cols[2], y, 90, 20), Qt.AlignmentFlag.AlignLeft, status)
            painter.setPen(TEXT)
            painter.drawText(QRectF(cols[3], y, 90, 20), Qt.AlignmentFlag.AlignLeft, rul)
            painter.setPen(color)
            painter.drawText(QRectF(cols[4], y, 50, 20), Qt.AlignmentFlag.AlignCenter, trend)
            painter.setPen(TEXT)
            painter.drawText(QRectF(cols[5], y, self.width() - cols[5] - 8, 20), Qt.AlignmentFlag.AlignLeft, rec)
            y += 34

    def _health_bar(self, painter, rect, value):
        color = GREEN if value > 80 else ORANGE if value >= 70 else RED
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#e5e7eb"))
        painter.drawRoundedRect(rect, 5, 5)
        painter.setBrush(color)
        painter.drawRoundedRect(QRectF(rect.left(), rect.top(), rect.width() * value / 100, rect.height()), 5, 5)

    def _font(self, painter, size, bold=False):
        font = QFont("Segoe UI")
        font.setPixelSize(size)
        font.setBold(bold)
        painter.setFont(font)


class ForecastEfficiencyWidget(QWidget):
    """Forecast and efficiency mini panels."""

    forecast = [43.8, 44.0, 43.5, 44.2, 45.0, 44.6, 44.1]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(220)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor("#ffffff"))
        left = QRectF(8, 8, self.width() * 0.48 - 12, self.height() - 16)
        right = QRectF(left.right() + 16, 8, self.width() - left.right() - 24, self.height() - 16)
        self._panel(painter, left, "Expected H₂ Production (next 6 h)")
        self._panel(painter, right, "Efficiency Trend")
        self._forecast(painter, left.adjusted(14, 34, -14, -14))
        self._efficiency(painter, right.adjusted(14, 34, -14, -14))

    def _panel(self, painter, rect, title):
        painter.setPen(QPen(QColor("#d7dce3"), 1))
        painter.setBrush(QColor("#fbfcfe"))
        painter.drawRoundedRect(rect, 7, 7)
        self._font(painter, 10, True)
        painter.setPen(TEXT)
        painter.drawText(rect.adjusted(12, 8, -12, -8), Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft, title)

    def _forecast(self, painter, rect):
        chart = QRectF(rect.left(), rect.top(), rect.width(), rect.height() * 0.55)
        self._line_chart(painter, chart, self.forecast, 43.0, 45.4, BLUE)
        labels = ["Now", "+1h", "+2h", "+3h", "+4h", "+5h", "+6h"]
        self._font(painter, 8, True)
        painter.setPen(MUTED)
        for i, label in enumerate(labels):
            x = chart.left() + chart.width() * i / (len(labels) - 1)
            painter.drawText(QRectF(x - 18, chart.bottom() + 4, 36, 14), Qt.AlignmentFlag.AlignCenter, label)

    def _efficiency(self, painter, rect):
        self._font(painter, 8, True)
        y = rect.top()
        rows = [
            ("Specific energy now", f"{SPECIFIC_ENERGY_KWH_PER_KG} kWh/kg H₂"),
            ("24 h average", "56.5 kWh/kg H₂"),
            ("Target", "≤ 57 kWh/kg H₂"),
            ("Status", "On target"),
        ]
        for label, value in rows:
            painter.setPen(MUTED)
            painter.drawText(QRectF(rect.left(), y, rect.width() * 0.50, 22), Qt.AlignmentFlag.AlignLeft, label)
            painter.setPen(GREEN if value == "On target" else TEXT)
            painter.drawText(QRectF(rect.left() + rect.width() * 0.50, y, rect.width() * 0.50, 22), Qt.AlignmentFlag.AlignRight, value)
            y += 30

    def _line_chart(self, painter, rect, data, min_v, max_v, color):
        painter.setPen(QPen(GRID, 1))
        for i in range(3):
            y = rect.top() + rect.height() * i / 2
            painter.drawLine(QPointF(rect.left(), y), QPointF(rect.right(), y))
        path = QPainterPath()
        for i, value in enumerate(data):
            x = rect.left() + rect.width() * i / (len(data) - 1)
            y = rect.bottom() - ((value - min_v) / (max_v - min_v)) * rect.height()
            if i == 0:
                path.moveTo(x, y)
            else:
                path.lineTo(x, y)
        painter.setPen(QPen(color, 2.4))
        painter.drawPath(path)

    def _font(self, painter, size, bold=False):
        font = QFont("Segoe UI")
        font.setPixelSize(size)
        font.setBold(bold)
        painter.setFont(font)


class AnalyticsScreen(BaseScreen):
    """Analytics dashboard screen."""

    def __init__(self, state_manager, navigation, parent=None):
        super().__init__(state_manager, navigation, parent)
        self.setup_ui()

    def setup_ui(self):
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        container = QWidget()
        container.setStyleSheet("background-color: #f6f7f9;")
        root = QVBoxLayout(container)
        root.setContentsMargins(18, 16, 18, 18)
        root.setSpacing(12)

        header = QHBoxLayout()
        title_col = QVBoxLayout()
        title = QLabel("Analytics")
        title.setStyleSheet("font-size: 24pt; font-weight: 900; color: #111827; border: none;")
        subtitle = QLabel("Energy, production and equipment performance")
        subtitle.setStyleSheet("font-size: 10pt; font-weight: 600; color: #6b7280; border: none;")
        title_col.addWidget(title)
        title_col.addWidget(subtitle)
        header.addLayout(title_col)
        header.addStretch()
        back = QPushButton("Back to Overview")
        back.clicked.connect(lambda: self.navigation.navigate_to("home"))
        back.setCursor(Qt.CursorShape.PointingHandCursor)
        back.setStyleSheet(f"""
            QPushButton {{
                background-color: #ffffff;
                border: 1px solid #b8c2cc;
                border-radius: 6px;
                color: {config.TEXT_PRIMARY};
                font-weight: 800;
                padding: 8px 14px;
            }}
            QPushButton:hover {{
                background-color: #edf4fb;
            }}
        """)
        header.addWidget(back)
        root.addLayout(header)

        grid = QGridLayout()
        grid.setSpacing(10)

        trend = CardFrame("24 h Trend Analysis")
        period = QLabel("Last 24 hours")
        period.setAlignment(Qt.AlignmentFlag.AlignRight)
        period.setStyleSheet("color: #475569; font-size: 9pt; font-weight: 800; border: none;")
        trend.layout.insertWidget(1, period)
        trend.layout.addWidget(TrendChartWidget(), 1)

        energy = CardFrame("Energy Balance")
        energy.layout.addWidget(EnergyBalanceWidget(), 1)

        losses = CardFrame("Production Loss Analysis")
        losses.layout.addWidget(ProductionLossWidget(), 1)

        health = CardFrame("Predictive Maintenance & Equipment Health")
        health.layout.addWidget(EquipmentHealthTable(), 1)

        forecast = CardFrame("Forecast & Efficiency")
        forecast.layout.addWidget(ForecastEfficiencyWidget(), 1)

        grid.addWidget(trend, 0, 0, 2, 2)
        grid.addWidget(energy, 0, 2, 1, 1)
        grid.addWidget(losses, 1, 2, 1, 1)
        grid.addWidget(health, 2, 0, 1, 2)
        grid.addWidget(forecast, 2, 2, 1, 1)
        grid.setColumnStretch(0, 3)
        grid.setColumnStretch(1, 3)
        grid.setColumnStretch(2, 4)
        grid.setRowStretch(0, 3)
        grid.setRowStretch(1, 2)
        grid.setRowStretch(2, 3)
        root.addLayout(grid, 1)

        self.layout.addWidget(container, 1)
