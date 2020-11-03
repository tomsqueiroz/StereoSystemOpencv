import numpy as np
import cv2
import json

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

		print(f"{i}")
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

def getImagePoints(images):

	for image, i in zip(images, [1, 2]):

		print("\nLoading image...")

		#Get clicks on image from set 1 and 2
		img1 = cv2.imread(image)
		cv2.namedWindow('select points')
		cv2.setMouseCallback('select points', imageClick, param=i)

		while(1):

			cv2.imshow('select points', img1)
			if cv2.waitKey(20) & 0xFF == 27: 

				cv2.destroyWindow('select points')
				break 

			elif(i == 1 and len(inputCam1) == 2) or (i == 2 and len(inputCam2) == 2):

				cv2.destroyWindow('select points')
				break

def imageClick(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:

        if param == 1:

            inputCam1.append([(x, y)])

        elif param == 2:

            inputCam2.append([(x, y)])

if __name__ == "__main__":

	global mtx1
	global mtx2
	global tVecs1
	global tVecs2
	global rotMatrix1
	global rotMatrix2
	global inputCam1
	global inputCam2

	cam1 = [(455, 274), (454, 274), (455, 274), (481, 255), (605, 165), (700, 103), (764, 53), (821, 16), (852, -10), (-1, -1), (-1, -1), \
	(-1, -1), (787, 35), (731, 77), (688, 117), (576, 188), (402, 342), (218, 495), (187, 522)]

	cam2 = [(594, 307), (593, 306), (594, 307), (583, 285), (528, 159), (496, 70), (469, 11), (-1, -1), (-1, -1), (-1, -1), (-1, -1), \
	(-1, -1), (-1, -1), (462, 35), (-1, -1), (529, 179), (583, 210), (740, 442), (860, 677)]

	inputCam1 = []
	inputCam2 = []

	inputCam1.append(cam1)
	inputCam1.append([])
	inputCam2.append(cam2)
	inputCam2.append([])

	'''
	getImagePoints(['./camera1Undistorted/camera1Undistorted159.jpg', './camera2Undistorted/camera2Undistorted24.jpg'])

	inputCam1[0] = [(-1, -1)]
	print(f"\ncam1: {inputCam1}")
	print(f"\ncam2: {inputCam2}")'''

	mtx1, mtx2 = readIntrinsics('intrinsicsCalibration.json')
	tVecs1, rotMatrix1, tVecs2, rotMatrix2 = readExtrinsics('extrinsicsCalibration.json')
	#inputCam1, inputCam2 = readTrackedArrays()

	#Get world coordinates for point 1 (top)
	outputPoint1 = getWorldCoordinates(inputCam1[0], inputCam2[0])

	#Get world coordinates for point 2 (base)
	#outputPoint2 = getWorldCoordinates(inputCam1[1], inputCam2[1])

	#print(f"\nOutputPoint1: {outputPoint1}")
	#print(f"\nOutputPoint2: {outputPoint2}")

	convArr = [element.tolist() for element in outputPoint1]
	print(convArr)

	dumpArr = json.dumps(convArr)

	with open('output.json', 'w') as file:

		json.dump(dumpArr, file)

	print("\nOutput file generated!")

	