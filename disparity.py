import cv2
import numpy as np
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

	return np.array(data["tVecs1"]), np.array(data["rotMatrix1"]), \
		   np.array(data["tVecs2"]), np.array(data["rotMatrix2"])


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


if __name__ == "__main__":

    disparity = calc_disparity('./camera1Undistorted/camera1Undistorted159.jpg', './camera2Undistorted/camera2Undistorted24.jpg')

    print(disparity)

    DEPTH_VISUALIZATION_SCALE = 2048

    disparityVisualized = disparity / DEPTH_VISUALIZATION_SCALE
    
    cv2.imwrite('disparity.png', disparity*255/2048)

                

        