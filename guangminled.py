#-*- coding: UTF-8 -*-   
import time
import board
import neopixel
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pixel_pin = board.D18
num_pixels = 1
ORDER = neopixel.GRB
tilt=19
GPIO.setup(tilt, GPIO.IN)
br=GPIO.input(tilt)
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=br, auto_write=False,pixel_order=ORDER)

if br==1:
    pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=br, auto_write=False,pixel_order=ORDER)
    pixels.fill((255, 255, 255))
    pixels.show()
else:
    pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=br, auto_write=False,pixel_order=ORDER)
    pixels.fill((0,0,0))
    pixels.show()
