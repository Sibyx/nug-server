from abc import ABC, abstractmethod
from enum import Enum

from nug_server.core.context import Context


class BaseSecurityType(ABC):
    def __init__(self, context: Context):
        self.context = context

    class Result(Enum):
        RUNNING = 'running'
        FAILED = 'failed'
        OK = 'ok'

    @abstractmethod
    def handle(self, data: bytes) -> Result:
        return self.Result.RUNNING
