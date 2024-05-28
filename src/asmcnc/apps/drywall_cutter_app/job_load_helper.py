import re
import traceback
from datetime import datetime
from kivy.properties import NumericProperty, StringProperty


def log(message):
    timestamp = datetime.now()
    print(timestamp.strftime("%H:%M:%S.%f")[:12] + " " + message)


"""
Code taken from screen_file_loading.py and modified to be used in the JobLoader class
"""


class JobLoader:
    load_value = NumericProperty()
    progress_value = StringProperty()
    objectifile = None
    minimum_spindle_rpm = 3500
    maximum_spindle_rpm = 25000
    minimum_feed_rate = 100
    maximum_feed_rate = 5000
    usb_status = None
    default_font_size = "30sp"
    skip_check_decision = False
    continuing_to_recovery = False
    interrupt_line_threshold = 10000
    interrupt_delay = 0.1
    max_lines = 9999990

    def __init__(self, **kwargs):
        self.sm = kwargs.pop("screen_manager")
        self.m = kwargs.pop("machine")
        self.jd = kwargs.pop("job")
        self.l = kwargs.pop("localization")

    def load_gcode_file(self, job_file_path):
        log("> LOADING:")
        with open(job_file_path) as f:
            self.job_file_as_list = f.readlines()
        self.jd.generate_job_data(self.job_file_as_list)
        self.total_lines_in_job_file_pre_scrubbed = len(self.job_file_as_list)
        self.load_value = 1
        log(
            "> Job file loaded as list... "
            + str(self.total_lines_in_job_file_pre_scrubbed)
            + " lines"
        )
        log("> Scrubbing file...")
        self.preloaded_job_gcode = []
        self.lines_scrubbed = 0
        self.line_threshold_to_pause_and_update_at = self.interrupt_line_threshold
        self._scrub_file_loop()

    def _scrub_file_loop(self):
        print("scrubbing")
        try:
            if self.total_lines_in_job_file_pre_scrubbed > self.max_lines:
                log("File exceeds 10 million lines!")
                self.jd.reset_values()
                return
            if self.lines_scrubbed < self.total_lines_in_job_file_pre_scrubbed:
                break_threshold = min(
                    self.line_threshold_to_pause_and_update_at,
                    self.total_lines_in_job_file_pre_scrubbed,
                )
                while self.lines_scrubbed < break_threshold:
                    line = self.job_file_as_list[self.lines_scrubbed]
                    l_block = re.sub("\\s|\\(.*?\\)", "", line.strip().upper())
                    if (
                        l_block.find("%") == -1
                        and l_block.find("M6") == -1
                        and l_block.find("M06") == -1
                        and l_block.find("G28") == -1
                        and l_block.find("M30") == -1
                        and l_block.find("M2") == -1
                        and l_block.find("M02") == -1
                    ):
                        if l_block.find("M3") >= 0 or l_block.find("M03") >= 0:
                            self.sm.get_screen("check_job").flag_spindle_off = False
                            if l_block.find("S") >= 0:
                                rpm = int(
                                    float(
                                        l_block[l_block.find("S") + 1 :].split("M")[0]
                                    )
                                )
                                if (
                                    rpm > self.jd.spindle_speed_max
                                    or self.jd.spindle_speed_max == None
                                ):
                                    self.jd.spindle_speed_max = rpm
                                if (
                                    rpm < self.jd.spindle_speed_min
                                    or self.jd.spindle_speed_min == None
                                ):
                                    self.jd.spindle_speed_min = rpm
                                if self.m.spindle_voltage == 110:
                                    rpm = self.m.convert_from_110_to_230(rpm)
                                    l_block = "M3S" + str(rpm)
                                if rpm < self.minimum_spindle_rpm:
                                    l_block = "M3S" + str(self.minimum_spindle_rpm)
                                if rpm > self.maximum_spindle_rpm:
                                    l_block = "M3S" + str(self.maximum_spindle_rpm)
                        elif l_block.find("S0"):
                            l_block = l_block.replace("S0", "")
                        if l_block.find("F") >= 0:
                            try:
                                feed_rate = re.match(
                                    "\\d+", l_block[l_block.find("F") + 1 :]
                                ).group()
                                if (
                                    int(feed_rate) > self.jd.feedrate_max
                                    or self.jd.feedrate_max == None
                                ):
                                    self.jd.feedrate_max = int(feed_rate)
                                if (
                                    int(feed_rate) < self.jd.feedrate_min
                                    or self.jd.feedrate_min == None
                                ):
                                    self.jd.feedrate_min = int(feed_rate)
                                if float(feed_rate) < self.minimum_feed_rate:
                                    self.sm.get_screen(
                                        "check_job"
                                    ).flag_min_feed_rate = True
                                    if (
                                        float(feed_rate)
                                        < self.sm.get_screen("check_job").as_low_as
                                    ):
                                        self.sm.get_screen("check_job").as_low_as = (
                                            float(feed_rate)
                                        )
                                if float(feed_rate) > self.maximum_feed_rate:
                                    self.sm.get_screen(
                                        "check_job"
                                    ).flag_max_feed_rate = True
                                    if (
                                        float(feed_rate)
                                        > self.sm.get_screen("check_job").as_high_as
                                    ):
                                        self.sm.get_screen("check_job").as_high_as = (
                                            float(feed_rate)
                                        )
                            except:
                                print(
                                    "Failed to extract feed rate. Probable G-code error!"
                                )
                        if "N" in l_block:
                            l_block = self.jd.remove_line_number(l_block)
                        self.preloaded_job_gcode.append(l_block)
                    self.lines_scrubbed += 1
                self.line_threshold_to_pause_and_update_at += (
                    self.interrupt_line_threshold
                )
                self._scrub_file_loop()
            else:
                log("> Finished scrubbing " + str(self.lines_scrubbed) + " lines.")
                self.jd.job_gcode = self.preloaded_job_gcode
                self.jd.create_gcode_summary_string()
        except Exception as e:
            print(e)
            log(traceback.format_exc())
            self.jd.reset_values()

    def _get_gcode_preview_and_ranges(self):
        self.load_value = 2
        self.gcode_preview_widget = self.sm.get_screen("home").gcode_preview_widget
        log("> get_non_modal_gcode")
        self.gcode_preview_widget.prep_for_non_modal_gcode(
            self.jd.job_gcode, False, self.sm, 0
        )
