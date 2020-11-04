# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import cv2

def trackObject(path):

    vs = cv2.VideoCapture(path)

    initBB = None
    updateFlag = True
    coordinates = []

    while True:

        if updateFlag == True:
            ret, frame = vs.read()

            if not ret:
                break

            frame = cv2.resize(frame, (1280, 720))
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

    return coordinates

if __name__ == "__main__":

    res1 = trackObject("./camera1.webm")
    res2 = trackObject("./camera2.webm")

    #Syncronized frames to be selected
    frames1 = [167, 181, 198, 223, 244, 262, 284, 308, 322, 346, 380, 410, 422, 433, 443, 452, 469, 483, 512]
    frames2 = [27, 34, 42, 53, 63, 72, 82, 93, 100, 113, 127, 141, 147, 152, 157, 161, 168, 176, 189]
    out1 = [res1[i] for i in frames1]
    out2 = [res2[i] for i in frames2]

    print(f"{out1}")