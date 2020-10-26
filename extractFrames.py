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

    #Crop image
    #x,y,w,h = roi
    #dst = dst[y:y+h, x:x+w]
    return undistortedImage

def generateUndistortedImagesFromVideo(mtx, dist, videoPath, cameraName):
    print('Generating Undistorted Images for Camera: ' + cameraName)

    path = createFolder(cameraName + "Undistorted")

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

def generateImagesFromVideo(videoPath, cameraName):
    print('Generating Undistorted Images for Camera: ' + cameraName)

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

if __name__ == "__main__":

    #generateImagesFromVideo('/home/pedro/Documentos/UnB/PVC/StereoSystemOpencv/camera1.webm', 'camera1')
    #generateImagesFromVideo('/home/pedro/Documentos/UnB/PVC/StereoSystemOpencv/camera2.webm', 'camera2')