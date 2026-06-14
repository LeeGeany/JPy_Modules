'''
@brief 로그를 전시하는 view
@details
    * on_clicked_clear() 로그를 전시 하는 기능
    * on_write_msg(_str) 로그를 클리어 하는 기능
@todo.
    1) 체크 박스 onclicked 시 로그를 파일로 저장하는 기능 추가
'''

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, QThread, QObject, pyqtSlot, QMetaObject, Qt, Q_ARG

class CLoggingWorker(QObject):
    sg_send_to_ui = pyqtSignal(str)
    sg_request_clear = pyqtSignal()

    @pyqtSlot(str)
    def on_signal_write_log(self, _str):
        self.sg_send_to_ui.emit(_str)

    @pyqtSlot()
    def on_signal_clear_log(self):
        self.sg_request_clear.emit()


class CLogging(QtWidgets.QTextBrowser):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 로그를 전시하는 쓰레드
        self.thread = QThread(self)
        self.worker = CLoggingWorker(self)
        self.worker.moveToThread(self.thread)
        self.thread.start()

        # 쓰레드로 전달
        self.worker.sg_send_to_ui.connect(self.append)
        self.worker.sg_request_clear.connect(self.clear)


    def on_clicked_clear(self):
        # invokeMethod를 쓰거나, 아래처럼 시그널-슬롯 구조를 유지합니다.
        QMetaObject.invokeMethod(self.worker, "on_signal_clear_log", Qt.QueuedConnection)

    def on_write_msg(self, _str):
        QMetaObject.invokeMethod(self.worker, "on_signal_write_log",
                                 Qt.QueuedConnection,
                                 Q_ARG(str, _str))

    def on_recode_msg(self, _str):
        print("Not Yet")