import signal
import subprocess
import threading

import cv2 as cv
import prctl
from decouple import config
from picamera2 import Picamera2


class Camera:
    FFMPEG_COMMAND = [
        "ffmpeg",
        "-thread_queue_size",
        "1",
        "-re",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "bgr24",
        "-r",
        "25",
        "-s",
        "640x480",
        "-i",
        "-",
        "-ar",
        "44100",
        "-ac",
        "2",
        "-acodec",
        "pcm_s16le",
        "-f",
        "s16le",
        "-ac",
        "2",
        "-i",
        "/dev/zero",
        "-acodec",
        "aac",
        "-ab",
        "64k",
        "-strict",
        "experimental",
        "-vcodec",
        "h264",
        "-pix_fmt",
        "yuv420p",
        "-g",
        "50",
        "-vb",
        "1024k",
        "-profile:v",
        "baseline",
        "-preset",
        "ultrafast",
        "-r",
        "25",
        "-f",
        "flv",
        "rtmp://x.rtmp.youtube.com/live2/ect7-wqu9-tpce-qp22-d81u",
    ]

    def __init__(self):
        self._finished = False
        self.camera = Picamera2()
        cameraConfig = self.camera.create_preview_configuration(
            main={"format": "RGB888", "size": (640, 480)}
        )
        self.camera.configure(cameraConfig)
        self.camera.start()
        self.threadCamera = threading.Thread(target=self.__camera, name="camera")
        self.threadCamera.start()

    def deinit(self):
        self._finished = True
        self.threadCamera.join()
        self.threadStreaming.join()

    def startStreaming(self):
        with open(config("FFMPEG_LOG", default="/dev/null"), "a") as ffmpeglog:
            self.pipe = subprocess.Popen(
                self.FFMPEG_COMMAND,
                stdin=subprocess.PIPE,
                stdout=ffmpeglog,
                stderr=subprocess.STDOUT,
                preexec_fn=lambda: prctl.set_pdeathsig(signal.SIGKILL),
            )
        self.threadStreaming = threading.Thread(
            target=self.__streaming, name="streaming"
        )
        self.threadStreaming.start()

    def __camera(self):
        while not self._finished:
            ## OpenCV code goes here, for now
            self._frame = self.camera.capture_array()
            # cv.imshow("frame", self._frame)
            if cv.waitKey(1) == ord("q"):
                break

    def __streaming(self):
        while not self._finished:
            self.pipe.stdin.write(self._frame.tostring())
