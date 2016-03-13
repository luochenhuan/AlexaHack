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
var = 'isAsked'
colorVar = 'color'

def is_asked(conn):
    while(True):
        isAsked = firebase.get(repoName+var, None)
        conn.send(isAsked)
#        if (isAsked == True):
#            conn.close()
#            break

if __name__ == '__main__':    
    parent_conn, child_conn = Pipe()
    p = Process(target=is_asked, args=(child_conn,))
    p.start()
    cap = cv2.VideoCapture(0)
    time.sleep(0.5)
    while(True):
        ret, frame = cap.read()
        frame = cv2.flip(frame,1)
        # Display the resulting frame
        cv2.imshow('frame',frame)
#        ## Our operations on the frame come here
        recvSignal = parent_conn.recv()
        print recvSignal
        # if recvSignal == True:
        if cv2.waitKey(1) and recvSignal == True:
            colorValue = ImgColorReader.readMainColorOfPicture(frame)
            result = firebase.put(tableUrl, colorVar, colorValue)
            print(result)
            # break
           # get_color_p = Process(target=DetectColorAndSendService.detectAndSend, args=(tableUrl,frame))
           # get_color_p.start()
           # get_color_p.join()
#             break
    
    p.join()   
    cap.release()
    cv2.destroyAllWindows()
    print 'end'
