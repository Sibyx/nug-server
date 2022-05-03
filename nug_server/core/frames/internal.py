from enum import IntEnum

from nug_server.core.frames import fields
from nug_server.core.frames.base import Frame


class MessageType(IntEnum):
    START_STREAM = 1
    STOP_STREAM = 2
    POINTER_EVENT = 3
    KEY_EVENT = 4


class StartStream(Frame):
    type = fields.U8()
    width = fields.U16()
    height = fields.U16()
    name = fields.StringField(header=fields.U8())


class StopStream(Frame):
    type = fields.U8()


class KeyEvent(Frame):
    type = fields.U8()
    down = fields.U8()
    key = fields.U32()


class PointerEvent(Frame):
    type = fields.U8()
    buttons = fields.U8()
    x = fields.U16()
    y = fields.U16()
