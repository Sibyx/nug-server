from nug_server.rfb import frames
from nug_server.rfb.security.base import BaseSecurityType


class NoneSecurityType(BaseSecurityType):
    def handle(self, data: bytes):
        security_result = frames.SecurityResult(result=0)
        self.context.transport.write(security_result.get_value())
        return BaseSecurityType.Result.OK
