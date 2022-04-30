import logging
from enum import IntEnum
from io import BytesIO

from nug_server.core.service import ServiceType
from nug_server.core.states import BaseState
from nug_server.rfb.frames import SetPixelFormat, PointerEvent, FramebufferUpdateRequest


class ActiveState(BaseState):
    class ClientToServerType(IntEnum):
        SET_PIXEL_FORMAT = 0
        SET_ENCODINGS = 2
        FRAMEBUFFER_UPDATE_REQUEST = 3
        KEY_EVENT = 4
        POINTER_EVENT = 5
        CLIENT_CUT_TEXT = 6

    def handle(self, data: bytes):
        buffer = BytesIO(data)
        match self.ClientToServerType(data[0]):
            case self.ClientToServerType.SET_PIXEL_FORMAT:
                payload = SetPixelFormat()
                payload.read(buffer)
                self.set_pixel_format(payload)
            case self.ClientToServerType.POINTER_EVENT:
                payload = PointerEvent()
                payload.read(buffer)
                self.pointer_event(payload)
            case self.ClientToServerType.FRAMEBUFFER_UPDATE_REQUEST:
                payload = FramebufferUpdateRequest()
                payload.read(buffer)
                self.framebuffer_update_request(payload)
        return self

    def __str__(self) -> str:
        return "ACTIVE"

    def _parser(self, payload: bytes):

        pass

    def set_pixel_format(self, payload: SetPixelFormat):
        self.context.pixel_format = payload.pixel_format.value.to_dict()
        logging.debug("Pixel format: %s", self.context.pixel_format)

    def set_encodings(self, payload):
        pass

    def key_event(self, payload):
        pass

    def pointer_event(self, payload: PointerEvent):
        for device in self.context.devices.service(ServiceType.POINTER):
            # Create Nug Frame
            data = payload.get_value()[1:]
            device.transport.write(data)

        logging.debug(f'Received PointerEvent: {payload}')

    def client_cuts_text(self, payload):
        pass

    def framebuffer_update_request(self, payload: FramebufferUpdateRequest):
        crop = self.context.video_processor.frame[payload.y.value:payload.y.value + payload.height.value, payload.x.value:payload.x.value + payload.width.value]
        logging.debug(self.context.video_processor.frame)
