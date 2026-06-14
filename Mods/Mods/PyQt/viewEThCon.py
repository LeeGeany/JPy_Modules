'''
@brief  file 읽어오는 view
@details
    *
    *
    *
@todo.
    1)
@dependency
    * Mods/Utils/myUtil.py 에서 is_range, is_integer, is_positive 함수 가지고 옴
'''

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, QThread, QObject, pyqtSlot

from Mods.Utils.myUtil import is_range, is_integer, is_positive

class CTCPConWorker(QObject):
    sg_read_info    = pyqtSignal()
    sg_status_conn  = pyqtSignal(bool)

    def __init__(self, _obj : object, parent=None):
        super().__init__(parent)
        self.obj = _obj

    '''
        @brief  연결 버튼이 클릭되면 실행되는 함수
        @detail 여기 _obj로 전제 CModalConnection 객체를 전달 받는다.
    '''
    @pyqtSlot()
    def isInfoCheck(self):
        _ip_a = self.obj.le_ip_a.text()
        _ip_b = self.obj.le_ip_b.text()
        _ip_c = self.obj.le_ip_c.text()
        _ip_d = self.obj.le_ip_d.text()

        _ip_list = [_ip_a, _ip_b, _ip_c, _ip_d]
        for i in _ip_list:
            if not (is_integer(i) or is_positive(i)):
                QtWidgets.QMessageBox.warning(self, "주의", "IP가 정수가 아닙니다.")
                return
            if not is_range(255, 0, int(i)):
                QtWidgets.QMessageBox.warning(self, "주의", "IP가 범위에 벗어났습니다. (65535 ~ 0)")
                return

        _ip = _ip_a + "." + _ip_b + "." + _ip_c + "." + _ip_d

        _port = self.obj.le_port.text()
        if not (is_integer(_port) or is_positive(_port)):
            QtWidgets.QMessageBox.warning(self, "주의", "Port 번호가 정수가 아닙니다.")
            return
        if not is_range(65535, 0, int(_port)):
            QtWidgets.QMessageBox.warning(self, "주의", "Port 번호가 범위에 벗어났습니다. (65535 ~ 0)")
            return

        self.obj.sg_get_info.emit(_ip, int(_port))


    '''
    
    '''
    @pyqtSlot(bool)
    def statusChange(self, _isConnected):
        if _isConnected:
            self.obj.lb_now.setText("연결")
        else:
            self.obj.lb_now.setText("연결 해제")


class CTCPCon(QtWidgets.QDialog):
    sg_get_info = pyqtSignal(str, int)

    def __init__(self, _name : str, parent=None):
        super(CTCPCon, self).__init__(parent)

        self.on_Connect = None   # 생성 할 떄 수행 함수
        self.on_Disconnect = None  # 해제 할 떄 수행 함수

        # 상태 제어 쓰레드
        self.thread = QThread(self)
        self.worker = CTCPConWorker(self)
        self.worker.moveToThread(self.thread)
        self.thread.start()

        # 전체 레이아웃
        self.layout = QtWidgets.QVBoxLayout(self)

        # 라벨

        self.lb_ip = QtWidgets.QLabel(f"{_name} Connection")
        self.inner_layout1 = QtWidgets.QHBoxLayout()
        self.inner_layout1.addWidget(self.lb_ip)
        self.inner_layout1.addStretch()

        # IP
        self.lb_ip = QtWidgets.QLabel("Server IP : ")
        self.le_ip_a = QtWidgets.QLineEdit("127")
        self.lb_ip_a = QtWidgets.QLabel(".")
        self.le_ip_b = QtWidgets.QLineEdit("0")
        self.lb_ip_b = QtWidgets.QLabel(".")
        self.le_ip_c = QtWidgets.QLineEdit("0")
        self.lb_ip_c = QtWidgets.QLabel(".")
        self.le_ip_d = QtWidgets.QLineEdit("1")

        self.inner_layout2 = QtWidgets.QHBoxLayout()
        self.inner_layout2.addWidget(self.lb_ip)
        self.inner_layout2.addWidget(self.le_ip_a)
        self.inner_layout2.addWidget(self.lb_ip_a)
        self.inner_layout2.addWidget(self.le_ip_b)
        self.inner_layout2.addWidget(self.lb_ip_b)
        self.inner_layout2.addWidget(self.le_ip_c)
        self.inner_layout2.addWidget(self.lb_ip_c)
        self.inner_layout2.addWidget(self.le_ip_d)

        self.inner_layout3 = QtWidgets.QHBoxLayout()
        self.lb_port = QtWidgets.QLabel("Server Port : ")
        self.le_port = QtWidgets.QLineEdit("16500")
        self.inner_layout3.addWidget(self.lb_port)
        self.inner_layout3.addWidget(self.le_port)

        self.inner_layout4 = QtWidgets.QHBoxLayout()
        self.lb_status = QtWidgets.QLabel("Status : ")
        self.lb_now = QtWidgets.QLabel("Disconnected")
        self.pb_connect = QtWidgets.QPushButton("연결")
        self.pb_disconnect = QtWidgets.QPushButton("연결 해제")

        self.inner_layout4.addWidget(self.lb_status)
        self.inner_layout4.addWidget(self.lb_now)
        self.inner_layout4.addWidget(self.pb_connect)
        self.inner_layout4.addWidget(self.pb_disconnect)

        # 전체 레이아웃
        self.layout.addLayout(self.inner_layout1,1)
        self.layout.addLayout(self.inner_layout2,2)
        self.layout.addLayout(self.inner_layout3,3)
        self.layout.addLayout(self.inner_layout4,4)

        # 버튼 연결
        self.pb_connect.clicked.connect(self.on_clicked_connect)
        self.pb_disconnect.clicked.connect(self.on_clicked_disconnect)

        # 시그널 연결
        self.worker.sg_status_conn.connect(self.worker.statusChange)
        self.worker.sg_read_info.connect(self.worker.isInfoCheck)
        self.sg_get_info.connect(self.tryConnect)

    def closeEvent(self, event):
        self.thread.quit()

        if not self.thread.wait(2000):  # 최대 2초 대기
            self.thread.terminate()  # 안 끝나면 강제 종료
            self.thread.wait()

        event.accept()

    def on_clicked_connect(self):
        self.worker.sg_read_info.emit()


    def on_clicked_disconnect(self):
        if self.on_Disconnect is not None:
            self.on_Disconnect()
        else:
            print("on_Discoonect is None")

        self.changeStatusDisconnect()


    def tryConnect(self, _ip, _port):
        if self.on_Connect is not None:
            self.on_Connect(_ip, _port)
        else:
            print("on_Connect is None")
        self.changeStatusConnect()

    def changeStatusConnect(self):
        self.worker.sg_status_conn.emit(True)


    def changeStatusDisconnect(self):
        self.worker.sg_status_conn.emit(False)


    def setOnConnect(self, _callback):
        self.on_Connect = _callback


    def setOnDisconnect(self, _callback):
        self.on_Disconnect = _callback
