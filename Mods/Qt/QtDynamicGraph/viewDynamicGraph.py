
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

        self._view_model = CViewModelDynamicGraph(self)

        self._create_ui()
        self._connect_signals()

        # 최신 그래프 데이터만 보관
        self._pending_data = None

        # GUI 스레드에서 최대 30 Hz로 그래프 갱신
        self._graph_timer = QTimer(self)
        self._graph_timer.setInterval(self.GRAPH_INTERVAL_MS)
        self._graph_timer.timeout.connect(self._update_graph)
        self._graph_timer.start()

    def _create_ui(self):
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
            )
        )
        self._vertical_line = None



        layout = QVBoxLayout(self)
        layout.addWidget(self._plot)

    def _connect_signals(self):
        self._view_model.signal_grid_changed.connect(
            self._on_grid_changed
        )

        self._view_model.signal_data_changed.connect(
            self._on_data_changed
        )

        self._view_model.signal_x_range_changed.connect(
            self._on_x_range_changed
        )

        self._view_model.signal_y_range_changed.connect(
            self._on_y_range_changed
        )

        self._view_model.signal_vertical_line_changed.connect(
            self._on_vertical_line_changed
        )

        self._view_model.signal_clear.connect(
            self._on_clear
        )

    @Slot(bool, bool, float)
    def _on_grid_changed(self, x_grid, y_grid, alpha):
        self._plot.showGrid(x_grid, y_grid, alpha=alpha)

    @Slot(object)
    def _on_data_changed(self, data):
        # 이 슬롯에서는 그리지 않고 최신 데이터만 저장
        self._pending_data = np.asarray(
            data, dtype=np.float64
        ).reshape(-1)

    @Slot()
    def _update_graph(self):
        if self._pending_data is None:
            return

        data = self._pending_data
        self._pending_data = None

        self._curve.setData(data)

    @Slot(int, int)
    def _on_x_range_changed(self, x_min, x_max):
        self._plot.setXRange(x_min, x_max)

    @Slot(int, int)
    def _on_y_range_changed(self, y_min, y_max):
        self._plot.setYRange(y_min, y_max)

    @Slot(int)
    def _on_vertical_line_changed(self, x):
        if self._vertical_line is not None:
            self._plot.removeItem(self._vertical_line)
        self._vertical_line = pg.InfiniteLine(
            pos=x,
            angle=90,
            movable=False,
            pen=pg.mkPen(
                color=(255, 0, 0),
                width=1
            )
        )
        self._plot.addItem(self._vertical_line)

    @Slot()
    def _on_clear(self):
        self._pending_data = None
        if self._vertical_line is not None:
            self._plot.removeItem(self._vertical_line)
            self._vertical_line = None
        self._curve.clear()

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
