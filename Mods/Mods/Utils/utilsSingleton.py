from __future__ import annotations

import threading
from typing import Any, Type, TypeVar, Generic, cast

T = TypeVar('T', bound='CSingletonBase')

class CSingletonMeta(type):
    _instance: dict[Type[Any], Any]                = {}
    _instance_lock: dict[Type[Any], threading.Lock] = {}

    def __call__(cls: Type[T], *args: Any, **kwargs: Any) -> T:
        if cls not in cls._instance_lock:
            with threading.Lock():
                if cls not in cls._instance_lock:
                    cls._instance_lock[cls] = threading.Lock()

        with cls._instance_lock[cls]:
            if cls not in cls._instance:
                instance = super().__call__(*args, **kwargs)
                cls._instance[cls] = instance
            else:
                instance = cls._instance[cls]

        return cast(T, instance)

class CSingletonBase(metaclass=CSingletonMeta):
    __initialized : bool = False

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if self.__initialized:
            return
        self.__initialized = True