import socket
import threading
import time

class CTCPClient:
    def __init__(self, _host, _port):
        self.host               = _host                 # 연결할 서버 IP
        self.port               = _port                 # 연결할 서버 Port

        self.client_socket      = None
        self.is_running         = False                 # 사용자가 명시적으로 stop했는지 여부
        self.is_connected       = False                 # 현재 소켓이 연결된 상태인지 여부
        self.reconnect_interval = 1                     # 재연결 시도 간격 (초)

    def start(self):
        self.is_running = True
        self.thread = threading.Thread(target=self.connection_manager, daemon=True)
        self.thread.start()

    def connection_manager(self):
        """연결 상태를 감시하며 끊겼을 경우 재연결을 시도하는 매니저"""
        while self.is_running:
            if not self.is_connected:
                print(f"[*] {self.host}:{self.port} 연결 시도 중...")
                if self.connect():
                    print("[*] 서버에 연결되었습니다.")
                else:
                    print(f"[!] 연결 실패. {self.reconnect_interval}초 후 재시도합니다.")
                    time.sleep(self.reconnect_interval)
            else:
                # 연결된 상태라면 짧게 대기하며 상태 감시
                time.sleep(3)


    def connect(self) -> bool:
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.settimeout(3.0)  # 연결 타임아웃 3초
            self.client_socket.connect((self.host, self.port))
            self.client_socket.settimeout(None)  # 연결 후에는 블로킹 모드
            self.is_connected = True
            return True
        except Exception as e:
            self.cleanup_socket()
            return False


    def receive(self, _recvSize=1024):
        if not (self.is_running and self.is_connected):
            return None

        try:
            data = self.client_socket.recv(_recvSize)

            if not data:
                print("[Info] 서버가 연결을 정상적으로 닫았습니다.")
                self.handle_disconnect()
                return None

            return data.decode('utf-8')

        except ConnectionResetError:
            print("[Error] 서버와의 연결이 강제로 끊겼습니다.")
            self.handle_disconnect()
            return None

        except Exception as e:
            if self.is_running:
                print(f"[Receive Error] {e}")
                self.handle_disconnect()
            return None


    def handle_disconnect(self):
        was_connected = self.is_connected
        self.is_connected = False
        self.cleanup_socket()


    def cleanup_socket(self):
        if self.client_socket:
            try:
                self.client_socket.shutdown(socket.SHUT_RDWR)
                self.client_socket.close()
            except:
                pass
            self.client_socket = None


    def send(self, message):
        if not self.is_connected:
            print("[Send Error] 연결되어 있지 않습니다.")
            return False

        try:
            #self.client_socket.sendall(message.encode('utf-8'))
            self.client_socket.sendall(message)
            return True
        except Exception as e:
            print(f"[Send Error] {e}")
            return False


    def stop(self):
        self.is_running = False
        self.is_connected = False
        self.cleanup_socket()
        if self.thread and self.thread.is_alive():
            self.thread.join()


    def isStop(self):
        return self.is_running