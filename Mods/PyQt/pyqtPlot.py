from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MatplotlibCanvas(QWidget):
    """PyQt5에서 쉽게 사용할 수 있는 Matplotlib 위젯 래퍼 클래스"""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        super().__init__(parent)

        # Matplotlib Figure 및 Canvas 생성
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.figure.add_subplot(111)

        # ✅ Canvas를 Layout에 추가해야 실제 표시됨
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def plot(self, x, y, clear=True, title=None):
        """기본 선 그래프를 그리는 함수"""
        if clear:
            self.axes.clear()
        self.axes.plot(x, y)
        if title:
            self.axes.set_title(title)
        self.canvas.draw()

    def scatter(self, x, y, clear=True, title=None):
        """산점도 그래프"""
        if clear:
            self.axes.clear()
        self.axes.scatter(x, y)
        if title:
            self.axes.set_title(title)
        self.canvas.draw()

    def clear(self):
        """그래프를 초기화"""
        self.axes.clear()
        self.canvas.draw()