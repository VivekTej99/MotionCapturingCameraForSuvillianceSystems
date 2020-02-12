""" Idea and Code By : Vivek Tej
	CCTV recording when motion is captured """

#Importing The Required Modules..

import cv2						#Computer Vision
import datetime as dt , time	#DateTime and time modules
import argparse 				#Command Line Arguments Module
from threading import Thread 	#Threads module for simulatenously usage of memory
import os 						#Os module to deal with filenames.....

#Adding the Command Line Arguments

ap = argparse.ArgumentParser()
ap.add_argument("-w","--webcam",default=0,help="Give the webacm index to use (like 0 or 1)")
ap.add_argument("-u","--url",help="Give the address of ip_webcamera if you wanto stream video from ip_webcam")
args = vars(ap.parse_args())

cam =0
first_frame =0      #First_frame variable to capture first frame as background frame

#Intiating the Webcam(or ip_webcam) and reading the first_frame.

if(args['url']==None):
	cap = cv2.VideoCapture(args['webcam'])
	print("\n\t\t[*]  Loading The stream Of Webcamera.....\n")
	time.sleep(1)
	cam = 1

	test , first_frame = cap.read()
	gray = cv2.cvtColor(first_frame,cv2.COLOR_BGR2GRAY)
	first_frame = cv2.GaussianBlur(gray , (21,21),0)

else:
	cap = cv2.VideoCapture(args['url'])
	time.sleep(1)
	print("\n\t\t[*]  Loading The stream of ip_webcamera....\n")

	test , first_frame = cap.read()
	gray = cv2.cvtColor(first_frame,cv2.COLOR_BGR2GRAY)
	first_frame = cv2.GaussianBlur(gray , (21,21),0)

#Creating filename to store in current working Directory...
time_n = dt.datetime.now()
filename = time_n.strftime("%d%b%Y_%I %M %p")
current_dir = str(os.getcwd())

#Initializing the VideoWriter which saves the Video.
out = cv2.VideoWriter(current_dir+"\\"+filename+".avi" , cv2.VideoWriter_fourcc(*'XVID') , 23 , (int(cap.get(3)), int(cap.get(4))))

motion = 0
ti = 48

while test:
	motion = 0

	test , frame = cap.read()
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray , (21,21),0)

	#Calculating the difference between and Calculating the thresholdframe
	delta_frame = cv2.absdiff(first_frame,gray)              
	thresh_frame = cv2.threshold(delta_frame,30,255,cv2.THRESH_BINARY)[1]
	thresh_frame = cv2.dilate(thresh_frame,None,iterations=2)

	#Finding the motion in the frames and drawing a green rectangle
	(cnts,_)=cv2.findContours(thresh_frame.copy() , cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE) 

	for contour in cnts :
		if cv2.contourArea(contour)<1000:
			continue
		motion = 1
		x,y,w,h = cv2.boundingRect(contour)                #Drawing Rectangles for contours that occupy 1000 pixels

		cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)

	if motion == 1:
		time_1 = dt.datetime.now()
		cv2.putText(frame,time_1.strftime("%I:%M:%S.%p"),(10,460),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0,0), 2)

		out.write(frame)  # Saving the video frames when motion is detected...

	cv2.imshow("Gray_frame",gray)
	cv2.imshow("Delta_Frame",delta_frame)
	cv2.imshow("Thresh_frame",thresh_frame)     #Showing The Respective Frames
	cv2.imshow("Color_Frame",frame)
	

	key = cv2.waitKey(1)
	if key == ord('q'):							#Press q key to exit from code..
		break

	#Updating the backgorund frame after every 3 second..
	if(ti == 0):
		test,first_frame = cap.read()
		first_frame = cv2.cvtColor(first_frame,cv2.COLOR_BGR2GRAY)
		first_frame = cv2.GaussianBlur(first_frame , (21,21),0)
		ti = 48

	ti-=1

#Closing all the windows and releasing the streaming and saving..
cv2.destroyAllWindows()
cap.release()
out.release()
