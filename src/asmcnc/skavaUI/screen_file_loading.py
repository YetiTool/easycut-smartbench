"""
Created on 25 Feb 2019

@author: Letty

This screen does three things: 
- Reads a file from filechooser into an object passed throughout easycut.
- Prevents the user from clicking on things while a file is loading or being checked. 
- Asks the user to check their file before sending it to the machine
"""
import re
import traceback
from datetime import datetime
from functools import partial

from asmcnc.comms.logging_system.logging_system import Logger
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.properties import (
    NumericProperty,
    StringProperty,
)
from kivy.uix.screenmanager import Screen

from asmcnc.geometry import job_envelope
from asmcnc.skavaUI import popup_info

from asmcnc.core_UI.scaling_utils import get_scaled_sp

Builder.load_string(
    """

<LoadingScreen>:

    check_button:check_button
    home_button:home_button
    filename_label:filename_label
    # warning_title_label:warning_title_label
    warning_body_label:warning_body_label
    usb_status_label:usb_status_label
    
    canvas:
        Color: 
            rgba: hex('#E5E5E5FF')
        Rectangle: 
            size: self.size
            pos: self.pos
             
    BoxLayout:
        orientation: 'vertical'
        padding: 0
        spacing: 0
        size_hint_x: 1

        Label:
            font_size: str(0.01875 * app.width) + 'sp'
            id: usb_status_label
            canvas.before:
                Color:
                    rgba: hex('#333333FF')
                Rectangle:
                    size: self.size
                    pos: self.pos
            size_hint_y: 0.7
            markup: True
            font_size: str(0.0225*app.width) + 'sp'   
            valign: 'middle'
            halign: 'left'
            text_size: self.size
            padding:[dp(0.0125)*app.width, 0]

        BoxLayout: 
            spacing: 0
            padding:[dp(0.025)*app.width, 0, dp(0.025)*app.width, dp(0.0416666666667)*app.height]
            orientation: 'vertical'
            size_hint_y: 7.81
             
            Label:
                id: header_label
                size_hint_y: 0.8
                markup: True
                valign: 'bottom'
                halign: 'center'
                size: self.texture_size
                text_size: self.size
                color: hex('#333333ff')
                font_size: str(0.05*app.width) + 'sp'
                text: root.progress_value          

            Label:
                id: filename_label
                font_size: str(0.025*app.width) + 'sp'
                size_hint_y: 0.5
                markup: True
                valign: 'top'
                halign: 'center'
                size: self.texture_size
                text_size: self.size
                color: hex('#333333ff')
                text: 'Filename here'
                
            Label:
                id: warning_body_label
                font_size: str(0.0275*app.width) + 'sp'
                halign: 'center'
                valign: 'center'
                size_hint_y: 1.7
                markup: True
                size: self.texture_size
                text_size: self.size
                color: hex('#333333ff')

            BoxLayout:
                orientation: 'horizontal'
                padding:[dp(0.025)*app.width, dp(0.0208333333333)*app.height, dp(0.025)*app.width, dp(0.0208333333333)*app.height]
                spacing:0.075*app.width
                size_hint_y: 3

                Button:
                    id: home_button
                    size_hint_x: 1
                    valign: "middle"
                    halign: "center"
                    markup: True
                    font_size: root.default_font_size
                    text_size: self.size
                    background_normal: "./asmcnc/skavaUI/img/blank_blue_btn_2-1_rectangle.png"
                    background_down: "./asmcnc/skavaUI/img/blank_blue_btn_2-1_rectangle.png"
                    background_disabled_normal: "./asmcnc/skavaUI/img/blank_blue_btn_2-1_rectangle.png"
                    border: [dp(30)]*4
                    padding:[dp(0.0375)*app.width, dp(0.0625)*app.height]
                    on_press: root.quit_to_home()

                Button:
                    id: check_button
                    size_hint_x: 1
                    on_press: root.go_to_check_job()
                    valign: "middle"
                    halign: "center"
                    markup: True
                    font_size: root.default_font_size
                    text_size: self.size
                    background_normal: "./asmcnc/skavaUI/img/blank_blue_btn_2-1_rectangle.png"
                    background_down: "./asmcnc/skavaUI/img/blank_blue_btn_2-1_rectangle.png"
                    background_disabled_normal: "./asmcnc/skavaUI/img/blank_blue_btn_2-1_rectangle.png"
                    border: [dp(30)]*4
                    padding:[dp(0.0375)*app.width, dp(0.0625)*app.height]
"""
)
job_cache_dir = "./jobCache/"
job_q_dir = "./jobQ/"


