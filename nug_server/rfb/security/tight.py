from nug_server.core.context import Context
from nug_server.rfb.security.base import BaseSecurityType


class TightSecurityType(BaseSecurityType):
    def __init__(self, context: Context):
        super().__init__(context)
        self._state = None

    def handle(self, data: bytes):
        pass
