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
    # name = fields.ArrayField(fields.StructField('c'), header=fields.U8())


class StopStream(Frame):
    type = fields.U8()
