import numpy as np
import cv2
import json

def stereoCalibration():

	print("STEREO CALIBRATION...")
	mtx1, mtx2, dist1, dist2 = readJson("intrinsicsCalibration.json")
	print(f"\nIntrinsic parameters imported!")

	objectPoints = np.array([[0.0, 0.0, 0.0], [0.0, 1.4, 0.0], [2.6, 0.0, 0.0], [2.6, 1.4, 0.0]], dtype=np.float32)

	print(f"\nStereo calibration finished!")
	return cv2.stereoCalibrate([objectPoints], [np.array(imgPointsCam1, dtype=np.float32)], [np.array(imgPointsCam2, dtype=np.float32)],
	       mtx1, dist1, mtx2, dist2, (1280, 720), flags=cv2.CALIB_FIX_INTRINSIC)

def readJson(file):

	with open(file, 'r') as file:

		data = json.load(file)
		data = json.loads(data)

	return np.array(data["cameraMatrix1"]), np.array(data["cameraMatrix2"]), np.array(data["distortionVector1"]), np.array(data["distortionVector2"])

def getImagePoints(images):

	print("\nDefine 4 image points to determine the Fundamental matrix or press ESC to leave:")

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

# draw the provided points on the image
def drawPoints(img, pts, colors):

    for pt, color in zip(pts, colors):
        cv2.circle(img, tuple(pt), 5, color, -1)

# draw the provided lines on the image
def drawLines(img, lines, colors):

	_, c, _ = img.shape
	for r, color in zip(lines, colors):

		x0, y0 = map(int, [0, -r[2]/r[1]])
		x1, y1 = map(int, [c, -(r[2]+r[0]*c)/r[1]])
		cv2.line(img, (x0, y0), (x1, y1), color, 1)

def result(images, F):

	#Blue, green, red, black, cyan, yellow, magenta, purple
	colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0), (255, 255, 0), (0, 255, 255), (255, 0, 255), (226, 43, 138)]
	img1 = cv2.imread(images[0])
	img2 = cv2.imread(images[1])

	print(f"\nGenerating epilines images...")

	# get 3 image points of interest from each image and draw them
	pts1 = np.asarray([imgPointsCam1[0], imgPointsCam1[1], imgPointsCam1[2], imgPointsCam1[3]])
	pts2 = np.asarray([imgPointsCam2[0], imgPointsCam2[1], imgPointsCam2[2], imgPointsCam2[3]])
	drawPoints(img1, pts1, colors[0:4])
	drawPoints(img2, pts2, colors[4:8])

	# find epilines corresponding to points in right image and draw them on the left image
	epilines2 = cv2.computeCorrespondEpilines(pts1.reshape(-1, 1, 2), 1, F)
	epilines2 = epilines2.reshape(-1, 3)
	drawLines(img2, epilines2, colors[0:4])
	#drawLines(img1, epilines2, colors[0:3])

	# find epilines corresponding to points in left image and draw them on the right image
	epilines1 = cv2.computeCorrespondEpilines(pts2.reshape(-1, 1, 2), 2, F)
	epilines1 = epilines1.reshape(-1, 3)
	drawLines(img1, epilines1, colors[4:8])
	#drawLines(img2, epilines1, colors[3:6])

	while(1):
		cv2.imshow("image 1", img1)
		cv2.imshow("image 2", img2)
		if cv2.waitKey(20) & 0xFF == 27: 

			cv2.destroyWindow('image 2')
			cv2.destroyWindow('image 1')
			break

	cv2.imwrite('istortEpiline1.png', img1)
	cv2.imwrite('istortEpiline2.png', img2)

def calc_disparity(left_image, right_image):

    window_size = 3

    left_image = cv2.imread(left_image)
    right_image = cv2.imread(right_image)

    left_image_gray = cv2.cvtColor(left_image, cv2.COLOR_BGR2GRAY)
    right_image_gray = cv2.cvtColor(right_image, cv2.COLOR_BGR2GRAY)

    stereoMatcherBM = cv2.StereoBM_create()

    stereoMatcherBM.setMinDisparity(-4)
    stereoMatcherBM.setNumDisparities(128)
    stereoMatcherBM.setBlockSize(5)
    stereoMatcherBM.setSpeckleRange(160)
    stereoMatcherBM.setSpeckleWindowSize(80)

    return stereoMatcherBM.compute(left_image_gray, right_image_gray).astype(np.float32)

def calc_depth(disparity, r, t, cm1, cm2, dc1, dc2):
	
	_3Dimage = None
	RL, RR, PL, PR, Q, _, _ = cv2.stereoRectify(cm1, dc1, cm2, dc2, (1280, 720), r, t)
	Q.reshape(4,4)

	cv2.reprojectImageTo3D(disparity, _3Dimage, Q)
	cv2.imshow('depth', _3Dimage)

if __name__ == "__main__":

	global imgPointsCam1
	global imgPointsCam2
	imgPointsCam1 = []
	imgPointsCam2 = []

	getImagePoints(['./camera1Undistorted/camera1Undistorted159.jpg', './camera2Undistorted/camera2Undistorted24.jpg'])
	#print(f"1: {imgPointsCam1}\n2: {imgPointsCam2}\n")

	retVal, cm1, dc1, cm2, dc2, r, t, e, f = stereoCalibration()
	#print(f"\nE: {e}\nF: {f}")

	#Codigo utilizado para printar linhas epipolares
	#result(['./camera1Undistorted/camera1Undistorted159.jpg', './camera2Undistorted/camera2Undistorted24.jpg'], f)

	disparity = calc_disparity('./camera1Undistorted/camera1Undistorted159.jpg', './camera2Undistorted/camera2Undistorted24.jpg')

	DEPTH_VISUALIZATION_SCALE = 2048

	disparityVisualized = disparity / DEPTH_VISUALIZATION_SCALE

	
	cv2.imwrite('disparity.png', disparity*255/2048)
	print("Disparity Map Generated")

	#calc_depth(disparity, r, t, cm1, cm2, dc1, dc2)







