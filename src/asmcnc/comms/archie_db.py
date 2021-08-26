from kivy.clock import Clock
import json, socket, datetime

def log(message):
    timestamp = datetime.datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))

class SQLRabbit:
    def __init__(self, screen_manager, machine):
        try:
            import pika
        except:
            log("Couldn't import pika lib")


        self.queue = 'machine_data'
        # Updated these variables to match convention throughout rest of code
        self.m = machine
        self.sm = screen_manager
        self.jd = self.m.jd
        
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters('51.89.232.215', 5672, '/', pika.credentials.PlainCredentials('console', '2RsZWRceL3BPSE6xZ6ay9xRFdKq3WvQb')))
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
        z_lube_percent_left = round((z_lube_hrs_left/z_lube_limit_hrs)*100, 2) # This was percentage left, not percentage used
    
        # spindle brush
        spindle_brush_limit_hrs = self.m.spindle_brush_lifetime_seconds/3600
        spindle_brush_used_hrs = self.m.spindle_brush_use_seconds/3600
        spindle_brush_hrs_left = round(spindle_brush_limit_hrs - spindle_brush_used_hrs, 2)
        spindle_brush_percent_left = round((spindle_brush_hrs_left/spindle_brush_limit_hrs)*100, 2) # This was percentage left, not percentage used
    
        # calibration
        calibration_limit_hrs = self.m.time_to_remind_user_to_calibrate_seconds/3600
        calibration_used_hrs = self.m.time_since_calibration_seconds/3600
        calibration_hrs_left = round(calibration_limit_hrs - calibration_used_hrs, 2)
        calibration_percent_left = round((calibration_hrs_left/calibration_limit_hrs)*100, 2) # This was percentage left, not percentage used
        print(json.dumps(self.jd.metadata_dict))
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

                    "z_lube_%_left": z_lube_percent_left,
                    "z_lube_hrs_before_next": z_lube_hrs_left,
    
                    "spindle_brush_%_left": spindle_brush_percent_left,
                    "spindle_brush_hrs_before_next": spindle_brush_hrs_left,
    
                    "calibration_%_left": calibration_percent_left,
                    "calibration_hrs_before_next": calibration_hrs_left,

                    "file_name": self.jd.filename or '',
                    "job_time": self.sm.get_screen('go').time_taken_seconds or '',
                    "gcode_line": self.m.s.g_count or 0,
                    "job_percent": self.sm.get_screen('go').percent_thru_job or 0.0,
                    "overload_peak": float(self.sm.get_screen('go').overload_peak) or 0.0
                },
                "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]
        
        return data

    #0 - info
    #1 - warning
    #2 - critical
    def send_event(self, event_severity, event_name, event_description):
        data = [
            {
                "payload_type": "event",
                "machine_info": {
                    "hostname": socket.gethostname()
                },
                "event": {
                    "severity": event_severity,
                    "name": event_name,
                    "description": event_description
                },
                "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]

        try:
            self.channel.basic_publish(exchange='', routing_key=self.queue, body=json.dumps(data))
        except Exception as e:
            log("Event send exception: " + str(e))
        log(str(data))

    #send payload containing all data
    def send_full_payload(self):
        try:
            self.channel.basic_publish(exchange='', routing_key=self.queue, body=json.dumps(self.get_data()))
        except Exception as e:
            log("Data send exception: " + str(e))
        log(self.get_data())

    #send alive 'ping' to server
    def send_alive(self):
        data = [
            {
                "payload_type": "alive",
                "machine_info": {
                    "hostname": socket.gethostname()
                },
                "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]

        try:
            self.channel.basic_publish(exchange='', routing_key=self.queue, body=json.dumps(data))
        except Exception as e:
            log("Data send exception: " + str(e))
        log(data)

    def run(self, dt):
        if self.m.s.m_state == "Idle":
            self.send_alive()
        else:
            self.send_full_payload()
