pkill -f main.py
#sleep 5
at now + 5 seconds avrdude -C/home/pi/easycut-smartbench/src/avrdude_gpio.conf -patmega2560 -cwiring -P/dev/ttyS0 -b115200 -D -Uflash:w:/home/pi/easycut-smartbench/src/GRBL104.hex:i