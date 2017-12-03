import RPi.GPIO as  GPIO
import picamera
import picamera.array
import time
import numpy as np
from random import *


servo = 22 # azimuth, side to side

# Variables that will handle the random movement of the robot
randAngle = 0
randDistance = 0
randDirection = 0


# Variables to track the location of the light
maxLight = 0
maxLightAngle = 0




# Sets the desired pin numbering system to BCM
GPIO.setmode(GPIO.BCM)

# Disables warnings in case the RPI.GPIO detects that a pin has been configured
# to something other than the default (input)
GPIO.setwarnings(False)

# These are the pins we will be using.
chan_list = [servo]

# Sets the pins stated above as inputs
GPIO.setup(chan_list,GPIO.OUT)

# These are the pins we will be using.
# ENA-6, ENB-26, IN1-12, IN2-13, IN3-20, IN4-21
ENA = 6
ENB = 26
IN1 = 12
IN2 = 13
IN3 = 20
IN4 = 21


### ************************************************************************* ###
# The following functions will control the robot's movement throughout the course
### ************************************************************************* ###

#Functions to carry out movement of the robot
# 0 = GPIO.LOW  1 = GPIO.HIGH
def moveForward():
#    print("Moving Forward...")
    GPIO.output(IN1,GPIO.HIGH)
    GPIO.output(IN2,GPIO.LOW)
    GPIO.output(IN3,GPIO.LOW)
    GPIO.output(IN4,GPIO.HIGH)

def stop():
#    print("Stopping...")
    GPIO.output(IN1,GPIO.LOW)
    GPIO.output(IN2,GPIO.LOW)
    GPIO.output(IN3,GPIO.LOW)
    GPIO.output(IN4,GPIO.LOW)

def moveBackward():
#    print("Moving Backward...")
    GPIO.output(IN1,GPIO.LOW)
    GPIO.output(IN2,GPIO.HIGH)
    GPIO.output(IN3,GPIO.HIGH)
    GPIO.output(IN4,GPIO.LOW)

def pivotRight():
#    print("Right Pivot...")
    GPIO.output(IN1,GPIO.HIGH)
    GPIO.output(IN2,GPIO.LOW)
    GPIO.output(IN3,GPIO.HIGH)
    GPIO.output(IN4,GPIO.LOW)

def pivotLeft():
#    print("Left Pivot...")
    GPIO.output(IN1,GPIO.LOW)
    GPIO.output(IN2,GPIO.HIGH)
    GPIO.output(IN3,GPIO.LOW)
    GPIO.output(IN4,GPIO.HIGH)


# Function for changing the duty cycle
def ServoAngle(angle):
	p1.ChangeDutyCycle(2.5 + 10.0*angle/180)


# Will generate a random movement for the robot
def randomMovement():
	# Will generate a random angle between 20 and 100
	randAngle = randint(20, 100)
	randTime = randint(1, 3)
	randDirection = random()

	# move backwards a random amount of time
	moveBackward()
	time.sleep(randTime)
	stop()

	# Add your stuff here razwan. for the random angles that it will turn
	if (randDirection == 0):
		pivotRight()
		# pivot some angle

		stop()
	else:
		pivotLeft()

		# pivot some angle

		stop()

	
	randTime = randint(1, 3)

	# move forward a random amount of time
	moveForward()
	time.sleep(randTime)
	stop()

# Will scan horizontally to find the light source, and adjust the robot to face it
def findLight():
	with picamera.PiCamera() as camera:
	    camera.resolution = (128, 80)
	   
	    while(1):
	    	with picamera.array.PiRGBArray(camera) as stream:
	        	camera.exposure_mode = 'auto'
	        	camera.awb_mode = 'auto'
	        	camera.capture(stream, format='rgb')
	        	pixAverage = int(np.average(stream.array[...,1]))
			
			print ("Light sdfsdMeter pixAverage=%i" % pixAverage)




### ************************************************************************* ###





# Creates object "p1", sets frequency to 50 Hz, starts at 0% duty cycle
p1 = GPIO.PWM(servo,50)
p1.start(0)

findLight()








# Cleans up resources
p1.stop()
GPIO.cleanup()