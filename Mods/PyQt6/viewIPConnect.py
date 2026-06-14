"""
@brief
@date
@version
"""
import ipaddress

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton, QMessageBox

class CViewIPConnect(QWidget):

    def __init__(self, _ip_a : str = "", _ip_b : str = "", _ip_c : str = "", _ip_d : str = "", parent=None):
        super().__init__(parent)

        self.ip = None
        self.callback_connect = None
        self.callback_disconnect = None

        ### UI 초기 설정(위젯 생성 및 배치)
        self.layer = QHBoxLayout(self)

        self.ip_a = QLineEdit(_ip_a)
        self.ip_b = QLineEdit(_ip_b)
        self.ip_c = QLineEdit(_ip_c)
        self.ip_d = QLineEdit(_ip_d)
        self.pb_connect = QPushButton("Connect")
        self.pb_disconnect = QPushButton("Disconnect")

        self.layer.addWidget(self.ip_a)
        self.layer.addWidget(self.ip_b)
        self.layer.addWidget(self.ip_c)
        self.layer.addWidget(self.ip_d)
        self.layer.addWidget(self.pb_connect)
        self.layer.addWidget(self.pb_disconnect)

        self.pb_connect.clicked.connect(self.on_clicked_connect)
        self.pb_disconnect.clicked.connect(self.on_clicked_disconnect)

    def is_input_valid(self) -> bool:
        ip_a = self.ip_a.text()
        ip_b = self.ip_b.text()
        ip_c = self.ip_c.text()
        ip_d = self.ip_d.text()
        self.ip = f"{ip_a}.{ip_b}.{ip_c}.{ip_d}"
        try:
            # IP 주소 객체를 만들어봅니다. 잘못되면 에러가 발생합니다.
            ipaddress.ip_address(self.ip)
            return True
        except ValueError:
            self.ip = None
            return False

    def connect_button_connect(self, _callback):
        self.callback_connect = _callback

    def connect_button_disconnect(self, _callback):
        self.callback_disconnect = _callback

    def on_clicked_connect(self):
        if self.is_input_valid():
            if self.callback_connect is not None:
                self.callback_connect(self.ip, 16500)
            else:
                QMessageBox.warning(self, "연결 에러", "콜백 등록 필요")
        else:
            QMessageBox.warning(self, "연결 에러", "연결 실패")

    def on_clicked_disconnect(self):
        if self.callback_connect is not None:
            self.callback_disconnect()
