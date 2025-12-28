from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QStackedWidget, QWidget

class CStackWidget(QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 페이지를 이름으로 관리하기 위한 딕셔너리
        self.pages = {}

    def add_named_page(self, widget: QWidget, name: str):
        """페이지를 추가하고 이름을 지정합니다."""
        if name in self.pages:
            print(f"Warning: '{name}' 이름의 페이지가 이미 존재합니다.")
            return

        index = self.addWidget(widget)
        self.pages[name] = index
        return index

    def switch_to(self, name: str):
        """지정한 이름의 페이지로 전환합니다."""
        if name in self.pages:
            self.setCurrentIndex(self.pages[name])
        else:
            print(f"Error: '{name}' 이름의 페이지를 찾을 수 없습니다.")

    # @brief
    # @return
    def get_current_name(self) -> str:
        """현재 보여지는 페이지의 이름을 반환합니다."""
        for name, index in self.pages.items():
            if index == self.currentIndex():
                return name
        return None