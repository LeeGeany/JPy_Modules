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
        self.pushbutton_callback = {}
        for item in items:
            if item["type"] == "Label":
                label_temp = QLabel(item["content"])
                #if item["size"][0] == 0 and item["size"][1] == 0  is not True : label_temp.resize(item["size"][0], item["size"][1])
                self.item_list.append(label_temp)
            elif item["type"] == "LineEdit":
                lineedit_temp = QLineEdit()
                lineedit_temp.setText(item["content"])
                lineedit_temp.setAlignment(Qt.AlignmentFlag.AlignRight)
                if item["size"][1] != 0 : lineedit_temp.setFixedWidth(item["size"][0])
                if item["size"][1] != 0 : lineedit_temp.setFixedHeight(item["size"][1])
                self.item_list.append(lineedit_temp)
            elif item["type"] == "Space":
                self.item_list.append("Space")
            elif item["type"] == "PushButton":
                pushbutton_temp = QPushButton()
                pushbutton_temp.setText(item["content"])
                if not (item["size"][0] == 0 and item["size"][1] == 0) : pushbutton_temp.resize(item["size"][0], item["size"][1])
                self.item_list.append(pushbutton_temp)
                self.pushbutton_callback[item["content"]] = None

        for item in self.item_list:
            if item == "Space":
                self.layout.addStretch()
            else:
                self.layout.addWidget(item)

    # ----------------------------------------
    # User Interface
    # ----------------------------------------
    def callback_subscribe(self, _name : str, _callback):
        self.pushbutton_callback[_name] = _callback