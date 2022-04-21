from abc import ABC, abstractmethod

from nug_server.rfb.frames import ProtocolVersion


class BaseState(ABC):
    def __init__(self, context):
        self._context = context

    @abstractmethod
    def handle(self, data: bytes):
        pass


class VersionState(BaseState):
    def handle(self, data: bytes):
        # Receive version string
        protocol_version = ProtocolVersion()
        protocol_version.read(data)
        self._context.version = protocol_version.version.value

        # Send security types

        # Change state
        self._context.state = SecurityTypeState(self._context)

    def __str__(self):
        return "VERSION"


class SecurityTypeState(BaseState):
    def handle(self, data: bytes):
        pass

    def __str__(self):
        return "SECURITY_TYPE"
