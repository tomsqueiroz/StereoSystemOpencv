# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import cv2

tracker = cv2.TrackerCSRT_create() 

vs = cv2.VideoCapture("/home/tom/Downloads/camera2.webm")

fps = None
initBB = None
while True:

    ret, frame = vs.read()

    if not ret:
        break

    frame = imutils.resize(frame, width=500)
    (H, W) = frame.shape[:2]
    if initBB is not None:
# grab the new bounding box coordinates of the object
        (success, box) = tracker.update(frame)
# check to see if the tracking was a success
        if success:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h),
            (0, 255, 0), 2)
# update the FPS counter
            fps.update()
            fps.stop()
# initialize the set of information we'll be displaying on
# the frame
            info = [
                    ("Tracker", "CSRT"),
                    ("Success", "Yes" if success else "No"),
                    ("FPS", "{:.2f}".format(fps.fps())),
                    ]
# loop over the info tuples and draw them on our frame
            for (i, (k, v)) in enumerate(info):
                text = "{}: {}".format(k, v)
                cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

# show the output frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
# if the 's' key is selected, we are going to "select" a bounding
# box to track
    if key == ord("s"):
# select the bounding box of the object we want to track (make
# sure you press ENTER or SPACE after selecting the ROI)
        initBB = cv2.selectROI("Frame", frame, fromCenter=False,
        showCrosshair=True)
# start OpenCV object tracker using the supplied bounding box
# coordinates, then start the FPS throughput estimator as well
        tracker.init(frame, initBB)
        fps = FPS().start()
# if the `q` key was pressed, break from the loop
    elif key == ord("q"):
        break

vs.release()
# close all windows
cv2.destroyAllWindows()


print(tracker)

print(cv2.__version__)