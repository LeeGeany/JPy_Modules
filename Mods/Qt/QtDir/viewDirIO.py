"""
파일 이름: viewDirIO.py
설명: 일는 파일
작성자: 이진희 (tjrgl@naver.com)
작성일: 2026-06-11
수정 이력:
    - None
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                              QPushButton, QFileDialog, QMessageBox)
from typing import Callable, Optional

class CViewDirIOTypeA(QWidget):
    def __init__(self,
                 _title : str = "",
                 _find_callback: Optional[Callable[[str], None]] = None,
                 parent=None):
        super().__init__(parent)

        # 함수 객체
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

        self.pb_find.clicked.connect(self.on_clicked_dir_search)

    def on_clicked_dir_search(self):
        fname = QFileDialog.getExistingDirectory(
            None,
            '파일 선택',
            '../',
        )
        if fname:
            self.le_filepath.setText(fname)
            if self.find_callback is not None:
                self.find_callback(fname)
            else:
                QMessageBox.warning(self, "에러", "콜백 등록 필요")