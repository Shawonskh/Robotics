#!/usr/bin/env python3
# coding=utf-8
import serial
import gopigo as go
import time
import cv2
import json
import os
import time
import numpy as np
import _thread

img_orig = cv2.imread('map.png')
gospeed = 40

us_pos = 0
enc_pos = 0
cam_pos = 0
scale = 0.5

enc_start0 = go.enc_read(0)
enc_start1 = go.enc_read(1)

video = cv2.VideoCapture(0)  
time_start = 0          
  

file = open("new.txt" , "r")   
text = file.read().splitlines()  
                                
lB = int(text[0])
lG = int(text[1])
lR = int(text[2])
hB = int(text[3])
hG = int(text[4])
hR = int(text[5])
kernel = int(text[6])      
   
file.close()

blobparams = cv2.SimpleBlobDetector_Params()  
blobparams.filterByArea = False            
blobparams.filterByCircularity = False     
blobparams.filterByInertia = False       
blobparams.filterByConvexity = False
blobparams.filterByColor = 0
blobparams.minDistBetweenBlobs = 200    
detector = cv2.SimpleBlobDetector_create(blobparams)  
kernel2 = np.ones(kernel,np.uint8) 

def updateValue(new_value):   
    global lB
    lB = new_value  
    return
def updateValue_2(new_value):   
    global lG 
    lG = new_value  
    return
def updateValue_3(new_value):   
    global lR 
    lR = new_value  
    return
def updateValue_4(new_value):
    global hB 
    hB = new_value  
    return
def updateValue_5(new_value):  
    global hG 
    hG = new_value  
    return
def updateValue_6(new_value):  
    global hR 
    hR = new_value  
    return


running = True

def getDistanceWithCam(size):
    if size > 0:
        return 59915.85/size - 117.47
    return -1

