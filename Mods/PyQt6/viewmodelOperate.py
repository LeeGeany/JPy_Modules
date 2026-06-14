from PySide6.QtCore import QObject, Signal

class CSignalBus(QObject):
    _instance = None

    def __init__(self):
        super().__init__()
        self._registry = {}  # 위젯 객체를 보관할 딕셔너리

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = CSignalBus()
        return cls._instance

    def register_service(self, name: str, obj: object):
        self._registry[name] = obj

    def get_service(self, name: str):
        return self._registry.get(name)