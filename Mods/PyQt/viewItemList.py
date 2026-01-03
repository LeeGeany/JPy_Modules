'''
@brief  file 읽어오는 view
@details
    *
    *
    *
@todo.
    1)
@dependency
    *
'''

from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot , QThread

class CListViewWorker(QObject):
    sg_add_item     = pyqtSignal()

    def __init__(self):
        super().__init__()

    @pyqtSlot()
    def addItem(self):
        print("addItem")

class CListView(QtWidgets.QListView):  # QListView를 직접 상속
    def __init__(self, parent=None):
        super().__init__(parent)

        self.thread = QThread()
        self.worker = CListViewWorker()
        self.worker.moveToThread(self.thread)

        # 모델 설정 (상속받았으므로 self.setModel을 직접 호출)
        self.model = QStandardItemModel()
        self.setModel(self.model)

    def add_item(self, text, data=None):
        self.worker.sg_add_item.connect(self.worker.addItem)


