# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 20:36:23 2016

@author: zhenhaiyu
"""
import cv2
import time, os
#from firebase import firebase

pwd = os.getcwd()
video_path = os.path.join(pwd,'videos')
face_xml = os.path.join(pwd,'haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier(face_xml)

#firebase = firebase.FirebaseApplication('https://hackalexa.firebaseio.com', None)
#endpoint = '/face/'
#out_var = 'isOut'

fps = 20.0
THRESH_HOLD = 10

def detect_face():
    camera = cv2.VideoCapture(0)
    width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    noFileOpen = True
    filename = None
    nobodyCount = 0
    
    if (camera.isOpened() == False):
        print("fail to open camera")
    else:
        while(True):            
            # Capture frame-by-frame
            ret, frame = camera.read()
            # flip and display
            frame = cv2.flip(frame,1)
#            cv2.imshow('frame',frame)
            cv2.waitKey(1)
            # running the classifiers
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)                        
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3)

            # Draw rectangles around the faces
            if faces != ():
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255,0,0),2)
                

                if noFileOpen == True:
                    print("new file")
                    filename = os.path.join(video_path,time.strftime("%m-%d-%H-%M-%S") + '.avi')
                    out = cv2.VideoWriter(filename,fourcc, fps, ((width,height)))
                    noFileOpen = False                
                
                out.write(frame)
            # nobody
            else:
                if noFileOpen == False:
                    nobodyCount = nobodyCount+1
                    if nobodyCount >= THRESH_HOLD:
                        print('count >= THRESH_HOLD')
                        out.release()
                        print('nobody, save and quit')
                        break
            cv2.imshow('frame',frame)
            
        cv2.destroyAllWindows()
        camera.release()

    
if __name__ == '__main__':
    detect_face()