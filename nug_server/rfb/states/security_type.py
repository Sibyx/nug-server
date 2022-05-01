import logging

from nug_server.core.context import Context
from nug_server.core.utils import resolve_from_path
from nug_server.core.states import BaseState
from nug_server.rfb.frames.server import SecurityType


class SecurityTypeState(BaseState):
    def __init__(self, context: Context):
        super().__init__(context)
        self._security = None

    async def handle(self):
        if not self._security:
            security_type = SecurityType()
            await security_type.read(self.context.reader)

            try:
                driver = resolve_from_path(self.context.security_types[security_type.method.value])
                self._security = driver(self.context)
            except KeyError as e:
                logging.critical("Unknown security type %d", security_type.method.value)

        return self._security

    def __str__(self):
        return "SECURITY_TYPE"
