import threading
import time

class Spinlock:
    __slots__ = ('_lock', 'pause')

    def __init__(self, pause:float = 0.0):
        self._lock = threading.Lock()
        self.pause = pause

    def acquire(self) -> bool:
        return self._lock.acquire(blocking=False)

    def release(self) -> None:
        self._lock.release()

    def __enter__(self):
        while not self.acquire():
            if self.pause:
                time.sleep(self.pause)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
