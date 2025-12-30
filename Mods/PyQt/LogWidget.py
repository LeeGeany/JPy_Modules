from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSignal, QThread, QObject, pyqtSlot

class CLoggingWorker(QObject):
    sg_write_log = pyqtSignal(str)
    sg_clear_log = pyqtSignal()

    def __init__(self, _obj : object, parent=None):
        super().__init__(parent)
        self.obj = _obj

    '''
        @brief  로그를 입력하는 콜백 함수
        @detail 여기 _obj로 전제 CModalConnection 객체를 전달 받는다.
    '''
    @pyqtSlot(str)
    def on_signal_write_log(self, str):
        self.obj.tb_log.setMarkdown(str)

    '''
        @brief  연결 종료 버튼이 클릭되면 실행되는 함수
        @detail 여기 _obj로 전제 CModalConnection 객체를 전달 받는다.
    '''
    @pyqtSlot()
    def on_signal_clear_log(self):
        self.obj.tb_log.setMarkdown('')


class CLogging(QtWidgets.QTextBrowser):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("../UIs/Logging.ui", self)

        # 쓰레드 생성부
        self.thread = QThread(self)
        self.worker = CLoggingWorker(self, self)
        self.worker.moveToThread(self.thread)

        # 시그널 연결부
        self.worker.sg_write_log.connect(self.worker.on_signal_write_log)
        self.worker.sg_clear_log.connect(self.worker.on_signal_clear_log)

        # 버튼 연결 부
        self.pb_clear.clicked.connect(self.on_clicked_clear)

        self.thread.start()



    def closeEvent(self, event):
        self.thread.quit()

        if not self.thread.wait(2000):  # 최대 2초 대기
            self.thread.terminate()  # 안 끝나면 강제 종료
            self.thread.wait()

        event.accept()

    def on_clicked_clear(self):
        self.worker.sg_clear_log.emit()

    def writeLog(self, _str):
        self.worker.sg_write_log.emit(_str)