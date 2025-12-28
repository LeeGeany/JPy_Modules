
from PyQt5.QtWidgets import QListView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt

class ListViewWrapper:
    def __init__(self, list_view_widget: QListView):
        """
        Designer에서 만든 QListView 객체를 인자로 받습니다.
        """
        self.view = list_view_widget
        self.model = QStandardItemModel()
        self.view.setModel(self.model)

    def add_item(self, text, data=None):
        """항목 추가 (표시 텍스트와 숨겨진 데이터)"""
        item = QStandardItem(text)
        if data is not None:
            item.setData(data, Qt.UserRole)
        self.model.appendRow(item)

    def get_selected_data(self):
        """선택된 항목의 데이터 반환"""
        indexes = self.view.selectedIndexes()
        if indexes:
            return indexes[0].data(Qt.UserRole)
        return None

    def clear(self):
        """리스트 초기화"""
        self.model.clear()

    def on_click(self, callback):
        """클릭 이벤트 연결"""
        self.view.clicked.connect(callback)