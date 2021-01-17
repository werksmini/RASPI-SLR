from picamera import PiCamera                   #picamera library
import os                                       #allows command line instructions as well as .py - used here to assign save location to images
import digitalio                                #used to configure CS and CD pins in some adafruit examples, not sure what it's doing here
import board                                    #allows python to know what board this is and what pins it has
from PIL import Image, ImageDraw                #Python imaging library adds image processing capabilities to your Python interpreter.
import ST7789 as ST7789                         #ST7789 LCD screen library

from io import BytesIO                          #used in defining temp_img - unsure
from PIL import Image, ImageDraw, ImageOps      #redundant? just adds ImageOps

from gpiozero import Button                     #button library

from datetime import datetime                   #obvious library
from time import sleep                          #sleep function at end of while loop

sav_loc = os.path.dirname(os.path.realpath(__file__))

triggerBtn = Button(27)
batteryLow = Button(4)

disp = ST7789.ST7789(
    port=0,
    cs=1,
    dc=9,
    backlight=19,
    spi_speed_hz= 80 * 1000 * 1000
)

disp.begin()

def preview(mode):    
    temp_img = BytesIO()
    with PiCamera() as cam:
        if (mode == 1):
            cam.zoom = (0.4,0.4,0.2,0.2)
        for foo in cam.capture_continuous(temp_img, format='jpeg',resize = (240, 180)): #240x180 for Screen, 240 width, 180 height to keep aspect ratio of original picture (actually calculates 240x179.88)   
            temp_img.truncate()
            temp_img.seek(0)
            image = Image.open(temp_img)
            #image= ImageOps.expand(image, (0,0,0,60),0) #add bar at bottom of screen, black

            if (batteryLow.is_pressed == True):
            	batteryWarning = 'red'
            else:
                batteryWarning = 'black'
            image= ImageOps.expand(image, (0,60,0,0),fill=batteryWarning) #add bar at top of screen, black
            
            disp.display(image)
            
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
                cam.capture(sav_loc+"/Lego_"+ time +".jpg")
                image = Image.open(sav_loc+"/Lego_"+ time +".jpg")
                image = image.resize((240, 180))
                image = ImageOps.expand(image, (0,60,0,0),0)
            
                disp.display(image)
                sleep(5)
            
        
        


