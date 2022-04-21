from abc import ABC, abstractmethod

from nug_server.core.context import Context


class BaseSecurityType(ABC):
    def __init__(self, context: Context):
        self._context = context

    @abstractmethod
    def handle(self, data: bytes):
        pass
