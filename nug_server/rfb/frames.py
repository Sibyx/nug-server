from enum import Enum

from nug_server.core.frames.base import Frame
from nug_server.core.frames.fields import String


class ProtocolVersion(Frame):
    class RFBVersion(Enum):
        RFB_003_003 = "RFB 003.003\n"
        RFB_003_007 = "RFB 003.007\n"
        RFB_003_008 = "RFB 003.008\n"

    version = String()


class SecurityTypes(Frame):
    pass
