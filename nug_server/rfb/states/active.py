import logging
import struct
import time
from enum import IntEnum

from nug_server.core.service import ServiceType
from nug_server.core.states import BaseState
from nug_server.rfb.frames.client import SetPixelFormat, SetEncodings, PointerEvent, KeyEvent, FramebufferUpdateRequest


class ActiveState(BaseState):
    class ClientToServerType(IntEnum):
        SET_PIXEL_FORMAT = 0
        SET_ENCODINGS = 2
        FRAMEBUFFER_UPDATE_REQUEST = 3
        KEY_EVENT = 4
        POINTER_EVENT = 5
        CLIENT_CUT_TEXT = 6

        @classmethod
        def parse(cls, value: bytes):
            data = struct.unpack("B", value)[0]
            return cls(data)

    async def handle(self):
        try:
            frame_type = self.ClientToServerType.parse(await self.context.reader.read(1))
        except ValueError:
            logging.error("Invalid frame type received")
            return self

        match self.ClientToServerType(frame_type):
            case self.ClientToServerType.SET_PIXEL_FORMAT:
                payload = SetPixelFormat()
                await payload.read(self.context.reader)
                self.set_pixel_format(payload)
            case self.ClientToServerType.SET_ENCODINGS:
                payload = SetEncodings()
                await payload.read(self.context.reader)
                self.set_encodings(payload)
            case self.ClientToServerType.POINTER_EVENT:
                payload = PointerEvent()
                await payload.read(self.context.reader)
                self.pointer_event(payload)
            case self.ClientToServerType.KEY_EVENT:
                payload = KeyEvent()
                await payload.read(self.context.reader)
                self.key_event(payload)
            case self.ClientToServerType.FRAMEBUFFER_UPDATE_REQUEST:
                payload = FramebufferUpdateRequest()
                await payload.read(self.context.reader)
                self.framebuffer_update_request(payload)

        return self

    def __str__(self) -> str:
        return "ACTIVE"

    def set_pixel_format(self, payload: SetPixelFormat):
        self.context.pixel_format = payload.pixel_format.value.to_dict()
        logging.debug("Pixel format: %s", self.context.pixel_format)

    def set_encodings(self, payload: SetEncodings):
        self.context.encodings = payload.encodings.value
        logging.debug("Encodings: %s", self.context.encodings)

    def key_event(self, payload: KeyEvent):
        logging.debug(f'Received KeyEvent: {payload}')

    def pointer_event(self, payload: PointerEvent):
        for device in self.context.devices.service(ServiceType.POINTER):
            # Create Nug Frame
            data = payload.get_value()
            device.transport.write(data)

        logging.debug(f'Received PointerEvent: {payload}')

    def client_cuts_text(self, payload):
        pass

    def framebuffer_update_request(self, payload: FramebufferUpdateRequest):
        logging.debug(payload)

        while self.context.video_processor.frame is None:
            time.sleep(1)

        if self.context.video_processor.frame is None:
            return

        logging.debug(self.context.video_processor.frame)

        crop = self.context.video_processor.frame[
               payload.y.value:payload.y.value + payload.height.value,
               payload.x.value:payload.x.value + payload.width.value
               ]

        logging.debug(crop)
