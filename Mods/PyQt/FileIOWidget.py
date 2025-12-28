from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLineEdit, QHBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import pyqtSignal

class CFileIO(QtWidgets.QWidget):
    sgFileSuccess = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)  # 여백 제거

        # 2. 라인 에디트
        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText("파일 경로가 여기에 표시됩니다...")
        self.path_edit.setReadOnly(True)

        # 3. 버튼들 생성
        self.btn_search = QPushButton("찾기")
        self.btn_read = QPushButton("읽기")

        # 4. 레이아웃에 위젯들 추가 (넣는 순서대로 가로로 배치됨)
        self.layout.addWidget(self.path_edit)
        self.layout.addWidget(self.btn_search)
        self.layout.addWidget(self.btn_read)

        self.btn_search.clicked.connect(self.search_file)
        self.btn_read.clicked.connect(self.read_action)

    def search_file(self):
        fname, _ = QFileDialog.getOpenFileName(
            self,
            '파일 선택',
            '',
            'Excel Files (*.xlsx)'
        )
        if fname:
            self.path_edit.setText(fname)

    def read_action(self):
        path = self.path_edit.text()
        if path:
            # 파일 읽기 로직 (예시)
            self.sgFileSuccess.emit(f"성공: {path}")