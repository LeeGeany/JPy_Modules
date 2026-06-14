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
from PyQt5.QtCore import QStringListModel, pyqtSignal, QThread, QObject, pyqtSlot, QMetaObject, Qt, Q_ARG

class CListViewWorker(QObject):
    sg_list_refresh     = pyqtSignal(object)

    def __init__(self):
        super().__init__()

    @pyqtSlot(object)
    def on_refresh_list(self, _obj):
        self.sg_list_refresh.emit(_obj)


class CItemList(QtWidgets.QListView):  # QListView를 직접 상속
    def __init__(self, parent=None):
        super().__init__(parent)

        # 데이터 리스트
        self.nameList = []

        # 이벤트 수행 하는 쓰레드
        self.thread = QThread()
        self.worker = CListViewWorker()
        self.worker.moveToThread(self.thread)
        self.thread.start()

        # 리스트에 주입할 모델 생성
        self.model = QStringListModel()

        # 시그널 연결
        self.worker.sg_list_refresh.connect(self.setModel)

    def addList(self, _listName : str):
        self.nameList.append(_listName)

    def addAllList(self, _listAllname : list):
        self.nameList = _listAllname

    def removeList(self, _idx : int):
        if self.nameList:
            self.nameList.pop(_idx)

    def removeAllList(self):
        self.nameList.clear()

    def selectIndex(self):
        return self.currentIndex()

    def refreshList(self):
        self.model.setStringList(self.nameList)
        QMetaObject.invokeMethod(self.worker, "on_refresh_list",
                                 Qt.QueuedConnection,
                                 Q_ARG(object, self.model))
