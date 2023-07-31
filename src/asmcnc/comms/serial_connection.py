"""
Created on 31 Jan 2018
@author: Ed
Module to manage all serial comms between pi (EasyCut s/w) and realtime arduino chip (GRBL f/w)
"""
from kivy.config import Config
import serial, sys, time, string, threading, serial.tools.list_ports
from datetime import datetime, timedelta
from os import listdir
from kivy.clock import Clock
import re
from functools import partial
from serial.serialutil import SerialException
from asmcnc.core_UI.sequence_alarm import alarm_manager
BAUD_RATE = 115200
ENABLE_STATUS_REPORTS = True
GRBL_SCANNER_MIN_DELAY = 0.01


def log(message):
    timestamp = datetime.now()
    print(timestamp.strftime('%H:%M:%S.%f')[:12] + ' ' + str(message))


class SerialConnection(object):
    STATUS_INTERVAL = 0.1
    s = None
    sm = None
    yp = None
    grbl_out = ''
    response_log = []
    suppress_error_screens = False
    FLUSH_FLAG = False
    write_command_buffer = []
    write_realtime_buffer = []
    write_protocol_buffer = []
    last_protocol_send_time = 0
    monitor_text_buffer = ''
    overload_state = 0
    prev_overload_state = 0
    is_ready_to_assess_spindle_for_shutdown = True
    power_loss_detected = False
    grbl_scanner_running = False

    def __init__(self, machine, screen_manager, settings_manager,
        localization, job):
        self.sm = screen_manager
        self.sett = settings_manager
        self.m = machine
        self.jd = job
        self.l = localization
        self.alarm = alarm_manager.AlarmSequenceManager(self.sm, self.sett,
            self.m, self.l, self.jd)
        self.FINAL_TEST = False

    def __del__(self):
        if self.s:
            self.s.close()
        log('Serial connection destructor')

    def is_use_yp(self):
        if self.yp:
            return self.yp.use_yp
        else:
            return False

    def set_use_yp(self, val):
        if self.yp:
            self.yp.use_yp = val

    def get_serial_screen(self, serial_error):
        try:
            if (self.sm.current != 'serialScreen' and self.sm.current !=
                'rebooting'):
                self.sm.get_screen('serialScreen'
                    ).error_description = self.l.get_str(serial_error)
                self.sm.current = 'serialScreen'
        except:
            log('Serial comms interrupted but no serial screen - are you in diagnostics mode?'
                )
            log('Serial error: ' + str(serial_error))

    def is_port_SmartBench(self, available_port):
        try:
            log('Try to connect to: ' + available_port)
            self.s = serial.Serial(str(available_port), BAUD_RATE, timeout=
                6, writeTimeout=20)
            self.s.close()
            self.s.open()
            time.sleep(1)
            try:
                self.s.flushInput()
                self.s.write('\x18')
                time.sleep(1)
                first_bytes = self.s.inWaiting()
                log('Is port SmartBench? ' + str(available_port) +
                    '| First read: ' + str(first_bytes))
                if first_bytes:

                    def strip_and_log(input_string):
                        new_string = input_string.strip()
                        log(new_string)
                        return new_string
                    stripped_input = list(map(strip_and_log, self.s.
                        readlines()))
                    if any('SmartBench' in ele for ele in stripped_input):
                        SmartBench_port = available_port
                        return SmartBench_port
                    else:
                        self.s.close()
                else:
                    self.s.close()
            except:
                log('Could not communicate with that port at all')
        except:
            log('Wow definitely not that port')
        return ''

    def quick_connect(self, available_port):
        try:
            log('Try to connect to: ' + available_port)
            self.s = serial.Serial(str(available_port), BAUD_RATE, timeout=
                6, writeTimeout=20)
            self.s.flushInput()
            self.s.write('\x18')
            return available_port
        except:
            log('Could not connect to given port.')
            return ''

    def establish_connection(self, win_port):
        log('Start to establish connection...')
        SmartBench_port = ''
        if sys.platform == 'win32':
            self.suppress_error_screens = True
            SmartBench_port = self.quick_connect(win_port)
            if not SmartBench_port:
                port_list = [port.device for port in serial.tools.
                    list_ports.comports() if 'n/a' not in port.description]
                print('Windows port list: ')
                print(str(port_list))
                for comport in port_list:
                    print('Windows port to try: ')
                    print(comport)
                    SmartBench_port = self.is_port_SmartBench(comport)
                    if SmartBench_port:
                        break
                if not SmartBench_port:
                    log('No arduino connected')
        elif sys.platform == 'darwin':
            self.suppress_error_screens = True
            filesForDevice = listdir('/dev/')
            for line in filesForDevice:
                if line.startswith('tty.usbmodem'):
                    print('Mac port to try: ')
                    print(line)
                    SmartBench_port = self.is_port_SmartBench('/dev/' + str
                        (line))
                    if SmartBench_port:
                        break
            if not SmartBench_port:
                log('No arduino connected')
        else:
            try:
                default_serial_port = 'ttyS'
                ACM_port = 'ttyACM'
                USB_port = 'ttyUSB'
                AMA_port = 'ttyAMA'
                port_list = [default_serial_port, ACM_port, USB_port, AMA_port]
                filesForDevice = listdir('/dev/')
                list_of_available_ports = [port for potential_port in
                    port_list for port in filesForDevice if potential_port in
                    port]
                for available_port in list_of_available_ports:
                    SmartBench_port = self.is_port_SmartBench('/dev/' + str
                        (available_port))
                    if SmartBench_port:
                        break
                if SmartBench_port == '':
                    first_port = list_of_available_ports[0]
                    last_port = list_of_available_ports[-1]
                    try:
                        if default_serial_port in first_port:
                            first_list_index = 1
                            self.s = serial.Serial('/dev/' + first_port,
                                BAUD_RATE, timeout=6, writeTimeout=20)
                            SmartBench_port = (
                                ': could not identify if any port was SmartBench, so attempting '
                                 + first_port)
                    except:
                        if AMA_port in last_port:
                            last_list_index = -1
                            self.s = serial.Serial('/dev/' + last_port,
                                BAUD_RATE, timeout=6, writeTimeout=20)
                            SmartBench_port = (
                                ': could not identify if any port was SmartBench, so attempting '
                                 + last_port)
                    if SmartBench_port == '':
                        Clock.schedule_once(lambda dt: self.
                            get_serial_screen(
                            'Could not establish a connection on startup.'), 5)
            except:
                Clock.schedule_once(lambda dt: self.get_serial_screen(
                    'Could not establish a connection on startup.'), 5)
        log('Serial connection status: ' + str(self.is_connected()) + ' ' +
            str(SmartBench_port))
        try:
            if self.is_connected():
                log('Initialising grbl...')
                self.write_direct('\r\n\r\n', realtime=False, show_in_sys=
                    False, show_in_console=False)
        except:
            Clock.schedule_once(lambda dt: self.get_serial_screen(
                'Could not establish a connection on startup.'), 5)

    def is_connected(self):
        if self.s != None:
            return True
        else:
            return False

    def start_services(self, dt):
        log('Starting services')
        self.s.flushInput()
        self.next_poll_time = time.time()
        self.grbl_scanner_running = True
        t = threading.Thread(target=self.grbl_scanner)
        t.daemon = True
        t.start()
        self.m.bootup_sequence()
        self.m.starting_serial_connection = False
    VERBOSE_ALL_PUSH_MESSAGES = False
    VERBOSE_ALL_RESPONSE = False
    VERBOSE_STATUS = False

    def grbl_scanner(self, run_grbl_scanner_once=False):
        log('Running grbl_scanner thread')
        while self.grbl_scanner_running or run_grbl_scanner_once:
            if self.FLUSH_FLAG == True:
                self.s.flushInput()
                self.FLUSH_FLAG = False
            if self.next_poll_time < time.time():
                self.write_direct('?', realtime=True, show_in_sys=False,
                    show_in_console=False)
                self.next_poll_time = time.time() + self.STATUS_INTERVAL
            command_counter = 0
            for command in self.write_command_buffer:
                self.write_direct(*command)
                command_counter += 1
            del self.write_command_buffer[0:command_counter]
            realtime_counter = 0
            for realtime_command in self.write_realtime_buffer:
                self.write_direct(realtime_command[0], altDisplayText=
                    realtime_command[1], realtime=True)
                realtime_counter += 1
            del self.write_realtime_buffer[0:realtime_counter]
            if (self.write_protocol_buffer and self.last_protocol_send_time +
                0.05 < time.time()):
                protocol_command = self.write_protocol_buffer[0]
                self.write_direct(protocol_command[0], altDisplayText=
                    protocol_command[1], protocol=True)
                del self.write_protocol_buffer[0]
            if self.s.inWaiting():
                try:
                    rec_temp = self.s.readline().strip()
                except Exception as e:
                    log('serial.readline exception:\n' + str(e))
                    rec_temp = ''
                    self.get_serial_screen(
                        'Could not read line from serial buffer.')
            else:
                rec_temp = ''
            if len(rec_temp):
                if self.VERBOSE_ALL_RESPONSE:
                    if rec_temp.startswith('<'):
                        log(rec_temp)
                    else:
                        log('< ' + rec_temp)
                try:
                    self.sm.get_screen('home'
                        ).gcode_monitor_widget.update_monitor_text_buffer('rec'
                        , rec_temp)
                except:
                    pass
                try:
                    if rec_temp.startswith(('ok', 'error')):
                        self.process_grbl_response(rec_temp)
                    else:
                        self.process_grbl_push(rec_temp)
                except Exception as e:
                    log('Process response exception:\n' + str(e))
                    self.get_serial_screen(
                        'Could not process grbl response. Grbl scanner has been stopped.'
                        )
                    raise
                if (self.is_job_streaming and not self.m.is_machine_paused and
                    not 'Alarm' in self.m.state()):
                    if self.is_use_yp(
                        ) and self.m.has_spindle_health_check_passed(
                        ) and self.m.is_using_sc2():
                        if (self.digital_spindle.ld_qdA >= 0 and self.
                            grbl_ln is not None and self.
                            digital_spindle.mains_voltage >= 0 and not self
                            .in_inrush):
                            self.yp.add_status_to_yetipilot(self.
                                digital_spindle.ld_qdA, self.
                                digital_spindle.mains_voltage, self.
                                feeds_and_speeds.feed_override, int(self.
                                feeds_and_speeds.feed_rate))
                    if self.is_stream_lines_remaining:
                        self.stuff_buffer()
                    elif self.g_count == self.l_count:
                        self.end_stream()
                if (self._ready_to_send_first_sequential_stream and self.
                    is_buffer_clear()):
                    self._send_next_sequential_stream()
            run_grbl_scanner_once = False
        log('Killed grbl_scanner')
        self.m_state = 'Off'
    GRBL_BLOCK_SIZE = 35
    RX_BUFFER_SIZE = 255
    is_job_streaming = False
    is_stream_lines_remaining = False
    g_count = 0
    l_count = 0
    c_line = []
    stream_start_time = 0
    stream_end_time = 0
    stream_pause_start_time = 0
    stream_paused_accumulated_time = 0
    check_streaming_started = False
    NOT_SKELETON_STUFF = True

    def check_job(self, job_object):
        log('Checking job...')
        self.m.enable_check_mode()
        self.set_use_yp(False)

        def check_job_inner_function():
            if self.m_state == 'Check':
                self.check_streaming_started = True
                self.suppress_error_screens = True
                self.response_log = []
                self.run_job(job_object)
                Clock.schedule_interval(partial(self.return_check_outcome,
                    job_object), 0.1)
            else:
                Clock.schedule_once(lambda dt: check_job_inner_function(), 0.9)
        Clock.schedule_once(lambda dt: check_job_inner_function(), 0.9)

    def return_check_outcome(self, job_object, dt):
        if len(self.response_log) >= len(job_object):
            self.suppress_error_screens = False
            self.sm.get_screen('check_job').error_log = self.response_log
            return False

    def run_job(self, job_object):
        self.grbl_ln = None
        self.jd.grbl_mode_tracker = []
        self.jd.job_gcode_running = job_object
        log('Job starting...')
        if self.initialise_job() and self.jd.job_gcode_running:
            Clock.schedule_once(lambda dt: self.set_streaming_flags_to_true
                (), 2)
        elif not self.jd.job_gcode_running:
            log('Could not start job: File empty')
            self.sm.get_screen('go').reset_go_screen_prior_to_job_start()

    def initialise_job(self):
        if self.m_state != 'Check':
            self.m.set_led_colour('GREEN')
            self.m.zUp()
        self.FLUSH_FLAG = True
        self.NOT_SKELETON_STUFF = True
        time.sleep(0.1)
        self._reset_counters()
        return True

    def run_skeleton_buffer_stuffer(self, gcode_obj):
        self.grbl_ln = None
        self.jd.grbl_mode_tracker = []
        self.jd.job_gcode_running = gcode_obj
        self.m.set_pause(False)
        log('Skeleton buffer stuffing starting...')
        self.FLUSH_FLAG = True
        self.NOT_SKELETON_STUFF = False
        time.sleep(0.1)
        self._reset_counters()
        if self.jd.job_gcode_running:
            Clock.schedule_once(lambda dt: self.set_streaming_flags_to_true
                (), 2)

    def _reset_counters(self):
        self.l_count = 0
        self.g_count = 0
        self.c_line = []
        self.stream_pause_start_time = 0
        self.stream_paused_accumulated_time = 0
        self.stream_start_time = time.time()
        if self.sm.has_screen('go'):
            self.sm.get_screen('go').total_runtime_seconds = 0

    def set_streaming_flags_to_true(self):
        self.is_stream_lines_remaining = True
        self.is_job_streaming = True
        log('Job running')

    def stuff_buffer(self):
        while self.l_count < len(self.jd.job_gcode_running):
            line_to_go = self.add_line_number_to_gcode_line(self.jd.
                job_gcode_running[self.l_count], self.l_count)
            serial_space = self.RX_BUFFER_SIZE - sum(self.c_line)
            if len(line_to_go) + 1 <= serial_space:
                self.scrape_last_sent_modes(line_to_go)
                self.add_to_g_mode_tracker(self.last_sent_motion_mode, self
                    .last_sent_feed, self.last_sent_speed)
                self.c_line.append(len(line_to_go) + 1)
                self.write_direct(line_to_go, show_in_sys=True,
                    show_in_console=False)
                self.l_count += 1
            else:
                return
        self.is_stream_lines_remaining = False
    last_line_executed = 0
    last_sent_motion_mode = ''
    last_sent_feed = 0
    last_sent_speed = 0
    feed_pattern = re.compile('F\\d+\\.?\\d*')
    speed_pattern = re.compile('S\\d+\\.?\\d*')
    g_motion_pattern = re.compile('((?<=G)|(?<=G0))([0-3])((?=\\D)|(?=$))')

    def add_line_number_to_gcode_line(self, line, i):
        return line if self.gcode_line_is_excluded(line) else 'N' + str(i
            ) + line

    def gcode_line_is_excluded(self, line):
        return ('(' in line or ')' in line or '$' in line or 'AE' in line or
            'AF' in line or '*L' in line)

    def get_grbl_float(self, line, pattern, last_thing=None):
        match_obj = re.search(pattern, line)
        return float(match_obj.group()[1:]) if match_obj else last_thing

    def get_grbl_mode(self, line, grbl_pattern, last_thing=None):
        match_obj = re.search(grbl_pattern, line)
        return int(match_obj.group()) if match_obj else last_thing

    def scrape_last_sent_modes(self, line_to_go):
        self.last_sent_motion_mode = self.get_grbl_mode(line_to_go, self.
            g_motion_pattern, self.last_sent_motion_mode)
        self.last_sent_feed = self.get_grbl_float(line_to_go, self.
            feed_pattern, self.last_sent_feed)
        self.last_sent_speed = self.get_grbl_float(line_to_go, self.
            speed_pattern, self.last_sent_speed)

    def add_to_g_mode_tracker(self, motion, feed, speed):
        self.jd.grbl_mode_tracker += (motion, feed, speed),

    def remove_from_g_mode_tracker(self, line_diff):
        if line_diff:
            del self.jd.grbl_mode_tracker[:line_diff]

    def process_grbl_response(self, message):
        if self.suppress_error_screens == True:
            self.response_log.append(message)
        if message.startswith('error'):
            log('ERROR from GRBL: ' + message)
            if (self.suppress_error_screens == False and self.sm.current !=
                'errorScreen'):
                self.sm.get_screen('errorScreen').message = message
                if self.sm.current == 'alarmScreen':
                    self.sm.get_screen('errorScreen'
                        ).return_to_screen = self.sm.get_screen('alarmScreen'
                        ).return_to_screen
                else:
                    self.sm.get_screen('errorScreen'
                        ).return_to_screen = self.sm.current
                self.sm.current = 'errorScreen'
        if self._process_oks_from_sequential_streaming:
            self._send_next_sequential_stream()
        elif self.is_job_streaming:
            self.g_count += 1
            if self.c_line != []:
                del self.c_line[0]

    def end_stream(self):
        log('Ending stream...')
        self.is_job_streaming = False
        self.is_stream_lines_remaining = False
        self.m.set_pause(False)
        self.set_use_yp(False)
        if self.NOT_SKELETON_STUFF:
            if self.m_state != 'Check':
                if str(self.jd.job_gcode_running).count('M3') > str(self.jd
                    .job_gcode_running).count('M30'
                    ) and self.m.stylus_router_choice != 'stylus':
                    Clock.schedule_once(lambda dt: self.
                        update_machine_runtime(), 0.4)
                    self.sm.get_screen('spindle_cooldown'
                        ).return_screen = 'job_feedback'
                    self.sm.current = 'spindle_cooldown'
                else:
                    self.m.spindle_off()
                    time.sleep(0.4)
                    self.update_machine_runtime()
                    self.sm.current = 'job_feedback'
                if not self.jd.job_recovery_skip_recovery:
                    self.jd.write_to_recovery_file_after_completion()
            else:
                self.check_streaming_started = False
                self.m.disable_check_mode()
                self.suppress_error_screens = False
                self._reset_counters()
        else:
            self._reset_counters()
            self.NOT_SKELETON_STUFF = True
        self.jd.job_gcode_running = []
        self.jd.grbl_mode_tracker = []
        self.grbl_ln = None
        self.jd.percent_thru_job = 100

    def cancel_stream(self):
        self.is_job_streaming = False
        self.is_stream_lines_remaining = False
        self.m.set_pause(False)
        self.jd.job_gcode_running = []
        self.set_use_yp(False)
        self.jd.grbl_mode_tracker = []
        cancel_line = self.grbl_ln
        self.grbl_ln = None
        if self.m_state != 'Check':
            self.FLUSH_FLAG = True
            Clock.schedule_once(lambda dt: self.m.zUp(), 0.5)
            Clock.schedule_once(lambda dt: self.m.vac_off(), 1)
            time.sleep(0.4)
            time_taken_seconds = self.update_machine_runtime()
            if not self.jd.job_recovery_skip_recovery:
                self.jd.write_to_recovery_file_after_cancel(cancel_line,
                    time_taken_seconds)
        else:
            self.check_streaming_started = False
            self.m.disable_check_mode()
            self.suppress_error_screens = False
            self.FLUSH_FLAG = True
            self._reset_counters()
        self.NOT_SKELETON_STUFF = True
        log('G-code streaming cancelled!')

    def update_machine_runtime(self):
        log('G-code streaming finished!')
        self.stream_end_time = time.time()
        time_taken_seconds = int(self.stream_end_time - self.stream_start_time
            ) + 10
        only_running_time_seconds = (time_taken_seconds - self.
            stream_paused_accumulated_time)
        self.jd.pause_duration = str(timedelta(seconds=self.
            stream_paused_accumulated_time)).split('.')[0]
        self.jd.total_time = str(timedelta(seconds=time_taken_seconds)).split(
            '.')[0]
        self.jd.actual_runtime = str(timedelta(seconds=
            only_running_time_seconds)).split('.')[0]
        log('Time elapsed: ' + self.jd.total_time)
        log('Time paused: ' + self.jd.pause_duration)
        log('Actual running time: ' + self.jd.actual_runtime)
        if self.m.stylus_router_choice == 'router':
            self.m.spindle_brush_use_seconds += only_running_time_seconds
            self.m.write_spindle_brush_values(self.m.
                spindle_brush_use_seconds, self.m.
                spindle_brush_lifetime_seconds)
        self.m.time_since_calibration_seconds += only_running_time_seconds
        self.m.write_calibration_settings(self.m.
            time_since_calibration_seconds, self.m.
            time_to_remind_user_to_calibrate_seconds)
        self.m.time_since_z_head_lubricated_seconds += (
            only_running_time_seconds)
        self.m.write_z_head_maintenance_settings(self.m.
            time_since_z_head_lubricated_seconds)
        time_without_current_pause = (self.stream_pause_start_time - self.
            stream_start_time - self.stream_paused_accumulated_time)
        self._reset_counters()
        return time_without_current_pause
    m_state = 'Unknown'
    m_x = '0.0'
    m_y = '0.0'
    m_z = '0.0'
    x_change = False
    y_change = False
    z_change = False
    w_x = '0.0'
    w_y = '0.0'
    w_z = '0.0'
    wco_x = '0.0'
    wco_y = '0.0'
    wco_z = '0.0'
    g28_x = '0.0'
    g28_y = '0.0'
    g28_z = '0.0'
    grbl_ln = None
    spindle_speed = 0
    feed_rate = 0
    feed_override_percentage = 100
    speed_override_percentage = 100
    spindle_load_voltage = None
    digital_spindle_ld_qdA = None
    digital_spindle_temperature = None
    digital_spindle_kill_time = None
    digital_spindle_mains_voltage = None
    digital_load_pattern = re.compile('Ld:\\d+,\\d+,\\d+,\\d+')
    inrush_counter = 0
    inrush_max = 20
    in_inrush = True
    spindle_freeload = None
    limit_x = False
    limit_X = False
    limit_y = False
    limit_Y = False
    limit_z = False
    probe = False
    dust_shoe_cover = False
    spare_door = False
    limit_Y_axis = False
    stall_X = False
    stall_Z = False
    stall_Y = False
    grbl_waiting_for_reset = False
    serial_blocks_available = GRBL_BLOCK_SIZE
    serial_chars_available = RX_BUFFER_SIZE
    print_buffer_status = True
    expecting_probe_result = False
    fw_version = ''
    hw_version = ''
    motor_driver_temp = None
    pcb_temp = None
    transistor_heatsink_temp = None
    microcontroller_mV = None
    LED_mV = None
    PSU_mV = None
    spindle_speed_monitor_mV = None
    sg_z_motor_axis = None
    sg_x_motor_axis = None
    sg_y_axis = None
    sg_y1_motor = None
    sg_y2_motor = None
    sg_x1_motor = None
    sg_x2_motor = None
    last_stall_tmc_index = None
    last_stall_motor_step_size = None
    last_stall_load = None
    last_stall_threshold = None
    last_stall_travel_distance = None
    last_stall_temperature = None
    last_stall_x_coord = None
    last_stall_y_coord = None
    last_stall_z_coord = None
    last_stall_status = None
    record_sg_values_flag = False
    spindle_serial_number = None
    spindle_production_year = None
    spindle_production_week = None
    spindle_firmware_version = None
    spindle_total_run_time_seconds = None
    spindle_brush_run_time_seconds = None
    spindle_mains_frequency_hertz = None
    grbl_initialisation_message = "^Grbl .+ \\['\\$' for help\\]$"
    measure_running_data = False
    running_data = []
    measurement_stage = 0
    spindle_health_check = False
    spindle_health_check_data = []

    def process_grbl_push(self, message):
        if self.VERBOSE_ALL_PUSH_MESSAGES:
            print(message)
        if message.startswith('<'):
            status_parts = message.translate(string.maketrans('', ''), '<>'
                ).split('|')
            if status_parts[0] != 'Idle' and status_parts[0
                ] != 'Run' and not status_parts[0].startswith('Hold'
                ) and status_parts[0] != 'Jog' and status_parts[0
                ] != 'Alarm' and not status_parts[0].startswith('Door'
                ) and status_parts[0] != 'Check' and status_parts[0
                ] != 'Home' and status_parts[0] != 'Sleep':
                log('ERROR status parse: Status invalid: ' + message)
                return
            if not '|Pn:' in message:
                self.pin_info.limit_x = False
                self.pin_info.limit_X = False
                self.pin_info.limit_y = False
                self.pin_info.limit_Y = False
                self.pin_info.limit_z = False
                self.pin_info.probe = False
                self.pin_info.dust_shoe_cover = False
                self.pin_info.spare_door = False
                self.pin_info.limit_Y_axis = False
                self.pin_info.stall_X = False
                self.stall_guard.stall_Z = False
                self.pin_info.stall_Y = False
            if not re.search(self.digital_load_pattern, message
                ) or self.digital_spindle.ld_qdA == 0:
                self.inrush_counter = 0
                self.in_inrush = True
            elif self.inrush_counter < self.inrush_max:
                self.inrush_counter += 1
            elif self.inrush_counter == self.inrush_max and self.in_inrush:
                self.in_inrush = False
            self.m_state = status_parts[0]
            for part in status_parts:
                if part.startswith('MPos:'):
                    pos = part[5:].split(',')
                    try:
                        float(pos[0])
                        float(pos[1])
                        float(pos[2])
                    except:
                        log('ERROR status parse: Position invalid: ' + message)
                        return
                    self.x_change = self.machine_position.x != pos[0]
                    self.y_change = self.machine_position.y != pos[1]
                    self.machine_position.z_change = (self.
                        machine_position.z != pos[2])
                    self.machine_position.x = pos[0]
                    self.machine_position.y = pos[1]
                    self.machine_position.z = pos[2]
                elif part.startswith('WPos:'):
                    pos = part[5:].split(',')
                    try:
                        float(pos[0])
                        float(pos[1])
                        float(pos[2])
                    except:
                        log('ERROR status parse: Position invalid: ' + message)
                        return
                    self.w_x = pos[0]
                    self.w_y = pos[1]
                    self.w_z = pos[2]
                elif part.startswith('WCO:'):
                    pos = part[4:].split(',')
                    try:
                        float(pos[0])
                        float(pos[1])
                        float(pos[2])
                    except:
                        log('ERROR status parse: Position invalid: ' + message)
                        return
                    self.wco.x = pos[0]
                    self.work_coordinate_offset.y = pos[1]
                    self.wco.z = pos[2]
                elif part.startswith('Bf:'):
                    buffer_info = part[3:].split(',')
                    try:
                        int(buffer_info[0])
                        int(buffer_info[1])
                    except:
                        log('ERROR status parse: Buffer status invalid: ' +
                            message)
                        return
                    if self.buffer_info.serial_chars_available != buffer_info[1
                        ]:
                        self.buffer_info.serial_chars_available = buffer_info[1
                            ]
                        self.print_buffer_status = True
                    if self.buffer_info.serial_blocks_available != buffer_info[
                        0]:
                        self.buffer_info.serial_blocks_available = buffer_info[
                            0]
                        self.print_buffer_status = True
                    if self.print_buffer_status == True:
                        self.print_buffer_status = False
                elif part.startswith('Ln:'):
                    value = part[3:]
                    try:
                        int(value)
                    except:
                        log('ERROR status parse: Line number invalid: ' +
                            message)
                        return
                    if self.grbl_ln is not None:
                        self.remove_from_g_mode_tracker(int(value) - self.
                            grbl_ln)
                    else:
                        self.remove_from_g_mode_tracker(int(value))
                    self.grbl_ln = int(value)
                elif part.startswith('Pn:'):
                    pins_info = part.split(':')[1]
                    self.pin_info.limit_x = 'x' in pins_info
                    self.pin_info.limit_X = 'X' in pins_info
                    self.pin_info.limit_z = 'Z' in pins_info
                    if 'P' in pins_info:
                        self.pin_info.probe = True
                    else:
                        self.pin_info.probe = False
                    if 'g' in pins_info:
                        self.pin_info.spare_door = True
                    else:
                        self.pin_info.spare_door = False
                    if 'G' in pins_info:
                        self.pin_info.dust_shoe_cover = True
                    else:
                        self.pin_info.dust_shoe_cover = False
                    if 'Y' or 'y' in pins_info:
                        if self.versions.firmware and int(self.
                            versions.firmware.split('.')[0]) < 2:
                            self.pin_info.limit_y = 'y' in pins_info
                            self.pin_info.limit_Y = 'Y' in pins_info
                        else:
                            self.pin_info.limit_Y_axis = 'y' in pins_info
                            self.pin_info.stall_Y = 'Y' in pins_info
                    else:
                        self.pin_info.limit_y = False
                        self.pin_info.limit_Y = False
                        self.pin_info.limit_Y_axis = False
                        self.pin_info.stall_Y = False
                    self.pin_info.stall_X = 'S' in pins_info
                    self.stall_guard.stall_Z = 'z' in pins_info
                    if (self.pin_info.stall_X or self.pin_info.stall_Y or
                        self.stall_guard.stall_Z):
                        self.alarm.sg_alarm = True
                    if ('r' in pins_info and not self.power_loss_detected and
                        sys.platform not in ['win32', 'darwin']):
                        self.m._grbl_door()
                        self.sm.get_screen('door').db.send_event(2,
                            'Power loss',
                            'Connection loss: Check power and WiFi', 0)
                        self.m.set_pause(True)
                        log('Power loss or DC power supply')
                        self.power_loss_detected = True
                        Clock.schedule_once(lambda dt: self.m.
                            resume_from_a_soft_door(), 1)
                elif part.startswith('Door'
                    ) and self.m.is_machine_paused == False:
                    if part.startswith('Door:3'):
                        pass
                    else:
                        self.m.set_pause(True)
                        if self.sm.current != 'door':
                            log('Hard ' + self.m_state)
                            self.sm.get_screen('door'
                                ).return_to_screen = self.sm.current
                            self.sm.current = 'door'
                elif part.startswith('Ld:'):
                    spindle_feedback = part.split(':')[1]
                    if ',' in spindle_feedback:
                        digital_spindle_feedback = spindle_feedback.split(',')
                        try:
                            int(digital_spindle_feedback[0])
                            int(digital_spindle_feedback[1])
                            int(digital_spindle_feedback[2])
                            int(digital_spindle_feedback[3])
                        except:
                            log(
                                'ERROR status parse: Digital spindle feedback invalid: '
                                 + message)
                            return
                        self.digital_spindle.ld_qdA = int(
                            digital_spindle_feedback[0])
                        self.digital_spindle.temperature = int(
                            digital_spindle_feedback[1])
                        self.digital_spindle.kill_time = int(
                            digital_spindle_feedback[2])
                        self.digital_spindle.mains_voltage = int(
                            digital_spindle_feedback[3])
                        if self.spindle_health_check and not self.in_inrush:
                            self.spindle_health_check_data.append(self.
                                digital_spindle.ld_qdA)
                        if self.digital_spindle.kill_time >= 160:
                            overload_mV_equivalent_state = 0
                        elif self.digital_spindle.kill_time >= 80:
                            overload_mV_equivalent_state = 20
                        elif self.digital_spindle.kill_time >= 40:
                            overload_mV_equivalent_state = 40
                        elif self.digital_spindle.kill_time >= 20:
                            overload_mV_equivalent_state = 60
                        elif self.digital_spindle.kill_time >= 10:
                            overload_mV_equivalent_state = 80
                        elif self.digital_spindle.kill_time < 10:
                            overload_mV_equivalent_state = 100
                        else:
                            log('Killtime value not recognised')
                    else:
                        try:
                            int(spindle_feedback)
                        except:
                            log(
                                'ERROR status parse: Analogue spindle feedback invalid: '
                                 + message)
                            return
                        self.analog_spindle.load_voltage = int(spindle_feedback
                            )
                        if self.analog_spindle.load_voltage < 400:
                            overload_mV_equivalent_state = 0
                        elif self.analog_spindle.load_voltage < 1000:
                            overload_mV_equivalent_state = 20
                        elif self.analog_spindle.load_voltage < 1500:
                            overload_mV_equivalent_state = 40
                        elif self.analog_spindle.load_voltage < 2000:
                            overload_mV_equivalent_state = 60
                        elif self.analog_spindle.load_voltage < 2500:
                            overload_mV_equivalent_state = 80
                        elif self.analog_spindle.load_voltage >= 2500:
                            overload_mV_equivalent_state = 100
                        else:
                            log('Overload value not recognised')
                    if overload_mV_equivalent_state != self.overload_state:
                        self.overload_state = overload_mV_equivalent_state
                        log('Overload state change: ' + str(self.
                            overload_state))
                        log('Load voltage: ' + str(self.
                            analog_spindle.load_voltage))
                        try:
                            self.sm.get_screen('go').update_overload_label(self
                                .overload_state)
                            if (20 <= self.overload_state < 100 and self.
                                is_ready_to_assess_spindle_for_shutdown):
                                self.prev_overload_state = self.overload_state
                                Clock.schedule_once(self.
                                    check_for_sustained_peak, 1)
                        except:
                            log('Unable to update overload state on go screen')
                    if (self.overload_state == 100 and self.
                        is_ready_to_assess_spindle_for_shutdown):
                        self.is_ready_to_assess_spindle_for_shutdown = False
                        Clock.schedule_once(self.
                            check_for_sustained_max_overload, 0.5)
                elif part.startswith('FS:'):
                    feed_speed = part[3:].split(',')
                    self.feeds_and_speeds.feed_rate = feed_speed[0]
                    self.feeds_and_speeds.spindle_speed = feed_speed[1]
                elif part.startswith('Ov:'):
                    values = part[3:].split(',')
                    try:
                        int(values[0])
                        int(values[1])
                        int(values[2])
                    except:
                        log('ERROR status parse: Ov values invalid: ' + message
                            )
                        return
                    self.feeds_and_speeds.feed_override = int(values[0])
                    self.feeds_and_speeds.speed_override = int(values[2])
                elif part.startswith('TC:'):
                    temps = part[3:].split(',')
                    try:
                        float(temps[0])
                        float(temps[1])
                    except:
                        log('ERROR status parse: Temperature invalid: ' +
                            message)
                        return
                    self.temperatures.motor_driver = float(temps[0])
                    self.temperatures.pcb = float(temps[1])
                    try:
                        float(temps[2])
                        self.temperatures.transistor_heatsink = float(temps[2])
                    except IndexError:
                        pass
                    except:
                        log('ERROR status parse: Temperature invalid: ' +
                            message)
                        return
                elif part.startswith('V:'):
                    voltages = part[2:].split(',')
                    try:
                        float(voltages[0])
                        float(voltages[1])
                        float(voltages[2])
                        float(voltages[3])
                    except:
                        log('ERROR status parse: Voltage invalid: ' + message)
                        return
                    self.voltages.microcontroller_mV = float(voltages[0])
                    self.voltages.LED_mV = float(voltages[1])
                    self.voltages.PSU_mV = float(voltages[2])
                    self.voltages.spindle_speed_monitor_mV = float(voltages[3])
                elif part.startswith('SG:'):
                    sg_values = part[3:].split(',')
                    try:
                        int(sg_values[0])
                        int(sg_values[1])
                        int(sg_values[2])
                        int(sg_values[3])
                        int(sg_values[4])
                    except:
                        log('ERROR status parse: SG values invalid: ' + message
                            )
                        return
                    self.stall_guard.z_motor_axis = int(sg_values[0])
                    self.stall_guard.x_motor_axis = int(sg_values[1])
                    self.stall_guard.y_axis = int(sg_values[2])
                    self.stall_guard.y1_motor = int(sg_values[3])
                    self.stall_guard.y2_motor = int(sg_values[4])
                    try:
                        int(sg_values[5])
                        int(sg_values[6])
                    except IndexError:
                        pass
                    except:
                        log('ERROR status parse: SG values invalid: ' + message
                            )
                        return
                    else:
                        self.stall_guard.x1_motor = int(sg_values[5])
                        self.stall_guard.x2_motor = int(sg_values[6])
                    if self.record_sg_values_flag:
                        self.m.temp_sg_array.append([self.
                            stall_guard.z_motor_axis, self.
                            stall_guard.x_motor_axis, self.
                            stall_guard.y_axis, self.stall_guard.y1_motor,
                            self.stall_guard.y2_motor, self.
                            stall_guard.x1_motor, self.stall_guard.x2_motor])
                    if self.FINAL_TEST:
                        if self.sm.has_screen('calibration_testing'):
                            self.sm.get_screen('calibration_testing').measure()
                        if self.sm.has_screen('overnight_testing'):
                            self.sm.get_screen('overnight_testing').measure()
                        if self.sm.has_screen('current_adjustment'):
                            self.sm.get_screen('current_adjustment').measure()
                elif part.startswith('SGALARM:'):
                    sg_alarm_parts = part[8:].split(',')
                    try:
                        int(sg_alarm_parts[0])
                        int(sg_alarm_parts[1])
                        int(sg_alarm_parts[2])
                        int(sg_alarm_parts[3])
                        int(sg_alarm_parts[4])
                        float(sg_alarm_parts[5])
                        float(sg_alarm_parts[6])
                        float(sg_alarm_parts[7])
                    except:
                        log(
                            'ERROR status parse: SGALARM pins_info invalid: ' +
                            message)
                        return
                    self.last_stall_tmc_index = int(sg_alarm_parts[0])
                    self.stall_guard.last_stall.motor_step_size = int(
                        sg_alarm_parts[1])
                    self.stall_guard.last_stall.load = int(sg_alarm_parts[2])
                    self.last_stall_threshold = int(sg_alarm_parts[3])
                    self.last_stall_travel_distance = int(sg_alarm_parts[4])
                    self.last_stall_temperature = int(sg_alarm_parts[5])
                    self.stall_guard.last_stall.x_coord = float(sg_alarm_parts
                        [6])
                    self.stall_guard.last_stall.y_coord = float(sg_alarm_parts
                        [7])
                    self.stall_guard.last_stall.z_coord = float(sg_alarm_parts
                        [8])
                    self.stall_guard.last_stall.status = message
                elif part.startswith('Sp:'):
                    spindle_statistics = part[3:].split(',')
                    try:
                        int(spindle_statistics[0])
                        int(spindle_statistics[1])
                        int(spindle_statistics[2])
                        int(spindle_statistics[3])
                        int(spindle_statistics[4])
                        int(spindle_statistics[5])
                        int(spindle_statistics[6])
                    except:
                        log('ERROR status parse: Sp values invalid: ' + message
                            )
                        return
                    self.spindle_statistics.serial_number = int(
                        spindle_statistics[0])
                    self.spindle_statistics.production_year = int(
                        spindle_statistics[1])
                    self.spindle_statistics.production_week = int(
                        spindle_statistics[2])
                    self.spindle_statistics.firmware_version = int(
                        spindle_statistics[3])
                    self.spindle_statistics.total_run_time_seconds = int(
                        spindle_statistics[4])
                    self.spindle_statistics.brush_run_time_seconds = int(
                        spindle_statistics[5])
                    self.spindle_statistics.mains_frequency_hertz = int(
                        spindle_statistics[6])
                elif part.startswith('TREG:'):
                    tmc_registers = part[5:].split(',')
                    try:
                        int(tmc_registers[0])
                        int(tmc_registers[1])
                        int(tmc_registers[2])
                        int(tmc_registers[3])
                        int(tmc_registers[4])
                        int(tmc_registers[5])
                        int(tmc_registers[6])
                        int(tmc_registers[7])
                        int(tmc_registers[8])
                        int(tmc_registers[9])
                        int(tmc_registers[10])
                    except:
                        log('ERROR status parse: TMC registers invalid: ' +
                            message)
                        return
                    self.m.TMC_motor[int(tmc_registers[0])].shadowRegisters[0
                        ] = int(tmc_registers[1])
                    self.m.TMC_motor[int(tmc_registers[0])].shadowRegisters[1
                        ] = int(tmc_registers[2])
                    self.m.TMC_motor[int(tmc_registers[0])].shadowRegisters[2
                        ] = int(tmc_registers[3])
                    self.m.TMC_motor[int(tmc_registers[0])].shadowRegisters[3
                        ] = int(tmc_registers[4])
                    self.m.TMC_motor[int(tmc_registers[0])].shadowRegisters[4
                        ] = int(tmc_registers[5])
                    self.m.TMC_motor[int(tmc_registers[0])
                        ].ActiveCurrentScale = int(tmc_registers[6])
                    self.m.TMC_motor[int(tmc_registers[0])
                        ].standStillCurrentScale = int(tmc_registers[7])
                    self.m.TMC_motor[int(tmc_registers[0])
                        ].stallGuardAlarmThreshold = int(tmc_registers[8])
                    self.m.TMC_motor[int(tmc_registers[0])
                        ].max_step_period_us_SG = int(tmc_registers[9])
                    self.m.TMC_motor[int(tmc_registers[0])
                        ].temperatureCoefficient = int(tmc_registers[10])
                    self.m.TMC_motor[int(tmc_registers[0])
                        ].got_registers = True
                    try:
                        self.m.print_tmc_registers(int(tmc_registers[0]))
                    except:
                        log('Could not print TMC registers')
                elif part.startswith('TCAL:M'):
                    [motor_index, all_cal_data] = part[6:].split(':')
                    all_cal_data_list = all_cal_data.strip(',').split(',')
                    try:
                        list(map(int, all_cal_data_list))
                    except:
                        log('ERROR status parse: TCAL registers invalid: ' +
                            message)
                        return
                    self.m.TMC_motor[int(motor_index)
                        ].calibration_dataset_SG_values = [int(i) for i in
                        all_cal_data_list[0:128]]
                    self.m.TMC_motor[int(motor_index)
                        ].calibrated_at_current_setting = int(all_cal_data_list
                        [128])
                    self.m.TMC_motor[int(motor_index)
                        ].calibrated_at_sgt_setting = int(all_cal_data_list
                        [129])
                    self.m.TMC_motor[int(motor_index)
                        ].calibrated_at_toff_setting = int(all_cal_data_list
                        [130])
                    self.m.TMC_motor[int(motor_index)
                        ].calibrated_at_temperature = int(all_cal_data_list
                        [131])
                    self.m.TMC_motor[int(motor_index)
                        ].got_calibration_coefficients = True
                    try:
                        calibration_report_string = (
                            '-------------------------------------' + '\n' +
                            'MOTOR ID: ' + str(int(motor_index)) + '\n' +
                            'Calibration coefficients: ' + str(
                            all_cal_data_list[0:128]) + '\n' +
                            'Current setting: ' + str(self.m.TMC_motor[int(
                            motor_index)].calibrated_at_current_setting) +
                            '\n' + 'SGT setting: ' + str(self.m.TMC_motor[
                            int(motor_index)].calibrated_at_sgt_setting) +
                            '\n' + 'TOFF setting: ' + str(self.m.TMC_motor[
                            int(motor_index)].calibrated_at_toff_setting) +
                            '\n' + 'Calibration temperature: ' + str(self.m
                            .TMC_motor[int(motor_index)].
                            calibrated_at_temperature) + '\n' +
                            '-------------------------------------')
                        list(map(log, calibration_report_string.split('\n')))
                    except:
                        log('Could not print calibration output')
            if self.VERBOSE_STATUS:
                print((self.m_state, self.machine_position.x, self.
                    machine_position.y, self.machine_position.z, self.
                    buffer_info.serial_blocks_available, self.
                    buffer_info.serial_chars_available))
            if self.measure_running_data:
                try:
                    self.running_data.append([int(self.measurement_stage),
                        float(self.machine_position.x), float(self.
                        machine_position.y), float(self.machine_position.z),
                        int(self.stall_guard.x_motor_axis), int(self.
                        stall_guard.y_axis), int(self.stall_guard.y1_motor),
                        int(self.stall_guard.y2_motor), int(self.
                        stall_guard.z_motor_axis), int(self.
                        temperatures.motor_driver), int(self.
                        temperatures.pcb), int(self.
                        temperatures.transistor_heatsink), datetime.now(),
                        int(self.feeds_and_speeds.feed_rate), self.
                        stall_guard.x1_motor, self.stall_guard.x2_motor])
                except:
                    pass
        elif message.startswith('ALARM:'):
            self.grbl_waiting_for_reset = True
            log('ALARM from GRBL: ' + message)
            self.alarm.alert_user(message)
        elif message.startswith('$'):
            log(message)
            setting_and_value = message.split('=')
            setting = setting_and_value[0]
            value = float(setting_and_value[1])
            if setting == '$0':
                self.settings.s0 = value
            elif setting == '$1':
                self.settings.s1 = value
            elif setting == '$2':
                self.settings.s2 = value
            elif setting == '$3':
                self.settings.s3 = value
            elif setting == '$4':
                self.settings.s4 = value
            elif setting == '$5':
                self.settings.s5 = value
            elif setting == '$6':
                self.settings.s6 = value
            elif setting == '$10':
                self.settings.s10 = value
            elif setting == '$11':
                self.settings.s11 = value
            elif setting == '$12':
                self.settings.s12 = value
            elif setting == '$13':
                self.settings.s13 = value
            elif setting == '$20':
                self.settings.s20 = value
            elif setting == '$21':
                self.settings.s21 = value
            elif setting == '$22':
                self.settings.s22 = value
            elif setting == '$23':
                self.settings.s23 = value
            elif setting == '$24':
                self.settings.s24 = value
            elif setting == '$25':
                self.settings.s25 = value
            elif setting == '$26':
                self.settings.s26 = value
            elif setting == '$27':
                self.settings.s27 = value
            elif setting == '$30':
                self.settings.s30 = value
            elif setting == '$31':
                self.settings.s31 = value
            elif setting == '$32':
                self.settings.s32 = value
            elif setting == '$50':
                self.settings.s50 = value
            elif setting == '$51':
                self.settings.s51 = value
            elif setting == '$53':
                self.settings.s53 = value
            elif setting == '$54':
                self.settings.s54 = value
            elif setting == '$100':
                self.settings.s100 = value
            elif setting == '$101':
                self.settings.s101 = value
            elif setting == '$102':
                self.settings.s102 = value
            elif setting == '$110':
                self.settings.s110 = value
                self.sm.get_screen('home'
                    ).common_move_widget.fast_x_speed = value
                self.sm.get_screen('home').common_move_widget.set_jog_speeds()
            elif setting == '$111':
                self.settings.s111 = value
                self.sm.get_screen('home'
                    ).common_move_widget.fast_y_speed = value
                self.sm.get_screen('home').common_move_widget.set_jog_speeds()
            elif setting == '$112':
                self.settings.s112 = value
                self.sm.get_screen('home'
                    ).common_move_widget.fast_z_speed = value
                self.sm.get_screen('home').common_move_widget.set_jog_speeds()
            elif setting == '$120':
                self.settings.s120 = value
            elif setting == '$121':
                self.settings.s121 = value
            elif setting == '$122':
                self.settings.s122 = value
            elif setting == '$130':
                self.settings.s130 = value
                self.m.grbl_x_max_travel = value
                self.m.set_jog_limits()
            elif setting == '$131':
                self.settings.s131 = value
                self.m.grbl_y_max_travel = value
                self.m.set_jog_limits()
            elif setting == '$132':
                self.settings.s132 = value
                self.m.grbl_z_max_travel = value
                self.m.set_jog_limits()
        elif message.startswith('['):
            stripped_message = message.translate(string.maketrans('', ''), '[]'
                )
            if stripped_message.startswith('G28:'):
                pos = stripped_message[4:].split(',')
                self.g28.x = pos[0]
                self.g28.y = pos[1]
                self.g28.z = pos[2]
            elif stripped_message.startswith('G54:'):
                pos = stripped_message[4:].split(',')
                self.g54.x = pos[0]
                self.g54.y = pos[1]
                self.g54_z = pos[2]
            elif self.expecting_probe_result and stripped_message.startswith(
                'PRB'):
                log(stripped_message)
                successful_probe = stripped_message.split(':')[2]
                if successful_probe:
                    z_machine_coord_when_probed = stripped_message.split(':')[1
                        ].split(',')[2]
                    log('Probed at machine height: ' +
                        z_machine_coord_when_probed)
                    self.m.probe_z_detection_event(z_machine_coord_when_probed)
                self.expecting_probe_result = False
            elif stripped_message.startswith('ASM CNC'):
                fw_hw_versions = stripped_message.split(';')
                try:
                    self.versions.firmware = fw_hw_versions[1].split(':')[1]
                    log('FW version: ' + str(self.versions.firmware))
                except:
                    log('Could not retrieve FW version')
                try:
                    self.versions.hardware = fw_hw_versions[2].split(':')[1]
                    log('HW version: ' + str(self.versions.hardware))
                except:
                    log('Could not retrieve HW version')
        elif re.match(self.grbl_initialisation_message, message):
            self.grbl_waiting_for_reset = False

    def check_for_sustained_max_overload(self, dt):
        try:
            if self.overload_state == 100 and sys.platform != 'win32':
                self.m.stop_for_a_stream_pause('spindle_overload')
                self.sm.get_screen('spindle_shutdown'
                    ).reason_for_pause = 'spindle_overload'
                self.sm.get_screen('spindle_shutdown').return_screen = str(self
                    .sm.current)
                self.sm.current = 'spindle_shutdown'
                try:
                    self.sm.get_screen('go').update_overload_peak(self.
                        overload_state)
                except:
                    log('Unable to update overload peak on go screen')
            else:
                self.is_ready_to_assess_spindle_for_shutdown = True
        except:
            log('Could not display spindle overload - are you on diagnostics mode?'
                )

    def check_for_sustained_peak(self, dt):
        if (self.overload_state >= self.prev_overload_state and self.
            overload_state != 100):
            try:
                self.sm.get_screen('go').update_overload_peak(self.
                    prev_overload_state)
            except:
                log('Unable to update overload peak on go screen')
    is_sequential_streaming = False
    _sequential_stream_buffer = []
    _reset_grbl_after_stream = False
    _ready_to_send_first_sequential_stream = False
    _process_oks_from_sequential_streaming = False
    _dwell_time = 0.5
    _dwell_command = 'G4 P' + str(_dwell_time)
    _micro_dwell_command = 'G4 P' + str(0.01)

    def start_sequential_stream(self, list_to_stream,
        reset_grbl_after_stream=False, end_dwell=False):
        self.is_sequential_streaming = True
        log('Start_sequential_stream')
        if reset_grbl_after_stream:
            list_to_stream.append(self._dwell_command)
        elif end_dwell:
            list_to_stream.append(self._micro_dwell_command)
        self._sequential_stream_buffer = list_to_stream
        self._reset_grbl_after_stream = reset_grbl_after_stream
        self._ready_to_send_first_sequential_stream = True

    def _send_next_sequential_stream(self):
        if self._ready_to_send_first_sequential_stream:
            self._ready_to_send_first_sequential_stream = False
            self._process_oks_from_sequential_streaming = True
        if self._sequential_stream_buffer:
            try:
                self.write_direct(self._sequential_stream_buffer[0])
                if self._after_grbl_settings_insert_dwell():
                    self._sequential_stream_buffer[0] = self._dwell_command
                else:
                    del self._sequential_stream_buffer[0]
            except IndexError:
                log('Sequential streaming buffer empty')
                return
        else:
            self._process_oks_from_sequential_streaming = False
            log('Sequential stream ended')
            if self._reset_grbl_after_stream:
                self._reset_grbl_after_stream = False
                self.m._grbl_soft_reset()
                log('GRBL Reset after sequential stream ended')
            self.is_sequential_streaming = False

    def _after_grbl_settings_insert_dwell(self):
        if self._sequential_stream_buffer[0].startswith('$'):
            try:
                if not self._sequential_stream_buffer[1].startswith('$'
                    ) and not self._sequential_stream_buffer[1
                    ] == self._dwell_command:
                    return True
            except:
                return True
        return False

    def cancel_sequential_stream(self, reset_grbl_after_cancel=False):
        self._sequential_stream_buffer = []
        self._process_oks_from_sequential_streaming = False
        self._ready_to_send_first_sequential_stream = False
        if reset_grbl_after_cancel or self._reset_grbl_after_stream:
            self._reset_grbl_after_stream = False
            self.m._grbl_soft_reset()
            print('GRBL Reset after sequential stream cancelled')
        self.is_sequential_streaming = False

    def is_buffer_clear(self):
        if int(self.buffer_info.serial_chars_available
            ) == self.RX_BUFFER_SIZE and int(self.
            buffer_info.serial_blocks_available) == self.GRBL_BLOCK_SIZE:
            return True
        return False

    def write_direct(self, serialCommand, show_in_sys=True, show_in_console
        =True, altDisplayText=None, realtime=False, protocol=False):
        if not serialCommand and not isinstance(serialCommand, str):
            serialCommand = str(serialCommand)
        try:
            if not serialCommand.startswith('?') and not protocol:
                log('> ' + serialCommand)
            if altDisplayText != None:
                log('> ' + str(altDisplayText))
            if show_in_console == True and altDisplayText == None:
                self.sm.get_screen('home'
                    ).gcode_monitor_widget.update_monitor_text_buffer('snd',
                    serialCommand)
            if altDisplayText != None:
                self.sm.get_screen('home'
                    ).gcode_monitor_widget.update_monitor_text_buffer('snd',
                    altDisplayText)
        except:
            log('FAILED to display on CONSOLE: ' + str(serialCommand) +
                ' (Alt text: ' + str(altDisplayText) + ')')
        if self.s:
            try:
                if realtime == True:
                    self.s.write(serialCommand)
                elif realtime == False and protocol == False:
                    self.s.write(serialCommand + '\n')
                elif protocol == True:
                    self.s.write(serialCommand)
                    self.last_protocol_send_time = time.time()
            except:
                try:
                    if not protocol:
                        log('FAILED to write to SERIAL: ' + str(
                            serialCommand) + ' (Alt text: ' + str(
                            altDisplayText) + ')')
                        self.get_serial_screen(
                            'Could not write last command to serial buffer.')
                    else:
                        log('FAILED to write to SERIAL: ' + hex(
                            serialCommand) + ' (Alt text: ' + str(
                            altDisplayText) + ')')
                        self.get_serial_screen(
                            'Could not write last command to serial buffer.')
                except:
                    log('FAILED to write to SERIAL: ' +
                        'unprintable command!' + ' (Alt text: ' + str(
                        altDisplayText) + ')')
                    self.get_serial_screen(
                        'Could not write last command to serial buffer.')
        else:
            try:
                if not protocol:
                    log('No serial! Command lost!: ' + str(serialCommand) +
                        ' (Alt text: ' + str(altDisplayText) + ')')
                    self.get_serial_screen(
                        'Could not write last command to serial buffer.')
                else:
                    log('No serial! Command lost!: ' + hex(serialCommand) +
                        ' (Alt text: ' + str(altDisplayText) + ')')
                    self.get_serial_screen(
                        'Could not write last command to serial buffer.')
            except:
                log('No serial! Command lost!: ' + 'unprintable command!' +
                    ' (Alt text: ' + str(altDisplayText) + ')')
                self.get_serial_screen(
                    'Could not write last command to serial buffer.')

    def write_command(self, serialCommand, **kwargs):
        self.write_command_buffer.append([serialCommand, kwargs])

    def write_realtime(self, serialCommand, altDisplayText=None):
        self.write_realtime_buffer.append([serialCommand, altDisplayText])

    def write_protocol(self, serialCommand, altDisplayText):
        self.write_protocol_buffer.append([serialCommand, altDisplayText])
        return serialCommand
