#!/bin/sh

cd /home/pi/RASPI-SLR
sudo python3 ./stream_server.py

#export DISPLAY=:0
#./kiosk.sh &

#/usr/bin/chromium-browser --noerrdialogs --disable-infobars --kiosk http://localhost:8000 &
#/usr/bin/chromium-browser --noerrdialogs --disable-infobars --kiosk https://www.adafruit.com &
