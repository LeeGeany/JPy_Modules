import socket
import threading
import time
from typing import Callable, Optional, List, Any


class CTCPClient:
    # ... (생성자 및 콜백 정의 부분은 유지)

    def __init__(
            self,
            host: str,
            port: int,
            *,
            recv_buffer: int = 4096,
            timeout: Optional[float] = None,
            reconnect: bool = True,
            reconnect_interval: Optional[float] = 5.0
    ):
        self.host = host
        self.port = port
        self.recv_buffer = recv_buffer
        self.timeout = timeout
        self.reconnect = reconnect
        self.reconnect_interval = reconnect_interval

        self._sock: Optional[socket.socket] = None
        self._recv_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()  # 초기화 시 생성
        self._is_connected = False

        # 콜백: on_receive의 시그니처를 (self, data_chunk)로 변경
        self._on_connect: Optional[Callable[[], None]] = None
        self._on_disconnect: Optional[Callable[[], None]] = None
        # 💡 변경: on_receive 콜백은 클라이언트 인스턴스와 수신된 청크를 받습니다.
        self._on_receive: Optional[Callable[[Any, bytes], None]] = None
        self._on_error: Optional[Callable[[Exception], None]] = None

    # ... (on_connect, on_disconnect, on_error 함수는 유지)

    def on_receive(self, cb: Callable[[Any, bytes], None]) -> None:
        self._on_receive = cb

    # 연결 및 해제 (connect/disconnect 함수는 이전 코드와 동일)
    def connect(self) -> None:
        if self._sock and self._is_connected:
            return

        try:
            # 💡 _stop_event의 상태를 초기화
            self._stop_event.clear()

            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if self.timeout:
                # connect()에는 settimeout(None)을 먼저 적용하고 connect 후 복원하는 것이 일반적이나,
                # 여기서는 전체 소켓 타임아웃을 유지합니다.
                self._sock.settimeout(self.timeout)

            self._sock.connect((self.host, self.port))
            self._is_connected = True

            if self._on_connect:
                self._on_connect()

            self._recv_thread = threading.Thread(
                target=self._recv_loop, daemon=True
            )
            self._recv_thread.start()  # 💡 스레드 시작 누락 수정

        except socket.error as e:
            self._sock = None
            self._is_connected = False
            if self._on_error:
                self._on_error(e)

            if self.reconnect and not self._stop_event.is_set():
                # 재접속 로직은 메인 스레드 블로킹 방지를 위해 별도의 스레드에서 호출하거나,
                # 여기서는 sleep 후 바로 호출하도록 유지합니다.
                time.sleep(self.reconnect_interval)
                self.connect()

    def disconnect(self) -> None:
        self._stop_event.set()
        self._is_connected = False

        if self._sock:
            try:
                self._sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            self._sock.close()
            self._sock = None

        if self._recv_thread and self._recv_thread.is_alive():
            self._recv_thread.join(timeout=0.1)

        if self._on_disconnect:
            self._on_disconnect()


    def send(self, data: bytes) -> None:
        if not self._sock or not self._is_connected:
            raise RuntimeError("TCPClient is not connected")

        # 💡 Union[bytes, str] 대신 bytes만 받도록 시그니처 변경
        if not isinstance(data, bytes):
            raise TypeError("send() must be called with bytes data")

        try:
            total_sent = 0
            while total_sent < len(data):
                sent = self._sock.send(data[total_sent:])
                if sent == 0:
                    raise ConnectionResetError("socket connection broken")
                total_sent += sent
        except Exception as e:
            if self._on_error:
                self._on_error(e)

            # 오류 발생 시 재접속 처리
            if self.reconnect:
                self.disconnect()
                # 💡 재연결은 비동기적으로 처리하는 것이 좋으나, 여기서는 동기적 호출 유지
                self.connect()
            else:
                raise


    # def recv_exact(self, size: int) -> bytes:
    #     if not self._sock or not self._is_connected:
    #         raise RuntimeError("TCPClient is not connected")
    #
    #     chunks: List[bytes] = []
    #     bytes_recd = 0
    #
    #     # 소켓 타임아웃은 self.timeout을 따릅니다.
    #     while bytes_recd < size:
    #         try:
    #             # 남은 바이트 수만큼만 요청하거나, 버퍼 크기만큼 요청
    #             remaining = size - bytes_recd
    #             chunk = self._sock.recv(min(remaining, self.recv_buffer))
    #
    #             if not chunk:
    #                 # 연결 끊김
    #                 raise ConnectionResetError("socket connection broken during recv")
    #
    #             chunks.append(chunk)
    #             bytes_recd += len(chunk)
    #
    #         except socket.timeout:
    #             # 타임아웃 발생 시, 아직 size만큼 다 받지 못했으면 재시도 (while 루프 유지)
    #             continue
    #         except Exception as e:
    #             # 그 외 오류 처리
    #             if self._on_error:
    #                 self._on_error(e)
    #             self.disconnect()
    #             raise
    #
    #     return b''.join(chunks)


    def _recv_loop(self):
        while not self._stop_event.is_set():
            try:
                if not self._sock:
                    break

                # 기존의 recv_buffer 크기만큼 청크를 수신
                chunk = self._sock.recv(self.recv_buffer)

                if not chunk:
                    # 연결 끊김
                    if not self._stop_event.is_set():
                        # 정상적인 disconnect 호출이 아니므로 재연결 고려
                        self.disconnect()
                        if self.reconnect:
                            time.sleep(self.reconnect_interval)
                            # 💡 재연결은 메인 스레드에서 관리하는 것이 더 안전하나, 여기서는 호출 유지
                            self.connect()
                    break

                if self._on_receive:
                    # 💡 콜백 시그니처 변경: (클라이언트 인스턴스, 수신 데이터 청크) 전달
                    self._on_receive(self, chunk)

            except socket.timeout:
                continue
            except Exception as e:
                if self._on_error:
                    self._on_error(e)

                # 오류 발생 시 정리 및 재접속 시도
                if not self._stop_event.is_set():
                    self.disconnect()
                    if self.reconnect:
                        time.sleep(self.reconnect_interval)
                        self.connect()
                break