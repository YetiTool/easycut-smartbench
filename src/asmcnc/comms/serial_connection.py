"""
@author archiejarvis on 04/07/2023
"""

import os
import re
import sys
import threading
import time
from datetime import datetime, timedelta

import serial
import serial.tools.list_ports
from kivy.clock import Clock

from asmcnc.comms import serial_classes
from asmcnc.core_UI.sequence_alarm import alarm_manager
from asmcnc.job.yetipilot import yetipilot

import traceback


class SerialConnection:
    # CONSTANTS
    STATUS_INTERVAL: float = 0.1
    BAUD_RATE: int = 115200
    TIMEOUT: int = 6
    WRITE_TIMEOUT: int = 20
    GRBL_BLOCK_SIZE: int = 35
    RX_BUFFER_SIZE: int = 255
    DIGITAL_LOAD_PATTERN = re.compile("Ld:\\d+,\\d+,\\d+,\\d+")
    GRBL_INITIALISATION_MESSAGE = "^Grbl .+ \\['\\$' for help\\]$"
    VALID_GRBL_STATUSES: list[str] = [
        "Idle",
        "Run",
        "Hold",
        "Jog",
        "Alarm",
        "Door",
        "Check",
        "Sleep",
        "Home",
    ]

    # VARIABLES
    port: str = None
    s: serial.Serial = None
    ports_to_try: dict[str] = {}
    next_poll_time: time = None
    last_protocol_send_time: time = None
    grbl_scanner_running: bool = False
    grbl_scanner_thread: threading.Thread = None
    flush_flag: bool = False
    suppress_error_screens: bool = False
    response_log: list = []
    power_loss_detected: bool = False
    overload_state: int = 0
    prev_overload_state: int = None
    is_ready_to_assess_spindle_for_shutdown: bool = True
    expecting_probe_result: bool = False
    grbl_waiting_for_reset: bool = False

    # SEQUENTIAL STREAMING VARIABLES
    _process_oks_from_sequential_streaming: bool = False
    _ready_to_send_first_sequential_stream: bool = False
    _sequential_stream_buffer: list = []
    _dwell_time: float = 0.5
    _dwell_command: str = "G4 P" + str(_dwell_time)
    _micro_dwell_command = "G4 P" + str(0.01)

    is_sequential_streaming: bool = False
    is_job_streaming: bool = False
    is_stream_lines_remaining: bool = False

    g_count: int = 0
    l_count: int = 0
    c_line: list = []

    stream_start_time: time = None
    stream_end_time: time = None
    stream_pause_start_time: time = None
    stream_paused_accumulated_time: time = None

    check_streaming_started: bool = False
    NOT_SKELETON_STUFF: bool = True

    # BUFFERS
    write_command_buffer: list = []
    write_realtime_buffer: list = []
    write_protocol_buffer: list = []

    # DATA CLASSES (probably replace all default values with None)
    machine_position: serial_classes.MachinePosition = serial_classes.MachinePosition(
        0, 0, 0, False, False, False
    )
    work_position: serial_classes.WorkPosition = serial_classes.WorkPosition(0, 0, 0)
    wco: serial_classes.WorkCoordinateOffset = serial_classes.WorkCoordinateOffset(
        0, 0, 0
    )
    buffer_info: serial_classes.BufferInfo = serial_classes.BufferInfo(0, 0, False)
    pin_info: serial_classes.PinInfo = serial_classes.PinInfo(
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
    )
    digital_spindle: serial_classes.DigitalSpindle = serial_classes.DigitalSpindle(
        0, 0, 0, 0, True, 0, 20
    )
    analog_spindle: serial_classes.AnalogSpindle = serial_classes.AnalogSpindle(0)
    feeds_and_speeds: serial_classes.FeedsAndSpeeds = serial_classes.FeedsAndSpeeds(
        0, 0, 0, 0
    )
    temperatures: serial_classes.Temperatures = serial_classes.Temperatures(0, 0, 0)
    voltages: serial_classes.Voltages = serial_classes.Voltages(0, 0, 0, 0)
    stall_guard: serial_classes.StallGuard = serial_classes.StallGuard(
        0, 0, 0, 0, 0, 0, 0, None
    )
    spindle_statistics: serial_classes.SpindleStatistics = (
        serial_classes.SpindleStatistics(0, 0, 0, 0, 0, 0)
    )
    tmc_registers: serial_classes.TMCRegisters = serial_classes.TMCRegisters(
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, False
    )
    settings: serial_classes.Settings = serial_classes.Settings()
    g28: serial_classes.G28 = serial_classes.G28(0, 0, 0)
    g54: serial_classes.G54 = serial_classes.G54(0, 0, 0)
    versions: serial_classes.Versions = serial_classes.Versions("", "")

    # COMMON / GENERAL
    grbl_ln: int = None
    m_state: str = None

    # DEBUG
    measurement_stage: int = None
    measure_running_data: bool = False
    running_data: list = None

    VERBOSE_STATUS: bool = False
    VERBOSE_ALL_RESPONSE: bool = False

    # LAST SENT VARIABLES
    last_sent_motion_mode: int = None
    last_sent_feed: int = None
    last_sent_speed: int = None

    # LAST SENT CONSTANTS
    G_MOTION_PATTERN = re.compile("((?<=G)|(?<=G0))([0-3])((?=\\D)|(?=$))")
    FEED_PATTERN = re.compile("F\\d+\\.?\\d*")
    SPEED_PATTERN = re.compile("S\\d+\\.?\\d*")

    # SPINDLE HEALTH CHECK
    spindle_health_check: bool = False
    spindle_health_check_data: list = []

    # YETIPILOT
    spindle_freeload: int = None
    yp: yetipilot.YetiPilot = None

    def __init__(
        self, machine, screen_manager, settings_manager, localization, job, logger
    ):
        self.m = machine
        self.sm = screen_manager
        self.sett = settings_manager
        self.l = localization
        self.jd = job
        self.logger = logger
        self.alarm = alarm_manager.AlarmSequenceManager(
            self.sm, self.sett, self.m, self.l, self.jd
        )

    def connect(self):
        self.get_ports_to_try()
        self.port = self.get_smartbench_port()

    def write_to_serial(self, message):
        if self.s is not None:
            message = message if isinstance(message, bytes) else message.encode("utf-8")
            self.s.write(message)

    def get_ports_to_try(self):
        # Populate ports_to_try with a list of ports to try for each platform
        if sys.platform == "win32":
            self.ports_to_try["win32"] = [
                port.device
                for port in serial.tools.list_ports.comports()
                if "n/a" not in port.description
            ]
        elif sys.platform == "darwin":
            filesForDevice = os.listdir("/dev/")

            self.ports_to_try["darwin"] = [
                "/dev/" + file for file in filesForDevice if "tty.usbmodem" in file
            ]
        else:
            potential_ports = ["ttyS", "ttyACM", "ttyUSB", "ttyAMA"]

            filesForDevice = os.listdir("/dev/")

            self.ports_to_try[sys.platform] = [
                "/dev/" + file
                for file in filesForDevice
                if any(port in file for port in potential_ports)
            ]

    def get_smartbench_port(self) -> str:
        ports_to_try = self.ports_to_try[sys.platform]

        for port in ports_to_try:
            if self.is_port_smartbench(port):
                return port

        self.logger.critical("Couldn't find SmartBench on any of the ports")
        self.logger.critical("Ports tried: " + str(ports_to_try))

    def is_port_smartbench(self, port) -> bool:
        self.s = serial.Serial(
            port, self.BAUD_RATE, timeout=self.TIMEOUT, write_timeout=self.WRITE_TIMEOUT
        )

        try:
            self.s.close()
            self.s.open()
        except serial.SerialException as e:
            self.logger.error(e)
            return False

        try:
            self.s.flushInput()
            self.write_to_serial("\x18")
            time.sleep(0.1)

            data = self.s.read(self.s.inWaiting())

            if data:
                messages = data.decode("utf-8").split("\n")

                return any("SmartBench" in message for message in messages)
            else:
                return False
        except serial.SerialException as e:
            self.logger.error(e)
            return False

    def start_services(self, dt=None):
        self.logger.info("Starting services")
        self.s.flushInput()

        self.next_poll_time = time.time()
        self.grbl_scanner_running = True

        self.grbl_scanner_thread = threading.Thread(target=self.grbl_scanner)
        self.grbl_scanner_thread.daemon = True
        self.grbl_scanner_thread.start()

        self.m.bootup_sequence()
        self.m.starting_serial_connection = False

    def update_next_poll_time(self):
        self.next_poll_time = time.time() + self.STATUS_INTERVAL

    def write_all_command_buffer(self):
        command_counter = 0
        for command in self.write_command_buffer:
            self.write_direct(*command)
            command_counter += 1
        del self.write_command_buffer[0:command_counter]

    def write_all_realtime_buffer(self):
        realtime_counter = 0
        for realtime_command in self.write_realtime_buffer:
            self.write_direct(
                realtime_command[0], alt_display_text=realtime_command[1], realtime=True
            )
            realtime_counter += 1
        del self.write_realtime_buffer[0:realtime_counter]

    def is_protocol_busy(self) -> bool:
        if self.last_protocol_send_time:
            return self.last_protocol_send_time + 0.05 > time.time()
        return False

    def write_all_protocol_buffer(self):
        if self.write_protocol_buffer and not self.is_protocol_busy():
            self.write_direct(
                self.write_protocol_buffer[0][0],
                protocol=True,
                alt_display_text=self.write_protocol_buffer[0][1],
            )
            del self.write_protocol_buffer[0]

    def grbl_scanner(self, run_grbl_scanner_once=False):
        self.logger.info("Starting GRBL scanner")

        while self.grbl_scanner_running or run_grbl_scanner_once:
            # If flush_flag is set, flush the input buffer
            if self.flush_flag:
                self.s.flushInput()
                self.flush_flag = False

            # If ready to poll, send a '?'
            if self.next_poll_time < time.time():
                self.write_direct(
                    "?", realtime=True, show_in_sys=False, show_in_console=False
                )
                self.update_next_poll_time()

            # Write any commands in the buffers
            self.write_all_command_buffer()
            self.write_all_realtime_buffer()
            self.write_all_protocol_buffer()

            # If there is data in the input buffer, read it
            if self.s.inWaiting():
                try:
                    received = self.s.readline().decode("utf-8").strip()
                except serial.SerialException as e:
                    self.logger.error(e)
                    continue

                # Process data received
                if len(received):
                    if self.VERBOSE_ALL_RESPONSE:
                        self.logger.info(" < " + received)

                    self.sm.get_screen(
                        "home"
                    ).gcode_monitor_widget.update_monitor_text_buffer("rec", received)

                    if received.startswith(("ok", "error")):
                        self.process_grbl_response(received)
                    else:
                        try:
                            self.process_grbl_push(received)
                        except Exception as e:
                            self.logger.error(e)
                            print(traceback.format_exc())

                    if (
                        self.is_job_streaming
                        and not self.m.is_machine_paused
                        and "Alarm" not in self.m.state()
                    ):
                        if (
                            self.is_ready_for_yetipilot()
                            and self.is_status_data_valid_for_yetipilot()
                        ):
                            self.yp.add_status_to_yetipilot(
                                self.digital_spindle.ld_qdA,
                                self.digital_spindle.mains_voltage,
                                self.feeds_and_speeds.feed_override,
                                int(self.feeds_and_speeds.feed_rate),
                            )

                        if self.is_stream_lines_remaining:
                            self.stuff_buffer()
                        elif self.g_count == self.l_count:
                            self.end_stream()

                    if (
                        self._ready_to_send_first_sequential_stream
                        and self.is_buffer_clear()
                    ):
                        self._send_next_sequential_stream()
                run_grbl_scanner_once = False

    def is_buffer_clear(self):
        return (
            int(self.buffer_info.serial_chars_available) == self.RX_BUFFER_SIZE
            and int(self.buffer_info.serial_blocks_available) == self.GRBL_BLOCK_SIZE
        )

    def stuff_buffer(self):
        while self.l_count < len(self.jd.job_gcode_running):
            line_to_go = self.add_line_number_to_gcode_line(
                self.jd.job_gcode_running[self.l_count], self.l_count
            )

            serial_space = self.RX_BUFFER_SIZE - sum(self.c_line)

            if len(line_to_go) + 1 >= serial_space:
                return

            self.scrape_last_sent_modes(line_to_go)

            self.add_to_g_mode_tracker(
                self.last_sent_motion_mode, self.last_sent_feed, self.last_sent_speed
            )

            self.c_line.append(len(line_to_go) + 1)

            self.write_direct(line_to_go, show_in_sys=True, show_in_console=False)

            self.l_count += 1

        self.is_stream_lines_remaining = False

    def end_stream(self):
        self.is_job_streaming = False
        self.is_stream_lines_remaining = False

        self.m.set_pause(False)
        self.set_use_yp(False)

        if self.NOT_SKELETON_STUFF:
            if self.m_state != "Check":
                if (
                    str(self.jd.job_gcode_running).count("M3")
                    > str(self.jd.job_gcode_running).count("M30")
                    and self.m.stylus_router_choice != "stylus"
                ):
                    Clock.schedule_once(lambda dt: self.update_machine_runtime(), 0.4)

                    self.sm.get_screen(
                        "spindle_cooldown"
                    ).return_screen = "job_feedback"
                    Clock.schedule_once(
                        lambda dt: self.raise_screen("spindle_cooldown")
                    )
                else:
                    self.m.spindle_off()
                    time.sleep(0.4)
                    self.update_machine_runtime()
                    Clock.schedule_once(lambda dt: self.raise_screen("job_feedback"))
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

    def update_machine_runtime(self):
        self.stream_end_time = time.time()

        time_taken_seconds = int(self.stream_end_time - self.stream_start_time) + 10

        if not self.stream_paused_accumulated_time:
            self.stream_paused_accumulated_time = 0

        only_running_time_seconds = (
            time_taken_seconds - self.stream_paused_accumulated_time
        )

        self.jd.pause_duration = str(
            timedelta(seconds=self.stream_paused_accumulated_time)
        ).split(".")[0]
        self.jd.total_time = str(timedelta(seconds=time_taken_seconds)).split(".")[0]
        self.jd.actual_runtime = str(
            timedelta(seconds=only_running_time_seconds)
        ).split(".")[0]

        # logs

        if self.m.stylus_router_choice == "router":
            self.m.spindle_brush_use_seconds += only_running_time_seconds

            self.m.write_spindle_brush_values(
                self.m.spindle_brush_use_seconds, self.m.spindle_brush_lifetime_seconds
            )

        self.m.time_since_calibration_seconds += only_running_time_seconds

        self.m.write_calibration_settings(
            self.m.time_since_calibration_seconds,
            self.m.time_to_remind_user_to_calibrate_seconds,
        )

        self.m.time_since_z_head_lubricated_seconds += only_running_time_seconds
        self.m.write_z_head_maintenance_settings(
            self.m.time_since_z_head_lubricated_seconds
        )

        if self.stream_pause_start_time:
            time_without_current_pause = (
                self.stream_pause_start_time
                - self.stream_start_time
                - self.stream_paused_accumulated_time
            )
        else:
            time_without_current_pause = (
                self.stream_start_time - self.stream_paused_accumulated_time
            )

        self._reset_counters()
        return time_without_current_pause

    def _reset_counters(self):
        self.l_count = 0
        self.g_count = 0
        self.c_line[:] = []  # TODO: check if this is correct

        self.stream_pause_start_time = None
        self.stream_paused_accumulated_time = None

        self.stream_start_time = time.time()

        if self.sm.has_screen("go"):
            self.sm.get_screen("go").total_runtime_seconds = 0

    def is_status_data_valid_for_yetipilot(self):
        return (
            self.digital_spindle.ld_qdA >= 0
            and self.grbl_ln is not None
            and self.digital_spindle.mains_voltage >= 0
            and not self.digital_spindle.in_inrush
        )

    def is_ready_for_yetipilot(self):
        return (
            self.is_use_yp()
            and self.m.has_spindle_health_check_passed()
            and self.m.is_using_sc2()
        )

    def write_direct(
        self,
        serial_command,
        show_in_sys=True,
        show_in_console=True,
        alt_display_text=None,
        realtime=False,
        protocol=False,
    ):
        if not serial_command and not isinstance(serial_command, str):
            serial_command = str(serial_command)

        if not protocol:
            if not serial_command.startswith("?"):
                self.logger.info(" >>> " + serial_command)

        if alt_display_text is not None:
            self.logger.info(" >>> " + alt_display_text)

        if show_in_console and alt_display_text is None:
            self.sm.get_screen("home").gcode_monitor_widget.update_monitor_text_buffer(
                "snd", serial_command
            )
        elif alt_display_text is not None:
            self.sm.get_screen("home").gcode_monitor_widget.update_monitor_text_buffer(
                "snd", alt_display_text
            )

        if self.s:
            if realtime:
                self.write_to_serial(serial_command)
            elif not protocol:
                self.write_to_serial(serial_command + "\n")
            else:
                self.write_to_serial(serial_command)
                self.last_protocol_send_time = time.time()

    def raise_error_screen(self):
        self.sm.current = "errorScreen"

    def raise_screen(self, screen_name):
        self.sm.current = screen_name

    def process_grbl_response(self, received):
        if self.suppress_error_screens:
            self.response_log.append(received)

        if received.startswith("error"):
            if not self.suppress_error_screens and self.sm.current != "errorScreen":
                self.sm.get_screen("errorScreen").message = received

                if self.sm.current == "alarmScreen":
                    self.sm.get_screen(
                        "errorScreen"
                    ).return_to_screen = self.sm.get_screen(
                        "alarmScreen"
                    ).return_to_screen
                else:
                    self.sm.get_screen("errorScreen").return_to_screen = self.sm.current

            Clock.schedule_once(lambda dt: self.raise_error_screen(), 0.1)

        if self._process_oks_from_sequential_streaming:
            self._send_next_sequential_stream()
        elif self.is_job_streaming:
            self.g_count += 1

            if self.c_line:
                del self.c_line[0]

    def process_grbl_push(self, message):
        if not isinstance(message, str):
            message = str(message)

        # print

        if message.startswith("<"):
            trans_table = str.maketrans("", "", "<>")
            status_parts = message.translate(trans_table).split("|")

            # Ensure valid status
            if status_parts[0] not in self.VALID_GRBL_STATUSES:
                self.logger.critical("Invalid status received: " + status_parts[0])
                return

            self.m_state = status_parts[0]

            if "|Pn" not in message:
                self.reset_limit_and_misc_parameters()

            # Inrush handling
            if (
                not re.search(self.DIGITAL_LOAD_PATTERN, message)
                or self.digital_spindle.ld_qdA == 0
            ):
                self.digital_spindle.inrush_counter = 0
                self.digital_spindle.in_inrush = True
            elif self.digital_spindle.inrush_counter < self.digital_spindle.inrush_max:
                self.digital_spindle.inrush_counter += 1

            if (
                self.digital_spindle.inrush_counter == self.digital_spindle.inrush_max
                and self.digital_spindle.in_inrush
            ):
                self.digital_spindle.in_inrush = False
                self.logger.info("Spindle no longer in inrush")

            # Read data in
            for part in status_parts:
                if part.startswith("MPos:"):
                    m_pos = part[5:].split(",")

                    self.process_m_pos(m_pos)
                elif part.startswith("WPos:"):
                    w_pos = part[5:].split(",")

                    self.process_w_pos(w_pos)
                elif part.startswith("WCO:"):
                    wco = part[4:].split(",")

                    self.process_wco(wco)
                elif part.startswith("Bf:"):
                    buffer_info = part[3:].split(",")

                    self.process_buffer_info(buffer_info)
                elif part.startswith("Ln:"):
                    grbl_ln = part[3:]

                    if grbl_ln.isdecimal():
                        if self.grbl_ln is None:
                            self.remove_from_g_mode_tracker(int(grbl_ln))
                        else:
                            self.remove_from_g_mode_tracker(int(grbl_ln) - self.grbl_ln)
                        self.grbl_ln = int(grbl_ln)
                elif part.startswith("Pn:"):
                    pin_info = part.split(":")[1]

                    self.process_pin_info(pin_info)
                elif part.startswith("Door") and not self.m.is_machine_paused:
                    if not part.startswith("Door:3"):
                        self.m.set_pause(True)

                        if self.sm.current != "door":
                            # log
                            self.sm.get_screen(
                                "door"
                            ).return_to_screen = self.sm.current
                            Clock.schedule_once(lambda dt: self.raise_screen("door"))
                elif part.startswith("Ld"):
                    spindle_feedback = part.split(":")[1]

                    if "," in spindle_feedback:
                        digital_spindle = spindle_feedback.split(",")

                        self.process_digital_spindle(digital_spindle)
                    else:
                        analog_spindle = spindle_feedback

                        self.process_analog_spindle(analog_spindle)

                    overload_mV_equivalent_state = (
                        self.get_digital_spindle_overload_mV_equivalent_state(
                            self.digital_spindle.kill_time
                        )
                        if "," in spindle_feedback
                        else self.get_analog_spindle_overload_mV_equivalent_state(
                            self.analog_spindle.load_voltage
                        )
                    )

                    self.process_spindle_overload(overload_mV_equivalent_state)
                elif part.startswith("FS:"):
                    feed_speed = part[3:].split(",")

                    self.process_feed_speed(feed_speed)
                elif part.startswith("Ov:"):
                    overrides = part[3:].split(",")

                    self.process_overrides(overrides)
                elif part.startswith("TC:"):
                    temps = part[3:].split(",")

                    self.process_temps(temps)
                elif part.startswith("V:"):
                    voltages = part[2:].split(",")

                    self.process_voltages(voltages)
                elif part.startswith("SG:"):
                    sg_values = part[3:].split(",")

                    self.process_sg_values(sg_values)
                elif part.startswith("SGALARM"):
                    sg_alarm_parts = part[8:].split(",")

                    self.process_sg_alarm_parts(sg_alarm_parts, message)
                elif part.startswith("Sp:"):
                    spindle_statistics = part[3:].split(",")

                    self.process_spindle_statistics(spindle_statistics)
                elif part.startswith("TREG:"):
                    tmc_registers = part[5:].split(",")

                    self.process_tmc_registers(tmc_registers)
                elif part.startswith("TCAL:M"):
                    [motor_index, all_cal_data] = part[6:].split(":")

                    all_cal_data_list = all_cal_data.strip(",").split(",")

                    self.process_tcal_m(all_cal_data_list, int(motor_index))

            # TODO: Rework into flags
            if self.VERBOSE_STATUS:
                log = (
                    self.m_state,
                    self.machine_position.x,
                    self.machine_position.y,
                    self.machine_position.z,
                    self.buffer_info.serial_blocks_available,
                    self.buffer_info.serial_chars_available,
                )
                self.logger.info(log)

            if self.measure_running_data:
                self.store_running_data()

        elif message.startswith("ALARM:"):
            self.grbl_waiting_for_reset = True

            self.alarm.alert_user(message)
        elif message.startswith("$"):
            setting, value = message.split("=", 1)

            self.process_setting(setting, value)
        elif message.startswith("["):
            trans_table = str.maketrans("", "", "[]")

            stripped_message = message.translate(trans_table)

            if stripped_message.startswith("G28"):
                g28 = stripped_message[4:].split(",")

                self.process_g28(g28)
            elif stripped_message.startswith("G54"):
                g54 = stripped_message[4:].split(",")

                self.process_g54(g54)
            elif self.expecting_probe_result and stripped_message.startswith("PRB"):
                successful_probe = stripped_message.split(":")[2]

                self.process_probe_result(successful_probe, stripped_message)
            elif stripped_message.startswith("ASM CNC"):
                fw_hw_versions = stripped_message.split(";")

                self.process_fw_hw_versions(fw_hw_versions)
        elif re.match(self.GRBL_INITIALISATION_MESSAGE, message):
            self.grbl_waiting_for_reset = False

        return True

    def process_m_pos(self, m_pos):
        if len(m_pos) != 3:
            raise ValueError(f"Invalid m_pos ({m_pos})")

        m_pos = [float(i) for i in m_pos]

        self.machine_position.x_change = self.machine_position.x != m_pos[0]
        self.machine_position.y_change = self.machine_position.y != m_pos[1]
        self.machine_position.z_change = self.machine_position.z != m_pos[2]

        self.machine_position.x = m_pos[0]
        self.machine_position.y = m_pos[1]
        self.machine_position.z = m_pos[2]

    def process_w_pos(self, w_pos):
        if len(w_pos) != 3:
            raise ValueError(f"Invalid w_pos ({w_pos})")

        w_pos = [float(i) for i in w_pos]

        self.work_position.x = w_pos[0]
        self.work_position.y = w_pos[1]
        self.work_position.z = w_pos[2]

    def process_wco(self, wco):
        if len(wco) != 3:
            raise ValueError(f"Invalid wco ({wco})")

        wco = [float(i) for i in wco]

        self.wco.x = wco[0]
        self.wco.y = wco[1]
        self.wco.z = wco[2]

    def process_buffer_info(self, buffer_info):
        if len(buffer_info) != 2:
            raise ValueError(f"Invalid buffer_info ({buffer_info})")

        buffer_info = [int(i) for i in buffer_info]

        if self.buffer_info.serial_chars_available != buffer_info[1]:
            self.buffer_info.serial_chars_available = buffer_info[1]
            self.buffer_info.print_buffer_status = True

        if self.buffer_info.serial_blocks_available != buffer_info[0]:
            self.buffer_info.serial_blocks_available = buffer_info[0]
            self.buffer_info.print_buffer_status = True

        if self.buffer_info.print_buffer_status:
            self.buffer_info.print_buffer_status = False

    def process_pin_info(self, pin_info):
        self.pin_info.limit_x = "x" in pin_info
        self.pin_info.limit_X = "X" in pin_info
        self.pin_info.limit_z = "Z" in pin_info

        self.pin_info.probe = "P" in pin_info
        self.pin_info.spare_door = "g" in pin_info
        self.pin_info.dust_shoe_cover = "G" in pin_info

        if "Y" or "y" in pin_info:
            if self.versions.firmware:
                if int(self.versions.firmware.split(".")[0]) < 2:
                    self.pin_info.limit_y = "y" in pin_info
                    self.pin_info.limit_Y = "Y" in pin_info
                else:
                    self.pin_info.limit_Y_axis = "y" in pin_info
                    self.pin_info.stall_Y = "Y" in pin_info
        else:
            self.pin_info.limit_y = False
            self.pin_info.limit_Y = False
            self.pin_info.limit_Y_axis = False
            self.pin_info.stall_Y = False

        self.pin_info.stall_X = "S" in pin_info
        self.pin_info.stall_Z = "z" in pin_info

        if self.pin_info.stall_X or self.pin_info.stall_Y or self.pin_info.stall_Z:
            self.alarm.sg_alarm = True

        if (
            "r" in pin_info
            and not self.power_loss_detected
            and sys.platform not in ["win32", "darwin"]
        ):
            self.m._grbl_door()
            self.sm.get_screen("door").db.send_event(
                2, "Power loss", "Connection loss: Check power and WiFi", 0
            )
            self.m.set_pause(True)
            self.power_loss_detected = True
            Clock.schedule_once(lambda dt: self.m.resume_from_a_soft_door(), 1)

    def process_digital_spindle(self, digital_spindle):
        if len(digital_spindle) != 4:
            raise ValueError(f"Invalid digital_spindle ({digital_spindle})")

        digital_spindle = [int(i) for i in digital_spindle]

        self.digital_spindle.ld_qdA = digital_spindle[0]
        self.digital_spindle.temperature = digital_spindle[1]
        self.digital_spindle.kill_time = digital_spindle[2]
        self.digital_spindle.mains_voltage = digital_spindle[3]

        if self.spindle_health_check and not self.digital_spindle.in_inrush:
            self.spindle_health_check_data.append(digital_spindle[0])

    def process_analog_spindle(self, analog_spindle):
        self.analog_spindle.load_voltage = int(analog_spindle)

    @staticmethod
    def get_analog_spindle_overload_mV_equivalent_state(load_voltage):
        load_voltage = int(load_voltage)
        if load_voltage < 400:
            return 0
        elif load_voltage < 1000:
            return 20
        elif load_voltage < 1500:
            return 40
        elif load_voltage < 2000:
            return 60
        elif load_voltage < 2500:
            return 80
        elif load_voltage >= 2500:
            return 100

    @staticmethod
    def get_digital_spindle_overload_mV_equivalent_state(kill_time):
        kill_time = int(kill_time)
        if kill_time >= 160:
            return 0
        elif kill_time >= 80:
            return 20
        elif kill_time >= 40:
            return 40
        elif kill_time >= 20:
            return 60
        elif kill_time >= 10:
            return 80
        elif kill_time < 10:
            return 100

    def process_spindle_overload(self, overload_mV_equivalent_state):
        if overload_mV_equivalent_state > self.overload_state:
            self.overload_state = overload_mV_equivalent_state

            self.sm.get_screen("go").update_overload_label(overload_mV_equivalent_state)

            if (
                20 <= self.overload_state < 100
                and self.is_ready_to_assess_spindle_for_shutdown
            ):
                self.prev_overload_state = overload_mV_equivalent_state
                Clock.schedule_once(self.check_for_sustained_peak, 1)

        if overload_mV_equivalent_state == 100:
            self.is_ready_to_assess_spindle_for_shutdown = False

            Clock.schedule_once(self.check_for_sustained_max_overload, 0.5)

    def process_feed_speed(self, feed_speed):
        if len(feed_speed) != 2:
            raise ValueError(f"Invalid feed_speed ({feed_speed})")

        feed_speed = [int(i) for i in feed_speed]

        self.feeds_and_speeds.feed_rate = feed_speed[0]
        self.feeds_and_speeds.spindle_speed = feed_speed[1]

    def process_overrides(self, overrides):
        if len(overrides) != 3:
            raise ValueError(f"Invalid overrides ({overrides})")

        overrides = [int(i) for i in overrides]

        self.feeds_and_speeds.feed_override = overrides[0]
        self.feeds_and_speeds.speed_override = overrides[1]

    def process_temps(self, temps):
        if len(temps) != 2 and len(temps) != 3:
            raise ValueError(f"Invalid temps ({temps})")

        if len(temps) >= 2:
            self.temperatures.motor_driver = float(temps[0])
            self.temperatures.pcb = float(temps[1])

        if len(temps) == 3:
            self.temperatures.transistor_heatsink = float(temps[2])

    def process_sg_values(self, sg_values):
        if len(sg_values) < 5:
            raise ValueError(f"Invalid sg_values ({sg_values})")

        self.stall_guard.z_motor_axis = int(sg_values[0])
        self.stall_guard.x_motor_axis = int(sg_values[1])
        self.stall_guard.y_axis = int(sg_values[2])
        self.stall_guard.y1_motor = int(sg_values[3])
        self.stall_guard.y2_motor = int(sg_values[4])

        if len(sg_values) == 7:
            self.stall_guard.x1_motor = int(sg_values[5])
            self.stall_guard.x2_motor = int(sg_values[6])

    def process_voltages(self, voltages):
        if len(voltages) != 4:
            raise ValueError(f"Invalid voltages ({voltages})")

        self.voltages.microcontroller_mV = float(voltages[0])
        self.voltages.LED_mV = float(voltages[1])
        self.voltages.PSU_mV = float(voltages[2])
        self.voltages.spindle_speed_monitor_mV = float(voltages[3])

    def process_sg_alarm_parts(self, sg_alarm_parts, message):
        if len(sg_alarm_parts) != 9:
            raise ValueError(f"Invalid sg_alarm_parts ({sg_alarm_parts})")

        # Argument mismatch in original code - look into
        self.stall_guard.last_stall = serial_classes.LastStall(
            int(sg_alarm_parts[0]),
            int(sg_alarm_parts[1]),
            int(sg_alarm_parts[2]),
            int(sg_alarm_parts[3]),
            int(sg_alarm_parts[4]),
            int(sg_alarm_parts[5]),
            float(sg_alarm_parts[6]),
            float(sg_alarm_parts[7]),
            float(sg_alarm_parts[8]),
            message,
        )

    def process_spindle_statistics(self, spindle_statistics):
        if len(spindle_statistics) != 7:
            raise ValueError(f"Invalid spindle_statistics ({spindle_statistics})")

        self.spindle_statistics.serial_number = int(spindle_statistics[0])
        self.spindle_statistics.production_year = int(spindle_statistics[1])
        self.spindle_statistics.production_week = int(spindle_statistics[2])
        self.spindle_statistics.firmware_version = int(spindle_statistics[3])
        self.spindle_statistics.total_run_time_seconds = int(spindle_statistics[4])
        self.spindle_statistics.brush_run_time_seconds = int(spindle_statistics[5])
        self.spindle_statistics.mains_frequency_hertz = int(spindle_statistics[6])

    def process_tmc_registers(self, tmc_registers):
        if len(tmc_registers) != 11:
            raise ValueError(f"Invalid tmc_registers ({tmc_registers})")

        self.tmc_registers.tmc_0 = int(tmc_registers[0])
        self.tmc_registers.tmc_1 = int(tmc_registers[1])
        self.tmc_registers.tmc_2 = int(tmc_registers[2])
        self.tmc_registers.tmc_3 = int(tmc_registers[3])
        self.tmc_registers.tmc_4 = int(tmc_registers[4])
        self.tmc_registers.tmc_5 = int(tmc_registers[5])
        self.tmc_registers.active_current_scale = int(tmc_registers[6])
        self.tmc_registers.stand_still_current_scale = int(tmc_registers[7])
        self.tmc_registers.stall_guard_alarm_threshold = int(tmc_registers[8])
        self.tmc_registers.max_step_period_us_SG = int(tmc_registers[9])
        self.tmc_registers.temperature_coefficient = int(tmc_registers[10])
        self.tmc_registers.got_registers = True

        self.m.TMC_motor[int(tmc_registers[0])].shadowRegisters[0] = int(
            tmc_registers[1]
        )
        self.m.TMC_motor[int(tmc_registers[0])].shadowRegisters[1] = int(
            tmc_registers[2]
        )
        self.m.TMC_motor[int(tmc_registers[0])].shadowRegisters[2] = int(
            tmc_registers[3]
        )
        self.m.TMC_motor[int(tmc_registers[0])].shadowRegisters[3] = int(
            tmc_registers[4]
        )
        self.m.TMC_motor[int(tmc_registers[0])].shadowRegisters[4] = int(
            tmc_registers[5]
        )
        self.m.TMC_motor[int(tmc_registers[0])].ActiveCurrentScale = int(
            tmc_registers[6]
        )
        self.m.TMC_motor[int(tmc_registers[0])].standStillCurrentScale = int(
            tmc_registers[7]
        )
        self.m.TMC_motor[int(tmc_registers[0])].stallGuardAlarmThreshold = int(
            tmc_registers[8]
        )
        self.m.TMC_motor[int(tmc_registers[0])].max_step_period_us_SG = int(
            tmc_registers[9]
        )
        self.m.TMC_motor[int(tmc_registers[0])].temperatureCoefficient = int(
            tmc_registers[10]
        )
        self.m.TMC_motor[int(tmc_registers[0])].got_registers = True

    # doesn't currently store anything (to a dataclass)
    def process_tcal_m(self, tcal_m, motor_index):
        if len(tcal_m) != 132:
            raise ValueError(f"Invalid tcal_m ({tcal_m})")

        self.m.TMC_motor[motor_index].calibration_dataset_SG_values = [
            int(i) for i in tcal_m[0:128]
        ]
        self.m.TMC_motor[motor_index].calibrated_at_current_setting = int(tcal_m[128])
        self.m.TMC_motor[motor_index].calibrated_at_sgt_setting = int(tcal_m[129])
        self.m.TMC_motor[motor_index].calibrated_at_toff_setting = int(tcal_m[130])
        self.m.TMC_motor[motor_index].calibrated_at_temperature = int(tcal_m[131])
        self.m.TMC_motor[motor_index].got_calibration_coefficients = True

        calibration_report_string = (
            "-------------------------------------"
            + "\n"
            + "MOTOR ID: "
            + str(int(motor_index))
            + "\n"
            + "Calibration coefficients: "
            + str(tcal_m[0:128])
            + "\n"
            + "Current setting: "
            + str(self.m.TMC_motor[motor_index].calibrated_at_current_setting)
            + "\n"
            + "SGT setting: "
            + str(self.m.TMC_motor[motor_index].calibrated_at_sgt_setting)
            + "\n"
            + "TOFF setting: "
            + str(self.m.TMC_motor[motor_index].calibrated_at_toff_setting)
            + "\n"
            + "Calibration temperature: "
            + str(self.m.TMC_motor[motor_index].calibrated_at_temperature)
            + "\n"
            + "-------------------------------------"
        )

        # TODO: Rework this logging_system to not use print
        map(print, calibration_report_string.split("\n"))

    def process_fw_hw_versions(self, fw_hw_versions):
        if len(fw_hw_versions) != 3:
            raise ValueError(f"Invalid fw_hw_versions ({fw_hw_versions})")

        fw_version = fw_hw_versions[1].split(":")[1]
        hw_version = fw_hw_versions[2].split(":")[1]

        self.versions.firmware = fw_version
        self.versions.hardware = hw_version

    def process_probe_result(self, successful_probe, stripped_message):
        if successful_probe:
            z_machine_coord_when_probed = stripped_message.split(":")[1].split(",")[2]

            self.m.probe_z_detection_event(z_machine_coord_when_probed)
        self.expecting_probe_result = False

    def process_g28(self, g28):
        if len(g28) != 3:
            raise ValueError(f"Invalid g28 ({g28})")

        g28 = [float(i) for i in g28]

        self.g28.x = float(g28[0])
        self.g28.y = float(g28[1])
        self.g28.z = float(g28[2])

    def process_g54(self, g54):
        if len(g54) != 3:
            raise ValueError(f"Invalid g54 ({g54})")

        g54 = [float(i) for i in g54]

        self.g54.x = float(g54[0])
        self.g54.y = float(g54[1])
        self.g54.z = float(g54[2])

    def process_setting(self, setting, value):
        setting_num = int(setting[1:])

        # should these be float or int?
        value = float(value)
        self.settings.store_variable(setting_num, value)

        if setting_num == 110:
            self.sm.get_screen("home").common_move_widget.fast_x_speed = value
            self.sm.get_screen("home").common_move_widget.set_jog_speeds()
        elif setting_num == 111:
            self.sm.get_screen("home").common_move_widget.fast_y_speed = value
            self.sm.get_screen("home").common_move_widget.set_jog_speeds()
        elif setting_num == 112:
            self.sm.get_screen("home").common_move_widget.fast_z_speed = value
            self.sm.get_screen("home").common_move_widget.set_jog_speeds()
        elif setting_num == 130:
            self.m.grbl_x_max_travel = value
            self.m.set_jog_limits()
        elif setting_num == 131:
            self.m.grbl_y_max_travel = value
            self.m.set_jog_limits()
        elif setting_num == 132:
            self.m.grbl_z_max_travel = value
            self.m.set_jog_limits()

    def store_running_data(self):
        self.running_data.append(
            [
                self.measurement_stage,
                self.machine_position.x,
                self.machine_position.y,
                self.machine_position.z,
                self.stall_guard.x_motor_axis,
                self.stall_guard.y_axis,
                self.stall_guard.z_motor_axis,
                self.temperatures.motor_driver,
                self.temperatures.pcb,
                self.temperatures.transistor_heatsink,
                datetime.now(),
                self.feeds_and_speeds.feed_rate,
                self.stall_guard.x1_motor,
                self.stall_guard.x2_motor,
            ]
        )

    def reset_limit_and_misc_parameters(self):
        self.pin_info.limit_x = False
        self.pin_info.limit_X = False
        self.pin_info.limit_y = False
        self.pin_info.limit_Y = False
        self.pin_info.limit_z = False
        self.pin_info.limit_Y_axis = False

        self.pin_info.probe = False
        self.pin_info.dust_shoe_cover = False
        self.pin_info.spare_door = False

        self.pin_info.stall_X = False
        self.pin_info.stall_Y = False
        self.pin_info.stall_Z = False

    def _send_next_sequential_stream(self):
        if self._ready_to_send_first_sequential_stream:
            self._ready_to_send_first_sequential_stream = False
            self._process_oks_from_sequential_streaming = True

        if self._sequential_stream_buffer:
            self.write_direct(self._sequential_stream_buffer[0])

            if self._after_grbl_settings_insert_dwell():
                self._sequential_stream_buffer[0] = self._dwell_command
            else:
                del self._sequential_stream_buffer[0]
        else:
            self._process_oks_from_sequential_streaming = False
            if self._reset_grbl_after_stream:
                self._reset_grbl_after_stream = False
                self.m._grbl_soft_reset()
            self.is_sequential_streaming = False

    def _after_grbl_settings_insert_dwell(self):
        if self._sequential_stream_buffer:
            if self._sequential_stream_buffer[0].startswith("$"):
                return True
        return False

    def add_line_number_to_gcode_line(self, line, i):
        return line if self.gcode_line_is_excluded(line) else "N" + str(i) + line

    @staticmethod
    def gcode_line_is_excluded(line):
        return (
            "(" in line
            or ")" in line
            or "$" in line
            or "AE" in line
            or "AF" in line
            or "*L" in line
        )

    def scrape_last_sent_modes(self, line_to_go):
        self.last_sent_motion_mode = self.get_grbl_mode(
            line_to_go, self.G_MOTION_PATTERN, self.last_sent_motion_mode
        )

        self.last_sent_feed = self.get_grbl_float(
            line_to_go, self.FEED_PATTERN, self.last_sent_feed
        )

        self.last_sent_speed = self.get_grbl_float(
            line_to_go, self.SPEED_PATTERN, self.last_sent_speed
        )

    @staticmethod
    def get_grbl_float(line_to_go, pattern, last_sent):
        match_obj = re.search(pattern, line_to_go)
        return float(match_obj.group()[1:]) if match_obj else last_sent

    @staticmethod
    def get_grbl_mode(line_to_go, pattern, last_sent):
        match_obj = re.search(pattern, line_to_go)
        return int(match_obj.group()) if match_obj else last_sent

    def add_to_g_mode_tracker(
        self, last_sent_motion_mode, last_sent_feed, last_sent_speed
    ):
        self.jd.grbl_mode_tracker += (
            (last_sent_motion_mode, last_sent_feed, last_sent_speed),
        )

    def set_use_yp(self, use_yp):
        if self.yp:
            self.yp.use_yp = use_yp

    def is_use_yp(self):
        if self.yp:
            return self.yp.use_yp
        return False

    def remove_from_g_mode_tracker(self, line_diff):
        if line_diff:
            del self.jd.grbl_mode_tracker[:line_diff]

    def check_for_sustained_peak(self, dt=None):
        if (
            self.overload_state >= self.prev_overload_state
            and self.overload_state != 100
        ):
            self.sm.get_screen("go").update_overload_peak(self.prev_overload_state)

    def check_for_sustained_max_overload(self, dt=None):
        if self.overload_state == 100 and sys.platform != "win32":
            self.m.stop_for_a_stream_pause("spindle_overload")
            self.sm.get_screen("spindle_shutdown").reason_for_pause = "spindle_overload"
            self.sm.get_screen("spindle_shutdown").return_screen = self.sm.current
            Clock.schedule_once(lambda dt: self.raise_screen("spindle_shutdown"))

            self.sm.get_screen("go").update_overload_peak(self.overload_state)
        else:
            self.is_ready_to_assess_spindle_for_shutdown = True

    def write_command(self, serialCommand, **kwargs):
        self.write_command_buffer.append([serialCommand, kwargs])

    def write_realtime(self, serialCommand, altDisplayText=None):
        self.write_realtime_buffer.append([serialCommand, altDisplayText])

    def write_protocol(self, serialCommand, altDisplayText):
        self.write_protocol_buffer.append([serialCommand, altDisplayText])
        return serialCommand

    def is_connected(self):
        return self.s and self.s.is_open

    def start_sequential_stream(
        self, list_to_stream, reset_grbl_after_stream=False, end_dwell=False
    ):
        self.is_sequential_streaming = True
        print("Start_sequential_stream")
        if reset_grbl_after_stream:
            list_to_stream.append(self._dwell_command)
        elif end_dwell:
            list_to_stream.append(self._micro_dwell_command)
        self._sequential_stream_buffer = list_to_stream
        self._reset_grbl_after_stream = reset_grbl_after_stream
        self._ready_to_send_first_sequential_stream = True

    def cancel_sequential_stream(self, reset_grbl_after_cancel=False):
        self._sequential_stream_buffer = []
        self._process_oks_from_sequential_streaming = False
        self._ready_to_send_first_sequential_stream = False
        if reset_grbl_after_cancel or self._reset_grbl_after_stream:
            self._reset_grbl_after_stream = False
            self.m._grbl_soft_reset()
            print("GRBL Reset after sequential stream cancelled")
        self.is_sequential_streaming = False

    def check_job(self, job_object):
        self.m.enable_check_mode()
        self.set_use_yp(False)

        def check_job_inner_function():
            if self.m_state == "Check":
                self.check_streaming_started = True
                self.suppress_error_screens = True
                self.response_log = []
                self.run_job(job_object)
                Clock.schedule_interval(
                    lambda dt: self.return_check_outcome(job_object), 0.1
                )
            else:
                Clock.schedule_once(lambda dt: check_job_inner_function(), 0.9)

        Clock.schedule_once(lambda dt: check_job_inner_function(), 0.9)

    def return_check_outcome(self, job_object):
        if len(self.response_log) >= job_object:
            self.suppress_error_screens = False
            self.sm.get_screen("check_job").error_log = self.response_log
            return False

    def reset_job_info(self):
        self.grbl_ln = None
        self.jd.grbl_mode_tracker = []

    def run_job(self, job_object):
        self.reset_job_info()
        self.jd.job_gcode_running = job_object

        if self.initialise_job() and self.jd.job_gcode_running:
            Clock.schedule_once(lambda dt: self.set_streaming_flags_to_true(), 2)
        elif not self.jd.job_gcode_running:
            self.sm.get_screen("go").reset_go_screen_prior_to_job_start()

    def initialise_job(self):
        if self.m_state != "Check":
            self.m.set_led_colour("GREEN")
            self.m.zUp()

        self.flush_flag = True
        self.NOT_SKELETON_STUFF = True
        time.sleep(0.1)
        self._reset_counters()
        return True

    def run_skeleton_buffer_stuffer(self, job_object):
        self.reset_job_info()
        self.jd.job_gcode_running = job_object

        self.m.set_pause(False)
        self.flush_flag = True
        self.NOT_SKELETON_STUFF = False
        time.sleep(0.1)

        self._reset_counters()
        if self.jd.job_gcode_running:
            Clock.schedule_once(lambda dt: self.set_streaming_flags_to_true(), 2)

    def set_streaming_flags_to_true(self):
        self.is_stream_lines_remaining = True
        self.is_job_streaming = True
