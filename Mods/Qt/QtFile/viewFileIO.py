from typing import Callable, Optional
from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLineEdit,
                              QPushButton, QFileDialog, QMessageBox, QLabel)

class CViewFileIOTypeA(QWidget):
    def __init__(self
                 , _title : str = ""
                 , _find_callback: Optional[Callable[[str], None]] = None
                 , _read_callback: Optional[Callable[[str], None]] = None
                 , parent=None):
        super().__init__(parent)

        self.find_callback = _find_callback
        self.read_callback = _read_callback

        self.layout = QVBoxLayout(self)

        if _title != "":
            self.title_layout = QHBoxLayout(self)
            self.title_layout.addWidget(QLabel(f"[{_title}]"))
            self.layout.addLayout(self.title_layout)

        self.upper_layer = QHBoxLayout()
        self.le_filepath = QLineEdit(self)
        self.le_filepath.setPlaceholderText("파일 경로가 여기에 표시됩니다...")
        self.le_filepath.setReadOnly(True)
        self.upper_layer.addWidget(self.le_filepath)

        self.lower_layer = QHBoxLayout()
        self.lower_layer.addStretch(1)
        self.pb_find = QPushButton("찾기")
        self.pb_read = QPushButton("읽기")
        self.lower_layer.addWidget(self.pb_find)
        self.lower_layer.addWidget(self.pb_read)

        self.layout.addLayout(self.upper_layer)
        self.layout.addLayout(self.lower_layer)

        self.pb_find.clicked.connect(self.on_clicked_file_search)
        self.pb_read.clicked.connect(self.on_clicked_file_read)

    def on_clicked_file_search(self):
        fname, _ = QFileDialog.getOpenFileName(self
                                               , caption='파일 선택'
                                               , dir=''
                                               , filter='Excel Files (*.xlsx)')
        if fname:
            self.le_filepath.setText(fname)
            self.find_callback(str(fname))

    def on_clicked_file_read(self):
        if self.read_callback is not None:
            if self.file_path != "":
                self.read_callback(self.file_path)
            else:
                QMessageBox.warning(self, '파일 읽기 에러', '경로 없음')
        else:
            QMessageBox.warning(self, "파일 읽기 에러", "콜백 등록 필요")


class CViewFileIOTypeB(QWidget):
    def __init__(self
                 , _title : str = ""
                 , _find_callback: Optional[Callable[[str], None]] = None
                 , parent=None):
        super().__init__(parent)

        self.find_callback = _find_callback

        self.layout = QVBoxLayout(self)

        if _title != "":
            self.title_layout = QHBoxLayout(self)
            self.title_layout.addWidget(QLabel(f"[{_title}]"))
            self.layout.addLayout(self.title_layout)

        self.upper_layer = QHBoxLayout()
        self.le_filepath = QLineEdit(self)
        self.le_filepath.setPlaceholderText("파일 경로가 여기에 표시됩니다...")
        self.le_filepath.setReadOnly(True)
        self.upper_layer.addWidget(self.le_filepath)

        self.lower_layer = QHBoxLayout()
        self.lower_layer.addStretch(1)
        self.pb_find = QPushButton("찾기")
        self.lower_layer.addWidget(self.pb_find)

        self.layout.addLayout(self.upper_layer)
        self.layout.addLayout(self.lower_layer)

        self.pb_find.clicked.connect(self.on_clicked_file_search)

    def on_clicked_file_search(self):
        fname, _ = QFileDialog.getOpenFileName(self
                                               , caption='파일 선택'
                                               , dir=''
                                               , filter='Excel Files (*.xlsx)')
        if fname:
            self.le_filepath.setText(fname)
            if self.find_callback is not None:
                self.find_callback(fname)
            else:
                QMessageBox.warning(self, "에러", "콜백 등록 필요")