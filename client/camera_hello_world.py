from picamera2 import Picamera2
import numpy as np
import cv2 as cv
camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={"format": 'XRGB8888', "size": (320, 240)}))
camera.start()
while True:
    # Capture frame-by-frame
    frame = camera.capture_array()
    # Display the resulting frame
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cv.destroyAllWindows()
camera.stop()