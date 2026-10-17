import ipaddress
from typing import Callable, Optional
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
                               QPushButton, QMessageBox, QLabel)

class CViewIPConnectTypeA(QWidget):
    def __init__(self
                 , _title : str = ""
                 , _ip_a : str = ""
                 , _ip_b : str = ""
                 , _ip_c : str = ""
                 , _ip_d : str = ""
                 , _connect_callback: Optional[Callable[[str], None]] = None
                 , _disconnect_callback = None
                 , parent=None):
        super().__init__(parent)
        
        self.ip = None
        self.connect_callback = _connect_callback
        self.disconnect_callback = _disconnect_callback

        self.layout = QVBoxLayout(self)

        self.ip_a = QLineEdit(_ip_a)
        self.ip_b = QLineEdit(_ip_b)
        self.ip_c = QLineEdit(_ip_c)
        self.ip_d = QLineEdit(_ip_d)
        self.pb_connect = QPushButton("Connect")
        self.pb_disconnect = QPushButton("Disconnect")

        if _title != "":
            self.title_layout = QHBoxLayout(self)
            self.title_layout.addWidget(QLabel(f"[{_title}]"))
            self.layout.addLayout(self.title_layout)

        self.single_layout = QHBoxLayout(self)
        self.single_layout.addWidget(QLabel("IP:"))
        self.single_layout.addWidget(self.ip_a)
        self.single_layout.addWidget(QLabel("."))
        self.single_layout.addWidget(self.ip_b)
        self.single_layout.addWidget(QLabel("."))
        self.single_layout.addWidget(self.ip_c)
        self.single_layout.addWidget(QLabel("."))
        self.single_layout.addWidget(self.ip_d)
        self.single_layout.addWidget(self.pb_connect)
        self.single_layout.addWidget(self.pb_disconnect)
        self.layout.addLayout(self.single_layout)

        self.pb_connect.clicked.connect(self.on_clicked_connect)
        self.pb_disconnect.clicked.connect(self.on_clicked_disconnect)

    def is_input_valid(self) -> bool:
        ip_a = self.ip_a.text()
        ip_b = self.ip_b.text()
        ip_c = self.ip_c.text()
        ip_d = self.ip_d.text()
        self.ip = f"{ip_a}.{ip_b}.{ip_c}.{ip_d}"
        try:
            ipaddress.ip_address(self.ip)
            return True
        except ValueError:
            self.ip = None
            return False

    def get_data(self):
        ret = self.is_input_valid()
        return {
            "ip" : str(self.ip),
            "valid" : str(ret)
        }


    def on_clicked_connect(self):
        if self.is_input_valid():
            if self.connect_callback is not None:
                self.connect_callback(self.ip)
            else:
                QMessageBox.warning(self, "연결 에러", "콜백 등록 필요")
        else:
            QMessageBox.warning(self, "연결 에러", "유효하지 않은 IP 주소")


    def on_clicked_disconnect(self):
        if self.disconnect_callback is not None:
            self.disconnect_callback()
        else:
            QMessageBox.warning(self, "연결 에러", "콜백 등록 필요")



class CViewIPConnectTypeB(QWidget):
    def __init__(self,
                 _title : str = "",
                 _ip_a: str = "",
                 _ip_b: str = "",
                 _ip_c: str = "",
                 _ip_d: str = "",
                 _port : int = 16500,
                 _connect_callback: Optional[Callable[[str], None]] = None,
                 _disconnect_callback = None,
                 parent=None):
        super().__init__(parent)

        self.ip                     = None
        self.port                   = 0
        self.connect_callback       = _connect_callback
        self.disconnect_callback    = _disconnect_callback

        self.layout = QVBoxLayout(self)

        if _title != "":
            self.title_layout = QHBoxLayout(self)
            self.title_layout.addWidget(QLabel(f"[{_title}]"))
            self.layout.addLayout(self.title_layout)

        self.upper_layout = QHBoxLayout(self)
        self.ip_a = QLineEdit(_ip_a)
        self.ip_b = QLineEdit(_ip_b)
        self.ip_c = QLineEdit(_ip_c)
        self.ip_d = QLineEdit(_ip_d)
        self.port_ = QLineEdit(str(_port))
        self.upper_layout.addWidget(QLabel("IP:"))
        self.upper_layout.addWidget(self.ip_a)
        self.upper_layout.addWidget(QLabel("."))
        self.upper_layout.addWidget(self.ip_b)
        self.upper_layout.addWidget(QLabel("."))
        self.upper_layout.addWidget(self.ip_c)
        self.upper_layout.addWidget(QLabel("."))
        self.upper_layout.addWidget(self.ip_d)
        self.upper_layout.addWidget(QLabel("Port:"))
        self.upper_layout.addWidget(self.port_)
        self.layout.addLayout(self.upper_layout)

        self.lower_layout = QHBoxLayout(self)
        self.pb_connect         = QPushButton("Connect")
        self.pb_disconnect      = QPushButton("Disconnect")
        self.lower_layout.addStretch(1)
        self.lower_layout.addWidget(self.pb_connect)
        self.lower_layout.addWidget(self.pb_disconnect)
        self.layout.addLayout(self.lower_layout)

        self.pb_connect.clicked.connect(self.on_clicked_connect)
        self.pb_disconnect.clicked.connect(self.on_clicked_disconnect)

    def is_input_valid(self) -> bool:
        ip_a = self.ip_a.text()
        ip_b = self.ip_b.text()
        ip_c = self.ip_c.text()
        ip_d = self.ip_d.text()
        self.port = int(self.port_.text())
        self.ip = f"{ip_a}.{ip_b}.{ip_c}.{ip_d}"

        try:
            ipaddress.ip_address(self.ip)
            if 0 <  self.port < 65536:
                return True
            else:
                raise ValueError
        except ValueError:
            self.ip = None
            self.port = 0
            return False


    def get_data(self):
        ret = self.is_input_valid()
        return {
            "ip"    : str(self.ip),
            "port"  : int(self.port),
            "valid" : str(ret)
        }


    def on_clicked_connect(self):
        if self.is_input_valid():
            if self.connect_callback is not None:
                self.connect_callback(self.ip, 16500)
            else:
                QMessageBox.warning(self, "연결 에러", "콜백 등록 필요")
        else:
            QMessageBox.warning(self, "연결 에러", "유효하지 않은 값")


    def on_clicked_disconnect(self):
        if self.disconnect_callback is not None:
            self.disconnect_callback()
        else:
            QMessageBox.warning(self, "연결 에러", "콜백 등록 필요")
