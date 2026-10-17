from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser, QPushButton
from PySide6.QtCore import Signal, Slot, QThread
from PySide6.QtGui import QTextCursor

from Qt.QtLogViewer.vmLogViewer import CViewLogViewerWorker

class CViewLogViewer(QWidget):
    signal_log_to_worker = Signal(str)
    signal_clear_to_worker = Signal()

    def __init__(self, _mode = False, parent=None):
        super().__init__(parent)

        # ----------------------------------------
        # Widget 구성
        # ----------------------------------------
        self.layer = QVBoxLayout(self)
        self.browser_log = QTextBrowser(self)
        self.browser_log.document().setMaximumBlockCount(1000)
        self.pb_clear = QPushButton("Clear")
        self.layer.addWidget(self.browser_log)
        self.layer.addWidget(self.pb_clear)

        # ----------------------------------------
        # 환경 설정
        # ----------------------------------------
        self.mode = _mode

        # ----------------------------------------
        # Time Stamp 찍는 모드
        # ----------------------------------------
        if _mode:
            self.worker = CViewLogViewerWorker()
            self.thread = QThread(self)
            self.worker.moveToThread(self.thread)
            self.thread.finished.connect(self.worker.deleteLater)
            self.thread.start()

        self.signal_log_to_worker.connect(self.worker.on_signal_log_write)
        self.signal_clear_to_worker.connect(self.worker.on_signal_log_clear)
        self.worker.signal_log_to_base.connect(self.on_signal_log_write)
        self.worker.signal_clear_to_base.connect(self.on_signal_log_clear)
        self.pb_clear.clicked.connect(self.clear)

    @Slot(str)
    def on_signal_log_write(self, text):
        self.browser_log.append(text)
        self.browser_log.moveCursor(QTextCursor.End)

    @Slot()
    def on_signal_log_clear(self):
        self.browser_log.clear()

    def closeEvent(self, event):
        if self.thread.isRunning():
            self.thread.quit()
            if not self.thread.wait(1000):
                self.thread.terminate()
        super().closeEvent(event)


    # ----------------------------------------
    # User Interface
    # ----------------------------------------
    def log(self, _text : str):
        if self.mode :
            self.signal_log_to_worker.emit(_text)
        else:
            self.browser_log.append(_text)
            self.browser_log.moveCursor(QTextCursor.End)

    def clear(self):
        self.browser_log.clear()


