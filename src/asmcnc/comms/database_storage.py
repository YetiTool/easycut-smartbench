'''
Created on 31 Jan 2018
@author: Ed
This module defines the machine's properties (e.g. travel), services (e.g. serial comms) and functions (e.g. move left)
'''

from asmcnc.comms import serial_connection  # @UnresolvedImport
from kivy.clock import Clock
import sys, os
import os.path
from os import path
import time
import datetime

from __builtin__ import True
from kivy.uix.switch import Switch
from pickle import TRUE

def log(message):
    timestamp = datetime.datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))


class DatabaseStorage(object):


    client = None
    hostname = "SmartBench_0006" #TODO this needs to be serialised based on unique ID of SB console
    sw_branch = "flurry_poc1" #TODO this is just an example of how we could track what SW we're running which is sending the data
    
    
    def __init__(self):

        host = "localhost"  # RasPi
        port = 8086  # default port
        user = "sensor"  # the user/password created for the pi, with write access
        password = "sensor" 
        dbname = "sensor_data"  # the database we created earlier
        interval = 5  # Sample period in seconds
    
        try:
            # Ansible may not have pre-installed this
            from influxdb import InfluxDBClient # database lib
            self.client = InfluxDBClient(host, port, user, password, dbname)

        except:
            print "Unable to initialise Flurry database. Have libs been installed? Or check DatabaseStorage credentials?"


    def spindle_on(self):
        self.set_value("spindle_on_off", 1)


    def spindle_off(self):
        self.set_value("spindle_on_off", 0)


    def set_value(self, name, value):

        if self.client != None:

            # Create the JSON data structure
            log(str(name) + ": " + str(value))
    
            data = [
                {
                    "measurement": self.hostname,
                    "tags": {
                        "sw_branch": self.sw_branch,
                        "grbl": "whatever"
                    },
                    "time": datetime.datetime.now(),
                    "fields": {
                        "value": value
                    }
                }
            ]
            
            # Send the JSON data to InfluxDB
            self.client.write_points(data)      
     
