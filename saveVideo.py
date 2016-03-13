# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 05:35:22 2016

@author: zhenhaiyu
"""
import time
import face_detect
from firebase import firebase

firebase = firebase.FirebaseApplication('https://hackalexa.firebaseio.com', None)
endpoint = '/face/'
out_var = 'isOut'

def service_func():
    print 'service func'

if __name__ == '__main__':
    # service.py executed as script
    # do something
    while(True):
        is_out = firebase.get(endpoint+out_var, None)
        print is_out        
        if is_out:
            print ('is out')
            face_detect.detect_face()
        time.sleep(0.1)

