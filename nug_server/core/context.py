import logging
from asyncio import StreamReader, StreamWriter
from typing import Optional, Dict, Union, List
from uuid import uuid4, UUID

from nug_server.core.service import DeviceContainer
from nug_server.core.video_processor import VideoProcessor
from nug_server.rfb.frames.server import ProtocolVersion


class Context:
    def __init__(self, config: dict, devices: DeviceContainer, video_processor: Optional[VideoProcessor]):
        self._pixel_format = None
        self._encodings = None
        self._id = uuid4()
        self._config = config
        self._reader = None
        self._writer = None
        self._devices = devices
        self._version = ProtocolVersion.RFBVersion.RFB_003_003
        self._security_types = {
            1: 'nug_server.rfb.security.none_security_type.NoneSecurityType',
            # 2: 'nug_server.rfb.security.vnc.VNCSecurityType',
            # 16: 'nug_server.rfb.security.tight.TunnelingState'
        }
        self._video_processor = video_processor

    def __str__(self):
        return str(self._id)

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def reader(self) -> StreamReader:
        return self._reader

    @reader.setter
    def reader(self, value: StreamReader):
        self._reader = value

    @property
    def writer(self) -> StreamWriter:
        return self._writer

    @writer.setter
    def writer(self, value: StreamWriter):
        self._writer = value

    @property
    def config(self) -> dict:
        return self._config

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

    @property
    def devices(self) -> DeviceContainer:
        return self._devices

    @property
    def security_types(self) -> Dict[int, Union[str, None]]:
        return self._security_types

    @property
    def video_processor(self) -> Optional[VideoProcessor]:
        return self._video_processor

    @property
    def pixel_format(self) -> dict:
        return self._pixel_format

    @pixel_format.setter
    def pixel_format(self, value: dict):
        self._pixel_format = value

    @property
    def encodings(self) -> Optional[List[int]]:
        return self._encodings

    @encodings.setter
    def encodings(self, value: List[int]):
        self._encodings = value
