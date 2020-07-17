#!/bin/bash
pkill -f main.py
sleep 5

# this uses the default bt port - needs changing in PL before can be automated. 
# also need to create a standard location to find the hex file - currently this is just a dummy.
# might need to rewrite this script each time for new hex file. 
avrdude -patmega2560 -cwiring -P/dev/ttyAMA0 -b115200 -D -Uflash:w:/media/usb/GRBL*.hex:i