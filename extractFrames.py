import numpy as np
import cv2
import glob
import os
import json

def undistort(mtx, dist, distortedImage):

    h,  w = distortedImage.shape[:2]
    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

    #Undistort
    undistortedImage = cv2.undistort(distortedImage, mtx, dist, None, newcameramtx)

    return undistortedImage

def generateUndistortedImagesFromVideo(mtx, dist, videoPath, cameraName):
    print('Generating Undistorted frames for: ' + cameraName)

    path = createFolder(cameraName + "Undistorted")

    cap = cv2.VideoCapture(videoPath)
    i = 0

    while(cap.isOpened()):

        ret, frame = cap.read()
        if ret == False:
            break

        elif cameraName == 'camera1' and (i == 159 or i == 300):

            frame = cv2.resize(frame, (1280, 720))
            undistortedImage = undistort(mtx, dist, frame)
            cv2.imwrite(path + '/' + cameraName + 'Undistorted' + str(i) + '.jpg', undistortedImage)

        elif cameraName == 'camera2' and (i == 24 or i == 100):

            frame = cv2.resize(frame, (1280, 720))
            undistortedImage = undistort(mtx, dist, frame)
            cv2.imwrite(path + '/' + cameraName + 'Undistorted' + str(i) + '.jpg', undistortedImage)

        i+=1
 
    cap.release()
    cv2.destroyAllWindows()

def generateImagesFromVideo(videoPath, cameraName):
    print('Generating frames for: ' + cameraName)

    path = createFolder(cameraName)

    cap = cv2.VideoCapture(videoPath)
    i = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break

        frame = cv2.resize(frame, (1280, 720))
        cv2.imwrite(path + '/' + cameraName + str(i) + '.jpg', frame)
        i+=1
 
    cap.release()
    cv2.destroyAllWindows()

def createFolder(folderName):
    path = os.getcwd()

    try:
        if not os.path.exists(path + '/' + folderName):
            os.mkdir(path + '/' + folderName)
            return path + '/' + folderName
        else:
            return path + '/' + folderName

    except OSError:
        print ("Creation of the directory %s failed" % (path + folderName))
    else:
        print ("Successfully created the directory %s " % (path + folderName))

def readJson(file):

    with open(file, 'r') as file:

        data = json.load(file)
        data = json.loads(data)

    return np.array(data["cameraMatrix1"]), np.array(data["cameraMatrix2"]), np.array(data["distortionVector1"]), np.array(data["distortionVector2"])

if __name__ == "__main__":

    mtx1, mtx2, dist1, dist2 = readJson('intrinsicsCalibration.json')

    generateUndistortedImagesFromVideo(mtx1, dist1, './camera1.webm', 'camera1')
    generateUndistortedImagesFromVideo(mtx2, dist2, './camera2.webm', 'camera2')