#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import serial
import sys
import json
import socket
import numpy as np
import math
from kalman import Kalman

##########
# TASK 1 #
##########

# You will need to find your own magnetometer calibration values,
#  use the sample code that came with the LSM303 library!!!
# You will need to change these values both in here and in the Arduino code
MAG_X_MIN = -2913
MAG_Y_MIN = -2441
MAG_Z_MIN = -3249
MAG_X_MAX = +2474
MAG_Y_MAX = +2615
MAG_Z_MAX = +2056

##############
# TASK 1 END #
##############

ROLL_LIMIT = 90.0
PITCH_LIMIT = 180.0
YAW_LIMIT = 180.0

# Normalize a vector


def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

# Calculate roll and pitch from accelerometer data


def calculateRollPitch(data):
    try:
        roll = math.degrees(
            math.atan(data[1]/math.sqrt(data[0]**2+data[2]**2)))
        pitch = math.degrees(math.atan2(-data[0], data[2]))
    except IndexError as e:
        print(e)
        print(data)
        return 0, 0
    return roll, pitch

# Calculate yaw from accelerometer and magnetometer data


def calculateYaw(mag_data, acc_data):
    # subtract offset (average of min and max) from magnetometer readings
    avgX = (MAG_X_MIN + MAG_X_MAX)/2
    avgY = (MAG_Y_MIN + MAG_Y_MAX)/2
    avgZ = (MAG_Z_MIN + MAG_Z_MAX)/2

    corrigated_mag = np.array(
        [mag_data[0] - avgX, mag_data[1] - avgY, mag_data[2] - avgZ])
    # Compute E and N
    E = normalize(np.cross(corrigated_mag, acc_data))
    N = normalize(np.cross(acc_data, E))
    heading = math.atan2(np.dot(E, [1, 0, 0]),
                         np.dot(N, [1, 0, 0]))*180/math.pi
    if heading < 0:
        heading += 360
    if heading > 360:
        heading -= 360

    return heading

# Convert raw gyro values to dps


def calculateGyroRate(data):
    gyro = data[0:3]
    return np.array([x*0.00875 for x in gyro])

# Process incoming data and if data is not
# according to standards, checksum will be false


def processInputData(data):
    data = data.split(b':')
    try:
        data = [int(x) for x in data]
        if not len(data) == 10:
            raise Exception
        checkSum = True
    except:
        checkSum = False

    return checkSum, data


def sendDataToPlot(socketobj, x, y, z, xx, yy, zz):
    json_string = {'r': round(x, 3), 'p': round(y, 3), 'y': round(z, 3),
                   'kalman_r': round(xx, 3), 'kalman_p': round(yy, 3), 'kalman_y': round(zz, 3)}
    socketobj.send(json.dumps(json_string).ljust(150).encode('utf-8'))

# BEGIN PROGRAM 


# Create a serial object
ser = serial.Serial("/dev/ttyUSB0", 250000, timeout=1)

# Create a socket object
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


time.sleep(3)  # arduino will reset on serial open
# let it calibrate, has to be still

# Initialize orientation vectors
acc = [0.0, 0.0, 0.0]
mag = [0.0, 0.0, 0.0]

# Reset rpy
reset_condition = True

# Kalman objects
kalman_x = Kalman()
kalman_y = Kalman()
kalman_z = Kalman()

#####################################
# YOU NEED TO ADJUST THESE (TASK 4) #
#####################################

# Set Kalman sensor noise stdevs
kalman_x.setSensorNoise(0.2, 0.03)  # 0.2, 0.03
kalman_y.setSensorNoise(0.2, 0.03)  # 0.2, 0.03
kalman_z.setSensorNoise(0.6, 0.03)  # 0.6, 0.03


# Set Kalman process noise
kalman_x.setProcessNoise(0.0001, 0.0001)  # 0.0001, 0.0001
kalman_y.setProcessNoise(0.0001, 0.0001)  # 0.0001, 0.0001
kalman_z.setProcessNoise(0.0001, 0.0001)  # 0.0001, 0.0001

##############
# TASK 4 END #
##############

# Roll, pitch, yaw arrays initializations
rpy = np.array([0.0, 0.0, 0.0])
rpy_moving_average = np.array([0.0, 0.0, 0.0])
rpy_complimentary = np.array([0.0, 0.0, 0.0])
rpy_kalman = np.array([0.0, 0.0, 0.0])

# Moving average initialization

#####################################
# YOU NEED TO ADJUST THESE (TASK 2) #
#####################################

moving_avg_len = 1  # Length of the buffer for roll and pitch
moving_avg_len_mag = 1  # Length of the buffer for yaw

##########################
# ADJUSTING (TASK 2) END #
##########################

