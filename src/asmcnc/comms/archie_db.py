from kivy.clock import Clock
import json, socket, datetime


def log(message):
    timestamp = datetime.datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f')[:12] + ' ' + str(message))


class SQLRabbit:
    z_lube_percent_left_next = 50
    spindle_brush_percent_left_next = 50
    calibration_percent_left_next = 50
    initial_consumable_intervals_found = False

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
            self.connection = pika.BlockingConnection(pika.ConnectionParameters('51.89.232.215', 5672, '/',
                                                                                pika.credentials.PlainCredentials(
                                                                                    'console',
                                                                                    '2RsZWRceL3BPSE6xZ6ay9xRFdKq3WvQb')))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue)

        except Exception as e:
            log("Pika connection exception: " + str(e))

        self.interval = 10

        Clock.schedule_interval(self.run, self.interval)

    def get_data(self):
        z_lube_limit_hrs = self.m.time_to_remind_user_to_lube_z_seconds / 3600
        z_lube_used_hrs = self.m.time_since_z_head_lubricated_seconds / 3600
        z_lube_hrs_left = round(z_lube_limit_hrs - z_lube_used_hrs, 2)
        z_lube_percent_left = round((z_lube_hrs_left / z_lube_limit_hrs) * 100,
                                    2)  # This was percentage left, not percentage used

        # spindle brush
        spindle_brush_limit_hrs = self.m.spindle_brush_lifetime_seconds / 3600
        spindle_brush_used_hrs = self.m.spindle_brush_use_seconds / 3600
        spindle_brush_hrs_left = round(spindle_brush_limit_hrs - spindle_brush_used_hrs, 2)
        spindle_brush_percent_left = round((spindle_brush_hrs_left / spindle_brush_limit_hrs) * 100,
                                           2)  # This was percentage left, not percentage used

        # calibration
        calibration_limit_hrs = self.m.time_to_remind_user_to_calibrate_seconds / 3600
        calibration_used_hrs = self.m.time_since_calibration_seconds / 3600
        calibration_hrs_left = round(calibration_limit_hrs - calibration_used_hrs, 2)
        calibration_percent_left = round((calibration_hrs_left / calibration_limit_hrs) * 100,
                                         2)  # This was percentage left, not percentage used

        # Set initial values for the next percentage interval so that it doesn't go through each interval every time
        if not self.initial_consumable_intervals_found:
            self.find_initial_consumable_intervals(z_lube_percent_left, spindle_brush_percent_left,
                                                   calibration_percent_left)

        # Check if consumables have passed thresholds for sending events
        self.check_consumable_percentages(z_lube_percent_left, spindle_brush_percent_left, calibration_percent_left)

        file_name = self.jd.job_name

        data = [
            {
                "payload_type": "full",
                "machine_info": {
                    "name": self.m.device_label,
                    "location": self.m.device_location,
                    "hostname": socket.gethostname(),
                    "ec_version": self.m.sett.sw_version
                },
                "statuses": {
                    "status": "Run",

                    "z_lube_%_left": z_lube_percent_left,
                    "z_lube_hrs_before_next": z_lube_hrs_left,

                    "spindle_brush_%_left": spindle_brush_percent_left,
                    "spindle_brush_hrs_before_next": spindle_brush_hrs_left,

                    "calibration_%_left": calibration_percent_left,
                    "calibration_hrs_before_next": calibration_hrs_left,

                    "file_name": file_name or '',
                    "job_time": self.sm.get_screen('go').time_taken_seconds or '',
                    "gcode_line": self.m.s.g_count or 0,
                    "job_percent": self.jd.percent_thru_job or 0.0,
                    "overload_peak": float(self.sm.get_screen('go').overload_peak) or 0.0
                },
                "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]

        return data

    def find_initial_consumable_intervals(self, z_lube_percent, spindle_brush_percent, calibration_percent):

        def find_current_interval(value):
            # This looks stupid but I don't have a better idea without using loops
            if value < 50:
                if value < 25:
                    if value < 10:
                        if value < 5:
                            if value < 0:
                                if value < -10:
                                    return -25
                                return -10
                            return 0
                        return 5
                    return 10
                return 25
            return 50

        self.z_lube_percent_left_next = find_current_interval(z_lube_percent)
        self.spindle_brush_percent_left_next = find_current_interval(spindle_brush_percent)
        self.calibration_percent_left_next = find_current_interval(calibration_percent)

        self.initial_consumable_intervals_found = True

    def check_consumable_percentages(self, z_lube_percent, spindle_brush_percent, calibration_percent):
        # The next percentage to set the threshold to once one has been passed
        next_percent_dict = {50: 25, 25: 10, 10: 5, 5: 0, 0: -10, -10: -25, -25: -25}
        # The severity that passing each percentage corresponds to
        severity_dict = {50: 0, 25: 1, 10: 1, 5: 2, 0: 2, -10: 2, -25: 2}
        # The percentage that was last passed, used to check whether the percentage has increased
        previous_percent_dict = {50: 50, 25: 50, 10: 25, 5: 10, 0: 5, -10: 0, -25: -10}

        if z_lube_percent < self.z_lube_percent_left_next:
            self.send_event(severity_dict[self.z_lube_percent_left_next], 'Z-lube percentage left',
                            'Z-lube percentage passed below ' + str(self.z_lube_percent_left_next) + '%')
            self.z_lube_percent_left_next = next_percent_dict[self.z_lube_percent_left_next]

        if spindle_brush_percent < self.spindle_brush_percent_left_next:
            self.send_event(severity_dict[self.spindle_brush_percent_left_next], 'Spindle brush percentage left',
                            'Spindle brush percentage passed below ' + str(self.spindle_brush_percent_left_next) + '%')
            self.spindle_brush_percent_left_next = next_percent_dict[self.spindle_brush_percent_left_next]

        if calibration_percent < self.calibration_percent_left_next:
            self.send_event(severity_dict[self.calibration_percent_left_next], 'Calibration percentage left',
                            'Calibration percentage passed below ' + str(self.calibration_percent_left_next) + '%')
            self.calibration_percent_left_next = next_percent_dict[self.calibration_percent_left_next]

        # In case any percentages somehow increased past their previous threshold
        if z_lube_percent > previous_percent_dict[self.z_lube_percent_left_next] or spindle_brush_percent > \
                previous_percent_dict[self.spindle_brush_percent_left_next] or calibration_percent > \
                previous_percent_dict[self.calibration_percent_left_next]:
            self.find_initial_consumable_intervals(z_lube_percent, spindle_brush_percent, calibration_percent)

    def send_job_end(self, job_name, successful):

        # Send production notes here as well, from self.jd.production_notes

        data = [
            {
                "payload_type": "job_end",
                "machine_info": {
                    "hostname": socket.gethostname()
                },
                "job_data": {
                    "job_name": job_name,
                    "successful": successful,
                    "production_notes": self.jd.production_notes
                },
                "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]

        try:
            self.channel.basic_publish(exchange='', routing_key=self.queue, body=json.dumps(data))
        except Exception as e:
            log("Event send exception: " + str(e))
        log(str(data))

        self.jd.post_job_data_update_post_send()


    def send_job_start(self, job_name, metadata_dict):

        data = [
            {
                "payload_type": "job_start",
                "machine_info": {
                    "hostname": socket.gethostname()
                },
                "job_data": {
                    "job_name": job_name,
                    "job_start": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                },
                "metadata": {

                },
                "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]

        data[0]["metadata"] = metadata_dict

        try:
            self.channel.basic_publish(exchange='', routing_key=self.queue, body=json.dumps(data))
        except Exception as e:
            log("Event send exception: " + str(e))
        # log(str(data))

    # 0 - info
    # 1 - warning
    # 2 - critical
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
        # log(str(data))

    # send payload containing all data
    def send_full_payload(self):
        try:
            self.channel.basic_publish(exchange='', routing_key=self.queue, body=json.dumps(self.get_data()))
        except Exception as e:
            log("Data send exception: " + str(e))
        # log(self.get_data())

    # send alive 'ping' to server
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
