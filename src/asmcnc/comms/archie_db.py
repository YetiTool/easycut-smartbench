from kivy.clock import Clock
import json, pika, socket, datetime

def log(message):
    timestamp = datetime.datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))

class SQLRabbit:
    def __init__(self, screen_manager, machine):
        self.queue = 'machine_data'
        # Updated these variables to match convention throughout rest of code
        self.m = m
        self.sm = sm
        
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue)
        
        except Exception as e:
            log("Pika connection exception: " + str(e))
        
        self.interval = 10
        
        Clock.schedule_interval(self.run, self.interval)
        
    def get_data(self):
        z_lube_limit_hrs = self.m.time_to_remind_user_to_lube_z_seconds/3600
        z_lube_used_hrs = self.m.time_since_z_head_lubricated_seconds/3600
        z_lube_hrs_left = round(z_lube_limit_hrs - z_lube_used_hrs, 2)
        z_lube_percent_used = round((z_lube_used_hrs/z_lube_limit_hrs)*100, 2) # This was percentage left, not percentage used
    
        # spindle brush
        spindle_brush_limit_hrs = self.m.spindle_brush_lifetime_seconds/3600
        spindle_brush_used_hrs = self.m.spindle_brush_use_seconds/3600
        spindle_brush_hrs_left = round(spindle_brush_limit_hrs - spindle_brush_used_hrs, 2)
        spindle_brush_percent_used = round((spindle_brush_used_hrs/spindle_brush_limit_hrs)*100, 2) # This was percentage left, not percentage used
    
        # calibration
        calibration_limit_hrs = self.m.time_to_remind_user_to_calibrate_seconds/3600
        calibration_used_hrs = self.m.time_since_calibration_seconds/3600
        calibration_hrs_left = round(calibration_limit_hrs - calibration_used_hrs, 2)
        calibration_percent_used = round((calibration_used_hrs/calibration_limit_hrs)*100, 2) # This was percentage left, not percentage used
        
        data = [
            {
                "payload_type": "full",
                "machine_info": {
                    "name": self.m.device_label,
                    "location": "Office" or '',
                    "hostname": socket.gethostname()
                },
                "statuses": {
                    "status": self.m.s.m_state,
                    "file_name": self.sm.get_screen('go').job_name_only or '',
                    "overload_peak": float(self.sm.get_screen('go').overload_peak) or '',
    
                    "job_time": self.sm.get_screen('go').time_taken_seconds or '',
                    "job_percent": self.sm.get_screen('go').percent_thru_job or 0.0,
                    "job_name": self.sm.get_screen('go').job_name_only or '',
    
                    "z_lube_%_thru": z_lube_percent_used,
                    "z_lube_hrs_before_next": z_lube_hrs_left,
    
                    "spindle_brush_%_thru": spindle_brush_percent_used,
                    "spindle_brush_hrs_before_next": spindle_brush_hrs_left,
    
                    "calibration_%_thru": calibration_percent_used,
                    "calibration_hrs_before_next": calibration_hrs_left,
                    
                    "gcode_line": self.m.s.g_count or 0
                },
                "events": {
                    "placeholder": ""
                },
                "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]
        
        return data
        # except:
        #     data = [
        #         {
        #             "payload_type": "semi",
        #             "machine_info": {
        #                 "name": self.m.device_label,
        #                 "location": "Office",
        #                 "hostname": socket.gethostname()
        #             },
        #             "statuses": {
        #                 "status": self.m.s.m_state,
        #                 "z_lube_%_thru": z_lube_percent_used,
        #                 "z_lube_hrs_before_next": z_lube_hrs_left,
        #                 "spindle_brush_%_thru": spindle_brush_percent_used,
        #                 "spindle_brush_hrs_before_next": spindle_brush_hrs_left,
        #                 "calibration_%_thru": calibration_percent_used,
        #                 "calibration_hrs_before_next": calibration_hrs_left,
        #                 "gcode_line": self.m.s.g_count
        #             },
        #             "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #         }
        #     ]
        
    ###    
    ### Don't send data unless machine is running job - old data from job end will
    ### will still be relevant.
    ###   
     
    def run(self, dt):
        # if self.m.s.m_state != "Idle":
        #     return 
        try: self.channel.basic_publish(exchange='', routing_key=self.queue, body=json.dumps(self.get_data()))
        except Exception as e: log("Data send exception: " + str(e))
        log(self.get_data())
        