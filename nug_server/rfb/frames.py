from enum import Enum

from nug_server.core.frames.base import Frame
from nug_server.core.frames.fields import EnumField, StructField, ArrayField


class ProtocolVersion(Frame):
    class RFBVersion(Enum):
        RFB_003_003 = "RFB 003.003\n"
        RFB_003_007 = "RFB 003.007\n"
        RFB_003_008 = "RFB 003.008\n"

    version = EnumField(RFBVersion)


class SecurityTypes(Frame):
    size = StructField('B')
    types = ArrayField(StructField('B'))


class SecurityType(Frame):
    method = StructField('B')


class SecurityResult(Frame):
    result = StructField('L')
