#coding=utf-8

import servo
from time import sleep
import RPi.GPIO as GPIO
import servo

def rotate_to(position,big,small):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(big, GPIO.OUT)
    GPIO.setup(small, GPIO.OUT)
    #servo.angle90small(small)
    if position==0:
        servo.angle0(big)
        servo.angle180small(small)
        servo.angle90small(small)
        servo.angle135(big)
    elif position==1:
        servo.angle90(big)
        servo.angle180small(small)
        servo.angle90small(small)
        servo.angle135(big)
    elif position==2:
        servo.angle180(big)
        servo.angle180small(small)
        servo.angle90small(small)
        servo.angle135(big)
    elif position==3:
        servo.angle270(big)
        servo.angle180small(small)
        servo.angle90small(small)
        servo.angle135(big)
    GPIO.cleanup()
    
if __name__ == '__main__':
    rotate_to(3,27,17)