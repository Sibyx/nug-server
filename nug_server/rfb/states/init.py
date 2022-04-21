from nug_server.rfb.states.base import BaseState


class InitState(BaseState):
    def handle(self, data: bytes):
        return self

    def __str__(self):
        return "init"
