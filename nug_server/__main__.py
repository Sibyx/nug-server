import argparse
import logging
from logging.handlers import SysLogHandler
from pathlib import Path

import tomli as tomli

from nug_server.services.video import VideoService

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

    services = []

    # if args.video:
    #     video_service = VideoService(args.video)
    #     video_service.start()
