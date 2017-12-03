import RPi.GPIO as  GPIO
import picamera
import picamera.array
import time
import numpy as np

servo = 22 # azimuth, side to side

angle = 0 # starting angle for servo1


with picamera.PiCamera() as camera:
    camera.resolution = (128, 80)
   
    while(1):
    	with picamera.array.PiRGBArray(camera) as stream:
        	camera.exposure_mode = 'auto'
        	camera.awb_mode = 'auto'
        	camera.capture(stream, format='rgb')
        	pixAverage = int(np.average(stream.array[...,1]))
		print ("Light Meter pixAverage=%i" % pixAverage)

#