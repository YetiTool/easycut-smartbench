from asmcnc.comms.logging_system.logging_system import Logger
from kivy.clock import Clock
import json, socket, datetime, time
from requests import get
import threading, queue
from time import sleep
import traceback

try:
    import pika
except:
    pika = None
    Logger.error("Couldn't import pika lib")


class DatabaseEventManager:
    z_lube_percent_left_next = 50
    spindle_brush_percent_left_next = 50
    calibration_percent_left_next = 50
    initial_consumable_intervals_found = False
    VERBOSE = False
    public_ip_address = ""
    routine_updates_channel = None
    routine_update_thread = None
    thread_for_send_event = None
    event_send_timeout = 5 * 60

    def __init__(self, screen_manager, machine, settings_manager):
        self.queue = "machine_data"
        self.m = machine
        self.sm = screen_manager
        self.jd = self.m.jd
        self.set = settings_manager
        self.event_queue = queue.Queue()

    def __del__(self):
        Logger.info("Database Event Manager closed - garbage collected!")

    def get_local_time(self):
        return datetime.datetime.now(self.set.timezone).strftime("%Y-%m-%d %H:%M:%S")

    def start_connection_to_database_thread(self):
        if pika:
            initial_connection_thread = threading.Thread(
                target=self.set_up_pika_connection
            )
            initial_connection_thread.daemon = True
            initial_connection_thread.start()
            self.send_events_to_database()

    def set_up_pika_connection(self):
        Logger.info("Try to set up pika connection")
        while True:
            if self.set.ip_address and self.set.wifi_available:
                try:
                    self.connection = pika.BlockingConnection(
                        pika.ConnectionParameters(
                            "sm-receiver.yetitool.com",
                            5672,
                            "/",
                            pika.credentials.PlainCredentials(
                                "console", "2RsZWRceL3BPSE6xZ6ay9xRFdKq3WvQb"
                            ),
                        )
                    )
                    Logger.info("Connection established")
                    self.routine_updates_channel = self.connection.channel()
                    self.routine_updates_channel.queue_declare(queue=self.queue)
                    try:
                        if not self.routine_update_thread.is_alive():
                            self.send_routine_updates_to_database()
                    except:
                        self.send_routine_updates_to_database()
                    break
                except:
                    Logger.exception("Pika connection exception")
                    sleep(10)
            else:
                sleep(10)

    def reinstate_channel_or_connection_if_missing(self):
        Logger.debug("Attempt to reinstate channel or connection")
        try:
            if self.connection.is_closed:
                Logger.debug("Connection is closed, set up new connection")
                self.set_up_pika_connection()
            elif self.routine_updates_channel.is_closed:
                if self.VERBOSE:
                    Logger.debug("Channel is closed, set up new channel")
                self.routine_updates_channel = self.connection.channel()
                self.routine_updates_channel.queue_declare(queue=self.queue)
            else:
                try:
                    Logger.warning("Close connection and start again")
                    self.connection.close()
                    self.set_up_pika_connection()
                except:
                    Logger.error("sleep and try reinstating connection again in 10s")
                    sleep(10)
                    self.reinstate_channel_or_connection_if_missing()
        except:
            try:
                self.routine_updates_channel.close()
            except:
                pass
            try:
                self.connection.close()
            except:
                pass
            self.connection = None
            self.set_up_pika_connection()

    def send_routine_updates_to_database(self):

        def do_routine_update_loop():
            while True:
                if self.set.ip_address:
                    try:
                        if self.m.s.m_state == "Idle":
                            self.send_alive()
                        else:
                            self.publish_event_with_routine_updates_channel(
                                self.generate_full_payload_data(),
                                "Routine Full Payload",
                            )
                    except:
                        Logger.exception("Could not send routine update")
                sleep(10)

        self.routine_update_thread = threading.Thread(target=do_routine_update_loop)
        self.routine_update_thread.daemon = True
        self.routine_update_thread.start()

    def send_events_to_database(self):

        def do_event_sending_loop():
            while True:
                event_task, args = self.event_queue.get()
                event_task(*args)

        self.thread_for_send_event = threading.Thread(target=do_event_sending_loop)
        self.thread_for_send_event.daemon = True
        self.thread_for_send_event.start()

    def publish_event_with_routine_updates_channel(self, data, exception_type):
        if self.VERBOSE:
            Logger.info("Publishing data: " + exception_type)
        if self.set.wifi_available:
            try:
                self.routine_updates_channel.basic_publish(
                    exchange="", routing_key=self.queue, body=json.dumps(data)
                )
                if self.VERBOSE:
                    Logger.info(data)
            except:
                Logger.exception(exception_type + " sent exception")
                self.reinstate_channel_or_connection_if_missing()

    def publish_event_with_temp_channel(self, data, exception_type, timeout):
        Logger.info("Publishing data: " + exception_type)
        while time.time() < timeout and self.set.ip_address:
            if self.set.wifi_available:
                try:
                    temp_event_channel = self.connection.channel()
                    temp_event_channel.queue_declare(queue=self.queue)
                    try:
                        temp_event_channel.basic_publish(
                            exchange="", routing_key=self.queue, body=json.dumps(data)
                        )
                        if self.VERBOSE:
                            Logger.info(data)
                        if "Job End" in exception_type:
                            temp_event_channel.basic_publish(
                                exchange="",
                                routing_key=self.queue,
                                body=json.dumps(self.generate_full_payload_data()),
                            )
                            if self.VERBOSE:
                                Logger.info(data)
                    except:
                        Logger.exception(exception_type + " send exception")
                    temp_event_channel.close()
                    break
                except:
                    sleep(10)
            else:
                sleep(10)
        self.event_queue.task_done()

    def send_alive(self):
        data = {
            "payload_type": "alive",
            "machine_info": {
                "name": self.m.device_label,
                "location": self.m.device_location,
                "hostname": self.set.console_hostname,
                "ec_version": self.m.sett.sw_version,
                "public_ip_address": self.set.public_ip_address,
            },
            "time": self.get_local_time(),
        }
        self.publish_event_with_routine_updates_channel(data, "Alive")

    def generate_full_payload_data(self):
        z_lube_limit_hrs = self.m.time_to_remind_user_to_lube_z_seconds / 3600
        z_lube_used_hrs = self.m.time_since_z_head_lubricated_seconds / 3600
        z_lube_hrs_left = round(z_lube_limit_hrs - z_lube_used_hrs, 2)
        z_lube_percent_left = round(z_lube_hrs_left / z_lube_limit_hrs * 100, 2)
        spindle_brush_limit_hrs = self.m.spindle_brush_lifetime_seconds / 3600
        spindle_brush_used_hrs = self.m.spindle_brush_use_seconds / 3600
        spindle_brush_hrs_left = round(
            spindle_brush_limit_hrs - spindle_brush_used_hrs, 2
        )
        spindle_brush_percent_left = round(
            spindle_brush_hrs_left / spindle_brush_limit_hrs * 100, 2
        )
        calibration_limit_hrs = self.m.time_to_remind_user_to_calibrate_seconds / 3600
        calibration_used_hrs = self.m.time_since_calibration_seconds / 3600
        calibration_hrs_left = round(calibration_limit_hrs - calibration_used_hrs, 2)
        calibration_percent_left = round(
            calibration_hrs_left / calibration_limit_hrs * 100, 2
        )
        if not self.initial_consumable_intervals_found:
            self.find_initial_consumable_intervals(
                z_lube_percent_left,
                spindle_brush_percent_left,
                calibration_percent_left,
            )
        self.check_consumable_percentages(
            z_lube_percent_left, spindle_brush_percent_left, calibration_percent_left
        )
        status = self.m.state()
        if "Door" in status:
            if "3" in status:
                status = "Resuming"
            else:
                status = "Paused"
        data = {
            "payload_type": "full",
            "machine_info": {
                "name": self.m.device_label,
                "location": self.m.device_location,
                "hostname": self.set.console_hostname,
                "ec_version": self.m.sett.sw_version,
                "public_ip_address": self.set.public_ip_address,
            },
            "statuses": {
                "status": status,
                "z_lube_%_left": z_lube_percent_left,
                "z_lube_hrs_before_next": z_lube_hrs_left,
                "spindle_brush_%_left": spindle_brush_percent_left,
                "spindle_brush_hrs_before_next": spindle_brush_hrs_left,
                "calibration_%_left": calibration_percent_left,
                "calibration_hrs_before_next": calibration_hrs_left,
                "file_name": self.jd.job_name or "",
                "job_time": self.sm.get_screen("go").total_runtime_seconds or 0,
                "gcode_line": self.m.s.g_count or 0,
                "job_percent": self.jd.percent_thru_job or 0.0,
                "overload_peak": float(self.sm.get_screen("go").overload_peak) or 0.0,
            },
            "time": self.get_local_time(),
        }
        return data

    def find_initial_consumable_intervals(
        self, z_lube_percent, spindle_brush_percent, calibration_percent
    ):

        def find_current_interval(value):
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
        self.spindle_brush_percent_left_next = find_current_interval(
            spindle_brush_percent
        )
        self.calibration_percent_left_next = find_current_interval(calibration_percent)
        self.initial_consumable_intervals_found = True

    def check_consumable_percentages(
        self, z_lube_percent, spindle_brush_percent, calibration_percent
    ):
        next_percent_dict = {
            (50): 25,
            (25): 10,
            (10): 5,
            (5): 0,
            (0): -10,
            (-10): -25,
            (-25): -25,
        }
        severity_dict = {(50): 0, (25): 1, (10): 1, (5): 2, (0): 2, (-10): 2, (-25): 2}
        previous_percent_dict = {
            (50): 50,
            (25): 50,
            (10): 25,
            (5): 10,
            (0): 5,
            (-10): 0,
            (-25): -10,
        }
        if z_lube_percent < self.z_lube_percent_left_next:
            self.send_event(
                severity_dict[self.z_lube_percent_left_next],
                "Z-lube percentage left",
                "Z-lube percentage passed below "
                + str(self.z_lube_percent_left_next)
                + "%",
                2,
            )
            self.z_lube_percent_left_next = next_percent_dict[
                self.z_lube_percent_left_next
            ]
        if spindle_brush_percent < self.spindle_brush_percent_left_next:
            self.send_event(
                severity_dict[self.spindle_brush_percent_left_next],
                "Spindle brush percentage left",
                "Spindle brush percentage passed below "
                + str(self.spindle_brush_percent_left_next)
                + "%",
                2,
            )
            self.spindle_brush_percent_left_next = next_percent_dict[
                self.spindle_brush_percent_left_next
            ]
        if calibration_percent < self.calibration_percent_left_next:
            self.send_event(
                severity_dict[self.calibration_percent_left_next],
                "Calibration percentage left",
                "Calibration percentage passed below "
                + str(self.calibration_percent_left_next)
                + "%",
                2,
            )
            self.calibration_percent_left_next = next_percent_dict[
                self.calibration_percent_left_next
            ]
        if (
            z_lube_percent > previous_percent_dict[self.z_lube_percent_left_next]
            or spindle_brush_percent
            > previous_percent_dict[self.spindle_brush_percent_left_next]
            or calibration_percent
            > previous_percent_dict[self.calibration_percent_left_next]
        ):
            self.find_initial_consumable_intervals(
                z_lube_percent, spindle_brush_percent, calibration_percent
            )

    def send_job_end(self, successful):
        if pika:
            data = {
                "payload_type": "job_end",
                "machine_info": {
                    "name": self.m.device_label,
                    "location": self.m.device_location,
                    "hostname": self.set.console_hostname,
                    "ec_version": self.m.sett.sw_version,
                    "public_ip_address": self.set.public_ip_address,
                },
                "job_data": {
                    "job_name": self.jd.job_name or "",
                    "successful": successful,
                    "actual_job_duration": self.jd.actual_runtime,
                    "actual_pause_duration": self.jd.pause_duration,
                },
                "time": self.get_local_time(),
            }
            self.event_queue.put(
                (
                    self.publish_event_with_temp_channel,
                    [data, "Job End", time.time() + self.event_send_timeout],
                )
            )

    def send_job_summary(self, successful):
        if pika:
            data = {
                "payload_type": "job_summary",
                "machine_info": {
                    "name": self.m.device_label,
                    "location": self.m.device_location,
                    "hostname": self.set.console_hostname,
                    "ec_version": self.m.sett.sw_version,
                    "public_ip_address": self.set.public_ip_address,
                },
                "job_data": {
                    "job_name": self.jd.job_name or "",
                    "successful": successful,
                    "post_production_notes": self.jd.post_production_notes,
                    "batch_number": self.jd.batch_number,
                    "parts_made_so_far": self.jd.metadata_dict.get(
                        "Parts Made So Far", 0
                    ),
                },
                "time": self.get_local_time(),
            }
            self.event_queue.put(
                (
                    self.publish_event_with_temp_channel,
                    [data, "Job Summary", time.time() + self.event_send_timeout],
                )
            )
        self.jd.post_job_data_update_post_send()

    def send_job_start(self):
        if pika:
            data = {
                "payload_type": "job_start",
                "machine_info": {
                    "name": self.m.device_label,
                    "location": self.m.device_location,
                    "hostname": self.set.console_hostname,
                    "ec_version": self.m.sett.sw_version,
                    "public_ip_address": self.set.public_ip_address,
                },
                "job_data": {
                    "job_name": self.jd.job_name or "",
                    "job_start": self.get_local_time(),
                },
                "metadata": {},
                "time": self.get_local_time(),
            }
            metadata_in_json_format = {
                k.translate(None, " "): v for k, v in self.jd.metadata_dict.items()
            }
            data["metadata"] = metadata_in_json_format
            self.event_queue.put(
                (
                    self.publish_event_with_temp_channel,
                    [data, "Job Start", time.time() + self.event_send_timeout],
                )
            )

    def send_spindle_speed_info(self):
        if pika and self.sm.has_screen("go"):
            data = {
                "payload_type": "spindle_speed",
                "machine_info": {
                    "name": self.m.device_label,
                    "location": self.m.device_location,
                    "hostname": self.set.console_hostname,
                    "ec_version": self.m.sett.sw_version,
                    "public_ip_address": self.set.public_ip_address,
                },
                "speeds": {
                    "spindle_speed": self.m.s.spindle_speed,
                    "spindle_percentage": self.sm.get_screen(
                        "go"
                    ).speedOverride.speed_rate_label.text,
                    "max_spindle_speed_absolute": self.sm.get_screen(
                        "go"
                    ).spindle_speed_max_absolute
                    or "",
                    "max_spindle_speed_percentage": self.sm.get_screen(
                        "go"
                    ).spindle_speed_max_percentage
                    or "",
                },
            }
            self.event_queue.put(
                (
                    self.publish_event_with_temp_channel,
                    [data, "Spindle speed", time.time() + self.event_send_timeout],
                )
            )

    def send_feed_rate_info(self):
        if pika:
            data = {
                "payload_type": "feed_rate",
                "machine_info": {
                    "name": self.m.device_label,
                    "location": self.m.device_location,
                    "hostname": self.set.console_hostname,
                    "ec_version": self.m.sett.sw_version,
                    "public_ip_address": self.set.public_ip_address,
                },
                "feeds": {
                    "feed_rate": self.m.feed_rate(),
                    "feed_percentage": self.sm.get_screen(
                        "go"
                    ).feedOverride.feed_rate_label.text,
                    "max_feed_rate_absolute": self.sm.get_screen(
                        "go"
                    ).feed_rate_max_absolute
                    or "",
                    "max_feed_rate_percentage": self.sm.get_screen(
                        "go"
                    ).feed_rate_max_percentage
                    or "",
                },
            }
            self.event_queue.put(
                (
                    self.publish_event_with_temp_channel,
                    [data, "Feed rate", time.time() + self.event_send_timeout],
                )
            )

    def send_event(self, event_severity, event_description, event_name, event_type):
        if pika:
            data = {
                "payload_type": "event",
                "machine_info": {
                    "name": self.m.device_label,
                    "location": self.m.device_location,
                    "hostname": self.set.console_hostname,
                    "ec_version": self.m.sett.sw_version,
                    "public_ip_address": self.set.public_ip_address,
                },
                "event": {
                    "severity": event_severity,
                    "type": event_type,
                    "name": event_name,
                    "description": event_description,
                },
                "time": self.get_local_time(),
            }
            self.event_queue.put(
                (
                    self.publish_event_with_temp_channel,
                    [
                        data,
                        "Event: " + str(event_name),
                        time.time() + self.event_send_timeout,
                    ],
                )
            )
