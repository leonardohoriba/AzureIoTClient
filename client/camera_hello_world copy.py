from picamera2 import Picamera2
from time import sleep
import numpy as np
import cv2 as cv
camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)}))
camera.start()
#main.py

import subprocess 

command = ['ffmpeg',
            '-thread_queue_size', '1024',
            '-f', 'rawvideo',
            '-pix_fmt', 'bgr24',
            '-s','640x480',
            '-i','-',
            '-ar', '44100',
            '-ac', '2',
            '-acodec', 'pcm_s16le',
            '-f', 's16le',
            '-ac', '2',
            '-i','/dev/zero',   
            '-acodec','aac',
            '-ab','128k',
            '-strict','experimental',
            '-vcodec','h264',
            '-pix_fmt','yuv420p',
            '-g', '50',
            '-vb','1000k',
            '-profile:v', 'baseline',
            '-preset', 'ultrafast',
            '-r', '30',
            '-f', 'flv', 
            'rtmp://x.rtmp.youtube.com/live2/ect7-wqu9-tpce-qp22-d81u']

pipe = subprocess.Popen(command, stdin=subprocess.PIPE)
while True:
    # Capture frame-by-frame
    frame = camera.capture_array()
    # Display the resulting frame
    # cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break
    pipe.stdin.write(frame.tostring())
    # sleep(0.1)
# When everything done, release the capture
pipe.kill()
cv.destroyAllWindows()
camera.stop()