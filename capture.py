# Capturing photos for processing by target_detection.py
# Contributors: Brunston Poon

from picamera import PiCamera
from fractions import Fraction
from time import sleep

camera = PiCamera(resolution=(1640,1232)))
i = 0
for filename in camera.capture_continuous('img{counter:03d}'):
    sleep(5)
    i += 1
    if i > 540: #45 minutes of photos
        break
