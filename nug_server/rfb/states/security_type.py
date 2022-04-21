from nug_server.rfb.states.base import BaseState


class SecurityTypeState(BaseState):
    def handle(self, data: bytes):
        pass

    def __str__(self):
        return "SECURITY_TYPE"
