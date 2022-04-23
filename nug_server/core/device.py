import asyncio
import logging
from asyncio import Transport


class Device(asyncio.Protocol):
    def __init__(self, config: dict, container):
        self._config = config
        self._container = container
        self._transport = None
        self._host = None

    @property
    def transport(self) -> Transport:
        return self._transport

    def connection_made(self, transport: Transport):
        self._host, port = transport.get_extra_info('peername')
        self._transport = transport

        for service in self._config['services']:
            self._container.set(service, self._host, self)

        self._transport.write("Hi boy!".encode())
        logging.debug(
            "Making connection with %s:%d", self._host, port
        )

    def data_received(self, data):
        logging.debug("Received: %s (data=%s)", data.hex(), data.hex())

    def connection_lost(self, exc):
        self._container.remove(self._host)
        logging.debug("Connection lost")

    @classmethod
    def factory(cls, config: dict, container):
        loop = asyncio.new_event_loop()
        coro = loop.create_connection(
            lambda: Device(config, container),
            config['ip'], config['port']
        )
        logging.info("Connecting to %s:%d to provide: %s", config['ip'], config['port'], ', '.join(config['services']))
        loop.run_until_complete(coro)
        loop.run_forever()
        loop.close()