'''
A function to run in a separate thread from the line sensor. Since we want to
read the line sensors as quickly as possible then we would want to run slower
operations such as image processing here. This function will run in a separate thread
as long as the 'running' variable is True. This variable is only set to false
when the main thread is stopped.
'''
def slowThread():
    global us_pos
    global enc_pos
    global cam_pos
    global scale
    global running
    while running:
        ENC1_MOVED_TICKS = go.enc_read(0)-enc_start0
        ENC2_MOVED_TICKS = go.enc_read(1)-enc_start1
        
        MOVED_TICKS = int( (ENC1_MOVED_TICKS + ENC2_MOVED_TICKS) / 2 )
        enc_pos = (1478 - MOVED_TICKS*11.34)
        
        # Slower code goes here
        drawMap(enc_pos,us_pos,cam_pos)
        
        
        #read the image from the camera
        ret, frame = video.read()  
        lowerLimits = np.array([lB, lG, lR])   
        upperLimits = np.array([hB, hG, hR])   
        blur = cv2.blur(frame,(kernel, kernel))
        color = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)  
        thresh = cv2.inRange(color, lowerLimits, upperLimits)  
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel2)

        cv2.createTrackbar("lB", "Processed", lB, 255, updateValue)  
        cv2.createTrackbar("lG", "Processed", lG, 255, updateValue_2)  
        cv2.createTrackbar("lR", "Processed", lR, 255, updateValue_3)  
        cv2.createTrackbar("hB", "Processed", hB, 255, updateValue_4)  
        cv2.createTrackbar("hR", "Processed", hG, 255, updateValue_5)  
        cv2.createTrackbar("hG", "Processed", hR, 255, updateValue_6)
    
        keypoints = detector.detect(opening)  
        
        vid_new = cv2.drawKeypoints(frame, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        for keypoint in keypoints: #
            x = int(keypoint.pt [0]) #Let's get coordinate locations  
            y = int(keypoint.pt [1])    
            size = round(keypoint.size)
            cam_pos=getDistanceWithCam(size)
              
    #Write some text onto the frame
        vid_new = cv2.resize(vid_new, (0,0), fx=0.5, fy=0.5)
        opening = cv2.resize(opening, (0,0), fx=0.5, fy=0.5)

        cv2.imshow('Original', vid_new)  
        cv2.imshow('Processed', opening)  
        
        if cv2.waitKey(1) & 0xFF == ord('q'):  
            break
        
          
# Draws positions read from different sources on the map and then displays it.
def drawMap(us_pos=0, enc_pos=0, cam_pos=0, scale=0.5): 
    img = np.copy(img_orig)

    bluePos = int(-0.869565217 * cam_pos + 1478)   # camera
    greenPos = int(-0.869565217 * us_pos + 1478)    # ultrasonic
    redPos = int(-0.869565217 * enc_pos + 1478)   # encoders

    cv2.circle(img, (redPos,  100), int(15/scale), (0,0,255), -1)
    cv2.circle(img, (greenPos,180), int(15/scale), (0,255,0), -1)
    cv2.circle(img, (bluePos, 260), int(15/scale), (255,0,0), -1)
    cv2.putText(img, "Enc", (redPos, 100 - 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
    cv2.putText(img, "US",  (greenPos, 180 - 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
    cv2.putText(img, "Cam", (bluePos, 260), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2)
    img = cv2.resize(img, (0,0), fx=scale, fy=scale)
    cv2.imshow('map',img)
    cv2.waitKey(1)


print("Battery voltage: " + str(go.volt()))

ser = serial.Serial('/dev/ttyUSB0', 9600)

lineSensorOffset = 0
try:
    _thread.start_new_thread(slowThread, ()) # Start the second thread.
    go.set_speed(60)
    ls1 = 0
    ls2 = 0
    ls3 = 0
    ls4 = 0
    ls5 = 0
    clp = 0
    dist = -1

    # Make sure arduino is ready to send the data.
    print("Syncing serial...0%\r", end='')
    while ser.in_waiting == 0:
        ser.write("R".encode())
    print("Syncing serial...50%\r", end='')
    while ser.in_waiting > 0:
        ser.readline()
    print("Syncing serial...100%")


    '''
    This is the main thread, which should be running more important code such as
    Getting the sensor info from the serial and driving the robot.
    '''
    while True:

        # Read the serial input to string
        ser.write("R".encode()) # Send something to the Arduino to indicate we're ready to get some data.
        serial_line = ser.readline().strip() # Read the sent data from serial.

        try:

            # Decode the received JSON data
            data = json.loads(serial_line.decode())
            # Extract the sensor values
            ls1 = data['ls1']
            ls2 = data['ls2']
            ls3 = data['ls3']
            ls4 = data['ls4']
            ls5 = data['ls5']
            dist = data['us1']
        except Exception as e:  # Something went wrong extracting the JSON.
            dist = -1           # Handle the situation.
            print(e)
            pass
        
        if dist != -1: # If a JSON was correctly extracted, continue.
            # Print received to the console
            print("LS1: ", ls1, "LS2: ", ls2, "LS3: ", ls3, "LS4: ", ls4, "LS5: ", ls5, "DIST: ", dist)
            
            
            us_pos = dist
            
            # 0 = black
            # 1 = white

            # Line following logic goes here
            if ls5==1 and ls4==1 :
                go.set_left_speed(gospeed)
                go.set_right_speed(gospeed)
                go.fwd()
                
            elif ls5 ==1 and ls4!=1 :
                go.set_left_speed(gospeed)
                go.set_right_speed(gospeed+15)
                go.fwd()
            elif ls5!=1 and ls4 ==1 :
                go.set_left_speed(gospeed+15)
                go.set_right_speed(gospeed)
                go.fwd()
                
            else:
                go.fwd()
                         

  

except KeyboardInterrupt:
    print("Serial closed, program finished")

finally:
    ser.close()
    running = False # Stop other threads.
go.stop()

print('closing program')   #lõpetab kogu töö
video.release()
cv2.destroyAllWindows()




