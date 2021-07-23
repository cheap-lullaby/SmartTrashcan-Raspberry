import time
import RPi.GPIO as GPIO
import os
import numpy
from picamera import PiCamera, Color
from time import sleep
from fractions import Fraction
from classifier import classify, print_time
from rotate import rotate_to
import imageenhancement
from utils import *

demoCamera = PiCamera()


def main():
    while True:
        # do_something()
        GPIO.setmode(GPIO.BCM)  # 使用BCM编码方式
        # 定义引脚
        GPIO_OUT1 = 4
        GPIO.setwarnings(False)
        GPIO.setup(GPIO_OUT1, GPIO.IN)
        #guangminled.main()
        if GPIO.wait_for_edge(GPIO_OUT1, GPIO.FALLING):
            os.system('sudo python3 /home/pi/Desktop/SmartTrashcan/guangminled.py')
            print('Garbage detected!')
            print_time()
            sleep(1)
            demoCamera.resolution = (224, 224)  # 设置摄像头的分辨率
            demoCamera.capture('photo.jpg')  # 拍下并保存一张照片
            os.system("xdg-open photo.jpg")
            result=classify()
            position = result[0]
            prediction=result[1]          
            reliability = round(result[2],4)
            bm = BaseInformation(basePath)
            logger = MyLogger(bm.basePath + r'/utils/log_classify.txt', "client_logger2")
            logger.log_info('Prediction: '+prediction+'\tScore: '+str(reliability))

            db = DataBase()
            
            cmd = "INSERT INTO CLASSIFY(TIME,CLIENT_ID,RESULT,RELIABLITY) VALUES(now(),'%s','%s','%s');" % (
                bm.get_client_ID(), prediction, reliability)
            db.execute(cmd)

            rotate_to(position, 27, 17)
    GPIO.cleanup()
