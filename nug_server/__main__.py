import argparse
import logging
from ipaddress import ip_address

from nug_server.network.network_address import NetworkAddress
from nug_server.services.video import VideoService

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--log-level', type=str, choices=logging._nameToLevel.keys(), default='INFO')
    parser.add_argument(
        '--bind', '-b', type=ip_address, default=[ip_address('127.0.0.1'), ip_address('::1')], nargs='+'
    )
    parser.add_argument('--port', '-p', type=int, default=5900)
    parser.add_argument('--video', type=NetworkAddress, default=None)
    args = parser.parse_args()

    logging.getLogger().setLevel(args.log_level)
    if args.verbose:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(
            '[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d]: %(message)s',
            datefmt='%Y-%m-%dT%H:%M:%S%z'
        ))
        logging.getLogger().addHandler(stream_handler)

    services = []

    if args.video:
        video_service = VideoService(args.video)
        video_service.start()
