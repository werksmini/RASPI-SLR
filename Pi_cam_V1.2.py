from picamera import PiCamera           #picamera library
import os                               #required as this is root?
import digitalio                        #
import board                            
from PIL import Image, ImageDraw        #pillow library
#import ST7789 as ST7789                 #old library
import adafruit_rgb_display.st7789 as st7789

from io import BytesIO
from PIL import Image, ImageDraw, ImageOps      #duplicate?

from gpiozero import Button             #simple interface to GPIO devices

from datetime import datetime
from time import sleep

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 80000000

sav_loc = os.path.dirname(os.path.realpath(__file__))

triggerBtn = Button(23)
batteryLow = Button(24)

# Old display setup
#disp = ST7789.ST7789(
#    port=0,
#    cs=1,
#    dc=9,
#    backlight=19,
#    spi_speed_hz= 80 * 1000 * 1000
#)

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=240,
    height=240,
    x_offset=0,
    y_offset=0,
    rotation=0,
)

#disp.image()

def preview(mode):    
    temp_img = BytesIO()
    with PiCamera() as cam:
        if (mode == 1):
            cam.zoom = (0.4,0.4,0.2,0.2)
        for foo in cam.capture_continuous(temp_img, format='jpeg',resize = (240, 180)): #240x180 for Screen, 240 width, 180 height to keep aspect ratio of original picture (actually calculates 240x179.88)   
            temp_img.truncate()
            temp_img.seek(0)
            image = Image.open(temp_img)
           # image= ImageOps.expand(image, (0,0,0,60),0) #add bar at bottom of screen, black

            if (batteryLow.is_pressed == True):
            	batteryWarning = 'red'
            else:
                batteryWarning = 'black'
            #image= ImageOps.expand(image, (0,60,0,0),fill=batteryWarning) #add bar at top of screen, black
            
            disp.image(image)
            
            temp_img.seek(0)
            
            if ((mode==0) and (triggerBtn.is_pressed == True)):
                return(1)
            elif ((mode==1) and (triggerBtn.is_pressed == False)):
                return(2)     
            

while True:
    if preview(0)==1:
        if preview(1)==2:
            with PiCamera() as cam:
                time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
                cam.capture(sav_loc+"/camera_"+ time +".jpg")
                image = Image.open(sav_loc+"/camera_"+ time +".jpg")
                #image = image.resize((240, 180))
                #image = ImageOps.expand(image, (0,0,0,0),0)
            
                disp.image(image)
                sleep(5)
            
        
        


