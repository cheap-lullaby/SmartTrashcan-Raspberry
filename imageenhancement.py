#-*- coding: UTF-8 -*-   
 
from PIL import Image
from PIL import ImageEnhance
 
#原始图像
#image = Image.open('D:\dark.jpg')
#image.show()
def imageenhance(path):
    #亮度增强
    image = Image.open(path)
    enh_bri = ImageEnhance.Brightness(image)
    brightness = 3.0
    image_brightened = enh_bri.enhance(brightness)
    #image_brightened.show()
    #色度增强
    enh_col = ImageEnhance.Color(image_brightened)
    color = 2.7
    image_colored = enh_col.enhance(color)
    #image_colored.show()
    #对比度增强
    enh_con = ImageEnhance.Contrast(image_colored)
    contrast = 2.5
    image_contrasted = enh_con.enhance(contrast)
    #image_contrasted.show()
    #锐度增强
    enh_sha = ImageEnhance.Sharpness(image_contrasted)
    sharpness = 4.5
    image_sharped = enh_sha.enhance(sharpness)
    image_sharped.show()

