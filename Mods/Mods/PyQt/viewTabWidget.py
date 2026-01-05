from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, QThread, QObject, pyqtSlot, QMetaObject, Qt, Q_ARG

class CTabWidgetWorker(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

class CTabWidget(QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        ''' stacked 데이터를 저장하는 딕션너리'''
        self.pages = {}

        ''' '''
        self.thread = QThread(self)
        self.worker = CTabWidgetWorker(self)
        self.worker.moveToThread(self.thread)
        self.thread.start()

    def addStacked(self, _name: str, _widget: QtWidgets.QWidget):
        if _name in self.pages:
            print(f"Warning: '{_name}' 이름의 페이지가 이미 존재합니다.")
            index = None
        else:
            index = self.addTab(_widget, _name)
            self.pages[_name] = index
        return index