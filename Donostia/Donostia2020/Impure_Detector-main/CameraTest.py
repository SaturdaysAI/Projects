# Some cfg help
# https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/2
# test camera /dev :
#   sudo apt-get install v4l-utils
#   v4l2-ctl --list-devices
import numpy as np
import cv2
import time

cap = cv2.VideoCapture(2)

# allow the camera to warmup
time.sleep(0.1)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite('color.jpg', frame )
        print("Image is saved color")
        cv2.destroyAllWindows()
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
