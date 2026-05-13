'''
@brief
@date
@version
'''

from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QFileDialog, QMessageBox
from typing import Callable, Optional

class CViewFileIO(QWidget):
    def   __init__(self, _read_callback: Optional[Callable[[str], None]] = None, parent=None):
        super().__init__(parent)

        self.read_callback  = _read_callback
        self.file_path      = ""

        self.layer = QVBoxLayout(self)
        self.upper_layer = QHBoxLayout()
        self.lower_layer = QHBoxLayout()

        self.le_filepath = QLineEdit(self)
        self.le_filepath.setPlaceholderText("파일 경로가 여기에 표시됩니다...")
        self.le_filepath.setReadOnly(True)

        self.pb_find    = QPushButton("찾기")
        self.pb_read    = QPushButton("읽기")
        self.pb_find.setFixedWidth(80)
        self.pb_read.setFixedWidth(80)

        self.upper_layer.addWidget(self.le_filepath)
        self.lower_layer.addStretch(1)
        self.lower_layer.addWidget(self.pb_find)
        self.lower_layer.addWidget(self.pb_read)

        #self.layer.addStretch(1)
        self.layer.addLayout(self.upper_layer)
        self.layer.addLayout(self.lower_layer)
        self.layer.setContentsMargins(5, 5, 5, 5)
        self.layer.setSpacing(5)  # 레이아웃 사이 간격

        self.pb_find.clicked.connect(self.on_clicked_file_search)
        self.pb_read.clicked.connect(self.on_clicked_file_read)

    def on_clicked_file_search(self):
        fname, _ = QFileDialog.getOpenFileName(
            self,
            '파일 선택',
            '',
            'Excel Files (*.xlsx)'
        )
        if fname:
            self.le_filepath.setText(fname)
            self.file_path = fname

    def on_clicked_file_read(self):
        if self.read_callback is not None:
            if self.file_path != "":
                self.read_callback(self.file_path)
            else:
                QMessageBox.warning(self, "파일 읽기 에러", "경로 없음")
        else:
            QMessageBox.warning(self, "파일 읽기 에러", "콜백 등록 필요")
