import network
import time

SSID = "dan"
PASSWORD = "dandandandan"

def conn(ssid,pwd):
    wlan = network.WLAN(network.STA_IF) #create a station interface
    #check if the board is already connected
    if wlan.isconnected() == False:
        print("connecting to network...")
        wlan.active(True)
        wlan.connect(ssid,pwd)
    while not wlan.isconnected():
        pass
    print(wlan.ifconfig())
    print("Connected succesfuly to ",ssid)
    return(wlan.isconnected())
def connect():
    return(conn(SSID,PASSWORD))
    #print('connected successfully')
