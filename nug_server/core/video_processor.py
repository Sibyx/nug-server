import logging
from threading import Thread
from time import sleep

import cv2

'''
https://lindevs.com/capture-rtsp-stream-from-ip-camera-using-opencv/
https://stackoverflow.com/questions/20891936/rtsp-stream-and-opencv-python
'''


class VideoProcessor(Thread):
    def __init__(self, config: dict):
        super().__init__(name='video-processor')
        self._is_running = True
        self._current_frame = None
        self._config = config
        self._cap = None

    @property
    def frame(self):
        return self._current_frame

    def run(self) -> None:
        self._cap = cv2.VideoCapture(
            f"{self._config['general']['rtsp']}/{self._config['general']['name']}", cv2.CAP_FFMPEG
        )

        while self._is_running:
            result, self._current_frame = self._cap.read()

            if result is False:
                logging.debug("Received empty frame")
                sleep(1)

    def stop(self):
        self._is_running = False
        self._cap.release()
