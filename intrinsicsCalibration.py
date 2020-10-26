import numpy as np
import cv2
import glob
import json

#Calibrate each camera related to its dataset
def calibration(path, camera):

    #Criteria for termination of the iterative process of corner refinement
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    #Real object points
    objp = np.zeros((8*6, 3), np.float32)
    objp[:,:2] = np.mgrid[0:8, 0:6].T.reshape(-1, 2)

    print(f"\nCalibrating {camera}...\n")

    #Arrays to store object points and image points from all the images.
    objPoints = [] 
    imgPoints = [] 

    for file in glob.glob(path):

        img = cv2.imread(file)
        image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(image, (1280, 720))   
        ret, corners = cv2.findChessboardCorners(image, (8,6), cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)

        if (ret == True): 
                
            objPoints.append(objp)
            refinedCorners = cv2.cornerSubPix(image, corners, (11,11), (-1, -1), criteria)
            imgPoints.append(refinedCorners)

    return(cv2.calibrateCamera(objPoints, imgPoints, image.shape[::-1], cameraMatrix=None, distCoeffs=None, flags=(cv2.CALIB_FIX_K3 + cv2.CALIB_ZERO_TANGENT_DIST)))

#Get paths for calibration folders from user
def pathSetup():

    return [input(f"Path to calibration dataset {i}: ") + "/*.jpg" for i in [1, 2]]

#Save calibration file
def saveCalibrationFile(path):

    #Calibrate Camera 1
    ret1, mtx1, dist1, rvecs1, tvecs1 = calibration(path[0], "Camera 1")
    
    #Calibrate Camera 2
    ret2, mtx2, dist2, rvecs2, tvecs2 = calibration(path[1], "Camera 2")

  
    dic = {"cameraMatrix1": mtx1.tolist(), "cameraMatrix2": mtx2.tolist(), "distortionVector1": dist1.tolist(), "distortionVector2": dist2.tolist()}
    dumpDic = json.dumps(dic)

    with open('intrinsicsCalibration.json', 'w') as file:

        json.dump(dumpDic, file)

    print("\nCalibration file generated!")


if __name__ == "__main__":

    path = pathSetup()

    saveCalibrationFile(path)