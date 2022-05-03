import logging
from time import sleep

from nug_server.core.frames import internal
from nug_server.core.service import ServiceType
from nug_server.rfb.frames.client import ClientInit
from nug_server.rfb.frames.server import ServerInit, PixelFormat
from nug_server.rfb.states.active import ActiveState
from nug_server.core.states import BaseState


class InitState(BaseState):
    async def handle(self):
        client_init = ClientInit()
        await client_init.read(self.context.reader)

        server_name = self.context.config['general'].get('name', 'Super Nug VNC Server')

        server_init = ServerInit(
            width=1280,
            height=1024,
            pixel_format=PixelFormat(
                bits_per_pixel=32,
                depth=24,
                big_endian=0,
                true_color=1,
                red_max=255,
                green_max=255,
                blue_max=255,
                red_shift=16,
                green_shift=8,
                blue_shift=0
            ),
            name=server_name
        )

        server_init.write(self.context.writer)

        for device in self.context.devices.service(ServiceType.VIDEO):
            start_stream = internal.StartStream(
                type=internal.MessageType.START_STREAM.value,
                width=1280,
                height=1024,
                name=self.context.config['general']['name']
            )
            device.transport.write(start_stream.get_value())
            logging.debug("Start stream: %s", start_stream.get_value().hex())
            # FIXME: picovina
            sleep(3)
            if not self.context.video_processor.is_alive():
                self.context.video_processor.start()

        return ActiveState(self.context)

    def __str__(self):
        return "INIT"