r_avg_array = np.zeros(moving_avg_len)
p_avg_array = np.zeros(moving_avg_len)
y_avg_array = np.zeros(moving_avg_len_mag)

# Moving average array initialization

##################
# USER FUNCTIONS #
##################

# YOU WILL NEED TO IMPLEMENT THESE

##########
# TASK 2 #
##########
def moving_average(r, p, y):
    global r_avg_array, p_avg_array, y_avg_array
    global rpy_moving_average

    # Shift list
    # YOUR CODE HERE

    # Add the new measurement
    # YOUR CODE HERE

    # Calculate average
    # YOUR CODE HERE

    # Output average
    # Change the zeros to your output
    rpy_moving_average[0] = 0.0
    rpy_moving_average[1] = 0.0
    rpy_moving_average[2] = 0.0
##############
# TASK 2 END #
##############

##########
# TASK 3 #
##########

def complimentary_filter(r, p, y, gx, gy, gz, dt):
    global rpy_complimentary
    # Complimentary filter implementation
    # YOUR CODE HERE

    # Filter output
    # Change the zeros to your output
    rpy_complimentary[0] = 0.0
    rpy_complimentary[1] = 0.0
    rpy_complimentary[2] = 0.0

##############
# TASK 3 END #
##############

def kalman_filter(r, p, y, gx, gy, gz, dt):
    global rpy_kalman, kalman_x, kalman_y, kalman_z

    # Kalman magic
    rpy_kalman[0] = kalman_x.getAngle(r, gx, dt)
    rpy_kalman[1] = kalman_y.getAngle(p, gy, dt)
    rpy_kalman[2] = kalman_z.getAngle(y, gz, dt)


try:
    # You will need to change these values to display on another computer
    host = 'localhost'  # '172.19.36.197'
    port = 12345
    soc.connect((host, port))
    print("I have connected to server at " + host + " Port " + str(port))
    i = 0
    # Set socket to non-blocking mode
    soc.setblocking(0)
    while(1):
        try:
            # Read data
            ser.write(b'g')
            data = ser.readline().strip()

            checkSum, data_vector = processInputData(data)

            if (checkSum):
                # Separate measurements
                acc = data_vector[0:3]
                mag = data_vector[3:6]
                gyro = data_vector[6:10]

                # Calculate roll, pitch, yaw
                rpy[0], rpy[1] = calculateRollPitch(acc)
                rpy[2] = calculateYaw(mag, acc)

                ##################
                # Moving average #
                ##################

                moving_average(rpy[0], rpy[1], rpy[2])

                # Set kalman initial angle
                if(reset_condition):
                    kalman_x.setAngle(rpy[0])
                    kalman_y.setAngle(rpy[1])
                    kalman_z.setAngle(rpy[2])
                    reset_condition = False
                else:
                    # Sent time is in microseconds, convert to seconds
                    dt = gyro[3]/1000000.0
                    # Convert raw to dps
                    gyro = calculateGyroRate(gyro)
                    # Check if flipped
                    if(abs(rpy[0]) > 90):
                        gyro[0] = -gyro[0]
                    else:
                        gyro[2] = -gyro[2]

                    ########################
                    # Complimentary filter #
                    ########################
                    complimentary_filter(
                        rpy[0], rpy[1], rpy[2], gyro[0], gyro[1], gyro[2], dt)

                    #################
                    # Kalman filter #
                    #################
                    kalman_filter(rpy_moving_average[0], rpy_moving_average[1],
                                  rpy_moving_average[2], gyro[0], gyro[1], gyro[2], dt)

                # Send to plotting 3 times slower than measured
                if i % 3 == 0:
                    ###################################################
                    #YOU NEED TO COMMENT/UNCOMMENT THE RIGHT FUNCTION #
                    ###################################################

                    # TASK 2
                    # sendDataToPlot(
                    #     soc, rpy[0], rpy[1], rpy[2], rpy_moving_average[0], rpy_moving_average[1], rpy_moving_average[2])
                    # TASK 3
                    # sendDataToPlot(
                    #     soc, rpy[0], rpy[1], rpy[2], rpy_complimentary[0], rpy_complimentary[1], rpy_complimentary[2])
                    # TASK 4
                    # sendDataToPlot(
                    #     soc, rpy[0], rpy[1], rpy[2], rpy_kalman[0], rpy_kalman[1], rpy_kalman[2])

                    ########################
                    # COMMENTING BLOCK END #
                    ########################
            else:
                print("Borken data")
                print(data)

        except socket.error as e:
            print(e)
            print("Unexpected socket error! Closing program!")
            break

        i += 1

except KeyboardInterrupt:
    print("Keyboard interrupt")

finally:
    ser.close()
    print("Serial connection closed")
    soc.close()
    print("Socket closed!")
