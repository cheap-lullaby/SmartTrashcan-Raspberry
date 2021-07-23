import time
import RPi.GPIO as GPIO
import os
from picamera import PiCamera, Color
from time import sleep
from fractions import Fraction

demoCamera = PiCamera()
GPIO.setmode(GPIO.BOARD)  # 使用BCM编码方式
# 定义引脚
GPIO_OUT1 = 7
#GPIO_OUT2 = 24
#led = 7
# 设置引脚为输入和输出
GPIO.setwarnings(False)
# 设置23针脚为输入，接到红外避障传感器模块的out引脚
GPIO.setup(GPIO_OUT1, GPIO.IN)
#GPIO.setup(GPIO_OUT2, GPIO.IN)
#GPIO.setup(led, GPIO.OUT)


# def warn():  # 亮灯来作为垃圾装满时发出的警告
#     time.sleep(0.5)
#     GPIO.output(led, GPIO.HIGH)


while True:
    # if GPIO.input(GPIO_OUT1) == 0:  # 当有障碍物（即垃圾已满时）时，传感器输出低电平，所以检测低电平
    #     warn()
    # else:
    #     time.sleep(0.01)
    #     GPIO.output(led, GPIO.LOW)
    if GPIO.input(GPIO_OUT1) == 0:
        demoCamera.start_preview()  # 打开摄像头预览
        demoCamera.annotate_background = Color('white')
        demoCamera.annotate_foreground = Color('red')
        demoCamera.brightness = 60
        #demoCamera.resolution = (224, 224)  # 设置摄像头的分辨率
        #demoCamera.framate = 60  # 设定摄像头的帧率
        sleep(0.5)  # 休息0.01秒
        demoCamera.capture('photo.jpg')  # 拍下并保存一张照片
        demoCamera.stop_preview()  # 关闭摄像头预览
        os.system("xdg-open photo.jpg")
        break
GPIO.cleanup()