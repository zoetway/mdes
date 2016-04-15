## edit /boot/config.txt to add framebuffer_depth=24 to render image with SimpleCV correctly

from SimpleCV import *

cam = Camera()

while True:
    img = cam.getImage()
    faces = img.findHaarFeatures('/home/pi/PythonProjects/haarcascade_frontalface_alt.xml');                           
    if faces:
        for face in faces:
            face.draw()
    img.show()
