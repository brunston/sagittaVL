# Capturing photos for processing by target_detection.py
# Contributors: Brunston Poon

from picamera import PiCamera
from fractions import Fraction

camera = PiCamera(resolution=(1640,1232)), framerate=Fraction(1,10))



