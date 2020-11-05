# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

# reference pins by GPIO numbers
GPIO.setmode(GPIO.BCM)
# disable warnings
GPIO.setwarnings(False)

# define row and column pin numbers
row_pins = [25, 8, 7, 12, 16, 20, 21]
col_pins = [5, 6, 13, 19, 26]

# set all the pins as outputs and set column pins high, row pins low
GPIO.setup(col_pins, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(row_pins, GPIO.OUT, initial=GPIO.LOW)

# Sets the waiting time between rows. With larger wait times (0.1) you can see that rows are lit up at different times. With smaller times (0.01) the LEDs appear to be not blinking at all
wait_time = 0.05

# Displays image for a set number of times
for i in range(50):

  # sets column number 3 low
  GPIO.output(col_pins[2], GPIO.LOW)
  # sets row number 4 high, this should light up the middle LED
  GPIO.output(row_pins[3], GPIO.HIGH)

  # wait
  time.sleep(wait_time)

  # set the pins back to previous states
  GPIO.output(col_pins[2], GPIO.HIGH)
  GPIO.output(row_pins[3], GPIO.LOW)

  # sets columns number 2, 4 low
  GPIO.output(col_pins[1], GPIO.LOW)
  GPIO.output(col_pins[3], GPIO.LOW)

  # sets row number 5 high
  GPIO.output(row_pins[4], GPIO.HIGH)

  # wait
  time.sleep(wait_time)

  # set the pins back to previous states
  GPIO.output(col_pins[1], GPIO.HIGH)
  GPIO.output(col_pins[3], GPIO.HIGH)
  GPIO.output(row_pins[4], GPIO.LOW)

# reset GPIO
GPIO.cleanup()
