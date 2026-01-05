from PyQt5 import QtWidgets

class CLine(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(CLine, self).__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)
