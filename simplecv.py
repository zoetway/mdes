## edit /boot/config.txt to add framebuffer_depth=24 to render image with SimpleCV correctly

from SimpleCV import Camera
import operator
import requests
import datetime
import alsaaudio #import as per http://stackoverflow.com/questions/1936828/how-get-sound-input-from-microphone-in-python-and-process-it-on-the-fly
import audioop, time #maybe remove these later, example imports for audio

cam = Camera()

#Define header for JSON API Request
headers = dict()
headers['Ocp-Apim-Subscription-Key']= 'empty'
headers['Content-Type']='application/octet-stream'
url = "https://api.projectoxford.ai/emotion/v1.0/recognize"
maxNumberRetries = 10
json = None
imagePath = '/home/pi/Pictures/'

#Read M$ API Key from file
pathToKeyFile = '/home/pi/keys.txt'

#Create audio input device
inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK) 

# Set audio attributes: Mono, 8000 Hz, 16 bit little endian samples
inp.setchannels(1)
inp.setrate(8000)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
inp.setperiodsize(160)

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

file = open(pathToKeyFile, 'r')
headers['Ocp-Apim-Subscription-Key']=file.readline()

while True:
    print("Searching for faces...")
    print("And listening for sounds now too!")
    
    img = cam.getImage()
    faces = img.findHaarFeatures('/home/pi/PythonProjects/haarcascade_frontalface_alt.xml')                           

    if faces:
        for face in faces:
            print("Found your face!")

            d = datetime.datetime.now()
            fileName = d.strftime('%d-%m-%Y_%H:%M:%S')
            imageSavePath = imagePath + fileName + '.jpeg'
            img.save(imageSavePath)

            with open(imageSavePath, 'rb') as f:
                data=f.read()
                result = processRequest(json, data, headers)

                for currentFace in result:
                    currentEmotion = max(currentFace['scores'].iteritems(), key=operator.itemgetter(1))[0]
                print(result)
                print('Microsoft thinks your current emotion is: ' + currentEmotion)
    
    #start checking for audio on mic
    l,audioData = inp.read()
    if l:
        print audioop.max(data,2)
    
