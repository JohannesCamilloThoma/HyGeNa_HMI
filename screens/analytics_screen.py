"""
Analytics screen for energy, production and equipment performance.
"""

from pathlib import Path

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPainterPath, QPen, QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from screens.base_screen import BaseScreen


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
ENERGY_BALANCE_IMAGE = Path(__file__).resolve().parents[1] / "images" / "icons" / "energy_balance.png"


class CardFrame(QFrame):
    """White rounded dashboard card."""

    def __init__(self, title="", parent=None, compact=False):
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
        if compact:
            self.layout.setContentsMargins(8, 8, 8, 8)
            self.layout.setSpacing(0)
        else:
            self.layout.setContentsMargins(16, 12, 16, 12)
            self.layout.setSpacing(8)

        if title:
            title_label = QLabel(title)
            title_label.setStyleSheet("""
                color: #111827;
                font-size: 12pt;
                font-weight: 900;
                border: none;
            """)
            title_label.setWordWrap(True)
            self.layout.addWidget(title_label)


class TrendChartWidget(QWidget):
    """Two stacked lightweight trend charts."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(286)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor("#ffffff"))

        chart_left = 48
        chart_width = max(260, self.width() - 78)
        legend_top = self.height() - 34
        chart_area_bottom = legend_top - 18
        top = QRectF(chart_left, 22, chart_width, max(64, (chart_area_bottom - 58) * 0.50))
        bottom = QRectF(chart_left, top.bottom() + 34, chart_width, max(58, chart_area_bottom - top.bottom() - 52))

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
        painter.save()
        painter.setClipRect(self.rect())
        painter.setPen(QPen(GRID, 1))
        for i in range(5):
            y = rect.top() + rect.height() * i / 4
            painter.drawLine(QPointF(rect.left(), y), QPointF(rect.right(), y))

        painter.setPen(QPen(QColor("#9aa6b2"), 1))
        painter.drawRect(rect)
        self._font(painter, 9, True)
        painter.setPen(MUTED)
        painter.drawText(QRectF(rect.left(), rect.top() - 16, 230, 14), Qt.AlignmentFlag.AlignLeft, label)

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

        self._font(painter, 8)
        painter.setPen(MUTED)
        for i, time in enumerate(TIMES):
            x = rect.left() + rect.width() * i / (len(TIMES) - 1)
            if i % 2 == 0 or i == len(TIMES) - 1:
                painter.drawText(QRectF(x - 22, rect.bottom() + 3, 44, 12), Qt.AlignmentFlag.AlignCenter, time)
        painter.restore()

    def _draw_legend(self, painter):
        items = [
            (BLUE, "H₂ Production (t/h)"),
            (GREEN, "NH₃ Production (t/h)"),
            (PURPLE, "Total Power Demand (GW)"),
            (ORANGE, "Renewable Availability (GW)"),
        ]
        self._font(painter, 8, True)
        col_w = max(220, (self.width() - 86) // 2)
        positions = [
            (46, self.height() - 29),
            (46 + col_w, self.height() - 29),
            (46, self.height() - 13),
            (46 + col_w, self.height() - 13),
        ]
        for (color, label), (x, y) in zip(items, positions):
            painter.setPen(QPen(color, 2.5))
            painter.drawLine(QPointF(x, y - 5), QPointF(x + 22, y - 5))
            painter.setPen(TEXT)
            painter.drawText(QRectF(x + 28, y - 12, col_w - 34, 14), Qt.AlignmentFlag.AlignLeft, label)

    def _font(self, painter, size, bold=False):
        font = QFont("Segoe UI")
        font.setPixelSize(size)
        font.setBold(bold)
        painter.setFont(font)


class EnergyBalanceImage(QWidget):
    """Paints the energy-balance image into all available card space."""

    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self._pixmap = QPixmap(str(image_path))
        self.setMinimumHeight(138)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setStyleSheet("background-color: transparent; border: none;")

    def paintEvent(self, event):
        if self._pixmap.isNull():
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        target = self.rect().adjusted(2, 2, -2, -2)
        scaled = self._pixmap.scaled(
            target.size() * self.devicePixelRatioF(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        scaled.setDevicePixelRatio(self.devicePixelRatioF())
        x = target.x() + (target.width() - scaled.width() / scaled.devicePixelRatio()) / 2
        y = target.y() + (target.height() - scaled.height() / scaled.devicePixelRatio()) / 2
        painter.drawPixmap(QPointF(x, y), scaled)


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
        self.setMinimumHeight(68)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor("#ffffff"))
        self._font(painter, 7, True)
        y = 4
        max_loss = 5.0
        for label, value, pct, color in self.rows:
            painter.setPen(TEXT)
            label_w = min(154, max(112, int(self.width() * 0.42)))
            painter.drawText(QRectF(10, y, label_w, 13), Qt.AlignmentFlag.AlignLeft, label)
            right_w = 92
            bar_left = label_w + 18
            bar = QRectF(bar_left, y + 3, max(58, self.width() - bar_left - right_w - 10), 8)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor("#edf2f7"))
            painter.drawRoundedRect(bar, 6, 6)
            painter.setBrush(color)
            painter.drawRoundedRect(QRectF(bar.left(), bar.top(), bar.width() * value / max_loss, bar.height()), 6, 6)
            painter.setPen(TEXT)
            painter.drawText(QRectF(bar.right() + 8, y, 48, 13), Qt.AlignmentFlag.AlignLeft, f"{value:.1f} t")
            painter.drawText(QRectF(self.width() - 44, y, 38, 13), Qt.AlignmentFlag.AlignRight, pct)
            y += 14
        painter.setPen(QPen(QColor("#e5e7eb"), 1))
        painter.drawLine(QPointF(10, y + 4), QPointF(self.width() - 10, y + 4))
        if y + 42 <= self.height():
            painter.setPen(TEXT)
            painter.drawText(QRectF(10, y + 9, self.width() - 20, 15), Qt.AlignmentFlag.AlignLeft, "24 h loss: 12.5 t H₂")
            painter.setPen(MUTED)
            painter.drawText(QRectF(10, y + 25, self.width() - 20, 15), Qt.AlignmentFlag.AlignLeft, "≈ 1.2 % of daily H₂ production")

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
        self.setMinimumHeight(126)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor("#ffffff"))
        w = self.width()
        cols = [
            12,
            int(w * 0.26),
            int(w * 0.44),
            int(w * 0.55),
            int(w * 0.66),
            int(w * 0.74),
        ]
        headers = ["Asset", "Health", "Status", "RUL", "Trend", "Next Recommendation"]
        self._font(painter, 9, True)
        painter.setPen(MUTED)
        for x, header in zip(cols, headers):
            painter.drawText(QRectF(x, 4, max(54, w - x - 8), 18), Qt.AlignmentFlag.AlignLeft, header)
        y = 22
        for asset, health, status, rul, trend, rec in self.rows:
            painter.setPen(QPen(QColor("#e5e7eb"), 1))
            painter.drawLine(QPointF(8, y - 7), QPointF(self.width() - 8, y - 7))
            self._font(painter, 7, True)
            painter.setPen(TEXT)
            painter.drawText(QRectF(cols[0], y, cols[1] - cols[0] - 10, 16), Qt.AlignmentFlag.AlignLeft, asset)
            health_bar_w = max(70, min(96, cols[2] - cols[1] - 56))
            self._health_bar(painter, QRectF(cols[1], y + 4, health_bar_w, 8), health)
            painter.drawText(QRectF(cols[1] + health_bar_w + 8, y, 44, 16), Qt.AlignmentFlag.AlignLeft, f"{health} %")
            color = GREEN if status == "Normal" else ORANGE
            painter.setPen(color)
            painter.drawText(QRectF(cols[2], y, 90, 16), Qt.AlignmentFlag.AlignLeft, status)
            painter.setPen(TEXT)
            painter.drawText(QRectF(cols[3], y, 90, 16), Qt.AlignmentFlag.AlignLeft, rul)
            painter.setPen(color)
            painter.drawText(QRectF(cols[4], y, 50, 16), Qt.AlignmentFlag.AlignCenter, trend)
            painter.setPen(TEXT)
            painter.drawText(QRectF(cols[5], y, self.width() - cols[5] - 8, 16), Qt.AlignmentFlag.AlignLeft, rec)
            y += 21

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
        self.setMinimumHeight(126)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor("#ffffff"))
        left = QRectF(8, 8, self.width() * 0.49 - 10, self.height() - 16)
        right = QRectF(left.right() + 16, 8, self.width() - left.right() - 24, self.height() - 16)
        self._panel(painter, left, "H₂ Forecast (next 6 h)")
        self._panel(painter, right, "Efficiency Trend")
        self._forecast(painter, left.adjusted(12, 28, -12, -12))
        self._efficiency(painter, right.adjusted(12, 30, -12, -10))

    def _panel(self, painter, rect, title):
        painter.setPen(QPen(QColor("#d7dce3"), 1))
        painter.setBrush(QColor("#fbfcfe"))
        painter.drawRoundedRect(rect, 7, 7)
        self._font(painter, 7 if rect.width() < 210 else 8, True)
        painter.setPen(TEXT)
        painter.drawText(rect.adjusted(10, 7, -10, -7), Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft, title)

    def _forecast(self, painter, rect):
        painter.save()
        painter.setClipRect(self.rect())
        chart = QRectF(rect.left(), rect.top(), rect.width(), max(28, rect.height() - 22))
        self._line_chart(painter, chart, self.forecast, 43.0, 45.4, BLUE)
        labels = ["Now", "+1h", "+2h", "+3h", "+4h", "+5h", "+6h"]
        self._font(painter, 7, True)
        painter.setPen(MUTED)
        for i, label in enumerate(labels):
            x = chart.left() + chart.width() * i / (len(labels) - 1)
            painter.drawText(QRectF(x - 16, chart.bottom() + 3, 32, 12), Qt.AlignmentFlag.AlignCenter, label)
        painter.restore()

    def _efficiency(self, painter, rect):
        self._font(painter, 7, True)
        y = rect.top()
        rows = [
            ("Now", f"{SPECIFIC_ENERGY_KWH_PER_KG} kWh/kg H₂"),
            ("24 h avg", "56.5 kWh/kg H₂"),
            ("Target", "≤ 57 kWh/kg H₂"),
            ("Status", "On target"),
        ]
        row_h = min(18, max(14, int(rect.height() / len(rows))))
        for label, value in rows:
            painter.setPen(MUTED)
            painter.drawText(QRectF(rect.left(), y, rect.width() * 0.42, row_h), Qt.AlignmentFlag.AlignLeft, label)
            painter.setPen(GREEN if value == "On target" else TEXT)
            painter.drawText(QRectF(rect.left() + rect.width() * 0.42, y, rect.width() * 0.58, row_h), Qt.AlignmentFlag.AlignRight, value)
            y += row_h + 3

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

        trend = CardFrame("24 h Trend Analysis")
        period = QLabel("Last 24 hours")
        period.setAlignment(Qt.AlignmentFlag.AlignRight)
        period.setStyleSheet("color: #475569; font-size: 9pt; font-weight: 800; border: none;")
        trend.layout.insertWidget(1, period)
        trend.layout.addWidget(TrendChartWidget(), 1)

        energy = CardFrame(compact=True)
        energy.setMinimumHeight(280)
        energy.layout.addWidget(EnergyBalanceImage(ENERGY_BALANCE_IMAGE), 1)

        losses = CardFrame("Production Loss Analysis")
        losses.layout.addWidget(ProductionLossWidget(), 1)

        health = CardFrame("Predictive Maintenance & Equipment Health")
        health.layout.addWidget(EquipmentHealthTable(), 1)

        forecast = CardFrame("Forecast & Efficiency")
        forecast.layout.addWidget(ForecastEfficiencyWidget(), 1)

        top = QHBoxLayout()
        top.setSpacing(12)
        right_column = QVBoxLayout()
        right_column.setSpacing(12)
        right_column.addWidget(energy, 5)
        right_column.addWidget(losses, 2)
        top.addWidget(trend, 5)
        top.addLayout(right_column, 3)

        bottom = QHBoxLayout()
        bottom.setSpacing(12)
        bottom.addWidget(health, 5)
        bottom.addWidget(forecast, 3)

        root.addLayout(top, 6)
        root.addLayout(bottom, 2)

        self.layout.addWidget(container, 1)
