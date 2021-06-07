import machine,time
import urequests as requests
import ujson
import wifi
import ssd1306
import framebuf

i2c = machine.I2C(scl = machine.Pin(22),sda=machine.Pin(21))
display =ssd1306.SSD1306_I2C(128,64,i2c)

p=''
d=''
page = 0
prevState = 0
"""
def pageCounter(Pin):
    global page
    page +=1
    global InterruptPin #interrupt -> 14

pageBtn =machine.Pin(14,machine.Pin.IN)
pageBtn.irq(trigger=machine.Pin.IRQ_RISING,handler=pageCounter)
"""
pageBtn =machine.Pin(14,machine.Pin.IN)

def clearScreen():
    display.fill(0)
    display.show()

def sliderPage(xPos):
    clearScreen()
    display.fill(0)
    display.rect(0,0,128,64,1)
    display.text("ESPotipy",35,7)
    display.line(0,20,128,20,1)
    display.line(10,30,118,30,1)
    #display.text("pos %f"%(sliderPos),)
    display.line(int(xPos+10),28,int(xPos+10),32,1)
    #dislay the progress and duration time
    display.text(p,10,60)
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
    accessToken="BQABvOP6V5thmCp7NboLOjKY9J1q9gRdKK5_16C8Dt6atzwtw4cExP6Wu4puPlzBfDma-CNZzV1gegxIwy8FE8Ws2h85f5WEQeWRJxfqkEZmJivhGSXTm5WdImeQssG6E2QXqiIlvI1Qd9SHVuYDr-WDnbHRhBYpMHN7nfnm1C14UXFEtgUfVhrGLZVmm74"
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
    display.text("ESPotipy",35,7)
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

def convTime(duration):
    #duration is in ms
    sec = (duration/1000)%60
    minutes = (duration/(1000*60))%60
    #print("%d:%d"%(minutes,sec))
    return [minutes,sec]

def getSliderPos(payload):
    sliderLength = 108 
    progressMs = float(payload['progress_ms'])
    durationMs = float(payload['item']['duration_ms'])
    #convert to min:sec
    d = convTime(durationMs)
    p = convTime(progressMs)
    #print("The progress: %d and the duration %d:"%(progressMs,durationMs))
    #get slider pos %
    sliderPos = float((progressMs*100)/durationMs);
    sliderX = float((sliderPos*sliderLength)/100)
    print("Slider Pos: %d sliderX: %d"%(sliderPos,sliderX))
    return sliderX
#page functions
def dispMain():
    getData(getPlaying())
    #time.sleep(1)

def dispSlider():
    sliderPos = getSliderPos(getPlaying())
    sliderPage(sliderPos)
    #time.sleep(1)


initialize()
time.sleep(1)
clearScreen()

while True:
    #getData(getPlaying())
    #sliderPos = getSliderPos(getPlaying())
    #sliderPage(sliderPos)
    #time.sleep(0.5)
    print(page)
    if((pageBtn.value())==0):
        dispMain()
        print("main page");
    else:
        print("slider page");
        dispSlider()
