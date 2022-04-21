from nug_server.rfb.frames import ProtocolVersion, SecurityTypes
from nug_server.rfb.states.base import BaseState
from nug_server.rfb.states.security_type import SecurityTypeState


class VersionState(BaseState):
    def handle(self, data: bytes):
        # Receive version string
        protocol_version = ProtocolVersion()
        protocol_version.read(data)
        self._context.version = protocol_version.version.value

        # Send security types
        security_types = SecurityTypes(
            size=len(self._context.security_types),
            types=self._context.security_types.keys()
        )
        security_types.write(self._context.transport)

        # Change state
        return SecurityTypeState(self._context)

    def __str__(self):
        return "VERSION"
