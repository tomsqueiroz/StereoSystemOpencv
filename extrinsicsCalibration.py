import numpy as np
import cv2
import glob
import json

def getImagePoints():

	images = ['./camera1Undistorted/camera1Undistorted300.jpg', './camera2Undistorted/camera2Undistorted100.jpg']
	print("\nDefine 4 image points to be used in extrinsic calibration or press ESC to leave:")

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

			elif(i == 1 and len(imgPointsCam1) == 4) or (i == 2 and len(imgPointsCam2) == 4):

				cv2.destroyWindow('select points')
				break

	if(len(imgPointsCam1) < 4 or len(imgPointsCam2) < 4):

		print("\nThe minimun ammount of values was not selected! Please, run again.")
		exit(0)

def imageClick(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:

        if param == 1:

            imgPointsCam1.append([x, y])

        elif param == 2:

            imgPointsCam2.append([x, y])

def saveCalibrationFile():

	rVecs1, tVecs1, rotMatrix1, cameraPosition1, rVecs2, tVecs2, rotMatrix2, cameraPosition2 = getCamPosition()

	dic = {"rVecs1": rVecs1.tolist(), "tVecs1": tVecs1.tolist(), "rotMatrix1": rotMatrix1.tolist(), "cameraPosition1": cameraPosition1.tolist(),
	       "rVecs2": rVecs2.tolist(), "tVecs2": tVecs2.tolist(), "rotMatrix2": rotMatrix2.tolist(), "cameraPosition2": cameraPosition2.tolist()}

	dumpDic = json.dumps(dic)

	with open('extrinsicsCalibration.json', 'w') as file:

		json.dump(dumpDic, file)

	print("\nCalibration file generated!")

def getCamPosition():

	#Import intrinsic parameters
	print("\nCALCULATING CAMERA POSITIONS")
	mtx1, mtx2, dist1, dist2 = readJson("intrinsicsCalibration.json")
	print(f"\nIntrinsic parameters imported!")

	#Define object points
	objectPoints = np.array([[0.0, 0.0, 0.0], [0.0, 1.4, 0.0], [2.6, 0.0, 0.0], [2.6, 1.4, 0.0]], dtype=np.float32)

	#Camera 1: obtain extrinsic parameters for rotation and translation an then camera position in 3D coordinates
	print("\nCamera 1...")
	ret1,rVecs1, tVecs1 = cv2.solvePnP(objectPoints, np.array(imgPointsCam1, dtype=np.float32), mtx1, dist1)
	rotMatrix1 = cv2.Rodrigues(rVecs1)[0]
	cameraPosition1 = -np.matrix(rotMatrix1).T * np.matrix(tVecs1)
	print(f"\nrVecs {rVecs1}\ntVecs {tVecs1}\nrotMatrix {rotMatrix1}\ncamPos {cameraPosition1}")

	#Camera 2: obtain extrinsic parameters for rotation and translation an then camera position in 3D coordinates
	print("\nCamera 2...")
	ret2,rVecs2, tVecs2 = cv2.solvePnP(objectPoints, np.array(imgPointsCam2, dtype=np.float32), mtx2, dist2)
	rotMatrix2 = cv2.Rodrigues(rVecs2)[0]
	cameraPosition2 = -np.matrix(rotMatrix2).T * np.matrix(tVecs2)
	print(f"\nrVecs {rVecs2}\ntVecs {tVecs2}\nrotMatrix {rotMatrix2}\ncamPos {cameraPosition2}")

	if ret1 == False or ret2 == False:

		print("Error calculating extrinsic parameters! Operation aborted!")
		exit(1)

	return rVecs1, tVecs1, rotMatrix1, cameraPosition1, rVecs2, tVecs2, rotMatrix2, cameraPosition2

def readJson(file):

	with open(file, 'r') as file:

		data = json.load(file)
		data = json.loads(data)

	return np.array(data["cameraMatrix1"]), np.array(data["cameraMatrix2"]), np.array(data["distortionVector1"]), np.array(data["distortionVector2"])

if __name__ == "__main__":

	global imgPointsCam1
	global imgPointsCam2
	imgPointsCam1 = []
	imgPointsCam2 = []

	getImagePoints()

	saveCalibrationFile()