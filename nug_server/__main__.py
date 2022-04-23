import argparse
import asyncio
import logging
import threading
from ipaddress import ip_address
from logging.handlers import SysLogHandler
from pathlib import Path

import tomli as tomli
from zeroconf import ServiceInfo, Zeroconf, IPVersion

from nug_server import version
from nug_server.core.device import Device
from nug_server.core.server import Server
from nug_server.core.service import DeviceContainer

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--config', '-c', type=Path)
    args = parser.parse_args()

    # Read config file
    with open(args.config, "rb") as f:
        config = tomli.load(f)

    # Set loglevel
    logging.getLogger().setLevel(config['general'].get('log_level', 'INFO'))

    if 'syslog' in config:
        handler = SysLogHandler(address=(config['syslog']['ip'], config['syslog']['port']))
        logging.getLogger().addHandler(handler)

    if args.verbose:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(
            '[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d]: %(message)s',
            datefmt='%Y-%m-%dT%H:%M:%S%z'
        ))
        logging.getLogger().addHandler(stream_handler)

    logging.info("Starting Nug RFB server %s", version.__version__)

    if config['general'].get('zeroconf'):
        logging.info("Registration of service using zeroconf")
        info = ServiceInfo(
            "_nug-vnc._tcp.local.",
            f"_{config['general'].get('name', 'vnc-nug-server')}._nug-vnc._tcp.local.",
            addresses=[ip_address(item).packed for item in config['general']['bind']],
            port=config['general']['port'],
            properties={
                'version': version.__version__,
                'services': ('vnc', )
            },
        )
        zeroconf = Zeroconf(ip_version=IPVersion.All)
        zeroconf.register_service(info)
    else:
        zeroconf = None
        info = None

    threads = []
    devices = DeviceContainer()

    for item in config.get('devices', []):
        device = threading.Thread(
            target=Device.factory,
            args=(item, devices),
            name=f"device:{item['ip']}:{item['port']}"
        )
        device.start()
        threads.append(device)

    try:
        asyncio.run(
            Server.factory(config, devices),
        )
    except KeyboardInterrupt:
        if zeroconf:
            logging.info("Unregister zeroconf services")
            zeroconf.unregister_service(info)
            zeroconf.close()
            exit(0)
        devices.shutdown()
        logging.info("Shutting down Nug RFB server %s", version.__version__)