class LoadingScreen(Screen):
    load_value = NumericProperty()
    progress_value = StringProperty()
    objectifile = None
    minimum_spindle_rpm = 3500
    maximum_spindle_rpm = 25000
    minimum_feed_rate = 100
    maximum_feed_rate = 5000
    usb_status = None
    default_font_size = get_scaled_sp("30sp")
    skip_check_decision = False
    continuing_to_recovery = False

    def __init__(self, **kwargs):
        super(LoadingScreen, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.m = kwargs["machine"]
        self.jd = kwargs["job"]
        self.l = kwargs["localization"]

    def on_pre_enter(self):
        self.filename_label.text = self.jd.job_name
        self.update_usb_status()
        self.sm.get_screen("home").gcode_has_been_checked_and_its_ok = False
        self.load_value = 0
        self.update_screen("Getting ready")
        self.jd.job_gcode = []
        Clock.schedule_once(partial(self.objectifiled, self.jd.filename), 0.1)

    def update_usb_status(self):
        if self.usb_status == "connected":
            self.usb_status_label.text = self.l.get_str(
                "USB connected: Please do not remove USB until file is loaded."
            )
            self.usb_status_label.canvas.before.clear()
            with self.usb_status_label.canvas.before:
                Color(76 / 255.0, 175 / 255.0, 80 / 255.0, 1.0)
                Rectangle(
                    pos=self.usb_status_label.pos, size=self.usb_status_label.size
                )
        elif self.usb_status == "ejecting":
            self.usb_status_label.text = (
                self.l.get_str("Ejecting USB: please wait") + "..."
            )
            self.usb_status_label.opacity = 1
            self.usb_status_label.canvas.before.clear()
            with self.usb_status_label.canvas.before:
                Color(51 / 255.0, 51 / 255.0, 51 / 255.0, 1.0)
                Rectangle(
                    pos=self.usb_status_label.pos, size=self.usb_status_label.size
                )
        elif self.usb_status == "ejected":
            self.usb_status_label.text = self.l.get_str("Safe to remove USB.")
            with self.usb_status_label.canvas.before:
                Color(76 / 255.0, 175 / 255.0, 80 / 255.0, 1.0)
                Rectangle(
                    pos=self.usb_status_label.pos, size=self.usb_status_label.size
                )
        else:
            self.usb_status_label.opacity = 0

    def quit_to_home(self):
        self.jd.checked = False
        self.sm.get_screen("home").z_datum_reminder_flag = True
        self.sm.current = "home"

    def return_to_filechooser(self):
        self.jd.job_gcode = []
        self.sm.current = "local_filechooser"

    def go_to_check_job(self):
        self.sm.get_screen("check_job").entry_screen = "file_loading"
        self.sm.current = "check_job"

    def objectifiled(self, job_file_path, dt):
        Logger.info("> LOADING:")
        with open(job_file_path) as f:
            self.job_file_as_list = f.readlines()
        if len(self.job_file_as_list) == 0:
            file_empty_warning = (
                self.l.get_str("File is empty!")
                + "\n\n"
                + self.l.get_str("Please load a different file.")
            )
            # popup_info.PopupError(self.sm, self.l, file_empty_warning)
            self.sm.pm.show_error_popup(file_empty_warning)
            self.sm.current = "local_filechooser"
            return
        self.jd.generate_job_data(self.job_file_as_list)
        self.total_lines_in_job_file_pre_scrubbed = len(self.job_file_as_list)
        self.load_value = 1
        Logger.debug(
            "> Job file loaded as list... "
            + str(self.total_lines_in_job_file_pre_scrubbed)
            + " lines"
        )
        Logger.info("> Scrubbing file...")
        self.preloaded_job_gcode = []
        self.lines_scrubbed = 0
        self.line_threshold_to_pause_and_update_at = self.interrupt_line_threshold
        Clock.schedule_once(self._scrub_file_loop, 0)

    interrupt_line_threshold = 10000
    interrupt_delay = 0.1
    max_lines = 9999990

    def _scrub_file_loop(self, dt):
        try:
            if self.total_lines_in_job_file_pre_scrubbed > self.max_lines:
                Logger.warning("File exceeds 10 million lines!")
                self.update_screen("Could not load - Exceeds 10 million lines")
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

                                # Ensure all rpms are above the minimum
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
                                        self.sm.get_screen(
                                            "check_job"
                                        ).as_low_as = float(feed_rate)
                                if float(feed_rate) > self.maximum_feed_rate:
                                    self.sm.get_screen(
                                        "check_job"
                                    ).flag_max_feed_rate = True
                                    if (
                                        float(feed_rate)
                                        > self.sm.get_screen("check_job").as_high_as
                                    ):
                                        self.sm.get_screen(
                                            "check_job"
                                        ).as_high_as = float(feed_rate)
                            except:
                                Logger.exception(
                                    "Failed to extract feed rate. Probable G-code error!"
                                )
                        if "N" in l_block:
                            l_block = self.jd.remove_line_number(l_block)
                        self.preloaded_job_gcode.append(l_block)
                    self.lines_scrubbed += 1
                self.line_threshold_to_pause_and_update_at += (
                    self.interrupt_line_threshold
                )
                percentage_progress = int(
                    self.lines_scrubbed
                    * 1.0
                    / self.total_lines_in_job_file_pre_scrubbed
                    * 1.0
                    * 100.0
                )
                self.update_screen("Preparing", percentage_progress)
                Clock.schedule_once(self._scrub_file_loop, self.interrupt_delay)
            else:
                Logger.info("> Finished scrubbing " + str(self.lines_scrubbed) + " lines.")
                self.jd.job_gcode = self.preloaded_job_gcode
                self.jd.create_gcode_summary_string()
                self._get_gcode_preview_and_ranges()
        except:
            Logger.exception('Failed to scrub file!')
            self.update_screen("Could not load")
            self.jd.reset_values()

    def _get_gcode_preview_and_ranges(self):
        self.load_value = 2
        self.gcode_preview_widget = self.sm.get_screen("home").gcode_preview_widget
        Logger.info("> get_non_modal_gcode")
        self.gcode_preview_widget.prep_for_non_modal_gcode(
            self.jd.job_gcode, False, self.sm, 0
        )

    def update_screen(self, stage, percentage_progress=0):
        if stage == "Getting ready":
            self.check_button.disabled = True
            self.home_button.disabled = True
            self.check_button.opacity = 0
            self.home_button.opacity = 0
            self.progress_value = self.l.get_str("Getting ready") + "..."
            self.warning_body_label.text = ""
            self.check_button.text = ""
            self.home_button.text = ""
        if stage == "Preparing":
            self.progress_value = (
                self.l.get_str("Preparing file")
                + ": "
                + str(percentage_progress)
                + " %"
            )
        if stage == "Analysing":
            self.progress_value = (
                self.l.get_str("Analysing file")
                + ": "
                + str(percentage_progress)
                + " %"
            )
        if stage == "Loaded":
            if self.continuing_to_recovery:
                self.continuing_to_recovery = False
                self.jd.checked = False
                self.sm.get_screen("home").z_datum_reminder_flag = True
                self.sm.get_screen("homing_decision").return_to_screen = "job_recovery"
                self.sm.get_screen("homing_decision").cancel_to_screen = "job_recovery"
                self.sm.current = "homing_decision"
            if self.skip_check_decision:
                self.skip_check_decision = False
                self.quit_to_home()
            self.progress_value = self.l.get_bold("Job loaded")
            self.warning_body_label.text = (
                self.l.get_bold("WARNING")
                + "[b]:[/b]\n"
                + self.l.get_str(
                    "We strongly recommend error-checking your job before it goes to the machine."
                )
                + "\n"
                + self.l.get_str("Would you like SmartBench to check your job now?")
            )
            self.check_button.text = self.l.get_str("Yes, check my job for errors")
            self.home_button.text = self.l.get_str("No, quit to home")
            self.check_button.disabled = False
            self.home_button.disabled = False
            self.check_button.opacity = 1
            self.home_button.opacity = 1
        if "Could not load" in stage:
            self.progress_value = self.l.get_str("Could not load job")
            self.warning_body_label.text = self.l.get_bold("ERROR") + "[b]:[/b]\n"
            if "Exceeds 10 million lines" in stage:
                self.warning_body_label.text += self.l.get_str(
                    "This file exceeds 10 million lines."
                )
            else:
                self.warning_body_label.text += (
                    self.l.get_str("It was not possible to load your job.")
                    + "\n"
                    + self.l.get_str(
                        "Please double check the file for errors before attempting to re-load it."
                    )
                )
            self.job_gcode = []
            self.loading_file_name = ""
            self.check_button.text = self.l.get_str("Check job")
            self.home_button.text = self.l.get_str("Quit to home")
            self.check_button.disabled = True
            self.home_button.disabled = False
            self.check_button.opacity = 1
            self.home_button.opacity = 1

    def _finish_loading(self, non_modal_gcode_list):
        job_box = job_envelope.BoundingBox()
        job_box.range_x[0] = self.gcode_preview_widget.min_x
        job_box.range_x[1] = self.gcode_preview_widget.max_x
        job_box.range_y[0] = self.gcode_preview_widget.min_y
        job_box.range_y[1] = self.gcode_preview_widget.max_y
        if [self.gcode_preview_widget.min_z, self.gcode_preview_widget.max_z] == [
            999999,
            -999999,
        ]:
            job_box.range_z[0] = 0
            job_box.range_z[1] = 0
        else:
            job_box.range_z[0] = self.gcode_preview_widget.min_z
            job_box.range_z[1] = self.gcode_preview_widget.max_z
        self.sm.get_screen("home").job_box = job_box
        self.sm.get_screen("home").non_modal_gcode_list = non_modal_gcode_list
        self.update_screen("Loaded")
        Logger.info("> END LOAD")
