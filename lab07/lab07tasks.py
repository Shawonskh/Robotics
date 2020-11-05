# -*- coding: utf-8 -*-

import cv2
import gopigo as go

# global variable for determining gopigo speed
gospeed = 50

# global variable for video feed
cap = None

def init():
    global cap, gospeed
    # This function should do everything required to initialize the robot.
    # Among other things it should open the camera and set gopigo speed.
    # Some of this has already been filled in.
    # You are welcome to add your own code, if needed.
    
    cap = cv2.VideoCapture(0)
    go.set_speed(gospeed)
    return


# TASK 1
def get_line_location(frame):
    # This function should use frame from camera to determine line location.
    # It should return location of the line in the frame.
    # Feel free to define and use any global variables you may need.
    # YOUR CODE HERE
    
    return 0


# TASK 2
def bang_bang(linelocation):
    # This function should use the line location to implement a simple bang-bang controller.
    # YOUR CODE HERE
    
    return


# TASK 3
def bang_bang_with_hysteresis(linelocation):
    # This function should use the line location to implement bang-bang controller with hysteresis.
    # YOUR CODE HERE
    
    return


# TASK 4
def proportional_controller(linelocation):
    # This function should use the line location to implement proportional controller.
    # Feel free to define and use any global variables you may need.
    # YOUR CODE HERE
    
    return


# TASK 5
def pid_controller(linelocation):
    # This function should use the line location to implement PID controller.
    # Feel free to define and use any global variables you may need.
    # YOUR CODE HERE
    
    return


# Initialization
init()

while True:
    # We read information from camera.
    ret, frame = cap.read()
    cv2.imshow('Original', frame)
    
    # Task 1: uncomment the following line and implement get_line_location function.
    #linelocation = get_line_location(frame)
    
    # Task 2: uncomment the following line and implement bang_bang function.
    #bang_bang(linelocation)
    
    # Task 3: uncomment the following line and implement bang_bang_with_hysteresis function.
    #bang_bang_with_hysteresis(linelocation)
    
    # Task 4: uncommment the following line and implement proportional_controller function.
    #proportional_controller(linelocation)
    
    # Task 5: uncomment the following line and implement pid_controller function.
    #pid_controller(linelocation)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
go.stop()
