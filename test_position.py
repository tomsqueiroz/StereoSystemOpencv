import numpy as np
import cv2
import glob
import os

def calibration(path):

    #Criteria for termination of the iterative process of corner refinement
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    #Real object points
    objp = np.zeros((8*6, 3), np.float32)
    objp[:,:2] = np.mgrid[0:8, 0:6].T.reshape(-1, 2)

    print(f"\nCalibrando a camera...\n")

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

def undistort(mtx, dist, distortedImage):

    h,  w = distortedImage.shape[:2]
    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

    #Undistort
    undistortedImage = cv2.undistort(distortedImage, mtx, dist, None, newcameramtx)

    #Crop image
    #x,y,w,h = roi
    #dst = dst[y:y+h, x:x+w]
    return undistortedImage

def generateUndistortedImagesFromVideo(mtx, dist, videoPath, cameraName):
    print('Generating Undistorted Images for Camera: ' + cameraName)

    path = createFolder(cameraName)

    cap = cv2.VideoCapture(videoPath)
    i = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break

        frame = cv2.resize(frame, (1280, 720))
        undistortedImage = undistort(mtx, dist, frame)
        cv2.imwrite(path + '/' + cameraName + 'Undistorted' + str(i) + '.jpg', undistortedImage)
        i+=1
 
    cap.release()
    cv2.destroyAllWindows()

def createFolder(folderName):
    path = os.getcwd()

    try:
        if not os.path.exists(path + '/' + folderName + 'Undistorted'):
            os.mkdir(path + '/' + folderName + 'Undistorted')
            return path + '/' + folderName + 'Undistorted'
        else:
            return path + '/' + folderName + 'Undistorted'

    except OSError:
        print ("Creation of the directory %s failed" % (path + folderName))
    else:
        print ("Successfully created the directory %s " % (path + folderName))

def extractImagePoints(mtx1, dist1, mtx2, dist2):

    print("Loading image...")

    #Get clicks on image from set 1
    img1 = cv2.imread('/home/pedro/Documentos/UnB/PVC/StereoSystemOpencv/camera1Undistorted/camera1Undistorted300.jpg')
    cv2.namedWindow('imageCam1')
    cv2.setMouseCallback('imageCam1', imageClick, param=1)

    while(1):

        cv2.imshow('imageCam1', img1)
        if cv2.waitKey(20) & 0xFF == 27: break
    cv2.destroyWindow('imageCam1')

    #Try to extract info using solvePnP
    objectPoints = np.array([[0.0, 0.0, 0.0], [0.0, 1.4, 0.0], [2.6, 0.0, 0.0], [2.6, 1.4, 0.0]], dtype=np.float32)
    listaO = []
    listaO.append(objectPoints)

    listaI = []
    listaI.append(np.array(imgPointsCam1, dtype=np.float32))

    ret,rVecs, tVecs = cv2.solvePnP(objectPoints, np.array(imgPointsCam1, dtype=np.float32), mtx1, dist1)
    rotM = cv2.Rodrigues(rVecs)[0]
    cameraPosition = -np.matrix(rotM).T * np.matrix(tVecs)

    print(f"solvePnP 1\nrVecs: {rVecs}\ntVecs: {tVecs}")
    print(f"rotM = {rotM}")
    print(f"cameraPosition = {cameraPosition}")


    # project 3D points to image plane
    points3d, jac = cv2.projectPoints(np.float32([[2,0,0], [0,2,0], [0,0,0.5]]).reshape(-1,3), rVecs, tVecs, mtx1, dist1)
    #print(f"\n3dPoints: {points3d}")
    img = draw(img1,np.array(imgPointsCam1, dtype=np.float32), points3d)
    cv2.imshow('img',img)
    k = cv2.waitKey(0) & 0xFF
    if k == ord('s'):
        cv2.imwrite('eixo1.png', img)
    cv2.destroyWindow('img')


    #Image2
    #Get clicks on image from set 2
    img2 = cv2.imread('/home/pedro/Documentos/UnB/PVC/StereoSystemOpencv/camera2Undistorted/camera2Undistorted100.jpg')
    cv2.namedWindow('imageCam2')
    cv2.setMouseCallback('imageCam2', imageClick, param=2)

    while(1):

        cv2.imshow('imageCam2', img2)
        if cv2.waitKey(20) & 0xFF == 27: break
    cv2.destroyWindow('imageCam2')

    ret2,rVecs2, tVecs2 = cv2.solvePnP(objectPoints, np.array(imgPointsCam2, dtype=np.float32), mtx2, dist2)
    rotM2 = cv2.Rodrigues(rVecs2)[0]
    cameraPosition2 = -np.matrix(rotM2).T * np.matrix(tVecs2)

    print(f"\nsolvePnP 2\nrVecs: {rVecs2}\ntVecs: {tVecs2}")
    print(f"rotM = {rotM2}")
    print(f"cameraPosition = {cameraPosition2}")


    # project 3D points to image plane
    points3d2, jac2 = cv2.projectPoints(np.float32([[2,0,0], [0,2,0], [0,0,0.5]]).reshape(-1,3), rVecs2, tVecs2, mtx2, dist2)
    #print(f"\n3dPoints: {points3d2}")
    img = draw(img2,np.array(imgPointsCam2, dtype=np.float32), points3d2)
    cv2.imshow('img',img)
    k = cv2.waitKey(0) & 0xFF
    if k == ord('s'):
        cv2.imwrite('eixo2.png', img)
    cv2.destroyWindow('img')

