from nug_server.core.states import BaseState
from nug_server.rfb.frames.server import SecurityResult
from nug_server.rfb.states.init import InitState


class NoneSecurityType(BaseState):
    async def handle(self):
        security_result = SecurityResult(result=0)
        security_result.write(self.context.writer)
        return InitState(self.context)

    def __str__(self):
        return "NONE_SECURITY_TYPE"

