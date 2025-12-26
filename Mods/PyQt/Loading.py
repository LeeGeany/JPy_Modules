import os
import time

from PyQt5 import uic
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget

from _Srcs.Config.Config import BASE_DIR

class LoaderThread(QThread):
    progress = pyqtSignal(int)
    done = pyqtSignal()

    def run(self):
        for i in range(1, 101):
            time.sleep(0.01)  # 실제 초기화 작업 대체
            self.progress.emit(i)
        self.done.emit()

class LoadingScreen(QWidget):
    Loading = pyqtSignal()

    def __init__(self):
        super().__init__()
        ui_path = os.path.join(BASE_DIR, "_UI", "Loading", "Loading.ui")
        uic.loadUi(ui_path, self)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(self.size())

        # 로딩 텍스트 초기화
        self.lb_status.setText("Loading...")

        # 로딩 프로그래스바 초기화
        self.progressBar.setValue(0)

        # 쓰레드 생성 및 연결
        self.loader = LoaderThread()
        self.loader.progress.connect(self.progressBar.setValue)
        self.loader.done.connect(self.loading_done)
        self.loader.start()

    def loading_done(self):
        self.lb_status.setText("Done.")
        self.Loading.emit()
        self.close()