def draw(img, corners, imgpts):
    corner = tuple(corners[0].ravel())
    img = cv2.line(img, corner, tuple(imgpts[0].ravel()), (255,0,0), 5)
    img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (0,255,0), 5)
    img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (0,0,255), 5)
    return img

def stereoExtrinsic(mtx1, mtx2, dist1, dist2):

    objectPoints = np.array([[0.0, 0.0, 0.0], [0.0, 1.4, 0.0], [2.6, 0.0, 0.0], [2.6, 1.4, 0.0]], dtype=np.float32)
    lista = []
    lista.append(objectPoints)
    listaIm1 = []
    listaIm1.append(np.array(imgPointsCam1, dtype=np.float32))
    listaIm2 = []
    listaIm2.append(np.array(imgPointsCam2, dtype=np.float32))
    print("Stereo")
    print(len(lista))
    print(len(listaIm1))
    print(len(listaIm2))
    return cv2.stereoCalibrate(lista, listaIm1, listaIm2, mtx1, dist1, mtx2, dist2, (1280, 720), flags=cv2.CALIB_FIX_INTRINSIC)

def imageClick(event, x, y, flags, param):

    #Check if left mouse button was clicked and stores RGB
    if event == cv2.EVENT_LBUTTONDOWN:

        if param == 1:

            imgPointsCam1.append([x, y])

        elif param == 2:

            imgPointsCam2.append([x, y])

if __name__ == "__main__":

    global imgPointsCam1
    #global imgPointsCam2
    imgPointsCam1 = []
    imgPointsCam2 = []

    paths = []
    paths.append(input("Caminho para o dataset 1: ") + "/*.jpg")
    paths.append(input("\nCaminho para o dataset 2: ") + "/*.jpg")

    ret1, mtx1, dist1, rvecs1, tvecs1 = calibration(paths[0])
    #print(f"\ndist1: {mtx1}")
    #generateUndistortedImagesFromVideo(mtx1, dist1, '/home/pedro/Documentos/UnB/PVC/StereoSystemOpencv/camera1.webm', 'camera1')

    
    #Calibrate Camera 2
    ret2, mtx2, dist2, rvecs2, tvecs2 = calibration(paths[1])
    '''print(f"\ndist2: {mtx2}")
    generateUndistortedImagesFromVideo(mtx2, dist2, '/home/pedro/Documentos/UnB/PVC/StereoSystemOpencv/camera2.webm', 'camera2')'''

    extractImagePoints(mtx1, dist1, mtx2, dist2)
    #print(f"Image points 1: {imgPointsCam1}\nImage points 2: {imgPointsCam2}\n")

    '''
    retVal, cm1, dc1, cm2, dc2, r, t, e, f = stereoExtrinsic(mtx1, mtx2, dist1, dist2)

    print(f"Matrizes\nR: {r}\nT: {t}\nE: {e}\nF: {f}")'''