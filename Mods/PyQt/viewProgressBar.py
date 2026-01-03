'''
@brief  프로그래스 바 view
@details
    * 객체 생성 시 title, 수행 함수 등록 하면 thread로 수행한다.
    * 전체 함수 실행이 정상 적으로 끝나면 sg_isDone을 emit 하여 외부에 종료를 알린다.
@todo.
    1) 없음
'''
from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot , QThread

class CProgressBarWorker(QObject):
    sg_finished     = pyqtSignal(object)
    sg_progress     = pyqtSignal(int)
    sg_error        = pyqtSignal(str)

    def __init__(self, func):
        super().__init__()
        self.func = func  # 실행할 함수 객체

    @pyqtSlot()
    def run(self):
        try:
            # 인자 전달 없이, 오직 진행률 콜백 함수 하나만 넘겨줍니다.
            result = self.func(self.sg_progress.emit)
            self.sg_finished.emit(result)
        except Exception as e:
            self.sg_error.emit(str(e))

class CProgressBar(QtWidgets.QProgressDialog):
    def __init__(self, title, func):
        super().__init__()

        # 다이얼로그 객체 설정
        self.setWindowTitle(title)
        self.setLabelText("작업을 시작합니다")
        self.setRange(0, 100)
        self.setModal(True)
        self.setMinimumDuration(0)

        # 쓰레드 및 워커 설정
        self.thread = QThread()
        self.worker = CProgressBarWorker(func)
        self.worker.moveToThread(self.thread)

        # 시그널 연결
        self.thread.started.connect(self.worker.run)
        self.worker.sg_progress.connect(self.setValue)
        self.worker.sg_finished.connect(self.on_finished)
        self.worker.sg_error.connect(self.on_error)

        # 취소 버튼 클릭 시 처리
        self.canceled.connect(self.on_canceled)

    def run(self):
        self.thread.start()
        self.exec_()

    def on_finished(self, result):
        self.thread.quit()
        self.thread.wait()
        self.accept()
        QtWidgets.QMessageBox.information(self, "완료", "완료")

    def on_error(self, err_msg):
        self.thread.quit()
        self.thread.wait()
        QtWidgets.QMessageBox.critical(self, "오류", err_msg)
        self.reject()

    def on_canceled(self):
        if self.thread.isRunning():
            self.thread.terminate()
            self.thread.wait()