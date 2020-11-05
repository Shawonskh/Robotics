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

running = True

def getDistanceWithCam(blobSize):
    if blobSize > 0:
        return 59915.85/blobSize - 117.47
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
        # Slower code goes here
        drawMap()

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

