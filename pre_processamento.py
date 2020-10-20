import numpy as np
import cv2
import glob

def calibration(path):

    #Criteria for termination of the iterative process of corner refinement
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    #Real object points
    objp = np.zeros((8*6, 3), np.float32)
    objp[:,:2] = np.mgrid[0:8, 0:6].T.reshape(-1, 2)

    print(f"\nCalibrando a camera...")

    #Arrays to store object points and image points from all the images.
    objPoints = [] 
    imgPoints = [] 

    for file in glob.glob(path):

        img = cv2.imread(file)
        image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   
        ret, corners = cv2.findChessboardCorners(image, (8,6), cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)

        if (ret == True): 
                
            objPoints.append(objp)

            refinedCorners = cv2.cornerSubPix(image, corners, (11,11), (-1, -1), criteria)
            imgPoints.append(refinedCorners)

    return(cv2.calibrateCamera(objPoints, imgPoints, image.shape[::-1], cameraMatrix=None, distCoeffs=None, flags=(cv2.CALIB_FIX_K3 + cv2.CALIB_ZERO_TANGENT_DIST)))

def undistort(mtx, dist):

    for file, i in zip(glob.glob('C:\\Users\\Pedro\\Documents\\UnB\\2020_1\\PVC\\Trabalho 1\\trabalho1_imagens\\Frames\\*.jpg'), range(10)):

        img = cv2.imread(file)
        h,  w = img.shape[:2]
        newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

        # undistort
        dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

        # crop the image
        #x,y,w,h = roi
        #dst = dst[y:y+h, x:x+w]
        cv2.imshow("teste", dst)
        cv2.waitKey(0)
        cv2.imwrite("calibResultUndistort" + str(i) + ".png", dst)

#Paths for image datasets
paths = ['C:\\Users\\Pedro\\Documents\\UnB\\2020_1\\PVC\\Trabalho 1\\trabalho1_imagens\\Calibration1\\*.jpg',
         'C:\\Users\\Pedro\\Documents\\UnB\\2020_1\\PVC\\Trabalho 1\\trabalho1_imagens\\Calibration2\\*.jpg']

#paths = []
#paths.append(input("Caminho para o dataset 1: ") + "\\*.jpg")
#paths.append(input("\nCaminho para o dataset 2: ") + "\\*.jpg")

ret1, mtx1, dist1, rvecs1, tvecs1 = calibration(paths[0])
print(f"\ndist1: {dist1}")

ret2, mtx2, dist2, rvecs2, tvecs2 = calibration(paths[1])
print(f"\ndist2: {dist2}")

undistort(mtx2, dist2)

