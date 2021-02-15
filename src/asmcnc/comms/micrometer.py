# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 10:21:18 2019

module for digital dial indicator (cheap noname Aliexpress micrometer, 25mm/0.001mm)

usage example: 

import micrometer
DTI = micrometer.micrometer("COM3")
reading = DTI.read_mm() # returns measured distance in millimiters in float format (accuracy up to first 3 decimal points)

"""


# ################################ setup DTI  ################################ 

import time
import serial
import threading
DTI_COM_DEFAULT = "COM5"


class micrometer(object):
    """
    Class to support reading from DIT

    """
    def __init__(self, addr=DTI_COM_DEFAULT):

        self.stop_threads = False
        self.result_mm = 0
        self.init_serial(addr)
        self.connected = False


    def init_serial(self, DTI_COM = DTI_COM_DEFAULT):        

        # Open serial port
        self.dti_serial = serial.Serial(DTI_COM, 9600)
 
        time.sleep(.1)   # Wait for initialize

        # start receiving thread
        self.SerialRxthread = threading.Thread(target=self.read_from_port)
        self.SerialRxthread.start()
        time.sleep(.1)   # Wait for initialize
        self.dti_serial.flushInput()  # Flush startup text in serial input        

        
    def read_mm(self):
        return self.result_mm


    # core read response thread
    def read_from_port(self):
        while True:
            if (self.stop_threads == True): 
                break

            try:
                dti_bytes = self.dti_serial.read_until(b'\r',20) # Wait for response with carriage return
            except:
                print('DTI read_until ERROR')                
            
            try:
                self.result_mm = int(dti_bytes[1:2]+dti_bytes[3:9])*0.001
            except:
                #print('DTI decode ERROR')                
                pass
                
# ################################ setup micrometer ################################ 


