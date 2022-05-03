import io
import logging
import struct
import time
from enum import IntEnum

import cv2

from nug_server.core.service import ServiceType
from nug_server.core.states import BaseState
from nug_server.rfb.frames import client
from nug_server.rfb.frames import server
from nug_server.core.frames import internal


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
        cmd = await self.context.reader.read(1)
        if not cmd:
            return self

        try:
            frame_type = self.ClientToServerType.parse(cmd)
        except ValueError:
            logging.error("Invalid frame type received")
            return self

        match frame_type:
            case self.ClientToServerType.SET_PIXEL_FORMAT:
                payload = client.SetPixelFormat()
                await payload.read(self.context.reader)
                self.set_pixel_format(payload)
            case self.ClientToServerType.SET_ENCODINGS:
                payload = client.SetEncodings()
                await payload.read(self.context.reader)
                self.set_encodings(payload)
            case self.ClientToServerType.POINTER_EVENT:
                payload = client.PointerEvent()
                await payload.read(self.context.reader)
                self.pointer_event(payload)
            case self.ClientToServerType.KEY_EVENT:
                payload = client.KeyEvent()
                await payload.read(self.context.reader)
                self.key_event(payload)
            case self.ClientToServerType.FRAMEBUFFER_UPDATE_REQUEST:
                payload = client.FramebufferUpdateRequest()
                await payload.read(self.context.reader)
                self.framebuffer_update_request(payload)

        return self

    def __str__(self) -> str:
        return "ACTIVE"

    def set_pixel_format(self, payload: client.SetPixelFormat):
        self.context.pixel_format = payload.pixel_format.value.to_dict()
        logging.debug("Pixel format: %s", self.context.pixel_format)

    def set_encodings(self, payload: client.SetEncodings):
        self.context.encodings = payload.encodings.value
        logging.debug("Encodings: %s", self.context.encodings)

    def key_event(self, payload: client.KeyEvent):
        logging.debug(f'Received KeyEvent: {payload}')
        frame = internal.KeyEvent(
            type=internal.MessageType.KEY_EVENT.value,
            down=payload.down.value,
            key=payload.key.value
        )
        for device in self.context.devices.service(ServiceType.KEYBOARD):
            device.transport.write(frame.get_value())

    def pointer_event(self, payload: client.PointerEvent):
        logging.debug(f'Received PointerEvent: {payload}')
        frame = internal.PointerEvent(
            type=internal.MessageType.POINTER_EVENT.value,
            buttons=payload.buttons.value,
            x=payload.x.value,
            y=payload.y.value
        )
        for device in self.context.devices.service(ServiceType.POINTER):
            device.transport.write(frame.get_value())

    def client_cuts_text(self, payload):
        pass

    def framebuffer_update_request(self, payload: client.FramebufferUpdateRequest):
        logging.debug(f'Received FramebufferUpdateRequest: {payload.to_dict()}')

        if not self.context.video_processor.is_alive():
            return

        while self.context.video_processor.frame is None:
            time.sleep(1)

        if self.context.video_processor.frame is None:
            return

        # https://jdhao.github.io/2019/07/06/python_opencv_pil_image_to_bytes/
        img_encode = cv2.imencode('.jpg', self.context.video_processor.frame)[1]

        frame = server.FramebufferUpdate(
            rectangles=[
                server.Rectangle(
                    x=0,
                    y=0,
                    width=1280,
                    height=1024,
                    encoding=21
                )
            ]
        )
        buffer = io.BytesIO()
        buffer.write(frame.get_value())
        buffer.write(img_encode.tobytes())

        self.context.writer.write(buffer.getvalue())
