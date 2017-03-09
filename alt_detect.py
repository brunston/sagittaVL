from scipy import ndimage
import numpy as np

def blober(image, rgb):
    # ndarray, rgb colors
    im = ndimage.imread('minor.jpg')
    print(im)
    print(im.shape)
    print(rgb.shape)
    print(rgb[0])
    im -= rgb
    print(im)

blober(np.array([]), np.array([[[239,239,239]]], dtype='uint8'))
