import signal
import subprocess
import threading

import cv2 as cv
import prctl
from decouple import config
from picamera2 import Picamera2

import settings


class Camera:
    __FFMPEG_COMMAND = settings.STREAM_FFMPEG_COMMAND
    _RESOLUTION_WIDTH = settings.CAMERA_RESOLUTION_WIDTH
    _RESOLUTION_HEIGHT = settings.CAMERA_RESOLUTION_HEIGHT

    def __init__(self):
        self._finished = False
        self.camera = Picamera2()
        cameraConfig = self.camera.create_preview_configuration(
            main={
                "format": "RGB888",
                "size": (self._RESOLUTION_WIDTH, self._RESOLUTION_HEIGHT),
            }
        )
        self.camera.configure(cameraConfig)
        self.camera.start()
        self.threadCamera = threading.Thread(target=self.__camera, name="camera")
        self.threadCamera.start()

    def deinit(self):
        self._finished = True
        self.threadCamera.join()
        self.threadStreaming.join()

    def __camera(self):
        while not self._finished:
            ## OpenCV code goes here, for now
            self._frame = self.processFrame(self.camera.capture_array())
            # cv.imshow("frame", self._frame)
            if cv.waitKey(1) == ord("q"):
                break

    def __streaming(self):
        # This thread must run at a constant frame rate, to avoid queue piling up or underrun
        while not self._finished:
            # write() has a timing limiter and thus if we add code here it would reduce the frame rate
            self.pipe.stdin.write(self._frame.tostring())

    def startStreaming(self):
        with open(config("FFMPEG_LOG", default="/dev/null"), "a") as ffmpeglog:
            self.pipe = subprocess.Popen(
                self.__FFMPEG_COMMAND,
                stdin=subprocess.PIPE,
                stdout=ffmpeglog,
                stderr=subprocess.STDOUT,
                preexec_fn=lambda: prctl.set_pdeathsig(signal.SIGKILL),
            )
        self.threadStreaming = threading.Thread(
            target=self.__streaming, name="streaming"
        )
        self.threadStreaming.start()

    def processFrame(self, frame):
        # Virtual method, returns the same frame if not implemented in child class
        return frame
