import asyncio
import logging
from asyncio import Protocol, Transport

from nug_server.core.context import Context
from nug_server.core.service import DeviceContainer
from nug_server.rfb.frames import ProtocolVersion
from nug_server.core.states import BaseState
from nug_server.rfb.states.version import VersionState


class Server(Protocol):
    def __init__(self, config: dict, services: DeviceContainer):
        self._context = Context(config, services)
        self._state = VersionState(self._context)

    @property
    def state(self) -> BaseState:
        return self._state

    @state.setter
    def state(self, value: BaseState):
        logging.debug(
            "State change %s -> %s (old=%s,new=%s)",
            self._state, value, self._state, value
        )
        self._state = value

    def connection_made(self, transport: Transport):
        self._context.transport = transport
        logging.debug(
            "Making connection with %s:%d (context=%s)", *transport.get_extra_info('peername'), self._context
        )
        version_frame = ProtocolVersion(
            version=ProtocolVersion.RFBVersion.RFB_003_008
        )
        self._context.transport.write(version_frame.get_value())

    def data_received(self, data: bytes):
        logging.debug("Received: %s (context=%s,data=%s)", data.hex(), self._context, data.hex())
        self.state = self.state.handle(data)

    def connection_lost(self, exc: BaseException):
        logging.debug("Connection lost (context=%s)", self._context)

    @classmethod
    async def factory(cls, config: dict, services: DeviceContainer):
        loop = asyncio.get_running_loop()
        server = await loop.create_server(
            lambda: Server(config, services),
            host=config['general']['bind'],
            port=config['general']['port']
        )
        logging.info("Biding to %s on TCP port %d", ', '.join(config['general']['bind']), config['general']['port'])

        async with server:
            await server.serve_forever()
