
import pyqtgraph as pg
import numpy as np

from PySide6.QtCore import Slot, QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout

from Qt.QtDynamicGraph.vmDynamicGraph import CViewModelDynamicGraph

class CViewDynamicGraph(QWidget):

    GRAPH_FPS = 30
    GRAPH_INTERVAL_MS = 1000 // GRAPH_FPS

    def __init__(self, parent=None):
        super().__init__(parent)

        self._create_ui()
        self._connect_signals()

        # 최신 그래프 데이터만 보관
        self._pending_data = None

        # GUI 스레드에서 최대 30 Hz로 그래프 갱신
        self._graph_timer = QTimer(self)
        self._graph_timer.setInterval(self.GRAPH_INTERVAL_MS)
        self._graph_timer.timeout.connect(self._update_graph)
        self._graph_timer.start()

        self._view_model = CViewModelDynamicGraph(self, self._plot)

    def _create_ui(self, _style = "line"):
        pg.setConfigOptions(
            useOpenGL=True,
            antialias=False
        )

        self._plot = pg.PlotWidget()
        self._plot.setMouseEnabled(
            x=False,
            y=True
        )
        self._curve = self._plot.plot(
            pen=pg.mkPen(
                color=(255, 255, 0),
                width=2
            ),
            symbol=None
        )

        if _style == "line":
            self._curve.setPen(
                pg.mkPen(color=(255, 255, 0), width=2)
            )
            self._curve.setSymbol(None)
        elif _style == "point":
            self._curve.setPen(None)
            self._curve.setSymbol("o")
            self._curve.setSymbolSize(5)
            self._curve.setSymbolPen(
                pg.mkPen(color=(255, 255, 0), width=1)
            )
            self._curve.setSymbolBrush(
                pg.mkBrush(color=(255, 255, 0))
            )
        elif _style == "both":
            self._curve.setPen(
                pg.mkPen(color=(255, 255, 0), width=2)
            )
            self._curve.setSymbol("o")
            self._curve.setSymbolSize(5)
            self._curve.setSymbolPen(
                pg.mkPen(color=(255, 255, 0), width=1)
            )
            self._curve.setSymbolBrush(
                pg.mkBrush(color=(255, 255, 0))
            )
        else:
            raise ValueError(
                f"Unsupported graph style: {_style}"
            )

        layout = QVBoxLayout(self)
        layout.addWidget(self._plot)


    # ----------------------------------------
    # User Interface
    # ----------------------------------------
    def draw_grid(self, x_grid, y_grid, alpha):
        self._view_model.show_grid(x_grid, y_grid, alpha)

    def draw_graph(self, data):
        self._view_model.set_data(data)

    def set_GridX(self, x_min, x_max):
        self._view_model.set_grid_x(x_min, x_max)

    def set_GridY(self, y_min, y_max):
        self._view_model.set_grid_y(y_min, y_max)

    def draw_vertical_line(self, x):
        self._view_model.show_vertical_line(x)

    def clear(self):
        self._view_model.clear()
