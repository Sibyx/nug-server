import cv2

from nug_server.network.network_address import NetworkAddress
from nug_server.services.base import Service

'''
https://lindevs.com/capture-rtsp-stream-from-ip-camera-using-opencv/
https://stackoverflow.com/questions/20891936/rtsp-stream-and-opencv-python
'''


class VideoService(Service):
    def __init__(self, network_address: NetworkAddress):
        super().__init__()
        self._network_address = network_address
        # self._cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)
