import asyncio
import logging
import uuid
from asyncio import Protocol, Transport

from nug_server.core.network import NetworkAddress
from nug_server.rfb.frames import ProtocolVersion
from nug_server.rfb.states import VersionState, BaseState


class RFBProtocol(Protocol):
    # class State(enum.IntEnum):
    #     VERSION = 1
    #     SECURITY_TYPE = 2
    #     SECURITY = 3
    #     INIT = 4
    #     ACTIVE = 5

    def __init__(self):
        # https://docs.python.org/3/library/asyncio-protocol.html#tcp-echo-server
        # TCP client: nc localhost <port>
        # TODO: state
        # TODO: parse config, prepare services
        self._id = uuid.uuid4()
        self._transport = None
        self._state = VersionState(self)
        self._version = ProtocolVersion.RFBVersion.RFB_003_003

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

    @property
    def version(self) -> ProtocolVersion.RFBVersion:
        return self._version

    @version.setter
    def version(self, value):
        logging.debug(
            "Changing server version %s -> %s (old=%s,new=%s)",
            self._version, value, self._version, value
        )
        self._version = ProtocolVersion.RFBVersion(value)

    def connection_made(self, transport: Transport):
        self._transport = transport
        logging.debug("Making connection with %s:%d (session=%s)", *transport.get_extra_info('peername'), self._id)
        version_frame = ProtocolVersion(
            version=ProtocolVersion.RFBVersion.RFB_003_008
        )
        version_frame.write(self._transport)

    def data_received(self, data: bytes):
        logging.error("Received: %s (session=%s,data=%s)", data.hex(), self._id, data.hex())

        self.state.handle(data)

        # test = ProtocolVersion(
        #     version=ProtocolVersion.RFBVersion.RFB_003_008.value
        # )
        # test.write(self._transport)

    def connection_lost(self, exc: BaseException):
        logging.debug("Connection lost (session=%s)", self._id)

    @classmethod
    async def factory(cls, bind: NetworkAddress):
        loop = asyncio.get_running_loop()

        server = await loop.create_server(
            lambda: RFBProtocol(),
            str(bind.ip_address), bind.port
        )

        async with server:
            await server.serve_forever()
