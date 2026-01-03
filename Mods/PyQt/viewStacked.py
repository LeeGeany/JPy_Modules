from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, QThread, QObject, pyqtSlot, QMetaObject, Qt, Q_ARG

class CStackedWorker(QObject):
    sg_switch_stacked_no    = pyqtSignal(int)
    sg_remove_stacked_no    = pyqtSignal(int)

    @pyqtSlot(int)
    def on_switch_stacked_no(self, _no):
        self.sg_switch_stacked_no.emit(_no)

    @pyqtSlot(QtWidgets.QWidget)
    def on_remove_stacked_no(self, _widget):
        self.sg_remove_stacked_no.emit(_widget)

class CStacked(QtWidgets.QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        ''' stacked 데이터를 저장하는 딕션너리'''
        self.pages = {}

        ''' '''
        self.thread = QThread(self)
        self.worker = CStackedWorker(self)
        self.worker.moveToThread(self.thread)
        self.thread.start()

        ''' '''
        self.worker.sg_switch_stacked_no.connect(self.setCurrentIndex)
        self.worker.sg_remove_stacked_no.connect(self.removeWidget)


    def addStacked(self, _name: str, _widget: QtWidgets.QWidget):
        if _name in self.pages:
            print(f"Warning: '{_name}' 이름의 페이지가 이미 존재합니다.")
            index = None
        else:
            index = self.addWidget(_widget)
            self.pages[_name] = index
        return index


    def removeStacked(self, _name: str):
        self.index = self.pages[_name]
        self.wg = self.widget(self.index_)

        QMetaObject.invokeMethod(self.worker, "sg_remove_stacked_no",
                                 Qt.QueuedConnection,
                                 Q_ARG(QtWidgets.QWidget, self.wg))

        self.wg.deleteLater()
        del self.pages[_name]


    def removeAllStacked(self):
        for key, value in self.pages.items():
            self.removeStacked(key)


    def switchStacked(self, _name : str):
        for key, value in self.pages.items():
            if key == _name:
                QMetaObject.invokeMethod(self.worker, "on_switch_stacked_no",
                                         Qt.QueuedConnection,
                                         Q_ARG(int, value))
            else:
                print(f"Error: '{_name}' 이름의 페이지를 찾을 수 없습니다.")

