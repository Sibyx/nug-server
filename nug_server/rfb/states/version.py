from io import BytesIO

from nug_server.rfb.frames import ProtocolVersion, SecurityTypes
from nug_server.core.states import BaseState
from nug_server.rfb.states.security_type import SecurityTypeState


class VersionState(BaseState):
    def handle(self, data: bytes):
        buffer = BytesIO(data)
        # Receive version string
        protocol_version = ProtocolVersion()
        protocol_version.read(buffer)
        self.context.version = protocol_version.version.value

        # Send security types
        security_types = SecurityTypes(
            size=len(self.context.security_types),
            types=self.context.security_types.keys()
        )
        self.context.transport.write(security_types.get_value())

        # Change state
        return SecurityTypeState(self.context)

    def __str__(self):
        return "VERSION"
