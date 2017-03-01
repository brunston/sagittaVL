# Checking images for the tarp HSV values
# Contributors: Nate Young, Brunston Poon

#import picamera
import time
import numpy as np
from PIL import Image
from colorsys import rgb_to_hsv

def withinXPercent(a, b, x): # Returns true if b is within x% of a.
	return abs(b - a) <= x / 100

def randomSearch(img, values, tolerance, chunk):
    imgArray = np.array(img)
    searchRow = np.random.choice(len(imgArray), 11) # for 1080px, ~96px even spacing
    searchCol = np.random.choice(len(imgArray[0]), 20) # 1920, 96px even
    for row in searchRow:
        for col in searchCol:
            pix = rgb_to_hsv(*[c/255 for c in imgArray[row, col]])
            if all([withinXPercent(values[i], pix[i], tolerance) for i in range(3)]):
                return True, [row, col]
    return False, [0, 0]

def search(img, values, tolerance, chunk):
	"""Searches an image for chunks of the specified HSV values (within tolerance %) of 
	minimum size chunk x chunk pixels"""
	imgArray = np.array(img)
	for row in range(0, len(imgArray), chunk):
		for col in range(0, len(imgArray[row]), chunk):
			pix = rgb_to_hsv(*[c/255 for c in imgArray[row, col]])
			if all([withinXPercent(values[i], pix[i], tolerance) for i in range(3)]):
				return True, [row, col]
	return False, [0, 0]
