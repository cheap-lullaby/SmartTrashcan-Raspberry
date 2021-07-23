import time
import RPi.GPIO as GPIO
from time import sleep
import os
from gpiozero import LED



def jianman():
    # 检测垃圾箱是否装满
    GPIO.setmode(GPIO.BCM)
    GPIO_OUT2 = 24
    GPIO_OUT3 = 13
    GPIO_OUT4 = 25
    led = LED(26)
    GPIO.setwarnings(False)
    GPIO.setup(GPIO_OUT2, GPIO.IN)
    GPIO.setup(GPIO_OUT3, GPIO.IN)
    GPIO.setup(GPIO_OUT4, GPIO.IN)
    if GPIO.input(GPIO_OUT2) == 0 or GPIO.input(GPIO_OUT3) == 0 or GPIO.input(GPIO_OUT4) == 0:  # 当有障碍物（即垃圾已满时）时，传感器输出低电平，所以检测低电平
        led.on()
        time.sleep(1)
        a = True
    else:
        led.off()
        time.sleep(1)
        a=False
    return a

    

if __name__ == '__main__':
    while True:
        jianman()