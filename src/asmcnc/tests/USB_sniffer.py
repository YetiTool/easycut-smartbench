port_1 = 'COM5'
port_2 = 'COM4'
BAUD_RATE = 115200

import serial, sys, time, string, threading
from datetime import datetime


s_1 = serial.Serial(port_1, BAUD_RATE, timeout = 0.05, writeTimeout = 1)
s_2 = serial.Serial(port_2, BAUD_RATE, timeout = 1, writeTimeout = 1)

while True:

    print(str(datetime.now() )+ ' Port 1: ' + str(s_1.readline().strip()))
    print(str(datetime.now()) + ' Port 2: ' + str(s_2.readline().strip()))


