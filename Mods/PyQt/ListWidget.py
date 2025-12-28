from PyQt5.QtWidgets import QListView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt

class CListView(QListView):  # QListView를 직접 상속
    def __init__(self, parent=None):
        super().__init__(parent)

        # 모델 설정 (상속받았으므로 self.setModel을 직접 호출)
        self.model = QStandardItemModel()
        self.setModel(self.model)

    def add_item(self, text, data=None):
        """항목 추가 (표시 텍스트와 숨겨진 데이터)"""
        item = QStandardItem(text)
        if data is not None:
            # Qt.UserRole은 사용자 정의 데이터를 저장하는 용도입니다.
            item.setData(data, Qt.UserRole)
        self.model.appendRow(item)

    def get_selected_data(self):
        """선택된 항목의 데이터 반환"""
        indexes = self.selectedIndexes()
        if indexes:
            return indexes[0].data(Qt.UserRole)
        return None

    def clear_all(self):  # 기존 clear()와 이름 중복 방지를 위해 clear_all로 명명
        """리스트 초기화"""
        self.model.clear()

    def on_item_clicked(self, callback):
        """클릭 이벤트 연결"""
        self.clicked.connect(callback)