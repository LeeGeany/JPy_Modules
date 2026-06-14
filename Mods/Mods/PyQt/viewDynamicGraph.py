'''
@brief
@details
    *
    *
@todo.
    1)
'''

import pyqtgraph as pg
from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread, QMetaObject, Qt, Q_ARG

class CDynamicGraphWorker(QObject):
    sg_show_grid = pyqtSignal(bool, bool, float)
    sg_show_line = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)

    @pyqtSlot(bool, bool, float)
    def sg_show_grid_cb(self, _x_grid, _y_grid, _alpha):
        self.sg_show_grid.emit(_x_grid, _y_grid, _alpha)

    @pyqtSlot(list)
    def sg_show_line_cb(self, _data):
        self.sg_show_line.emit(_data)

class CDynmaicGraph(QtWidgets.QWidget):
    def __init__(self, _title: str, parent=None):
        super().__init__(parent)

        # 쓰레드 설정
        self.thread = QThread(self)
        self.worker = CDynamicGraphWorker(self)
        self.worker.moveToThread(self.thread)
        self.thread.start()

        self.setWindowTitle(_title)

        # 위젯 설정
        self.layout = QtWidgets.QHBoxLayout(self)

        self.plot = pg.PlotWidget()
        self.plot.setLabel('left', 'Amplitude', units='dB')
        self.plot.setLabel('bottom', 'Frequency', units='Hz')
        self.curve = self.plot.plot(pen=pg.mkPen(color=(0,255,0), width=2))

        self.layout.addWidget(self.plot)

        self.worker.sg_show_grid.connect(self.plot.showGrid)
        self.worker.sg_show_line.connect(self.curve.setData)

    def show_grid(self, _x_grid, _y_grid, _alpha):
        QMetaObject.invokeMethod(self.worker, "sg_show_grid_cb",
                                 Qt.QueuedConnection,
                                 Q_ARG(bool, _x_grid),
                                 Q_ARG(bool, _y_grid),
                                 Q_ARG(float, _alpha),)

    def show_line(self, _data):
        QMetaObject.invokeMethod(self.worker, "sg_show_line_cb",
                                 Qt.QueuedConnection,
                                 Q_ARG(list, _data))