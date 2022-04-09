import logging
import threading

from nug_server.network.network_address import NetworkAddress
from nug_server.services.base import Service


class VideoService(Service):
    def __init__(self, network_address: NetworkAddress):
        self._network_address = network_address
        self.is_running = False
        self.thread = threading.Thread(target=self.run, args=(lambda: self.is_running, network_address,))

    @staticmethod
    def run(stop, network_address):
        cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)
        while True:
            if stop():
                logging.debug("Received stop signal")
                break

    def start(self):
        self.thread.start()

    def stop(self):
        self.is_running = False
