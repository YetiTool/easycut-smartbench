from kivy.clock import Clock
import json, pika, socket, datetime

class SQLRabbit:
    def __init__(self, router, screen):
        self.queue = 'machine_data'
        self.router = router
        self.screen = screen
        
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)
        
        self.interval = 10
        
        Clock.schedule_interval(self.run, self.interval)
        
    def get_data(self):
        z_lube_limit_hrs = self.router.time_to_remind_user_to_lube_z_seconds/3600
        z_lube_used_hrs = self.router.time_since_z_head_lubricated_seconds/3600
        z_lube_hrs_left = round(z_lube_limit_hrs - z_lube_used_hrs, 2)
        z_lube_percent_used = round((z_lube_hrs_left/z_lube_limit_hrs)*100, 2)
    
        # spindle brush
        spindle_brush_limit_hrs = self.router.spindle_brush_lifetime_seconds/3600
        spindle_brush_used_hrs = self.router.spindle_brush_use_seconds/3600
        spindle_brush_hrs_left = round(spindle_brush_limit_hrs - spindle_brush_used_hrs, 2)
        spindle_brush_percent_used = round((spindle_brush_hrs_left/spindle_brush_limit_hrs)*100, 2)
    
        # calibration
        calibration_limit_hrs = self.router.time_to_remind_user_to_calibrate_seconds/3600
        calibration_used_hrs = self.router.time_since_calibration_seconds/3600
        calibration_hrs_left = round(calibration_limit_hrs - calibration_used_hrs, 2)
        calibration_percent_used = round((calibration_hrs_left/calibration_limit_hrs)*100, 2)
        
        data = [
            {
                "payload_type": "full",
                "machine_info": {
                    "name": self.router.device_label,
                    "location": "Office" or '',
                    "hostname": socket.gethostname()
                },
                "statuses": {
                    "status": self.router.s.m_state,
                    "file_name": self.screen.get_screen('go').job_name_only or '',
                    "overload_peak": float(self.screen.get_screen('go').overload_peak) or '',
    
                    "job_time": self.screen.get_screen('go').time_taken_seconds or '',
                    "job_percent": self.screen.get_screen('go').percent_thru_job or 0.0,
                    "job_name": self.screen.get_screen('go').job_name_only or '',
    
                    "z_lube_%_thru": z_lube_percent_used,
                    "z_lube_hrs_before_next": z_lube_hrs_left,
    
                    "spindle_brush_%_thru": spindle_brush_percent_used,
                    "spindle_brush_hrs_before_next": spindle_brush_hrs_left,
    
                    "calibration_%_thru": calibration_percent_used,
                    "calibration_hrs_before_next": calibration_hrs_left,
                    
                    "gcode_line": self.router.s.g_count or 0
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
        #                 "name": self.router.device_label,
        #                 "location": "Office",
        #                 "hostname": socket.gethostname()
        #             },
        #             "statuses": {
        #                 "status": self.router.s.m_state,
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
        # if self.router.s.m_state != "Idle":
        #     return 
        self.channel.basic_publish(exchange='', routing_key=self.queue, body=json.dumps(self.get_data()))
        