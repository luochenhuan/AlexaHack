# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 23:03:44 2016

@author: zhenhaiyu
"""
import cv2, os, time
from firebase import firebase

firebase = firebase.FirebaseApplication('https://hackalexa.firebaseio.com', None)
endpoint = '/test/'
toPlay = 'playVideo'
index = 'playIndex'
play_ind = 0

pwd = os.getcwd()
video_path = os.path.join(pwd,'videos')
fps = 20.0

def play_video(path):
    cap = cv2.VideoCapture(path)
    cap.set(cv2.CAP_PROP_FPS, fps)
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret==True:
            cv2.imshow('frame',frame)
            if cv2.waitKey(1000/int(fps)) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

        
def to_play():
    while(True):
        to_play = firebase.get(endpoint+toPlay, None)       
        print ('toPlay: ' + str(to_play))
        if to_play == True:
            play_ind = firebase.get(endpoint+index, None)
            count = 0
            for file in os.listdir(video_path):
                 if file.endswith('.avi'):
                     count = count + 1
                 if count == play_ind:
                     print ('toPlay: ' + file)
                     play_video(os.path.join(video_path,file))
                     # set toPlay to false
                     firebase.put('https://hackalexa.firebaseio.com'+endpoint, toPlay, False)
                     break
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break

if __name__ == '__main__':    
    to_play()
    print('quit')
    

