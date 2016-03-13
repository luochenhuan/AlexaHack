# -*- coding: utf-8 -*-
import cv2
from firebase import firebase
from multiprocessing import Process, Pipe
from imgColorReader import ImgColorReader
from DetectColorAndSendService import DetectColorAndSendService
import time

userUrl = 'https://hackalexa.firebaseio.com'
repoName = '/test/'
tableUrl = userUrl + repoName
firebase = firebase.FirebaseApplication('https://hackalexa.firebaseio.com', None)

colorVar = 'color'



if __name__ == '__main__':    

    cap = cv2.VideoCapture(0)
    time.sleep(0.5)
    while(True):
        ret, frame = cap.read()
        frame = cv2.flip(frame,1)
        # Display the resulting frame
        cv2.imshow('frame',frame)

        if cv2.waitKey(1):
            colorValue = ImgColorReader.readMainColorOfPicture(frame)
            result = firebase.put(tableUrl, colorVar, colorValue)
            print(result)


    cap.release()
    cv2.destroyAllWindows()
    print 'end'
