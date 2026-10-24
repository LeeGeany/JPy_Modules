from email.policy import default
from typing import Callable, Optional

from PySide6.QtCore                 import Qt
from PySide6.QtWidgets              import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from Qt.QtConfigItem.vmConfigItem   import CVMConfigItem

class CViewConfigItem(QWidget):
    def __init__(self, items : list, _axis=0, parent=None, tcp_server=None):
        super().__init__(parent)

        self._view_model = CVMConfigItem()

        self.layout = None

        if _axis == 0:
            self.layout = QHBoxLayout(self)
        else :
            self.layout = QVBoxLayout(self)

        self.item_list = []
        self.callback_dict = {}

        ### 여기서 items은 list, item은 dictionary
        for item in items:
            if item["type"] == "Label":
                label_temp = QLabel(item["content"])
                item["item"] = label_temp
                self.item_list.append(item)

            elif item["type"] == "LineEdit":
                lineedit_temp = QLineEdit()
                lineedit_temp.setText(item["content"])
                lineedit_temp.setAlignment(Qt.AlignmentFlag.AlignRight)
                if item["size"][1] != 0 : lineedit_temp.setFixedWidth(item["size"][0])
                if item["size"][1] != 0 : lineedit_temp.setFixedHeight(item["size"][1])
                item["item"] = lineedit_temp
                self.item_list.append(item)

            elif item["type"] == "Space":
                item["item"] = "Space"
                self.item_list.append(item)

            elif item["type"] == "PushButton":
                pushbutton_temp = QPushButton()
                pushbutton_temp.setText(item["content"])
                if not (item["size"][0] == 0 and item["size"][1] == 0) : pushbutton_temp.resize(item["size"][0], item["size"][1])
                item["item"] = pushbutton_temp
                self.item_list.append(item)

        ### 아이템을 모아서 위젯을 그려주는 코드
        for item in self.item_list:
            if item["type"] == "Space":
                self.layout.addStretch()
            else:
                self.layout.addWidget(item["item"])

    def common_callback(self, _callback):
        list_ = []
        for item in self.item_list:
            if item["type"] == "LineEdit":
                list_.append(int(item["item"].text()))
        _callback(list_)

    # ----------------------------------------
    # User Interface
    # ----------------------------------------
    def subscribe_callback(self, _name : str, _callback):
        for item in self.item_list:
            if item["name"] == _name:
                item["item"].clicked.connect(lambda : self.common_callback( _callback))

