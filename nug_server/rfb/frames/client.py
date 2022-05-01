from nug_server.core.frames import fields
from nug_server.core.frames.base import Frame
from nug_server.rfb.frames.server import PixelFormat


class ClientInit(Frame):
    shared = fields.U8()


class SetPixelFormat(Frame):
    padding = fields.PaddingField(size=3)
    pixel_format = fields.FrameField(PixelFormat())


class SetEncodings(Frame):
    padding = fields.PaddingField(size=1)
    encodings = fields.ArrayField(fields.U32(), header=fields.U16())


class FramebufferUpdateRequest(Frame):
    incremental = fields.U8()
    x = fields.U16()
    y = fields.U16()
    width = fields.U8()
    height = fields.U8()


class KeyEvent(Frame):
    down = fields.U8()
    padding = fields.PaddingField(size=2)
    key = fields.U32()


class PointerEvent(Frame):
    buttons = fields.U8()
    x = fields.U16()
    y = fields.U16()


class ClientCutText(Frame):
    type = fields.U8()
    padding = fields.PaddingField(size=3)
