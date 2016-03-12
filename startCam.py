import numpy as np
import matplotlib.pyplot as plt
import cv2

cap = cv2.VideoCapture(0)
# # reduce frame size to speed it up
# w = 640
# cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, w) 
# cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, w * 3/4)


if (cap.isOpened() == False):
  print("fail to open camera")
else:
	while(True):
		# Capture frame-by-frame
		ret, frame = cap.read()
		frame = cv2.flip(frame,1)
		# Display the resulting frame
		cv2.imshow('frame',frame)
		## Our operations on the frame come here
		# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		## Display the resulting frame
		#cv2.imshow('frame',gray)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()