import logging
from asyncio import Transport
from typing import Optional, Dict
from uuid import uuid4, UUID

from nug_server.rfb.frames import ProtocolVersion


class Context:
    def __init__(self, config: dict):
        self._id = uuid4()
        self._config = config
        self._transport = None
        self._version = ProtocolVersion.RFBVersion.RFB_003_003
        self._security_types = {
            1: None,
            # 2: 'nug_server.rfb.security.vnc.VNCSecurityType',
            # 16: 'nug_server.rfb.security.tight.TightSecurityType'
        }

    def __str__(self):
        return str(self._id)

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def transport(self) -> Optional[Transport]:
        return self._transport

    @transport.setter
    def transport(self, value: Transport):
        self._transport = value

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
    def security_types(self) -> Dict[int, str]:
        return self._security_types
