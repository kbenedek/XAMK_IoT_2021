import picamera
from gpiozero import DistanceSensor
from time import sleep
sensor = DistanceSensor(23, 24)
camera = picamera.PiCamera()
camera.resolution= (640, 480)
i = 0
while True:
    if sensor.distance < 1.0:
        camera.capture("foo{i}.jpeg".format(i=i))
        i += 1
    sleep(1)
