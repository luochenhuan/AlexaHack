# Alexa, are there people coming today? -> read Boolean isThereVisitor
# Alexa, show me the videos of visitors? -> read Boolean toPlayVideo
# Alexa, what's the last time visitor come? -> read Time lastTimeVisited


import time
import thread
import cv2
from ThreadPlayVideo import VideoPlayer

from fireBaseMng import FireBaseMng
from ThreadFaceDetect import FaceDetector
from ThreadNumFile import NumFile

def getToPlayVideoVar():
    print('getToPlayVideoVar is running')
    while (True):
        b = fbm.getToPlayVideoVar()
        if b==True:
            print('toPlayVideo is '+str(b))
            fbm.setToPlayVideoVar(False)
            VideoPlayer()


def runFaceCapturer(camera):
    print('runFaceCapturer is running')
    FaceDetector(camera)

def runNumFile():
    print("runNumFile is running")
    NumFile()



if __name__ == '__main__':
    print("run main")
    fbm = FireBaseMng()
    camera = cv2.VideoCapture(0)
    thread.start_new_thread( getToPlayVideoVar, () )
    thread.start_new_thread( runFaceCapturer, (camera,) )
    thread.start_new_thread( runNumFile, () )
    while(True):
        time.sleep(100)

