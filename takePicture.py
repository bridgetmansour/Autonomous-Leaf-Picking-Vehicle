from picamera import PiCamera
from time import sleep

camera = PiCamera()

for i in range (1):
    camera.start_preview(3)
    camera.capture('/home/pi/Desktop/currentPic' + i + '.jpg')
    camera.stop_preview(3)