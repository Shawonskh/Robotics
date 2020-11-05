import cv2

from Commander import *
from Drive import *
from task1_astar import *
from task2_aruco import *
from task3_field import *
from task4_path import *
from task5_command import *


cap = cv2.VideoCapture(1)
ret, frame = cap.read()

# <-- Change the robot id number to the one written on the tag you're using
robotID = 1

# <-- Find the markers from the frame and calculate the shortest path


# drive = Drive(path)
commander = Commander(IP_ADDRESS, PORT_NR)

try:
	while True:
		# read the image from the camera
		ret, frame = cap.read()

		markers = detect(frame)

		# Display the resulting image with markers
		cv2.imshow('markers', frame)

		# <-- Find the coordinates of the front and back of the robot, get the next command from the drive object and pass it on to the commander

		# Quit the program when Q is pressed
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

finally:
	commander.sendCommand('S')  # Just in case
	commander.closeSocket()
	cap.release()
	cv2.destroyAllWindows()
