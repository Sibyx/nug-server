from enum import Enum
from typing import List

from nug_server.core.device import Device


class ServiceType(Enum):
    KEYBOARD = 'keyboard'
    VIDEO = 'video'
    POINTER = 'pointer'


class DeviceContainer:
    def __init__(self):
        self._by_service = {
            ServiceType.KEYBOARD: {},
            ServiceType.VIDEO: {},
            ServiceType.POINTER: {}
        }
        self._by_hostname = {}

    def set(self, service: str, host: str, device: Device):
        self._by_service[ServiceType(service)][host] = device
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

    def service(self, service: ServiceType) -> List[Device]:
        return list(self._by_service[service].values())

    def has_service(self, service: ServiceType) -> bool:
        return len(self._by_service[service]) > 0

    def __repr__(self):
        return self._by_service.__repr__()
