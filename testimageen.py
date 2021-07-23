#-*- coding: UTF-8 -*-   
import imageenhancement
import time
start =time.clock()

path='photo.jpg'
imageenhancement.imageenhance(path)

end = time.clock()
print('Running time: %s Seconds'%(end-start))