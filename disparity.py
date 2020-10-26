import cv2
import numpy as np


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

    stereoMatcherSGBM = cv2.StereoSGBM_create(
        minDisparity=4,
        numDisparities=7*16,  # max_disp has to be dividable by 16 f. E. HH 192, 256
        blockSize=window_size,
        P1=8 * 3 * window_size,
        # wsize default 3; 5; 7 for SGBM reduced size image; 15 for SGBM full size image (1300px and above); 5 Works nicely
        P2=32 * 3 * window_size,
        disp12MaxDiff=12,
        uniquenessRatio=10,
        speckleWindowSize=45,
        speckleRange=16,
        preFilterCap=63,
        mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY)



    return stereoMatcherSGBM.compute(left_image_gray, right_image_gray).astype(np.float32) 

if __name__ == "__main__":

    disparity = calc_disparity('./camera1Undistorted/camera1Undistorted159.jpg', './camera2Undistorted/camera2Undistorted24.jpg')

    print(disparity)

    DEPTH_VISUALIZATION_SCALE = 2048
    while(1):
        cv2.imshow('depth', disparity / DEPTH_VISUALIZATION_SCALE)

        if cv2.waitKey(20) & 0xFF == 27: 

            cv2.destroyWindow('depth')
            break
            

        