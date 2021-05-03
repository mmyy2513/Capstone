#!usr/bin/python3

#just take picture and save it to check the person is

import cv2

cap = cv2.VideoCapture(0)

if cap.isOpened():
	while(True):
		ret, frame = cap.read()
		if ret:
			cv2.imwrite("check.jpg",frame)
			break
	cap.release()
	
