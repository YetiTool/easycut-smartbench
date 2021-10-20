from kivy.clock import Clock
import json, socket, datetime
from requests import get
import threading
from time import sleep

def log(message):
    timestamp = datetime.datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f')[:12] + ' ' + str(message))

try:
    import pika
except:
    log("Couldn't import pika lib")


class DatabaseEventManager():

    z_lube_percent_left_next = 50
    spindle_brush_percent_left_next = 50
    calibration_percent_left_next = 50
    initial_consumable_intervals_found = False

    VERBOSE = True

    public_ip_address = ''

    routine_updates_channel = None
    routine_update_thread = None

    def __init__(self, screen_manager, machine, settings_manager):

        self.queue = 'machine_data'
        # Updated these variables to match convention throughout rest of code
        self.m = machine
        self.sm = screen_manager
        self.jd = self.m.jd
        self.set = settings_manager

    def __del__(self):

        log("Database Event Manager closed - garbage collected!")

    
    ## SET UP CONNECTION TO DATABASE
    # This is called from screen_welcome, when all connections are set up
    ##------------------------------------------------------------------------

    def start_connection_to_database_thread(self):

        self.start_get_public_ip_address_thread()        

        initial_connection_thread = threading.Thread(target=self.set_up_pika_connection)
        initial_connection_thread.daemon = True
        initial_connection_thread.start()


    def set_up_pika_connection(self):

        log("Try to set up pika connection")

        while True:

            if self.set.wifi_available:

                try:
                    self.connection = pika.BlockingConnection(pika.ConnectionParameters('sm-receiver.yetitool.com', 5672, '/',
                                                                                        pika.credentials.PlainCredentials(
                                                                                            'console',
                                                                                            '2RsZWRceL3BPSE6xZ6ay9xRFdKq3WvQb')))
                    
                    
                    try:
                        if self.routine_updates_channel is None:
                            self.routine_updates_channel = self.connection.channel()
                            self.routine_updates_channel.queue_declare(queue=self.queue)

                        elif self.routine_updates_channel.is_closed:
                            self.routine_updates_channel.open()

                    except:
                        try: 
                            self.routine_updates_channel.close()
                        except: 
                            pass
                        
                        self.routine_updates_channel = None
                        self.routine_updates_channel = self.connection.channel()
                        self.routine_updates_channel.queue_declare(queue=self.queue)


                    try: 
                        if not self.routine_update_thread.is_alive(): self.send_routine_updates_to_database()
                    except: 
                        self.send_routine_updates_to_database()
                    break


                except Exception as e:
                    log("Pika connection exception: " + str(e))
                    sleep(10)

            else:
                sleep(10)

    def reinstate_channel_or_connection_if_missing(self):

        log("Attempt to reinstate channel")

        if self.connection.is_closed:
            self.set_up_pika_connection()

        elif self.routine_updates_channel.is_closed:
            try:
                self.routine_updates_channel = self.connection.channel()
                self.routine_updates_channel.queue_declare(queue=self.queue)

            except:
                log("connection not closed, but could not set up channel")

        else: 

            try: 
                self.connection.close()
                self.set_up_pika_connection()

            except:
                sleep(10)
                self.reinstate_channel_or_connection_if_missing()

    ## MAIN LOOP THAT SENDS ROUTINE UPDATES TO DATABASE
    ##------------------------------------------------------------------------
    def send_routine_updates_to_database(self):

        def do_routine_update_loop():

            while True:

                if self.set.wifi_available:

                    if self.VERBOSE: log("Doing ma routine checksss")

                    try:
                        if self.m.s.m_state == "Idle":
                            self.send_alive()
                        else:
                            self.send_full_payload()

                    except Exception as e:
                        if self.VERBOSE: 
                            log("Could not send routine update:")
                            log(str(e))


                sleep(10)

        self.routine_update_thread = threading.Thread(target=do_routine_update_loop)
        self.routine_update_thread.daemon = True
        self.routine_update_thread.start()


    ## PUBLISH EVENT TO DATABASE
    ##------------------------------------------------------------------------
    def publish_event_with_routine_updates_channel(self, data, exception_type):

        if self.VERBOSE: log("Publishing data: " + exception_type)

        if self.set.wifi_available:

            try: 
                self.routine_updates_channel.basic_publish(exchange='', routing_key=self.queue, body=json.dumps(data))
                if self.VERBOSE: log(data)
            
            except Exception as e:
                if self.VERBOSE: log(exception_type + " send exception: " + str(e))
                self.reinstate_channel_or_connection_if_missing()


    def publish_event_with_temp_channel(self, data, exception_type):

        if self.VERBOSE: log("Publishing data: " + exception_type)

        if self.set.wifi_available:

            def nested_flurry_event_sender(data, exception_type):

                while self.set.wifi_available:
    
                    try: 
                        temp_event_channel = self.connection.channel()
                        temp_event_channel.queue_declare(queue=self.queue)

                        try: 
                            temp_event_channel.basic_publish(exchange='', routing_key=self.queue, body=json.dumps(data))
                            if self.VERBOSE: log(data)
                        
                        except Exception as e:
                            if self.VERBOSE: log(exception_type + " send exception: " + str(e))

                        temp_event_channel.close()
                        break

                    except: 
                        sleep(10)

            thread_for_send_event = threading.Thread(target=nested_flurry_event_sender, args=(data, exception_type))
            thread_for_send_event.daemon = True
            thread_for_send_event.start()


    ## ROUTINE EVENTS
    ##------------------------------------------------------------------------

    # send alive 'ping' to server when SmartBench is Idle
    def send_alive(self):
        data = {
                "payload_type": "alive",
                "machine_info": {
                    "name": self.m.device_label,
                    "location": self.m.device_location,
                    "hostname": self.set.console_hostname,
                    "ec_version": self.m.sett.sw_version,
                    "public_ip_address": get("https://api.ipify.org", timeout=2).content.decode("utf8")
                },
                "time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }


        self.publish_event_with_routine_updates_channel(data, "Data")


    # During a job, send full data about machine
    def send_full_payload(self):

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

        file_name = self.jd.filename.split("\\")[-1]

        data = {
                "payload_type": "full",
                "machine_info": {
                    "name": self.m.device_label,
                    "location": self.m.device_location,
                    "hostname": self.set.console_hostname,
                    "ec_version": self.m.sett.sw_version,
                    "public_ip_address": self.public_ip_address
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
                    "overload_peak": float(self.sm.get_screen('go').overload_peak) or 0.0,

                    "max_feed_rate_absolute": self.sm.get_screen('go').feed_rate_max_absolute or '',
                    "max_feed_rate_percentage": self.sm.get_screen('go').feed_rate_max_percentage or '',
                    "max_spindle_speed_absolute": self.sm.get_screen('go').spindle_speed_max_absolute or '',
                    "max_spindle_speed_percentage": self.sm.get_screen('go').spindle_speed_max_percentage or ''
                },
                "time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }


        self.publish_event_with_routine_updates_channel(data, "Data")


    ### PART OF SENDING FULL PAYLOAD

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
                            'Z-lube percentage passed below ' + str(self.z_lube_percent_left_next) + '%', 2)
            self.z_lube_percent_left_next = next_percent_dict[self.z_lube_percent_left_next]

        if spindle_brush_percent < self.spindle_brush_percent_left_next:
            self.send_event(severity_dict[self.spindle_brush_percent_left_next], 'Spindle brush percentage left',
                            'Spindle brush percentage passed below ' + str(self.spindle_brush_percent_left_next) + '%',
                            2)
            self.spindle_brush_percent_left_next = next_percent_dict[self.spindle_brush_percent_left_next]

        if calibration_percent < self.calibration_percent_left_next:
            self.send_event(severity_dict[self.calibration_percent_left_next], 'Calibration percentage left',
                            'Calibration percentage passed below ' + str(self.calibration_percent_left_next) + '%', 2)
            self.calibration_percent_left_next = next_percent_dict[self.calibration_percent_left_next]

        # In case any percentages somehow increased past their previous threshold
        if z_lube_percent > previous_percent_dict[self.z_lube_percent_left_next] or spindle_brush_percent > \
                previous_percent_dict[self.spindle_brush_percent_left_next] or calibration_percent > \
                previous_percent_dict[self.calibration_percent_left_next]:
            self.find_initial_consumable_intervals(z_lube_percent, spindle_brush_percent, calibration_percent)


    ## UNIQUE EVENTS
    ##------------------------------------------------------------------------

    ### BEGINNING AND END OF JOB
    def send_job_end(self, job_name, successful):

        data =  {
                "payload_type": "job_end",
                "machine_info": {
                    "name": self.m.device_label,
                    "location": self.m.device_location,
                    "hostname": self.set.console_hostname,
                    "ec_version": self.m.sett.sw_version,
                    "public_ip_address": self.public_ip_address
                },
                "job_data": {
                    "job_name": job_name,
                    "successful": successful,
                    "PostProductionNotes": self.jd.post_production_notes
                },
                "time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }


        self.publish_event_with_temp_channel(data, "Event")

        self.jd.post_job_data_update_post_send()

    def send_job_start(self, job_name, metadata_dict):
        data = {
                "payload_type": "job_start",
                "machine_info": {
                    "name": self.m.device_label,
                    "location": self.m.device_location,
                    "hostname": self.set.console_hostname,
                    "ec_version": self.m.sett.sw_version,
                    "public_ip_address": self.public_ip_address
                },
                "job_data": {
                    "job_name": job_name,
                    "job_start": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                "metadata": {

                },
                "time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        metadata_in_json_format = {k.translate(None, ' '): v for k, v in metadata_dict.iteritems()}

        data["metadata"] = metadata_in_json_format

        self.publish_event_with_temp_channel(data, "Event")


    ### FEEDS AND SPEEDS
    def send_spindle_speed_info(self):
        data = {
            "payload_type": "speed_info",
            "machine_info": {
                "name": self.m.device_label,
                "location": self.m.device_location,
                "hostname": self.set.console_hostname,
                "ec_version": self.m.sett.sw_version,
                "public_ip_address": self.public_ip_address
            },
            "speeds": {
                "spindle_speed": self.m.spindle_speed(),
                "spindle_percentage": self.sm.get_screen('go').speedOverride.speed_rate_label.text
            }
        }

        self.publish_event_with_temp_channel(data, "Spindle speed")


    def send_feed_rate_info(self):
        data = {
            "payload_type": "speed_info",
            "machine_info": {
                "name": self.m.device_label,
                "location": self.m.device_location,
                "hostname": self.set.console_hostname,
                "ec_version": self.m.sett.sw_version,
                "public_ip_address": self.public_ip_address
            },
            "feeds": {
                "feed_rate": self.m.feed_rate(),
                "feed_percentage": self.sm.get_screen('go').feedOverride.feed_rate_label.text,
            }
        }

        self.publish_event_with_temp_channel(data, "Feed rate")


    ### JOB CRITICAL EVENTS, INCLUDING ALARMS AND ERRORS

    # Severity
    # 0 - info
    # 1 - warning
    # 2 - critical

    # Type
    # 0 - errors
    # 1 - alarms
    # 2 - maintenance
    # 3 - job pause
    # 4 - job resume
    # 5 - job cancel
    # 6 - job start
    # 7 - job end

    def send_event(self, event_severity, event_description, event_name, event_type):
        data = {
                "payload_type": "event",
                "machine_info": {
                    "name": self.m.device_label,
                    "location": self.m.device_location,
                    "hostname": self.set.console_hostname,
                    "ec_version": self.m.sett.sw_version,
                    "public_ip_address": self.public_ip_address
                },
                "event": {
                    "severity": event_severity,
                    "type": event_type,
                    "name": event_name,
                    "description": event_description
                },
                "time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }


        self.publish_event_with_temp_channel(data, "Event")


    ## LOOP TO ROUTINELY CHECK IP ADDRESS

    def start_get_public_ip_address_thread(self):

        def do_ip_address_loop():

            while True:

                try: 
                    self.public_ip_address = get("https://api.ipify.org", timeout=2).content.decode("utf8")

                except:
                    self.public_ip_address = "Unavailable"


                sleep(600)

        ip_address_thread = threading.Thread(target=do_ip_address_loop)
        ip_address_thread.daemon = True
        ip_address_thread.start()







