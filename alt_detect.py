#!/usr/bin/python
from scipy import ndimage
from scipy.misc import imsave
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import time
#import picamera

# variables and things that don't change
START_TIME = int(round(time.time() * 1000.0)) # in ms
BTWN_PHOTOS = 1000 # ms
PCNT_PHOTO_DETECTED = 14400 # 1600x900 * 1% of the image
current_photo_num = 1

# detection on image 
# image is a filename, and rgb is a ndarray (np.array) of rgb values normalized to 1 for gray
# or a '#aabbcc' value
def detect(image, rgb):
    # ndarray, rgb colors
    im = ndimage.imread(image)
    im_unit = np.array(im/255, dtype='float32')
    im_unit -= rgb
    im_unit *= im_unit
    im_unit -= 0.05 # 5 percent variance
    whr = np.where(im_unit<0)
    plt.imshow(im_unit)
    plt.imshow("detected1")
    if (len(whr[0]<0) > PCNT_PHOTO_DETECTED or len(whr[1]<0) > PCNT_PHOTO_DETECTED or len(whr[2]<0) > PCNT_PHOTO_DETECTED):
        print(whr[0])
        print(im_unit[0])
        for i in range(len(whr[0])):
            im_unit[whr[0]][i] = 255
            im_unit[1][i] = 255
            im_unit[2][i] = 255
        imsave("detected" + str(current_photo_num), im_unit, format="png")
    plt.show()

def capture_store_detect_label():
#    camera = PiCamera(resolution=(1600,900))
#    camera.capture("photo" + str(current_photo_num))
    current_photo_num += 1
    # red
    # blue
    # green

# test
detect('minor.jpg', np.array([[[0.9373, 0.9373, 0.9373]]], dtype='float32'))

# loop
while True:
    current_time = int(round(time.time() * 1000.0)) # in ms
    elapsed = current_time - START_TIME # ms
    if elapsed >= BTWN_PHOTOS:
        capture_store_detect_label()
