#!/bin/bash
pkill -f main.py
sleep 5
avrdude -patmega2560 -cwiring -P/dev/ttyAMA0 -b115200 -D -Uflash:w:/home/pi/GRBL107.hex:i