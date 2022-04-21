from nug_server.rfb.frames import ProtocolVersion
from nug_server.rfb.states.base import BaseState
from nug_server.rfb.states.security_type import SecurityTypeState


class VersionState(BaseState):
    def handle(self, data: bytes):
        # Receive version string
        protocol_version = ProtocolVersion()
        protocol_version.read(data)
        self._context.version = protocol_version.version.value

        # Send security types

        # Change state
        return SecurityTypeState(self._context)

    def __str__(self):
        return "VERSION"
