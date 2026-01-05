'''
@brief  file 읽어오는 view
@details
    *
    *
    *
@todo.
    1) 범위에 맞지 않으면 팝업 뜨게 만든다.
@dependency
    *
'''
from PyQt5 import QtWidgets, QtCore

from Mods.PyQt.viewItemList import CItemList
from Mods.PyQt.viewLine import CLine

class CDefaultElement(QtWidgets.QWidget):
    def __init__(self, _dict : dict, parent=None):
        super().__init__(parent)

        self.data = _dict

        for key in self.data:
            self.lb_element = QtWidgets.QLabel(f"{str(key)} : \t")
        self.le_element = QtWidgets.QLineEdit()

        self.layout     = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.lb_element)
        self.layout.addWidget(self.le_element)

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)
        self.layout.addStretch(1)

    def getData(self) -> dict:
        print(f"{self.lb_element.text()}", self.le_element.text())
        return {
            f"{self.lb_element.text()}" : self.le_element.text()
        }


class CBitElement(QtWidgets.QWidget):
    def __init__(self, _dict : dict, parent=None):
        super().__init__(parent)

        self.dict = _dict

        self.layout = QtWidgets.QVBoxLayout(self)

        self.layout.addWidget(CLine())
        for key, value in self.dict.items():
            element_ = CDefaultElement({key:value})
            self.layout.addWidget(element_)
        self.layout.addWidget(CLine())

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)

        #self.layout.setSpacing(10)
        #self.layout.addStretch(1)


class CIterElement(QtWidgets.QWidget):
    def __init__(self, _dict : dict, parent=None):
        super().__init__(parent)

        self.data = {}
        self.elements = []

        self.layout = QtWidgets.QVBoxLayout(self)

        self.layout.addWidget(CLine())

        self.inner_layout = QtWidgets.QHBoxLayout(self)
        self.itemlist   = CItemList(self); self.itemlist.setFixedSize(300, 50)
        self.pb_insert  = QtWidgets.QPushButton("Insert")
        self.pb_delete  = QtWidgets.QPushButton("Delete")
        self.element    = CDefaultElement({"Element Name":0})

        self.inner_layout.addWidget(self.itemlist)
        self.inner_layout.addWidget(self.pb_insert)
        self.inner_layout.addWidget(self.pb_delete)
        self.inner_layout.setContentsMargins(0, 0, 0, 0)
        self.inner_layout.setSpacing(5)

        self.layout.addLayout(self.inner_layout, 0)
        self.layout.addWidget(self.element)

        for (key, value) in _dict.items():
            element_ = CDefaultElement({key:value})
            self.layout.addWidget(element_)
            self.elements.append(element_)

        self.layout.addWidget(CLine())

        #
        self.layout.setContentsMargins(0, 0, 0, 0)
        #self.layout.setSpacing(5)

        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)

        #
        self.pb_insert.clicked.connect(self.on_clicked_insert)
        self.pb_delete.clicked.connect(self.on_clicked_delete)

    def on_clicked_insert(self) -> None:
        _str = None
        for key, value in self.element.getData().items():
            _str = str(value)

        if _str != "":
            self.itemlist.addList(str(_str))
            self.itemlist.refreshList()
        else:
            QtWidgets.QMessageBox.warning(self,"주의", "이름을 입력하세요.")


    def on_clicked_delete(self):
        index = self.itemlist.selectIndex().row()

        if index != -1:
            self.itemlist.removeList(index)
            self.itemlist.refreshList()
        else:
            QtWidgets.QMessageBox.warning(self, "주의", "삭제할 요소를 선택하세요.")



class CWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignTop)

    def insertDefaultElement(self, _dict : dict):
        self.layout.addWidget(CDefaultElement(_dict))

    def insertBitElement(self, _dict : dict):
        self.layout.addWidget(CBitElement(_dict))

    def insertIterElement(self, _dict : dict):
        self.layout.addWidget(CIterElement(_dict))
