
#coding=utf-8



from time import sleep

import RPi.GPIO as GPIO



def angle0(servo):#����ת135��

    pwm = GPIO.PWM(servo, 50)

    pwm.start(7)

    dutyCycle = 3

    pwm.ChangeDutyCycle(dutyCycle)

    sleep(1)

    pwm.stop()



def angle90(servo):#����ת45��

    pwm = GPIO.PWM(servo, 50)

    pwm.start(7)

    dutyCycle = 115 / 27. + 2

    pwm.ChangeDutyCycle(dutyCycle)

    sleep(1)

    pwm.stop()

    

def angle180(servo):#����������ת45��

    pwm = GPIO.PWM(servo, 50)

    pwm.start(7)

    dutyCycle = 200 / 27. + 2

    pwm.ChangeDutyCycle(dutyCycle)

    sleep(1)

    pwm.stop()

    

def angle270(servo):#����������ת135��

    pwm = GPIO.PWM(servo, 50)

    pwm.start(7)

    dutyCycle = 12.5

    pwm.ChangeDutyCycle(dutyCycle)

    sleep(1)

    pwm.stop()



def angle135(servo):#������λ

    pwm = GPIO.PWM(servo, 50)

    pwm.start(7)

    dutyCycle = 7

    pwm.ChangeDutyCycle(dutyCycle)

    sleep(1)

    pwm.stop()



def angle180small(servo):#С���ת��90��

    pwm = GPIO.PWM(servo, 50)

    pwm.start(7)

    dutyCycle = 11.6

    pwm.ChangeDutyCycle(dutyCycle)

    sleep(1)

    pwm.stop()

    

def angle90small(servo):#С�����λ

    pwm = GPIO.PWM(servo, 50)

    pwm.start(7)

    dutyCycle = 7

    pwm.ChangeDutyCycle(dutyCycle)

    sleep(1)

    pwm.stop()


