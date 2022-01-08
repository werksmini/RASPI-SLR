#!/bin/sh

xset s noblank
xset s off
xset -dpms

cd ~/RASPI-SLR
sudo python3 ./stream_server.py &

/usr/bin/chromium-browser --noerrdialogs --disable-infobars --kiosk https://localhost:8000/ &
