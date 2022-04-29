from nug_server.core.states import BaseState
from nug_server.rfb import frames
from nug_server.rfb.states.init import InitState


class NoneSecurityType(BaseState):
    def handle(self, data: bytes):
        security_result = frames.SecurityResult(result=0)
        self.context.transport.write(security_result.get_value())
        return InitState(self.context)

    def __str__(self):
        return "NONE_SECURITY_TYPE"

