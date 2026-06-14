"""

"""

from PySide6.QtWidgets import QMainWindow, QVBoxLayout
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from PyQt6.viewLogBrowser import CViewLogBrowser

class CMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 1. UI 파일 로드
        loader = QUiLoader()
        ui_file = QFile("./main.ui")
        if not ui_file.exists():
            print("UI 파일을 찾을 수 없습니다.")
            return
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file)
        ui_file.close()

        # 2. 로드된 UI를 메인 윈도우의 중앙에 배치
        self.setCentralWidget(self.ui)
        self.setWindowTitle("Module Test System")
        self.resize(1200, 800)

        # 3. 로그 브라우저 객체 생성
        self.widget_log = CViewLogBrowser()

        # 4. [중요] 스크린샷에 보이는 'main_layout' 찾아서 위젯 추가
        # findChild를 사용하여 QVBoxLayout 타입의 'main_layout' 이름을 가진 객체를 찾습니다.
        target_layout = self.ui.findChild(QVBoxLayout, "right_layout")

        if target_layout:
            target_layout.addWidget(self.widget_log)
            # 여백을 없애고 싶다면 아래 코드 추가
            target_layout.setContentsMargins(0, 0, 0, 0)
            print("성공: main_layout에 로그 위젯을 추가했습니다.")
        else:
            # 레이아웃을 못 찾았을 때를 대비한 안전장치
            print("경고: main_layout을 찾지 못했습니다. centralwidget의 기본 레이아웃을 확인합니다.")
            if self.ui.centralwidget.layout():
                self.ui.centralwidget.layout().addWidget(self.widget_log)

        # 5. 테스트 로그 출력
        self.widget_log.log("시스템이 시작되었습니다.")