from ipaddress import ip_address
from typing import NamedTuple


class NetworkAddress:
    class Input(NamedTuple):
        address: str
        port: int = None

    def __init__(self, address: str):
        data = self.Input(*address.split(':'))

        self.ip_address = ip_address(data.address)
        self.port = data.port

    def __str__(self):
        return f"{self.ip_address}:{self.port}"
