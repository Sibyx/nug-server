from nug_server.rfb.frames import SecurityType, SecurityResult
from nug_server.rfb.states.base import BaseState
from nug_server.rfb.states.init import InitState


class SecurityTypeState(BaseState):
    def handle(self, data: bytes):
        security_type = SecurityType()
        security_type.read(data)
        if self._context.security_types[security_type.method.value[0]]:
            return self

        security_result = SecurityResult(result=0)
        security_result.write(self._context.transport)

        return InitState(self._context)

    def __str__(self):
        return "SECURITY_TYPE"
