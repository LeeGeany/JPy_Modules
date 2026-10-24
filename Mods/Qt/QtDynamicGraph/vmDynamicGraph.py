
import numpy as np

from PySide6.QtCore import QObject, Signal, Slot
class CViewModelDynamicGraph(QObject):

    signal_data_changed             = Signal(object)
    signal_grid_changed             = Signal(bool, bool, float)
    signal_x_range_changed          = Signal(int, int)
    signal_y_range_changed          = Signal(int, int)
    signal_vertical_line_changed    = Signal(int)
    signal_clear                    = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self._data = np.empty(0, dtype=np.float64)

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
