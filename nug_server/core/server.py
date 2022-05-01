import asyncio
import inspect
import logging
from asyncio import Protocol, StreamReader, StreamWriter
from typing import Optional

from nug_server.core.context import Context
from nug_server.core.service import DeviceContainer
from nug_server.core.video_processor import VideoProcessor
from nug_server.core.states import BaseState
from nug_server.rfb.frames.server import ProtocolVersion
from nug_server.rfb.states.version import VersionState


class Server(Protocol):
    def __init__(self, config: dict, services: DeviceContainer, video_processor: Optional[VideoProcessor] = None):
        self._context = Context(config, services, video_processor)
        self._state = None

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

    async def __call__(self, reader: StreamReader, writer: StreamWriter):
        self._context.reader = reader
        self._context.writer = writer

        logging.debug(
            "Making connection with %s:%d (context=%s)", *writer.get_extra_info('peername'), self._context
        )

        version_frame = ProtocolVersion(
            version=ProtocolVersion.RFBVersion.RFB_003_008.value
        )
        version_frame.write(self._context.writer)

        self.state = VersionState(self._context)

        while not self._context.reader.at_eof():
            state = self.state.handle()
            if inspect.iscoroutine(state):
                self.state = await state
            else:
                self.state = state
        else:
            logging.debug("Connection lost (context=%s)", self._context)

    @classmethod
    async def factory(cls, config: dict, services: DeviceContainer, video_processor: Optional[VideoProcessor] = None):
        server = await asyncio.start_server(
            Server(config, services, video_processor),
            host=config['general']['bind'],
            port=config['general']['port']
        )
        logging.info("Biding to %s on TCP port %d", ', '.join(config['general']['bind']), config['general']['port'])

        async with server:
            await server.serve_forever()
