from picamera2 import Picamera2
import cv2 as cv
import subprocess
import prctl
import signal
import threading
from time import sleep

class Camera:
    FFMPEG_COMMAND = [
        "ffmpeg",
        "-thread_queue_size",
        "8",
        "-re",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "bgr24",
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
        # "h264_v4l2m2m",
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
        "30",
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

    def startStreaming(self):
        self.pipe = subprocess.Popen(
            self.FFMPEG_COMMAND,
            stdin=subprocess.PIPE,
            preexec_fn=lambda: prctl.set_pdeathsig(signal.SIGKILL),
        )
        self.threadStreaming = threading.Thread(target=self.__streaming, name="streaming")
        self.threadStreaming.start()

    def __camera(self):
        while not self._finished:
            ## OpenCV code goes here, for now
            self._frame = self.camera.capture_array()
            # cv.imshow("frame", self._frame)
            if cv.waitKey(1) == ord("q"):
                break
            # if self._streaming:
            #     self.pipe.stdin.write(self._frame.tostring())

    def __streaming(self):
        while not self._finished:
            self.pipe.stdin.write(self._frame.tostring())
