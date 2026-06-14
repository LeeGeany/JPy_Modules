"""
@brief
@date
@version
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser, QPushButton
from PySide6.QtCore import Signal, Slot, QObject, QThread
from PySide6.QtGui import QTextCursor

from Utils.utilTimeStamp import time_stamp

class CViewLogBrowserWorker(QObject):
    signal_log_to_base    = Signal(str)
    signal_clear_to_base  = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot(str)
    def on_signal_log_write(self, text):
        current_ : str = time_stamp()
        log_ = f"[{current_}] {text}"
        self.signal_log_to_base.emit(log_)

    @Slot()
    def on_signal_log_clear(self):
        self.signal_clear_to_base.emit()

class CViewLogBrowser(QWidget):
    signal_log_to_worker    = Signal(str)
    signal_clear_to_worker  = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        ### UI 초기 설정(위젯 생성 및 배치)
        self.layer = QVBoxLayout(self)

        self.browser_log    = QTextBrowser(self)
        self.browser_log.document().setMaximumBlockCount(1000)

        self.pb_clear       = QPushButton("Clear")

        self.layer.addWidget(self.browser_log)
        self.layer.addWidget(self.pb_clear)

        ### Worker 및 Thread 설정
        self.worker = CViewLogBrowserWorker()
        self.thread = QThread(self)
        self.worker.moveToThread(self.thread)
        self.thread.finished.connect(self.worker.deleteLater)
        self.thread.start()

        ### 시그널/슬롯 연결 (Thread-Safe 통신)
        self.signal_log_to_worker.connect(self.worker.on_signal_log_write)
        self.signal_clear_to_worker.connect(self.worker.on_signal_log_clear)

        self.worker.signal_log_to_base.connect(self.on_signal_log_write)
        self.worker.signal_clear_to_base.connect(self.on_signal_log_clear)
        
        ### PushButton 이벤트 연결
        self.pb_clear.clicked.connect(self.clear)
        
    # --- UI 업데이트 슬롯 (Main Thread에서 실행됨) ---
    @Slot(str)
    def on_signal_log_write(self, text):
        self.browser_log.append(text)
        self.browser_log.moveCursor(QTextCursor.End)

    @Slot()
    def on_signal_log_clear(self):
        self.browser_log.clear()

    # --- 외부/내부 호출 인터페이스 ---
    ### 로그를 입력하는 친구
    def log(self, _text : str):
        self.signal_log_to_worker.emit(_text)

    def clear(self):
        self.signal_clear_to_worker.emit()

    ### --- 스레드 안전 종료 처리 ---
    def closeEvent(self, event):
        if self.thread.isRunning():
            self.thread.quit()  # 이벤트 루프 정지 요청
            if not self.thread.wait(1000):  # 최대 2초 대기
                self.thread.terminate()
        super().closeEvent(event)