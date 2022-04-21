import asyncio
import logging
from asyncio import Protocol, Transport

from nug_server.core.context import Context
from nug_server.core.network import NetworkAddress
from nug_server.rfb.frames import ProtocolVersion
from nug_server.rfb.states.base import BaseState
from nug_server.rfb.states.version import VersionState


class RFBProtocol(Protocol):
    # class State(enum.IntEnum):
    #     VERSION = 1
    #     SECURITY_TYPE = 2
    #     SECURITY = 3
    #     INIT = 4
    #     ACTIVE = 5

    def __init__(self, config: dict):
        # https://docs.python.org/3/library/asyncio-protocol.html#tcp-echo-server
        # TCP client: nc localhost <port>
        # TODO: state
        # TODO: parse config, prepare services
        self._context = Context(config)
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
        version_frame.write(self._context.transport)

    def data_received(self, data: bytes):
        logging.debug("Received: %s (context=%s,data=%s)", data.hex(), self._context, data.hex())

        self.state = self.state.handle(data)

        # test = ProtocolVersion(
        #     version=ProtocolVersion.RFBVersion.RFB_003_008.value
        # )
        # test.write(self._transport)

    def connection_lost(self, exc: BaseException):
        logging.debug("Connection lost (context=%s)", self._context)

    @classmethod
    async def factory(cls, config: dict):
        loop = asyncio.get_running_loop()
        bind = NetworkAddress(config['general']['bind'])

        server = await loop.create_server(
            lambda: RFBProtocol(config),
            str(bind.ip_address), bind.port
        )

        async with server:
            await server.serve_forever()
