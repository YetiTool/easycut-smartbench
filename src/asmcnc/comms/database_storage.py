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
    
    # LOCAL DB
    localDBClient = None
    
    # PIPE TO REMOTE DB
    rabbitMQ_connection = None
    remote_hostname = "flurry.yetitool.com"
    STATUS_POLL_INTERVAL = 10
    
    def __init__(self, screen_manager, router_machine):

        self.sm = screen_manager
        self.m = router_machine

        
        ### INTIALISE PIPE TO REMOTE DB
        
#         try:
        # Ansible may not have pre-installed this, hence try the import
        import pika

        # LOCAL CONNECTION
#             rabbitMQ_connection = pika.BlockingConnection(
#                 pika.ConnectionParameters(host='localhost'))

        # REMOTE CONNECTION
        # TODO: Fix this - GUEST IS NOT SECURE
        # Set the rabbitMQ_connection parameters to connect to rabbit-server1 on port 5672
        # on the / virtual host using the username "" and password ""
        self.credentials = pika.PlainCredentials('tempAdmin', 'jtdBWr3G7Bc7qUyN')
        self.rabbitMQ_parameters = pika.ConnectionParameters(self.remote_hostname,
                                               5672,
                                               '/',
                                               self.credentials)
        
        
        self.rabbitMQ_connection = pika.BlockingConnection(self.rabbitMQ_parameters)
        log("Channel to remote db intialised.")

        # OK, now we know it works, close it to prevent timeouts
#         self.rabbitMQ_connection.close()
        
#         log("Preparing status poll to remote...")
#         Clock.schedule_once(db._start_status_poll,20)
#         except:
#             log("Unable to create pipe to remote database. Have libs been installed? Or check DatabaseStorage credentials?")
        Clock.schedule_interval(self.test_print,1)


    def _start_status_poll(self, dt):
        log("Starting status poll schedule.")
        Clock.schedule_interval(self._send_status_update_to_remote_db, self.STATUS_POLL_INTERVAL)

    def test_print(self):
        log("Interval print check")

    def _send_status_update_to_remote_db(self, dt):
        
        log("Attempting to poll now")
        # TODO: Warning - this won't handle simulateneous calls!!!! Needs a locking mechanism.
#         try:
        

        job_time = self.sm.get_screen('go').time_taken_seconds
        job_percent = self.sm.get_screen('go').percent_thru_job

        message = "time;" + str(datetime.datetime.now()) + "|machineID;" + self.m.device_label + "|job_time;" + str(job_time) + "|job_percent;" + str(job_percent)

#         import pika
        self.credentials = pika.PlainCredentials('tempAdmin', 'jtdBWr3G7Bc7qUyN')
        self.rabbitMQ_parameters = pika.ConnectionParameters(self.remote_hostname,
                                               5672,
                                               '/',
                                               self.credentials)    
        self.rabbitMQ_connection = pika.BlockingConnection(self.rabbitMQ_parameters)
        channel = self.rabbitMQ_connection.channel()
        channel.queue_declare(queue='machine_status_1')
        print "Polling..."

        log("Sending: " + message)
        channel.basic_publish(exchange='', routing_key='machine_status_1', body=message)
        self.rabbitMQ_connection.close()
#         except:
#             log("Problem sending to remote db:" )
                



#     def init_local_db(self):
#
#        ### INTIALISE LOCAL DB
#        
#         local_hostname = "localhost"  # RasPi
#         port = 8086  # default port
#         user = "sensor"  # the user/password created for the pi, with write access
#         password = "sensor" 
#         dbname = "sensor_data"  # the database we created earlier
#         interval = 5  # Sample period in seconds
#
#
#         try:
#             # Ansible may not have pre-installed this
#             from influxdb import InfluxDBClient # database lib
#             self.localDBClient = InfluxDBClient(local_hostname, port, user, password, dbname)
#             log("Local db intialised.")
# 
#         except:
#             log("Unable to initialise local database. Have libs been installed? Or check DatabaseStorage credentials?")


#     def spindle_on(self):
#         self.record_value("spindle_on_off", 1)
# 
# 
#     def spindle_off(self):
#         self.record_value("spindle_on_off", 0)
# 
# 
#     def record_value(self, name, value):
# 
#         if self.localDBClient != None:
#             self._record_in_local_db(name, value)
#             
#         if self.rabbitMQ_connection != None:
#             self._send_to_remote_db(name, value)
#   
#     
#     def _record_in_local_db(self, name, value):
#         
#         # Create the JSON data structure
#         log(str(name) + ": " + str(value))
# 
#         data = [
#             {
#                 "measurement": self.machine_id,
#                 "tags": {
#                     "source": self.sw_branch,
#                 },
#                 "time": datetime.datetime.now(),
#                 "fields": {
#                     name: float(value)
#                 }
#             }
#         ]
#         
#         # Send the JSON data to InfluxDB
#         self.localDBClient.write_points(data)    
#         
#         
#     def _send_to_remote_db(self, name, value):
#         
#         # TODO: Warning - this won't handle simulateneous calls!!!! Needs a locking mechanism.
# #         try:
#         message = "time;" + str(datetime.datetime.now()) + "|machineID;" + self.machine_id + "|" + name + ";" + str(value)
# 
#         import pika
#         self.credentials = pika.PlainCredentials('tempAdmin', 'jtdBWr3G7Bc7qUyN')
#         self.rabbitMQ_parameters = pika.ConnectionParameters(self.remote_hostname,
#                                                5672,
#                                                '/',
#                                                self.credentials)    
#         self.rabbitMQ_connection = pika.BlockingConnection(self.rabbitMQ_parameters)
#         channel = self.rabbitMQ_connection.channel()
#         channel.queue_declare(queue='machine_status_1')
#         log("Sending: " + message)
#         channel.basic_publish(exchange='', routing_key='machine_status_1', body=message)
#         self.rabbitMQ_connection.close()
# #         except:
# #             log("Problem sending to remote db:" )        

