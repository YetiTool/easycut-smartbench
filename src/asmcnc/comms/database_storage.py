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
if sys.platform != 'win32':
    from influxdb import InfluxDBClient # database lib

def log(message):
    timestamp = datetime.datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))


class DatabaseStorage(object):

    # SETUP

    # Configure database (InfluxDB) connection variables
    
    def __init__(self):

        host = "localhost"  # RasPi
        port = 8086  # default port
        user = "sensor"  # the user/password created for the pi, with write access
        password = "sensor" 
        dbname = "sensor_data"  # the database we created earlier
        interval = 5  # Sample period in seconds
    
        # Create the InfluxDB client object
        self.client = InfluxDBClient(host, port, user, password, dbname)
        self.hostname = "SmartBench_0005" #TODO this needs to be serialised based on unique ID of SB console
        self.sw_branch = "flurry_poc1" #TODO this is just an example of how we could track what SW we're running which is sending the data


    def set_value(self, name, value):

        # Create the JSON data structure
        log(name, value)

        data = [
            {
                "measurement": self.hostname,
                "tags": {
                    "sw_branch": "test",
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
 
