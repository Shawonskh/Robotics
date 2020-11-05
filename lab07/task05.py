# -- coding: utf-8 --

import cv2
import gopigo as go
import numpy as np
import time
from gopigo import *



# global variable for determining gopigo speed

gospeed = 160
timestart = time.time()
Integral_t=0
previouserr=0
Ki=0
Kd=0


# global variable for video feed
cap = None


lH=9
def lHa(new):
    global lH
    lH = new
    return lH
lS=86
def lSa(new):
    global lS
    lS = new
    return lS
lV=60
def lVa(new):
    global lV
    lV = new
    return lV
hH=179
def hHa(new):
    global hH
    hH = new
    return hH
hS=255
def hSa(new):
    global hS
    hS = new
    return hS
hV=255
def hVa(new):
    global lV
    hV = new
    return hV




cv2.namedWindow("Processed")


cv2.createTrackbar("HueL", 'Processed', lH, 255, lHa)
cv2.createTrackbar("SaturationL", 'Processed', lS, 255, lSa)
cv2.createTrackbar("ValueL", 'Processed', lV, 255, lVa)
cv2.createTrackbar("HueH", 'Processed', hH, 255, hHa)
cv2.createTrackbar("SaturationH", 'Processed', hS, 255, hSa)
cv2.createTrackbar("ValueH", 'Processed', hV, 255, hVa)



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

        result = np.nonzero(thresholded)
        test=np.mean(result[1])
        medium=(round(test))
            
          
        
    
    # This function should use frame from camera to determine line location.
    # It should return location of the line in the frame.
    # Feel free to define and use any global variables you may need.
    # YOUR CODE HERE
    
        return medium


# TASK 2
def bang_bang(linelocation):
    
    if (linelocation) < 300:
        go.left()
    elif (linelocation) > 300:
        go.right()
    else:
        go.forward()
    # This function should use the line location to implement a simple bang-bang controller.
    # YOUR CODE HERE
    
    return


# TASK 3
def bang_bang_with_hysteresis(linelocation):
    
    higher = 320
    lower = 300
    if (linelocation) < higher:
        go.left()
    elif (linelocation) > lower:
        go.right()
    
    
    # This function should use the line location to implement bang-bang controller with hysteresis.
    # YOUR CODE HERE
    
    return


# TASK 4
def proportional_controller(linelocation):
    if linelocation == linelocation:
    
        e = 320-(linelocation)
        Kp = 0.099 #0.135
        Pout=Kp*e
        
        set_left_speed(int(gospeed-Pout))
        set_right_speed(int(gospeed+Pout))
        
    
 
    # This function should use the line location to implement proportional controller.
    # Feel free to define and use any global variables you may need.
    # YOUR CODE HERE
    
    return


# TASK 5
def pid_controller(linelocation):
    global timestart, timeend, previouserr, Integral_t
    if linelocation == linelocation:
        
        Ku = 0.099
        Tu = 2.915
        Kp = 0.6*Ku
        Ki = (1.2*Ku)/Tu
        Kd = (3*Ku*Tu)/40
        ##if i change these valus too low then the robot goes in one direction from the starting point & if these values are 
        ##too high then after few oscilation when it turns, it goes out from the line.
        
        timeend = time.time()
        t = timeend - timestart
        print(t)
        timestart=timeend
        
        e = 320 - linelocation
        P = Kp*e
        I = t*e
        Integral_t = Integral_t + I
        
        error = e -previouserr
        previouserr = e
        D = error/t
        
        PID_out = P + Ki*Integral_t +Kd*D
        
        set_left_speed(int(gospeed-PID_out))
        set_right_speed(int(gospeed+PID_out))
    
    
    
    

    
    # This function should use the line location to implement PID controller.
    # Feel free to define and use any global variables you may need.
    # YOUR CODE HERE
    
    return


# Initialization
init()

while True:
    # We read information from camera.
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    r=[len(frame)-150, len(frame)-130, 0, len(frame[0])]
    frame =frame[r[0]:r[1], r[2]:r[3]]
    lowerLimits = np.array([lH, lS, lV])
    upperLimits = np.array([hH, hS, hV])
    thresholded = cv2.inRange(frame, lowerLimits, upperLimits)
    #thresholded = cv2.morphologyEx(thresholded, cv2.MORPH_CLOSE, kernel)
    #outimage = cv2.bitwise_and(frame, frame, mask = thresholded)
    #thresholded = cv2.bitwise_not(thresholded)
                     
    go.forward()
            
            
    cv2.imshow("Processed", thresholded)
    
    
    # Task 1: uncomment the following line and implement get_line_location function.
    linelocation = get_line_location(frame)
    print(linelocation)
    
    # Task 2: uncomment the following line and implement bang_bang function.
    #bang_bang(linelocation)
    
    # Task 3: uncomment the following line and implement bang_bang_with_hysteresis function.
    #bang_bang_with_hysteresis(linelocation)
    
    # Task 4: uncommment the following line and implement proportional_controller function.
    #proportional_controller(linelocation)
    
    # Task 5: uncomment the following line and implement pid_controller function.
    pid_controller(linelocation)
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    
go.stop()
cap.release()
cv2.destroyAllWindows()
go.stop()



