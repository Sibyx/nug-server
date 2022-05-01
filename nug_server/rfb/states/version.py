from nug_server.core.states import BaseState
from nug_server.rfb.frames.server import ProtocolVersion, SecurityTypes
from nug_server.rfb.states.security_type import SecurityTypeState


class VersionState(BaseState):
    async def handle(self):
        # Receive version string
        protocol_version = ProtocolVersion()
        await protocol_version.read(self.context.reader)
        self.context.version = ProtocolVersion.RFBVersion(protocol_version.version.value)

        # Send security types
        security_types = SecurityTypes(
            size=len(self.context.security_types),
            types=self.context.security_types.keys()
        )
        security_types.write(self.context.writer)

        # Change state
        return SecurityTypeState(self.context)

    def __str__(self):
        return "VERSION"
