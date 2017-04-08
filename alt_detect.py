#!/usr/bin/python
from scipy import ndimage
from scipy.misc import imsave
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import time
import picamera
import os
# contributors: Brunston Poon, Dinesh Parimi

# variables and things that don't change
START_TIME = int(round(time.time() * 1000.0)) # in ms
BTWN_PHOTOS = 1000 # ms
PCNT_PHOTO_DETECTED = 14400 # 1600x900 * 1% of the image
ONE = np.array([[[0, 0.1255, 0.3569]]], dtype='float32')
TWO = np.array([[[ 1, 0.8196, 0]]], dtype='float32')
THREE = np.array([[[0.6510, 0.0353, 0.2392]]], dtype='float32')

current_photo_num = 1

# detection on image 
# image is a filename, and rgb is a ndarray (np.array) of rgb values normalized to 1 for gray
# or a '#aabbcc' value
def detect(image, rgb):
    # ndarray, rgb colors
    print("detecting " + str(current_photo_num))
    im = ndimage.imread(image)
    im_unit = np.array(im/255, dtype='float32')
    im_unit -= rgb
    im_unit *= im_unit
    im_unit -= 0.05 # 5 percent variance
    whr = np.where(im_unit<0)
    if (len(whr[0]<0) > PCNT_PHOTO_DETECTED or len(whr[1]<0) > PCNT_PHOTO_DETECTED or len(whr[2]<0) > PCNT_PHOTO_DETECTED):
        for i in range(len(whr[0])):
            im_unit[whr[0][i]][whr[1][i]][0] = 255
            im_unit[whr[0][i]][whr[1][i]][1] = 255
            im_unit[whr[0][i]][whr[1][i]][2] = 255
        imsave("detected" + str(current_photo_num), im_unit, format="png")
        os.remove("photosmall" + str(current_photo_num) + ".jpg")
    else:
        os.remove("photo" + str(current_photo_num) + ".jpg")
    
    plt.show()

def capture_store_detect_label():
    global current_photo_num
    camera = picamera.PiCamera(resolution=(1600,900))
    camera.capture("photo" + str(current_photo_num) + ".jpg", format="jpeg")
    camera.capture("photosmall" + str(current_photo_num) + ".jpg", resize=(400,225), format="jpeg")
    print("capturing photos " + str(current_photo_num))
    detect("photo" + str(current_photo_num) + ".jpg", ONE)
    detect("photo" + str(current_photo_num) + ".jpg", TWO)
    detect("photo" + str(current_photo_num) + ".jpg", THREE)
    current_photo_num += 1

# test
#detect('minor.jpg', np.array([[[0.9373, 0.9373, 0.9373]]], dtype='float32'))

# loop
while True:
    current_time = int(round(time.time() * 1000.0)) # in ms
    elapsed = current_time - START_TIME # ms
    if elapsed >= BTWN_PHOTOS:
        capture_store_detect_label()
