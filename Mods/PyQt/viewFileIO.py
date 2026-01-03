'''
@brief  file 읽어오는 view
@details
    * 파일을 찾고 읽어 올 수 있는 기능
    * 읽기 시 프로그래스 바가 생성되여 새로운 쓰레드로 수행
    * 사용 전 read_func 함수로 수행 함수를 정의 하여 등록 해야 한다.
@todo.
    1) 없음
@dependency
    * Mods/PyQt/viewProgressBar.py 프로그래스 바를 사용하기 위한 종속성 삽입
'''

from PyQt5 import QtWidgets
from Mods.PyQt.viewProgressBar import CProgressBar

class CFileIO(QtWidgets.QWidget):
    def   __init__(self, parent=None):
        super().__init__(parent)

        # 함수 객체
        self.readFunc = None

        # 구성 element 객체 생성
        self.path_edit  = QtWidgets.QLineEdit()
        self.pb_find    = QtWidgets.QPushButton("찾기")
        self.pb_read    = QtWidgets.QPushButton("읽기")

        self.path_edit.setPlaceholderText("파일 경로가 여기에 표시됩니다...")
        self.path_edit.setReadOnly(True)

        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.path_edit)
        layout.addWidget(self.pb_find)
        layout.addWidget(self.pb_read)

        # 콜백 함수 연결
        self.pb_find.clicked.connect(self.search_file)
        self.pb_read.clicked.connect(self.read_file)

    def read_func(self, _func):
        self.readFunc = _func

    def read_file(self):
        if self.readFunc is not None:
            progressbar = CProgressBar(title="메시지 파일 읽기", func=self.readFunc)
            progressbar.run()

    def search_file(self):
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            '파일 선택',
            '',
            'Excel Files (*.xlsx)'
        )
        if fname:
            self.path_edit.setText(fname)