#!/usr/bin/env python3
# coding=utf-8
import socket
from time import time
import json
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import sys

win = pg.GraphicsWindow()
win.setWindowTitle('Plotter')

p1 = win.addPlot()
p1.setLabel('top', "Roll")
p1.addLegend()
p2 = win.addPlot()
p2.setLabel('top', "Pitch")
p2.addLegend()
p3 = win.addPlot()
p3.setLabel('top', "Yaw")
p3.addLegend()

array_length = 500

rpy_r = np.zeros(array_length)
rpy_p = np.zeros(array_length)
rpy_y = np.zeros(array_length)

kalman_rpy_r = np.zeros(array_length)
kalman_rpy_p = np.zeros(array_length)
kalman_rpy_y = np.zeros(array_length)

############
# TASK 2-4 #
############
curvex = p1.plot(rpy_r, pen='r', name='raw')
curvey = p2.plot(rpy_p, pen='r', name='raw')
curvez = p3.plot(rpy_y, pen='r', name='raw')

# Change label names here according to task!
curvex_k = p1.plot(kalman_rpy_r, pen='g', name='foo')
curvey_k = p2.plot(kalman_rpy_p, pen='g', name='bar')
curvez_k = p3.plot(kalman_rpy_y, pen='g', name='bla')

################
# TASK 2-4 END #
################

r = 0
p = 0
y = 0
kalman_r = 0
kalman_p = 0
kalman_y = 0

ptr1 = 0


def update():
    global r, p, y, kalman_r, kalman_p, kalman_y
    global rpy_p, rpy_r, rpy_y, kalman_rpy_r, kalman_rpy_p, kalman_rpy_y
    global curvex, curvex_k, curvey, curvey_k, curvez, curvez_k

    try:
        received_string = ''
        rcv = connection.recv(150).decode('utf-8')
        begin_index = rcv.find('{')
        end_index = rcv.find('}', begin_index)
        if begin_index > -1 and end_index > begin_index:
            received_string = rcv[begin_index:end_index+1]
        if not rcv:
            print("I got no data from connection! Assuming it has closed!")
            soc.close()
            print("Websocket closed!")
            sys.exit(0)
        json_object = json.loads(received_string)
        r = json_object["r"]
        p = json_object["p"]
        y = json_object["y"]

        kalman_r = json_object["kalman_r"]
        kalman_p = json_object["kalman_p"]
        kalman_y = json_object["kalman_y"]

    except ValueError as e:
        print(rcv)

    rpy_r[:-1] = rpy_r[1:]
    rpy_p[:-1] = rpy_p[1:]
    rpy_y[:-1] = rpy_y[1:]

    kalman_rpy_r[:-1] = kalman_rpy_r[1:]
    kalman_rpy_p[:-1] = kalman_rpy_p[1:]
    kalman_rpy_y[:-1] = kalman_rpy_y[1:]

    rpy_r[-1] = r
    rpy_p[-1] = p
    rpy_y[-1] = y
    kalman_rpy_r[-1] = kalman_r
    kalman_rpy_p[-1] = kalman_p
    kalman_rpy_y[-1] = kalman_y

    curvex.setData(rpy_r)
    curvey.setData(rpy_p)
    curvez.setData(rpy_y)

    curvex_k.setData(kalman_rpy_r)
    curvey_k.setData(kalman_rpy_p)
    curvez_k.setData(kalman_rpy_y)


timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(2)

# Create a socket object
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host = socket.gethostname()
host = 'localhost'  # '172.19.36.197'
port = 12345  # Reserve a port for your service.

try:
    soc.bind((host, port))  # Bind to the port
    soc.listen(1)  # Now wait for client connection.
    connection, addr = soc.accept()  # Establish connection with client.
    print("Server got a connection")  # + str(addr))


except KeyboardInterrupt:
    print("Keyboard Interrupt for server.")

# Plotting
if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
    QtGui.QApplication.instance().exec_()

soc.close()
print("Websocket closed!")
