#coding=utf-8
import servo
from time import sleep
import RPi.GPIO as GPIO
import servo
import PIL

GPIO.setmode(GPIO.BOARD)

GPIO.setwarnings(False)

big = 13
small = 11

GPIO.setup(big, GPIO.OUT)
GPIO.setup(small, GPIO.OUT)
#servo.angle90small(small)



servo.angle180small(small)
servo.angle90small(small)

#servo.angle



GPIO.cleanup()


