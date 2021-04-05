'''
Created on 31 Jan 2018
@author: Ed
Reporting to Flurry server
'''

from kivy.clock import Clock
import sys, os
import os.path
from os import path
import time
import datetime
import json
import socket 

def log(message):
    timestamp = datetime.datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))

pika_lib_import_ok = False

try:
    # Safety to ensure that the `pika` lib exists on the platform (non-standard platform lib, therfore this module is dependent on platform update)
    import pika
    pika_lib_import_ok = True    
except:
    log("Couldn't import pika lib - has it been installed on platform? To install: python -m pip install pika --upgrade")


class DatabaseStorage(object):

    
    rabbitMQ_connection = None
    remote_hostname = "flurry.yetitool.com"
    STATUS_POLL_INTERVAL = 10

    # REMOTE CONNECTION CREDS
    # TODO: Work to be done with security:
    # - Password needs to be a github secret
    # - User serverside needs to be securely setup, was granted excessive admin rights
    credentials = pika.PlainCredentials('tempAdmin', 'jtdBWr3G7Bc7qUyN')
    rabbitMQ_parameters = pika.ConnectionParameters(remote_hostname, 5672, '/', credentials)

    #TODO this is just an example of how we could track what SW we're running which is sending the data   
    sw_branch = "flurry_poc1" 


    def __init__(self, screen_manager, router_machine):

        # Excessive ;-)
        self.sm = screen_manager
        self.m = router_machine
        
        if pika_lib_import_ok: 
            
            self._test_remote_connection()
            Clock.schedule_interval(self._send_status_update_to_remote_db, self.STATUS_POLL_INTERVAL)


    def _test_remote_connection(self):
                      
        try:
            self.rabbitMQ_connection = pika.BlockingConnection(self.rabbitMQ_parameters)
            log("Flurry connection test: OK.")
            # OK, now we know it works, close it to prevent timeouts
            self.rabbitMQ_connection.close()
        except:
            log("Flurry connection test: failed.")

        

    def _send_status_update_to_remote_db(self, dt):

        try:        
            measurement_type = "sb1_status"
            
            # to prevent potential clash of identity, tag 'user's name for machine + machine's unique ID'
            device_label = self.m.device_label + " (" + socket.gethostname() + ")"
            
            # z lube
            z_lube_limit_hrs = self.m.time_to_remind_user_to_lube_z_seconds/3600
            z_lube_used_hrs = self.m.time_since_z_head_lubricated_seconds/3600
            z_lube_hrs_left = round(z_lube_limit_hrs - z_lube_used_hrs, 2)
            z_lube_percent_used = round((z_lube_hrs_left/z_lube_limit_hrs)*100, 2)
    
            # spindle brush
            spindle_brush_limit_hrs = self.m.spindle_brush_lifetime_seconds/3600
            spindle_brush_used_hrs = self.m.spindle_brush_use_seconds/3600
            spindle_brush_hrs_left = round(spindle_brush_limit_hrs - spindle_brush_used_hrs, 2)
            spindle_brush_percent_used = round((spindle_brush_hrs_left/spindle_brush_limit_hrs)*100, 2)
    
            # calibration
            calibration_limit_hrs = self.m.time_to_remind_user_to_calibrate_seconds/3600
            calibration_used_hrs = self.m.time_since_calibration_seconds/3600
            calibration_hrs_left = round(calibration_limit_hrs - calibration_used_hrs, 2)
            calibration_percent_used = round((calibration_hrs_left/calibration_limit_hrs)*100, 2)
        except:
            log("Unable to scrape date for Flurry msg.")
        
        # TODO: Warning - this won't handle simulateneous calls!!!! Needs a locking mechanism.
        try:    
            data = [
                {
                    "measurement": measurement_type,
                    "tags": {
                        "device_ID": device_label,
                    },
                    "fields": {
                        "machine_name": self.m.device_label,
                        "status": self.m.s.m_state,
                        "overload_peak": float(self.sm.get_screen('go').overload_peak),

                        "job_time": self.sm.get_screen('go').time_taken_seconds,
                        "job_percent": self.sm.get_screen('go').percent_thru_job,
                        "job_name": self.sm.get_screen('go').job_name_only,

                        "z_lube_%_thru": z_lube_percent_used,
                        "z_lube_hrs_before_next": z_lube_hrs_left,

                        "spindle_brush_%_thru": spindle_brush_percent_used,
                        "spindle_brush_hrs_before_next": spindle_brush_hrs_left,

                        "calibration_%_thru": calibration_percent_used,
                        "calibration_hrs_before_next": calibration_hrs_left,
                        
                        "gcode_line": self.m.s.g_count                   
                    }
                }
            ]

            message = json.dumps(data)
    
            self.rabbitMQ_connection = pika.BlockingConnection(self.rabbitMQ_parameters)
            channel = self.rabbitMQ_connection.channel()
            channel.queue_declare(queue='machine_status_1')
    
            log("Status ping: " + message)
            channel.basic_publish(exchange='', routing_key='machine_status_1', body=message)
            self.rabbitMQ_connection.close()

        except:
            log("Problem pinging status to Flurry." )
                

