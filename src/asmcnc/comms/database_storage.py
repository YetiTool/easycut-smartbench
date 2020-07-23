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

    
    sw_branch = "flurry_poc1" #TODO this is just an example of how we could track what SW we're running which is sending the data
    machine_id = "SmartBench_0007" #TODO this needs to be serialised based on unique ID of SB console
    
    # LOCAL DB
    localDBClient = None
    
    # PIPE TO REMOTE DB
    channel = None
    remote_hostname = "flurry.yetitool.com"
    
    
    def __init__(self):

        
        ### INTIALISE LOCAL DB
        
        local_hostname = "localhost"  # RasPi
        port = 8086  # default port
        user = "sensor"  # the user/password created for the pi, with write access
        password = "sensor" 
        dbname = "sensor_data"  # the database we created earlier
        interval = 5  # Sample period in seconds
    
        try:
            # Ansible may not have pre-installed this
            from influxdb import InfluxDBClient # database lib
            self.localDBClient = InfluxDBClient(local_hostname, port, user, password, dbname)
            log("Local db intialised.")

        except:
            log("Unable to initialise local database. Have libs been installed? Or check DatabaseStorage credentials?")

        
        ### INTIALISE PIPE TO REMOTE DB
        
        try:
            # Ansible may not have pre-installed this
            import pika

            # LOCAL CONNECTION
#             connection = pika.BlockingConnection(
#                 pika.ConnectionParameters(host='localhost'))

            # REMOTE CONNECTION
            # TODO: Fix this - GUEST IS NOT SECURE
            # Set the connection parameters to connect to rabbit-server1 on port 5672
            # on the / virtual host using the username "guest" and password "guest"
            credentials = pika.PlainCredentials('guest', 'guest')
            parameters = pika.ConnectionParameters(self.remote_hostname,
                                                   5672,
                                                   '/',
                                                   credentials)
            connection = pika.BlockingConnection(parameters)
            
            self.channel = connection.channel()
            log("Channel to remote db intialised.")
            
        except:
            log("Unable to create pipe to remote database. Have libs been installed? Or check DatabaseStorage credentials?")

                

    def spindle_on(self):
        self.record_value("spindle_on_off", 1)


    def spindle_off(self):
        self.record_value("spindle_on_off", 0)


    def record_value(self, name, value):

        if self.localDBClient != None:
            self._record_in_local_db(name, value)
            
        if self.channel != None:
            self._send_to_remote_db(name, value)
  
    
    def _record_in_local_db(self, name, value):
        
        # Create the JSON data structure
        log(str(name) + ": " + str(value))

        data = [
            {
                "measurement": self.machine_id,
                "tags": {
                    "source": self.sw_branch,
                },
                "time": datetime.datetime.now(),
                "fields": {
                    name: float(value)
                }
            }
        ]
        
        # Send the JSON data to InfluxDB
        self.localDBClient.write_points(data)    
        
        
    def _send_to_remote_db(self, name, value):
        
        message = "time:" + str(datetime.datetime.now()) + "|machineID:" + self.machine_id + "|" + name + ":" + str(value)

        self.channel.queue_declare(queue='machine_status_1')
        
        log("Sending: " + message)
        self.channel.basic_publish(exchange='', routing_key='machine_status_1', body=message)
#         connection.close()
