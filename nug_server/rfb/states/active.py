from nug_server.core.states import BaseState


class ActiveState(BaseState):
    def handle(self, data: bytes):
        return self

    def __str__(self) -> str:
        return "active"
