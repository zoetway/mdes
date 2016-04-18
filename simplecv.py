## edit /boot/config.txt to add framebuffer_depth=24 to render image with SimpleCV correctly

from SimpleCV import Camera

import requests

cam = Camera()

url = "https://api.projectoxford.ai/emotion/v1.0/recognize"
key = "223b5e0b1a5843188b55e2e744798b4a"
maxNumberRetries = 10

def processRequest(json, data, headers):
    retries = 0
    result = None

    while True:
        response = requests.request( 'post', url, json=json, data=data, headers = headers, params = None)

        if response.status_code == 429:
            print'message: %s' %(response.json()['error']['message'])
        elif response.status_code == 200 or response.status_code == 201:
            if 'content-length' in response.headers and int(response.headers['content-length']) == 0:
                result = None
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str):
                if 'application/json' in response.headers['content-type'].lower():
                    result = response.json() if response.content else None 
                elif 'image' in response.headers['content-type'].lower():
                    result = response.content
        else:
            print'Error code: %d' % (response.status_code)
            print'Message: %s' % (response.json()['error']['message'])
        break
    return result

##while True:
##    print("Searching for faces...")
##    
##    img = cam.getImage()
##    faces = img.findHaarFeatures('/home/pi/PythonProjects/haarcascade_frontalface_alt.xml');                           
##
##    if faces:
##        for face in faces:
##            print("Found your face!")
##            img.save("/home/pi/Pictures/face.jpeg")
#            face.draw() #draws green face indicator
#    img.show() #draws camera image
print'done'

pathToFileOnDisk = '/home/pi/Pictures/face.jpeg'
with open(pathToFileOnDisk, 'rb') as f:
    data=f.read()

headers = dict()
headers['Ocp-Apim-Subscription-Key']=key
headers['Content-Type']='application/octet-stream'

json = None

result = processRequest(json, data, headers)

##for currFace in result:
##    print'face found'
print(result)
