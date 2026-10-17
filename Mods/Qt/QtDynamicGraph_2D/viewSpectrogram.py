import numpy as np
import pyqtgraph as pg
from pyqtgraph import useOpenGL

from pyqtgraph.Qt import QtWidgets
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal, Slot, QThread, QObject

class CSpectrogramGLWorker(QObject):
    signal_set_spectrogram       = Signal(int)
    signal_render_spectrogram    = Signal(list)
    signal_clear_spectrogram     = Signal()

    def __init__(self, img : object, parent=None):
        super().__init__(parent)
        self.img = img
        self.data_buffer : np.ndarray = np.zeros((100, 2001))

    @Slot(int)
    def on_signal_set_spectrogram_cb(self, _point : int):
        try:
            self.data_buffer = np.zeros((100, _point), dtype=np.float32)
        except Exception as e:
            print(f"In function on_signal_set_spectrogram_cb: {e}")

    @Slot(list)
    def on_signal_render_spectrogram_cb(self, _list : list):
        try:
            self.data_buffer[:-1, :] = self.data_buffer[1:, :]
            self.data_buffer[-1,:] = np.array(_list)
            self.img.setImage(self.data_buffer, autolevel=False)
        except Exception as e:
            print(f"In function on_signal_render_spectrogram_cb: {e}")

    @Slot()
    def on_signal_clear_spectrogram_cb(self):
        self.data_buffer.fill(0)
        self.img.setImage(self.data_buffer.T, autoLevels=True)

class CSpectrogramGL(QWidget):
    def __init__(self):
        super().__init__()

        pg.setConfigOptions(useOpenGL=True, antialias=False)
        self.view = pg.PlotWidget(useOpenGL=True)
        self.view.setViewport(QtWidgets.QOpenGLWidget())

        self.img = pg.ImageItem()
        self.img.setOpts(axisOrder='row-major')
        self.img.setLookupTable(pg.colormap.get("magma").getLookupTable())
        self.view.addItem(self.img)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.view)

        # 로그를 전시하는 쓰레드
        self.thread = QThread(self)
        self.worker = CSpectrogramGLWorker(self.img)
        self.worker.moveToThread(self.thread)
        self.thread.finished.connect(self.thread.start)
        self.thread.start()

        self.worker.signal_set_spectrogram.connect(self.worker.on_signal_set_spectrogram_cb)
        self.worker.signal_render_spectrogram.connect(self.worker.on_signal_render_spectrogram_cb)
        self.worker.signal_clear_spectrogram.connect(self.worker.on_signal_clear_spectrogram_cb)

    def set_graph(self, _point):
        self.worker.signal_set_spectrogram.emit(_point)

    def render_graph(self, _list):
        self.worker.signal_render_spectrogram.emit(_list)

    def clear_graph(self):
        self.worker.signal_clear_spectrogram.emit()