from io import BytesIO

from nug_server.rfb.frames import ClientInit, ServerInit, PixelFormat
from nug_server.rfb.states.active import ActiveState
from nug_server.core.states import BaseState


class InitState(BaseState):
    def handle(self, data: bytes):
        buffer = BytesIO(data)
        client_init = ClientInit()
        client_init.read(buffer)

        server_name = self.context.config['general'].get('name', 'Super Nug VNC Server')

        server_init = ServerInit(
            width=1024,
            height=768,
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
            name_length=len(server_name),
            name=server_name
        )

        self.context.transport.write(server_init.get_value())

        return ActiveState(self.context)

    def __str__(self):
        return "INIT"
