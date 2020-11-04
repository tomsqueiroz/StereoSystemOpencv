import numpy as np
import cv2
import json
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time

def readIntrinsics(file):

	with open(file, 'r') as file:

		data = json.load(file)
		data = json.loads(data)

	return np.array(data["cameraMatrix1"]), np.array(data["cameraMatrix2"])

def readExtrinsics(file):

	with open(file, 'r') as file:

		data = json.load(file)
		data = json.loads(data)

	return np.array(data["tVecs1"]), np.array(data["rotMatrix1"]), \
		   np.array(data["tVecs2"]), np.array(data["rotMatrix2"])

def getWorldCoordinates(array1, array2):

	output = []

	'''
	If any of the trackers missed the object (-1, -1), the out
	put is set to (-1, -1, -1). Otherwise, position is calc.
	'''
	for i in range(len(array1)):

		if array1[i] == (-1, -1) or array2[i] == (-1, -1):

			output.append(np.array([[-1], [-1], [-1]]))

		else:

			output.append(calculateCoordinates(array1[i], array2[i]))

	return output

def calculateCoordinates(coord1, coord2):

	projMatrix1 = computeProjMatrix(mtx1, rotMatrix1, tVecs1)
	projMatrix2 = computeProjMatrix(mtx2, rotMatrix2, tVecs2)

	coordinates = cv2.triangulatePoints(projMatrix1, projMatrix2, coord1, coord2)

	return np.array([coordinates[i]/coordinates[3] for i in range(3)])

def computeProjMatrix(mtx, rotMatrix, tVecs):

	aux = np.concatenate((rotMatrix, tVecs), axis=1)

	return np.matmul(mtx, aux)

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

def savePointsToFile(array):

	convArr = [element.tolist() for element in array]

	dumpArr = json.dumps(convArr)

	with open('output.json', 'w') as file:

		json.dump(dumpArr, file)

	print("\nOutput file generated!")

if __name__ == "__main__":

	global mtx1
	global mtx2
	global tVecs1
	global tVecs2
	global rotMatrix1
	global rotMatrix2

	mtx1, mtx2 = readIntrinsics('intrinsicsCalibration.json')
	tVecs1, rotMatrix1, tVecs2, rotMatrix2 = readExtrinsics('extrinsicsCalibration.json')

	res2 = trackObject("./camera2.webm")
	res1 = trackObject("./camera1.webm")
	
	#Syncronized frames to be selected
	frames1 = [167, 181, 198, 223, 244, 262, 284, 308, 322, 346, 380, 410, 422, 433, 443, 452, 469, 483, 512]
	frames2 = [27, 34, 42, 53, 63, 72, 82, 93, 100, 113, 127, 141, 147, 152, 157, 161, 168, 176, 189]
	out1 = [res1[i] for i in frames1]
	out2 = [res2[i] for i in frames2]

	outputPoint = getWorldCoordinates(out1, out2)

	#print(f"\nOutputPoint1: {outputPoint1}")
	#print(f"\nOutputPoint2: {outputPoint2}")

	savePointsToFile(outputPoint)