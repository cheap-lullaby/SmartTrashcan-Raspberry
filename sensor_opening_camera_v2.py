import time
from fractions import Fraction

import RPi.GPIO as GPIO
import os
from picamera import PiCamera, Color
from time import sleep

GPIO.setmode(GPIO.BCM)  # 使用BCM编码方式

# 定义引脚
GPIO_OUT1 = 23
# GPIO_OUT2 = 24
# GPIO_OUT3 = 18
# GPIO_OUT4 = 12
# GPIO_OUT5 = 21
# led = 7

# 设置引脚为输入和输出
GPIO.setwarnings(False)
# 设置23针脚为输入，接到红外避障传感器模块的out引脚
GPIO.setup(GPIO_OUT1, GPIO.IN)
# GPIO.setup(GPIO_OUT2, GPIO.IN)
# GPIO.setup(GPIO_OUT3, GPIO.IN)
# GPIO.setup(GPIO_OUT4, GPIO.IN)
# GPIO.setup(GPIO_OUT5, GPIO.IN)
# GPIO.setup(led, GPIO.OUT)


# def warn():  # 亮灯来作为垃圾装满时发出的警告
#     time.sleep(0.5)
#     GPIO.output(led, GPIO.HIGH)


while True:
    # if GPIO.input(GPIO_OUT2) == 0 or GPIO.input(GPIO_OUT3) == 0 or GPIO.input(GPIO_OUT4) == 0 or \
    #         GPIO.input(GPIO_OUT5) == 0:  # 当有障碍物（即垃圾已满时）时，传感器输出低电平，所以检测低电平
    #     warn()
    # else:
    #     time.sleep(0.01)
    #     GPIO.output(led, GPIO.LOW)
        if GPIO.input(GPIO_OUT1) == 0:
            with PiCamera() as demoCamera:
                demoCamera.resolution = (800, 575)
                # 设置帧率为1/6fps,然后将曝光时间设置为6秒
                # 最后将iso参数设置为800
                demoCamera.framerate = Fraction(1, 6)
                demoCamera.shutter_speed = 6000000
                demoCamera.exposure_mode = 'off'
                demoCamera.iso = 800
                # 给摄像头一个比较长的预热时间，让摄像头尽可能的适应周围的光线
                # 你也可以试试开启AWB【自动白平衡】来代替长时间的预热
                sleep(10)
                # 最后捕捉图像，因为我们将曝光时间设置为6秒，所以拍摄的时间比较长
                demoCamera.capture('/home/pi/Desktop/photo.jpg')  # 拍下并保存一张照片
                demoCamera.stop_preview()  # 关闭摄像头预览
GPIO.cleanup()