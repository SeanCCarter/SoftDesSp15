""" Experiment with face detection and image filtering using OpenCV """

import cv2
import numpy as np
import sys

webcam_video = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
kernel = np.ones((21,21),'uint8')

def remap_interval(val, input_interval_start, input_interval_end, output_interval_start, output_interval_end):
	"""This is to change the basic grid for the face, into something that scales with input"""
	scale_initial = input_interval_end-input_interval_start
	scale_final = output_interval_end - output_interval_start
	value_initial = val - input_interval_start
	value = value_initial*scale_final/float(scale_initial) + output_interval_start
	return int(value)

def draw_face(x, y, w, h, img):
	#Draw left eye white
	xcenter = remap_interval(-.45, -1, 1, x, x+w)
	ycenter = remap_interval(.45, 1, -1, y, y+h)
	radius = remap_interval(.15, 0, 1, 0, (w+h)/2)
	cv2.circle(img, (xcenter, ycenter), radius, (255, 255, 255), -1)

	#Draw left eye black
	xcenter = remap_interval(-.5, -1, 1, x, x+w)
	ycenter = remap_interval(.5, 1, -1, y, y+h)
	radius = remap_interval(.05, 0, 1, 0, (w+h)/2)
	cv2.circle(img, (xcenter, ycenter), radius, (0, 0, 0), -1)

	#Draw right eye white
	xcenter = remap_interval(.45, -1, 1, x, x+w)
	ycenter = remap_interval(.43, 1, -1, y, y+h)
	radius = remap_interval(.15, 0, 1, 0, (w+h)/2)
	cv2.circle(img, (xcenter, ycenter), radius, (255, 255, 255), -1)

	#Draw left eye black
	xcenter = remap_interval(.5, -1, 1, x, x+w)
	ycenter = remap_interval(.4, 1, -1, y, y+h)
	radius = remap_interval(.05, 0, 1, 0, (w+h)/2)
	cv2.circle(img, (xcenter, ycenter), radius, (0, 0, 0), -1)

	#Draw mouth
	xcenter = remap_interval(0, -1, 1, x, x+w)
	ycenter = remap_interval(-.2, 1, -1, y, y+h)
	major_axis = remap_interval(.2, 0, 1, 0, (w+h)/2)
	minor_axis = remap_interval(.35, 0, 1, 0, (w+h)/2)
	cv2.ellipse(img, (xcenter, ycenter), (major_axis, minor_axis), 0, 0, 180, (0, 0, 0), -1)

while(True):
	# Capture frame-by-frame
	ret, frame = webcam_video.read()
	faces = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(30,30))
	for (x,y,w,h) in faces:
		frame[y:y+h,x:x+w,:] = cv2.dilate(frame[y:y+h,x:x+w,:], kernel)
		draw_face(x, y, w, h, frame)
		#frame[y:y+h,x:x+w, :] = [255, 255, 255] - frame[y:y+h,x:x+w, :]
		
		cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,254))

	#Todo: use this section to do edit the viedo stream
	#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


	# Display the resulting frame
	cv2.imshow('frame', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

#This closes everything down, so that I don't accidentally break Ubuntu again
webcam_video.release()
cv2.destroyAllWindows()