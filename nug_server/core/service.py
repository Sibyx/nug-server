import abc
from enum import Enum
from typing import List

from nug_server.core.device import Device


class ServiceTypes(Enum):
    KEYBOARD = 'keyboard'
    VIDEO = 'video'
    MOUSE = 'mouse'


class DeviceContainer:
    def __init__(self):
        self._by_service = {
            'keyboard': {},
            'video': {},
            'mouse': {}
        }
        self._by_hostname = {}

    def set(self, service: str, host: str, device: Device):
        self._by_service[service][host] = device
        self._by_hostname[host] = device

    def remove(self, host: str):
        for service in self._by_service.keys():
            del self._by_service[service][host]

        del self._by_hostname[host]

    def shutdown(self):
        for host, transport in self._by_hostname.items():
            transport.close()
            self.remove(host)

    def all(self) -> List[Device]:
        return list(self._by_hostname.values())

    def __repr__(self):
        return self._by_service.__repr__()


class Service(abc.ABC):
    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def stop(self):
        pass
