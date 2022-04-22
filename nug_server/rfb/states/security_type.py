import logging

from nug_server.core.context import Context
from nug_server.core.utils import resolve_from_path
from nug_server.rfb import frames
from nug_server.rfb.security.base import BaseSecurityType
from nug_server.core.states import BaseState
from nug_server.rfb.states.init import InitState


class SecurityTypeState(BaseState):
    def __init__(self, context: Context):
        super().__init__(context)
        self._security = None

    def handle(self, data: bytes):
        if not self._security:
            security_type = frames.SecurityType()
            security_type.read(data)

            try:
                driver = resolve_from_path(self.context.security_types[security_type.method.value])
                logging.info("Security type %s", driver)
                self._security = driver(self.context)
            except KeyError as e:
                logging.critical("Unknown security type %d", security_type.method.value)

        match self._security.handle(data):
            case BaseSecurityType.Result.OK:
                return InitState(self.context)
            case BaseSecurityType.Result.RUNNING:
                return self
            case _:
                return self

    def __str__(self):
        return "SECURITY_TYPE"
