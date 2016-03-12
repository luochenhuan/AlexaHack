# -*- coding: utf-8 -*-
import cv2
from firebase import firebase
from multiprocessing import Process, Pipe

firebase = firebase.FirebaseApplication('https://hackalexa.firebaseio.com', None)
db = '/test/'
var = 'isAsked'

def is_asked(conn):
    while(True):
        isAsked = firebase.get(db+var, None)        
        conn.send(isAsked)
#        if (isAsked == True):
#            conn.close()
#            break

if __name__ == '__main__':    
    parent_conn, child_conn = Pipe()
    p = Process(target=is_asked, args=(child_conn,))
    p.start()
    cap = cv2.VideoCapture(0)
    while(True):
        ret, frame = cap.read()
        frame = cv2.flip(frame,1)
        # Display the resulting frame
        cv2.imshow('frame',frame)
#        ## Our operations on the frame come here
        recvSignal = parent_conn.recv()
        print recvSignal
        #if cv2.waitKey(1) & 0xFF == ord('q'):
        if cv2.waitKey(1) & recvSignal == True:
#            get_color_p = Process(target=color_detect, args(frame,))
#            get_color_p.start()
            break
    
    p.join()   
    cap.release()
    cv2.destroyAllWindows()
    print 'end'
