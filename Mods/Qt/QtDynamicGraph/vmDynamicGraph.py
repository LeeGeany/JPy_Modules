
import numpy as np

from PySide6.QtCore import QObject, Signal, Slot
class CViewModelDynamicGraph(QObject):

    signal_grid_changed             = Signal(bool, bool, float)
    signal_data_changed             = Signal(object)
    signal_x_range_changed          = Signal(int, int)
    signal_y_range_changed          = Signal(int, int)
    signal_vertical_line_changed    = Signal(int)
    signal_clear                    = Signal()

    def __init__(self, _ui, parent=None):
        super().__init__(parent)

        self._data = np.empty(0, dtype=np.float64)
        self._ui = _ui

        self.signal_grid_changed.connect(
            self.on_signal_grid_changed
        )

        self.signal_data_changed.connect(
            self._on_data_changed
        )

        self.signal_x_range_changed.connect(
            self._on_x_range_changed
        )

        self.signal_y_range_changed.connect(
            self._on_y_range_changed
        )

        self.signal_vertical_line_changed.connect(
            self._on_vertical_line_changed
        )

        self.signal_clear.connect(
            self._on_clear
        )

    @Slot(bool, bool, float)
    def on_signal_grid_changed(self, x_grid, y_grid, alpha):
        self._ui.showGrid(x_grid, y_grid, alpha=alpha)


    @Slot(bool, bool, float)
    def show_grid(self, x_grid, y_grid, alpha):
        self.signal_grid_changed.emit(x_grid, y_grid, alpha)

    @Slot(object)
    def set_data(self, data):
        if data is None:
            return

        try:
            # list, tuple, np.array, np.ndarray 모두 지원
            array = np.asarray(data, dtype=np.float32).copy()

            # 그래프는 1차원 데이터만 처리
            if array.ndim != 1:
                array = array.reshape(-1)

            self._data = array
            self.signal_data_changed.emit(array)

        except (TypeError, ValueError, OverflowError) as exc:
            print(f"[Graph] 데이터 변환 실패: {exc}")

    @Slot(int, int)
    def set_grid_x(self, x_min, x_max):
        self.signal_x_range_changed.emit(x_min, x_max)

    @Slot(int, int)
    def set_grid_y(self, y_min, y_max):
        self.signal_y_range_changed.emit(y_min, y_max)

    @Slot(int)
    def show_vertical_line(self, x):
        self.signal_vertical_line_changed.emit(x)

    @Slot()
    def clear(self):
        self.signal_clear.emit()


    @Slot(str)
    def _on_et_graph_style(self, style: str):
        """
        그래프 표시 방식 설정

        style:
            "line"   : 선만 표시
            "point"  : 점만 표시
            "both"   : 선과 점 모두 표시
        """





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
