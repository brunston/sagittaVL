#!/usr/bin/python
from scipy import ndimage
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
    im_hsv = colors.rgb_to_hsv(im_unit)
    hsv = colors.rgb_to_hsv(rgb)
    im_unit -= rgb
    im_hsv -= hsv
    print(im_hsv)
    im_unit *= im_unit
    im_hsv *= im_hsv
    im_unit -= 0.05
    im_hsv -= 0.05 # 5 percent variance
    plt.imshow(im_hsv)
    plt.show()
    print(len(np.where(im_unit<0)[0]), len(np.where(im_unit<0)[1]))
    plt.imshow(im_unit)
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
