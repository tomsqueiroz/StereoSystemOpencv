import numpy as np
import cv2
import json

def readIntrinsics(file):

	with open(file, 'r') as file:

		data = json.load(file)
		data = json.loads(data)

	return np.array(data["cameraMatrix1"]), np.array(data["cameraMatrix2"]), np.array(data["distortionVector1"]), np.array(data["distortionVector2"])

def readExtrinsics(file):

	with open(file, 'r') as file:

		data = json.load(file)
		data = json.loads(data)

	return np.array(data["rVecs1"]), np.array(data["tVecs1"]), np.array(data["rotMatrix1"]), np.array(data["cameraPosition1"]), \
		   np.array(data["rVecs2"]), np.array(data["tVecs2"]), np.array(data["rotMatrix2"]), np.array(data["cameraPosition2"])

def getImagePoints():

	images = ['./camera1Undistorted/camera1Undistorted300.jpg', './camera2Undistorted/camera2Undistorted100.jpg']

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

			elif(i == 1 and len(imgPointsCam1) == 1) or (i == 2 and len(imgPointsCam2) == 1):

				cv2.destroyWindow('select points')
				break

def imageClick(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:

        if param == 1:

            imgPointsCam1.append((x, y))

        elif param == 2:

            imgPointsCam2.append((x, y))

def getWorldBountify(mtx1, rotMatrix1):

	camMat = np.asarray(mtx1)
	iRot = np.linalg.inv(rotMatrix1)
	iCam = np.linalg.inv(camMat)

	uvPoint = np.ones((3, 1))

	# Image point
	uvPoint[0, 0] = imgPoints[0][0]
	uvPoint[1, 0] = imgPoints[0][1]

	tempMat = np.matmul(np.matmul(iRot, iCam), uvPoint)
	tempMat2 = np.matmul(iRot, tVecs1)

	s = tempMat2[2, 0] / tempMat[2, 0]
	wcPoint = np.matmul(iRot, (np.matmul(s * iCam, uvPoint) - tVecs1))

	print(wcPoint)

def computeProjMatrix(mtx, rotMatrix, tVecs):

	#print(f"\nrotMatrix: {rotMatrix}")
	#print(f"\ntVecs: {tVecs}")

	aux = np.concatenate((rotMatrix, tVecs), axis=1)
	#print(f"\nConcat: {aux}")

	#print(f"\n\nRes: {np.matmul(mtx, aux)}")

	return np.matmul(mtx, aux)

if __name__ == "__main__":

	global imgPointsCam1
	global imgPointsCam2
	imgPointsCam1 = []
	imgPointsCam2 = []
	getImagePoints()

	mtx1, mtx2, dist1, dist2 = readIntrinsics('intrinsicsCalibration.json')
	rVecs1, tVecs1, rotMatrix1, cameraPosition1, rVecs2, tVecs2, rotMatrix2, cameraPosition2 = readExtrinsics('extrinsicsCalibration.json')

	#getWorldBountify(mtx1, rotMatrix1)
	projMatrix1 = computeProjMatrix(mtx1, rotMatrix1, tVecs1)
	projMatrix2 = computeProjMatrix(mtx2, rotMatrix2, tVecs2)

	coordinates = cv2.triangulatePoints(projMatrix1, projMatrix2, imgPointsCam1[0], imgPointsCam2[0])

	answer = np.array([coordinates[i]/coordinates[3] for i in range(3)])

	print(f"\n{answer}")

