from picamera2 import Picamera2
from time import sleep
import numpy as np
import cv2 as cv
camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
camera.start()
writer = cv.VideoWriter()
# writer.open("appsrc ! videoconvert ! videoscale ! video/x-raw,width=640,height=480 ! x264enc ! flvmux ! rtmp2sink location=rtmp://x.rtmp.youtube.com/live2/ect7-wqu9-tpce-qp22-d81u app=live2", 0, 10, (640, 480), True)
writer.open('videotestsrc is-live=1 ! videoconvert ! "video/x-raw, width=1280, height=720, framerate=25/1" ! queue ! x264enc bitrate=2000 byte-stream=false key-int-max=60 bframes=0 aud=true tune=zerolatency ! "video/x-h264,profile=main" ! flvmux streamable=true name=mux ! rtmpsink location="rtmp://x.rtmp.youtube.com/live2/ect7-wqu9-tpce-qp22-d81u app=live2" audiotestsrc ! voaacenc bitrate=128000 ! mux.', 0, 10, (640, 480), True)
while True:
    # Capture frame-by-frame
    frame = camera.capture_array()
    # Display the resulting frame
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break
    writer.write(frame)
    sleep(0.1)
# When everything done, release the capture
cv.destroyAllWindows()
camera.stop()