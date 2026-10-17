import socket
import struct
from typing import Optional

class TcpServer:
    def __init__(
        self,
        host: str,
        port: int,
        backlog: int = 5,
        timeout: Optional[float] = None,
) -> None:

        self._host = host
        self._port = port
        self._backlog = backlog
        self._timeout = timeout

        self._server_socket: Optional[socket.socket] = None
        self._client_socket: Optional[socket.socket] = None

        self._client_address = None

    # ---------------------------------------------------------
    # Server
    # ---------------------------------------------------------

    def start(self) -> None:
        """Create and start listening socket."""

        if self._server_socket is not None:
            return

        server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        # Allow immediate rebinding after server restart.
        server_socket.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )

        if self._timeout is not None:
            server_socket.settimeout(self._timeout)

        server_socket.bind((self._host, self._port))
        server_socket.listen(self._backlog)

        self._server_socket = server_socket

    def stop(self) -> None:
        """Stop server and close current client."""

        self.disconnect_client()

        if self._server_socket is not None:
            try:
                self._server_socket.close()
            finally:
                self._server_socket = None

    # ---------------------------------------------------------
    # Client connection
    # ---------------------------------------------------------

    def accept_client(self) -> bool:
        """
        Wait for a client connection.

        If an old client is still connected, it is closed first.

        Returns:
            True  : client connected
            False : server socket is not available / timeout
        """

        if self._server_socket is None:
            raise RuntimeError("Server is not started.")

        self.disconnect_client()

        try:
            client_socket, client_address = (
                self._server_socket.accept()
            )
        except socket.timeout:
            return False

        if self._timeout is not None:
            client_socket.settimeout(self._timeout)

        print("accept_client")
        self._client_socket = client_socket
        self._client_address = client_address

        return True

    def disconnect_client(self) -> None:
        """Close current client connection."""

        if self._client_socket is not None:
            try:
                self._client_socket.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            finally:
                self._client_socket.close()
                self._client_socket = None
                self._client_address = None

    def is_connected(self) -> bool:
        """Return whether a client socket currently exists."""

        return self._client_socket is not None

    # ---------------------------------------------------------
    # Send
    # ---------------------------------------------------------

    def send_all(self, data: bytes) -> bool:
        """
        Send all bytes.

        socket.send() may transmit only part of the buffer,
        therefore sendall() is used.

        Returns:
            True  : success
            False : connection error
        """

        if self._client_socket is None:
            raise RuntimeError("Client is not connected.")

        try:
            self._client_socket.sendall(data)
            return True

        except (BrokenPipeError, ConnectionResetError, OSError):
            self.disconnect_client()
            return False

    def send_packet(self, data: bytes) -> bool:
        """
        Send length-prefixed packet.

        Packet:
            [4-byte payload length][payload]
        """

        if len(data) > 0xFFFFFFFF:
            raise ValueError("Packet is too large.")

        header = struct.pack(
            "!I",
            len(data)
        )

        if not self.send_all(header):
            return False

        return self.send_all(data)

    # ---------------------------------------------------------
    # Receive
    # ---------------------------------------------------------

    def recv_exact(self, size: int) -> Optional[bytes]:
        if self._client_socket is None:
            raise RuntimeError("Client is not connected.")

        if size < 0:
            raise ValueError("size must be >= 0")

        if size == 0:
            return b""

        received = bytearray()

        while len(received) < size:

            remaining = size - len(received)

            try:
                chunk = self._client_socket.recv(remaining)

            except socket.timeout:
                raise

            except (
                ConnectionResetError,
                BrokenPipeError,
                OSError
            ):
                self.disconnect_client()
                return None

            # recv() returning zero means peer closed connection.
            if not chunk:
                self.disconnect_client()
                return None

            received.extend(chunk)

        return bytes(received)


    def recv_packet(self, max_payload_size : int = 1024 * 1024) -> Optional[bytes]:

        header = self.recv_exact(4)

        if header is None:
            return None

        payload_size = struct.unpack("!I", header)[0]

        if payload_size > max_payload_size:
            raise ValueError(
                "Payload size exceeds maximum allowed size."
            )

        return self.recv_exact(payload_size)

    # ---------------------------------------------------------
    # Information
    # ---------------------------------------------------------

    @property
    def client_address(self):
        """Return connected client address."""

        return self._client_address

    @property
    def server_address(self):
        """Return server address."""

        if self._server_socket is None:
            return None

        return self._server_socket.getsockname()

    # ---------------------------------------------------------
    # Context manager
    # ---------------------------------------------------------

    def __enter__(self):
        self.start()
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback
    ):
        self.stop()

