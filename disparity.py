import cv2
import numpy as np


def calc_disparity(left_image, right_image):

    left_image = cv2.imread(left_image)
    right_image = cv2.imread(right_image)

    left_image_gray = cv2.cvtColor(left_image, cv2.COLOR_BGR2GRAY)
    right_image_gray = cv2.cvtColor(right_image, cv2.COLOR_BGR2GRAY)

    window_size = 7
    min_disp = 32
    num_disp = 112-min_disp


    stereoMatcher = cv2.StereoBM_create()

    stereoMatcher.setMinDisparity(7)
    stereoMatcher.setNumDisparities(80)
    stereoMatcher.setBlockSize(5)
    stereoMatcher.setSpeckleRange(80)
    stereoMatcher.setSpeckleWindowSize(65)

    return stereoMatcher.compute(left_image_gray, right_image_gray).astype(np.float32) 

if __name__ == "__main__":

    disparity = calc_disparity('./camera1Undistorted/camera1Undistorted159.jpg', './camera2Undistorted/camera2Undistorted24.jpg')

    print(disparity)

    DEPTH_VISUALIZATION_SCALE = 2048
    while(1):
        cv2.imshow('depth', disparity / DEPTH_VISUALIZATION_SCALE)

        if cv2.waitKey(20) & 0xFF == 27: 

            cv2.destroyWindow('depth')
            break
            

        