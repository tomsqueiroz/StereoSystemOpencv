# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import cv2

vs = cv2.VideoCapture("/home/pedro/Documentos/UnB/PVC/StereoSystemOpencv/camera1.webm")

initBB = None
updateFlag = True
coordinates = []

while True:

    if updateFlag == True:
        ret, frame = vs.read()

        if not ret:
            break

        frame = imutils.resize(frame, width=500)
        (H, W) = frame.shape[:2]

        if initBB is not None:

            updateFlag = True
            (success, box) = tracker.update(frame)

            if success:

                (x, y, w, h) = [int(v) for v in box]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                coordinates.append((x, y))

            else:

                coordinates.append((-1, -1))
                updateFlag = False

        else:

            coordinates.append((-1, -1))
            updateFlag = False

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("s"):

        initBB = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)
        tracker = cv2.TrackerCSRT_create()

        tracker.init(frame, initBB)
        updateFlag = True

    elif key == ord("q"):
        break

    elif key == ord("n"):
        updateFlag = True

vs.release()

cv2.destroyAllWindows()

print(coordinates[:10])