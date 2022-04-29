from enum import IntEnum

from nug_server.core.frames import fields
from nug_server.core.frames.base import Frame
from nug_server.core.states import BaseState
from nug_server.rfb import frames
from nug_server.rfb.states.init import InitState


class TightCapabilityFrame(Frame):
    code = fields.S32()
    vendor = fields.StructField("4s")
    signature = fields.StructField("8s")


class TightCapabilitiesFrame(Frame):
    capabilities = fields.ArrayField(field=fields.FrameField(TightCapabilityFrame()), header=fields.U32())


class TunnelingState(BaseState):
    class TunnelCapability(IntEnum):
        NOTUNNEL = 0

    capabilities = {
        TunnelCapability.NOTUNNEL: TightCapabilityFrame(
            code=0, vendor="TGHT".encode(), signature='NOTUNNEL'.encode(),
        )
    }

    def handle(self, data: bytes):
        frame = TightCapabilitiesFrame(
            capabilities=self.capabilities.values()
        )
        self.context.transport.write(frame.get_value())

        return SecurityState(self.context)

    def __str__(self):
        return "TIGHT_TUNNELING_STATE"


class SecurityState(BaseState):
    class TightAuthCapability(IntEnum):
        NONE = 1
        VNC_AUTHENTICATION = 2
        VENCRYPT = 19
        SASL = 20
        UNIX_LOGIN = 129
        EXTERNAL = 130

    capabilities = {
        TightAuthCapability.UNIX_LOGIN: TightCapabilityFrame(
            code=129, vendor="TGHT".encode(), signature='ULGNAUTH'.encode(),
        ),
        TightAuthCapability.NONE: TightCapabilityFrame(
            code=1, vendor="STDV".encode(), signature='NOAUTH__'.encode(),
        )
    }

    def handle(self, data: bytes):
        # FIXME: this probably doesn't work properly, check tcpdump output for more info
        frame = TightCapabilitiesFrame(
            capabilities=self.capabilities.values()
        )
        self.context.transport.write(frame.get_value())

        return AuthenticationState(self.context)

    def __str__(self):
        return "TIGHT_SECURITY_STATE"


class AuthenticationState(BaseState):
    def handle(self, data: bytes):
        security_result = frames.SecurityResult(result=0)
        self.context.transport.write(security_result.get_value())
        return InitState(self.context)

    def __str__(self):
        return "TIGHT_AUTHENTICATION_STATE"
