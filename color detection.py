# Python code for Multiple Color Detection 
import serial
import numpy as np 
import cv2 
import imutils
Arduino_serial = serial.Serial('COM2', 9600)
# Capturing video through webcam 
webcam = cv2.VideoCapture('http://192.168.1.9:4747/video')
# Start a while loop 
while(1): 
	
	# Reading the video from the 
	# webcam in image frames 
	_, imageFrame = webcam.read() 

	# Convert the imageFrame in 
	# BGR(RGB color space) to 
	# HSV(hue-saturation-value) 
	# color space 
	hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV) 

	# Set range for red color and 
	# define mask 
	red_lower = np.array([166, 84, 141], np.uint8)
	red_upper = np.array([186, 255, 255], np.uint8)
	red_mask = cv2.inRange(hsvFrame, red_lower, red_upper) 

	# Set range for green color and 
	# define mask 
	green_lower = np.array([23, 59, 119], np.uint8)
	green_upper = np.array([54, 255, 255], np.uint8)
	green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

	# Set range for blue color and 
	# define mask 
	blue_lower = np.array([97, 100, 117], np.uint8)
	blue_upper = np.array([117, 255, 255], np.uint8)
	blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper) 
	
	# Morphological Transform, Dilation 
	# for each color and bitwise_and operator 
	# between imageFrame and mask determines 
	# to detect only that particular color 
	kernal = np.ones((5, 5), "uint8") 
	
	# For red color 
	red_mask = cv2.dilate(red_mask, kernal) 
	res_red = cv2.bitwise_and(imageFrame, imageFrame, 
							mask = red_mask) 
	
	# For green color 
	green_mask = cv2.dilate(green_mask, kernal)
	res_green = cv2.bitwise_and(imageFrame, imageFrame,
								mask = green_mask)
	
	# For blue color 
	blue_mask = cv2.dilate(blue_mask, kernal) 
	res_blue = cv2.bitwise_and(imageFrame, imageFrame, 
							mask = blue_mask) 

	# Creating contour to track red color q
	contours, hierarchy = cv2.findContours(red_mask, 
										cv2.RETR_TREE, 
										cv2.CHAIN_APPROX_SIMPLE) 
	
	for pic, contour in enumerate(contours): 
		area = cv2.contourArea(contour) 
		if(area > 5000):
			x, y, w, h = cv2.boundingRect(contour)
			imageFrame = cv2.rectangle(imageFrame, (x, y), 
									(x + w, y + h), 
									(0, 0, 255), 2) 
			
			cv2.putText(imageFrame, "Mau Do", (x, y),
						cv2.FONT_HERSHEY_SIMPLEX, 1.0, 
						(0, 0, 255))
			print('Mau Do')
		Arduino_serial.write('2'.encode())

	# Creating contour to track green color 
	contours, hierarchy = cv2.findContours(green_mask,
										cv2.RETR_TREE, 
										cv2.CHAIN_APPROX_SIMPLE) 
	
	for pic, contour in enumerate(contours): 
		area = cv2.contourArea(contour) 
		if(area > 5000):
			x, y, w, h = cv2.boundingRect(contour) 
			imageFrame = cv2.rectangle(imageFrame, (x, y), 
									(x + w, y + h), 
									(0, 255, 217), 2)
			
			cv2.putText(imageFrame, "Mau Vang", (x, y),
						cv2.FONT_HERSHEY_SIMPLEX, 
						1.0, (0, 255, 217))
			print('Mau Vang')
		Arduino_serial.write('1'.encode())

	# Creating contour to track blue color 
	contours, hierarchy = cv2.findContours(blue_mask, 
										cv2.RETR_TREE, 
										cv2.CHAIN_APPROX_SIMPLE) 
	for pic, contour in enumerate(contours): 
		area = cv2.contourArea(contour) 
		if(area > 5000):
			x, y, w, h = cv2.boundingRect(contour) 
			imageFrame = cv2.rectangle(imageFrame, (x, y), 
									(x + w, y + h), 
									(255, 0, 0), 2) 
			
			cv2.putText(imageFrame, "Mau Xanh Duong", (x, y),
						cv2.FONT_HERSHEY_SIMPLEX, 
						1.0, (255, 0, 0))
			print('Mau Xanh Duong')
		Arduino_serial.write('3'.encode())
	Arduino_serial.write('0'.encode())
			
	# Program Termination 
	cv2.imshow("Nhan Dang Mau Nhay Led", imageFrame)
	if cv2.waitKey(10) & 0xFF == ord('q'): 
		cap.release() 
		cv2.destroyAllWindows() 
		break
