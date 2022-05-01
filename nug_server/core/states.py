from abc import abstractmethod, ABC

from nug_server.core.context import Context


class BaseState(ABC):
    def __init__(self, context: Context):
        self.context = context

    @abstractmethod
    async def handle(self):
        pass
