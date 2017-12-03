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
maxLightAngle = 0
servoAngle = 15



# Sets the desired pin numbering system to BCM
GPIO.setmode(GPIO.BCM)

# Disables warnings in case the RPI.GPIO detects that a pin has been configured
# to something other than the default (input)
GPIO.setwarnings(False)

# These are the pins we will be using.
#chan_list = [servo]


# These are the pins we will be using.
# ENA-6, ENB-26, IN1-12, IN2-13, IN3-20, IN4-21
ENA = 6
ENB = 26
IN1 = 12
IN2 = 13
IN3 = 20
IN4 = 21
CE0 = 8
CE1 = 7


# Sets all the pins stated above as outputs
chan_list_out = [servo, ENA,ENB,IN1,IN2,IN3,IN4]
chan_list_in = [CE0,CE1]
GPIO.setup(chan_list_out,GPIO.OUT)
GPIO.setup(chan_list_in,GPIO.IN)



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
	global servoAngle
	global maxLightAngle
	maxLight = 0

	with picamera.PiCamera() as camera:
	    camera.resolution = (128, 80)
	    
	    while(servoAngle < 100):
	    	ServoAngle(servoAngle)

	    	with picamera.array.PiRGBArray(camera) as stream:
	        	camera.exposure_mode = 'auto'
	        	camera.awb_mode = 'auto'
	        	camera.capture(stream, format='rgb')
	        	pixAverage = int(np.average(stream.array[...,1]))
			
			
			if (pixAverage > maxLight):
				maxLight = pixAverage
				maxLightAngle = servoAngle

			servoAngle += 5
	    	
			
			
	print("Light Meter pixAverage=%i" % pixAverage, maxLight, maxLightAngle)


def faceLight():
	global servoAngle
	global maxLightAngle

	lPrev = 0
	lCnt = 0
	rPrev = 0
	rCnt = 0
	pivotAmount = 0
	rCurr = 0
	lCurr = 0
	direction = 0

	p2.start(25)
	p3.start(25)

	if (maxLightAngle < 55):
		pivotRight()
		direction = 0
		    
	elif (maxLightAngle > 55):
		pivotLeft()
		direction = 1
		maxLightAngle = maxLightAngle - 55


	# Pivots about 45 degrees
	if(maxLightAngle == 15):
		if (direction == 1):
			pivotAmount = 1
		else:
			pivotAmount = 5

	# Pivots about 35 degrees
	elif(maxLightAngle >= 16 and maxLightAngle <= 25):
		if (direction == 1):
			pivotAmount = 2
		else:
			pivotAmount = 4

	# Pivots about 25 degrees
	elif(maxLightAngle >= 26 and maxLightAngle <= 35):
		pivotAmount = 3

	# Pivots about 15 degrees
	elif(maxLightAngle >= 36 and maxLightAngle <= 45):
		if (direction == 1):
			pivotAmount = 4
		else:
			pivotAmount = 2

	# Pivots about 5 degrees
	elif(maxLightAngle >= 46):
		if (direction == 1):
			pivotAmount = 5
		else:
			pivotAmount = 1
	
	
	

	while (rCnt < pivotAmount):
		rCurr = GPIO.input(CE0)
		lCurr = GPIO.input(CE1)
		
		if(rCurr == 1 and rPrev == 0):
			rCnt += 1
		rPrev = rCurr
		if(lCurr == 1 and lPrev == 0):
			lCnt += 1
		lPrev = lCurr

	print("lTicks: ", lCnt, " pivotAmount: ", pivotAmount, "\n")
	print("rTicks: ", rCnt, " pivotAmount: ", pivotAmount, "\n")
	stop()
### ************************************************************************* ###

# Creates object "p1", sets frequency to 50 Hz, starts at 0% duty cycle
p1 = GPIO.PWM(servo,50)
p1.start(0)

p2 = GPIO.PWM(ENA,50)
#p2.start(24.7)

p3 = GPIO.PWM(ENB,50)
#p3.start(25)




    	










#time.sleep(.5)

findLight()
faceLight()







# Cleans up resources
p1.stop()
GPIO.cleanup()