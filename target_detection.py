import picamera
import time
import numpy as np
from PIL import Image

def RGBtoHSV(pixel):
	rgbprime = [i / 255 for i in pixel]
	cmax = max(rgbprime)
	cmin = min(rgbprime)
	hsvpixel[0] = calcHue(rgbprime, cmax, cmin)
	hsvpixel[1] = calcSat(cmax, cmin)
	hsvpixel[2] = calcVal(cmax)
	return hsvpixel

def calcHue(prime, cMax, cMin):
	delta = cMax - cMin
	if delta == 0:
		return 0
	elif cMax == prime[0]:
		return 60 * (((prime[1] - prime[2]) / delta) % 6)
	elif cMax == prime[1]:
		return 60 * (((prime[2] - prime[0]) / delta) + 2)
	elif cMax == prime[2]:
		return 60 * (((prime[0] - prime[1]) / delta) + 4)
	else
		print("Error in hue calculation.")
		return 0

def calcSat(cMax, cMin):
	delta = cMax - cMin
	if cMax == 0:
		return 0
	else:
		return delta / cMax

def calcVal(cMax):
	return cMax

def withinXPercent(a, b, x):
	"""Returns true if b is within x% of a."""
	return abs((b - a) / a) == x / 100

def search(img, values, range, chunk):
	"""Searches an image for chunks of the specified HSV values (within range %) of 
	minimum size chunk x chunk pixels"""
	imgArray = np.array(img)
	for row in range(len(imgArray)):
		for col in range(len(row)):
			pix = RGBtoHSV(imgArray[row, col])
			for value in values:
				if all([withinXPercent(value[i], pix[i], range) for i in range(3)]):
					return True, [row, col]
	return False, [0, 0]
