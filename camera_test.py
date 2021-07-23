import picamera
from time import sleep
import os

camera = picamera.PiCamera()
camera.resolution = (224, 224) 
#camera.brightness = 55
camera.capture('photo.jpg')
os.system("xdg-open photo.jpg")

