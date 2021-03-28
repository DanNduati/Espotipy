import machine,time
import urequests as requests
import ujson
import wifi
import ssd1306
import framebuf

i2c = machine.I2C(scl = machine.Pin(22),sda=machine.Pin(21))
display =ssd1306.SSD1306_I2C(128,64,i2c)

def clearScreen():
    display.fill(0)
    display.show()

def handleOverflow(text,x,y):
    length = 16
    if (len(text)<=length and x==0):
        display.text(text,x,y)
    else:
        #handle overflow cases
        charBuffer=length-len(text)
        #non zero starting point with ovf
        if (len(text)>charBuffer):
            fl = text[:length]
            display.text(fl,x,y)
            sl = text[length:]
            display.text(sl,x,y+10)
        else:#non zero sp with no ovf
            display.text(text,x,y)

def initialize():
    display.fill(0)
    display.text("Initializing...",0,0)
    handleOverflow("Connecting to Wifi",0,10)
    wifi.connect()
    if (wifi.connect()):
        handleOverflow("Connected succesfully to wifi",0,30)
    else:
        HandleOverflow("Error trying to connect",0,30)
    display.show()

def getPlaying():
    #get current playing track on spotify
    #hard coded token for now until the shitty authcode route working
    accessToken="BQC3ug77I3tlTwgdwdJY2BGZVbCe38JCy9WjFaLK3_vqf76z5JaJBk0UW5ijtdu2Dwys9ZmzgfMaqJeh9Z8EgAwgNJtbEQeWHnVVF2xjlSux6E1TSgyWZvMPQVyo_CGw-nRAD4sTzjr6uEsQg8FJ9U0hgKgLgXO9u9nyVWfJ2S7tm5kbirv4ItBSlus"
    url ="https://api.spotify.com/v1/me/player/currently-playing"
    headers = {"Content-type":'application/json',"Authorization":' Bearer '+str(accessToken)+''}
    response = requests.get(url,headers=headers)
    data = response.json()
    #print(data)
    return data

def drawUi(songTitle,artists):
    clearScreen()
    display.fill(0)
    display.rect(0,0,128,64,1)
    display.text("ESPotify",35,7)
    display.line(0,20,128,20,1)
    handleOverflow(songTitle,10,25)
    handleOverflow(artists,1,40)
    display.show()


#get song title and artist
def getData(payload):
    artists = []
    songTitle = ""
    songTitle = payload['item']['name']
    wasanii = payload['item']['artists']
    for i in range(len(wasanii)):
        artists.append(wasanii[i]['name'])
    drawUi(songTitle,str(artists))
    print("Dan is currently listening to: " +songTitle +" By: "+ str(artists))


initialize()
time.sleep(2)
clearScreen()
while True:
    getData(getPlaying())
    time.sleep(5)
#spotify logo
"""
with open('logo.pbm','rb') as f:
    f.readline()
    f.readline()
    f.readline()
    data = bytearray(f.read())
fbuf = framebuf.FrameBuffer(data,128,64,framebuf.MONO_HLSB)
#display.invert(1)
#display.blit(fbuf,0,0)
"""
def sliderPage(progress_ms,duration_ms):
    clearScreen()
    display.fill(0)
    display.rect(0,0,128,64,1)
    display.text("ESPotify",35,7)
    display.line(0,20,128,20,1)
    display.line(10,40,118,40,1)
    #min sec conv for the 2 parameters
    #display parameters on both ends of slider
    #animate the slider

