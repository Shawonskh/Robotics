import cv2
from Marker import *

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)

def detect(frame, draw = True):
	# This function detects all the markers from the current frame
	# The returned structure is a list, where:
	# First element (index 0) is a tuple of ([list of marker corner coordinates (as lists first element)], [type of variable the coordinates are represented in])
	# Second element is list of marker id numbers, each as a list.
	# the lists are in same order (when using coordinate list like detected[0][0][0][0][0], then this is the first coordinate of marker with id detected[1][0][0])
	detected = cv2.aruco.detectMarkers(frame, dictionary)

	if draw:
		# This function prints the list of markers onto the frame (their main corner, contour and id)
		cv2.aruco.drawDetectedMarkers(frame, detected[0], detected[1])

	# Convert the complicated structure used by ArUco into a more convenient form. See Marker.py
	markers = parseMarkers(detected)

	return markers

def markerById(markers, id):
	# <-- Write a function for finding a marker with a specific id from the list of all markers
	return marker

def center(markers, id):
	# <-- Write a function for finding the center coordinates of a marker with a specific id
	return [x, y]

if __name__ == "__main__":

	# read the image from file
	frame = cv2.imread('example.jpg', 0)

	cv2.imshow('original', frame)

	markers = detect(frame)

	# <-- Here, find the center of the robot and print the coordinates

	# Display the resulting image with markers
	cv2.imshow('markers', frame)

	# Quit the program when any key is pressed
	cv2.waitKey(0)

	# When everything done, release the capture
	print('closing program')
	cv2.destroyAllWindows()
