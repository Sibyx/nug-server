from enum import Enum

from nug_server.core.frames.base import Frame
from nug_server.core.frames import fields


class ProtocolVersion(Frame):
    class RFBVersion(Enum):
        RFB_003_003 = "RFB 003.003\n"
        RFB_003_007 = "RFB 003.007\n"
        RFB_003_008 = "RFB 003.008\n"

    version = fields.EnumField(RFBVersion)


class SecurityTypes(Frame):
    size = fields.U8()
    types = fields.ArrayField(fields.U8())


class SecurityType(Frame):
    method = fields.U8()


class SecurityResult(Frame):
    result = fields.U32()


class ClientInit(Frame):
    shared = fields.U8()


class PixelFormat(Frame):
    bits_per_pixel = fields.U8()
    depth = fields.U8()
    big_endian = fields.U8()
    true_color = fields.U8()
    red_max = fields.U16()
    green_max = fields.U16()
    blue_max = fields.U16()
    red_shift = fields.U8()
    green_shift = fields.U8()
    blue_shift = fields.U8()
    padding = fields.PaddingField(size=3)


class ServerInit(Frame):
    width = fields.U16()
    height = fields.U16()
    pixel_format = fields.FrameField(PixelFormat())
    name_length = fields.U32()
    name = fields.StringField()


class SetPixelFormat(Frame):
    type = fields.U8()
    padding = fields.PaddingField(size=3)
    pixel_format = fields.FrameField(PixelFormat())


class SetEncodings(Frame):
    type = fields.U8()
    padding = fields.PaddingField(size=3)
    encodings = fields.ArrayField(fields.U32(), header=fields.U16())


class FramebufferUpdateRequest(Frame):
    type = fields.U8()
    incremental = fields.U8()
    x = fields.U16()
    y = fields.U16()
    width = fields.U8()
    height = fields.U8()


class KeyEvent(Frame):
    type = fields.U8()
    down = fields.U8()
    padding = fields.PaddingField(size=2)
    key = fields.U32()


class PointerEvent(Frame):
    type = fields.U8()
    buttons = fields.U8()
    x = fields.U16()
    y = fields.U16()


class ClientCutText(Frame):
    type = fields.U8()
    padding = fields.PaddingField(size=3)
