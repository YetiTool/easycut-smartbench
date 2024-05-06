# -*- coding: utf-8 -*-
"""
Created on 25 Feb 2019

@author: Letty

This screen checks the users job, and allows them to review any errors 
"""
from functools import partial

from asmcnc.comms.logging_system.logging_system import Logger
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import (
    StringProperty,
)
from kivy.uix.screenmanager import Screen

from asmcnc.geometry import job_envelope
from asmcnc.skavaUI import widget_gcode_view

ERROR_CODES = {
    "error:1": "G-code words consist of a letter and a value. Letter was not found.",
    "error:2": "Numeric value format is not valid or missing an expected value.",
    "error:3": "Grbl '$' system command was not recognized or supported.",
    "error:4": "Negative value received for an expected positive value.",
    "error:5": "Homing cycle is not enabled via settings.",
    "error:6": "Minimum step pulse time must be greater than 3 microseconds.",
    "error:7": "EEPROM read failed. Reset and restored to default values.",
    "error:8": "Grbl '$' command cannot be used unless Grbl is IDLE. Ensures smooth operation during a job.",
    "error:9": "G-code locked out during alarm or jog state.",
    "error:10": "Soft limits cannot be enabled without homing also enabled.",
    "error:11": "Max characters per line exceeded. Line was not processed and executed.",
    "error:12": "Compile Option Grbl '$' setting value exceeds the maximum step rate supported.",
    "error:13": "Interrupt bar detected as pressed. Check all four contacts at the interrupt bar ends are not pressed. Pressing each switch a few times may clear the contact.",
    "error:14": "Grbl-Mega Only Build info or startup line exceeded EEPROM line length limit.",
    "error:15": "Have you homed the machine yet? If not, please do so now. Jog target exceeds machine travel. Command ignored.",
    "error:16": "Jog command with no '=' or contains prohibited g-code.",
    "error:17": "Laser mode requires PWM output.",
    "error:20": "Unsupported or invalid g-code command found in block.",
    "error:21": "More than one g-code command from same modal group found in block.",
    "error:22": "Feed rate has not yet been set or is undefined.",
    "error:23": "G-code command in block requires an integer value.",
    "error:24": "Two G-code commands that both require the use of the XYZ axis words were detected in the block.",
    "error:25": "A G-code word was repeated in the block.",
    "error:26": "A G-code command implicitly or explicitly requires XYZ axis words in the block, but none were detected.",
    "error:27": "N line number value is not within the valid range of 1 - 9,999,999.",
    "error:28": "A G-code command was sent, but is missing some required P or L value words in the line.",
    "error:29": "Grbl supports six work coordinate systems G54-G59. G59.1, G59.2, and G59.3 are not supported.",
    "error:30": "The G53 G-code command requires either a G0 seek or G1 feed motion mode to be active. A different motion was active.",
    "error:31": "There are unused axis words in the block and G80 motion mode cancel is active.",
    "error:32": "A G2 or G3 arc was commanded but there are no XYZ axis words in the selected plane to trace the arc.",
    "error:33": "The motion command has an invalid target. G2, G3, and G38.2 generates this error, if the arc is impossible to generate or if the probe target is the current position.",
    "error:34": "A G2 or G3 arc, traced with the radius definition, had a mathematical error when computing the arc geometry. Try either breaking up the arc into semi-circles or quadrants, or redefine them with the arc offset definition.",
    "error:35": "A G2 or G3 arc, traced with the offset definition, is missing the IJK offset word in the selected plane to trace the arc.",
    "error:36": "There are unused, leftover G-code words that aren't used by any command in the block.",
    "error:37": "The G43.1 dynamic tool length offset command cannot apply an offset to an axis other than its configured axis. The Grbl default axis is the Z-axis.",
}
Builder.load_string(
    """

<CheckingScreen>:
    
    quit_button:quit_button
    load_file_now_button:load_file_now_button
    # load_file_now_label:load_file_now_label
    check_gcode_button:check_gcode_button
    # check_gcode_label:check_gcode_label
    filename_label:filename_label

    canvas:
        Color: 
            rgba: color_provider.get_rgba("light_grey")
        Rectangle: 
            size: self.size
            pos: self.pos

    BoxLayout:
        orientation: 'vertical'
        padding: 0
        spacing: 0

        BoxLayout:
            size_hint_y: 0.7

        Label:
            id: header_label
            size_hint_y: 1.04
            markup: True
            valign: 'center'
            halign: 'center'
            size: self.texture_size
            text_size: self.size
            color: color_provider.get_rgba("dark_grey")
            font_size: str(0.05*app.width) + 'sp'
            text: root.job_checking_checked

        Label:
            id: filename_label
            size_hint_y: 0.65
            size: self.texture_size
            text_size: self.size
            color: color_provider.get_rgba("dark_grey")
            font_size: str(0.025*app.width) + 'sp'
            halign: 'center'
            valign: 'top'

        BoxLayout:
            orientation: 'horizontal'
            padding: 0
            spacing:0.0833333333333*app.height
            size_hint_y: 6.12

            BoxLayout:
                orientation: 'vertical'
                size_hint_x: 1
                spacing: 0
                padding:[dp(0.025)*app.width, dp(0.0416666666667)*app.height]
                    
                Label:
                    size_hint_y: 3
                    size: self.texture_size
                    text_size: self.size
                    color: color_provider.get_rgba("dark_grey")
                    font_size: str(0.025*app.width) + 'sp'
                    halign: 'center'
                    valign: 'middle'
                    text: root.check_outcome
                    markup: True
                    
                BoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: 1
                    padding:[dp(0.030625)*app.width, 0]

                    Button:
                        id: quit_button
                        on_press: root.quit_to_home()
                        text: root.exit_label
                        background_normal: "./asmcnc/skavaUI/img/next.png"
                        background_down: "./asmcnc/skavaUI/img/next.png"
                        border: [dp(14.5)]*4
                        size_hint: (None,None)
                        width: dp(0.36375*app.width)
                        height: dp(0.164583333333*app.height)
                        font_size: str(0.035*app.width) + 'sp'
                        color: color_provider.get_rgba("near_white")
                        markup: True
                        center: self.parent.center
                        pos: self.parent.pos
            
            BoxLayout:
                size_hint_x: 1
                orientation: 'vertical'
                spacing:0.0104166666667*app.height
                padding:[0, 0, dp(0.025)*app.width, dp(0.0416666666667)*app.height]
                                
                ScrollView:
                    size_hint: 1, 1
                    pos_hint: {'center_x': .5, 'center_y': .5}
                    do_scroll_x: True
                    do_scroll_y: True
                    scroll_type: ['content']
                    
                    RstDocument:
                        text: root.display_output
                        background_color: color_provider.get_rgba("light_grey")
                        base_font_size: str(31.0/800.0*app.width) + 'sp'

                BoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: 0.15
                    spacing:0.0125*app.width
                    
                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        id: load_file_now_button
                        color: color_provider.get_rgba("near_white")
                        markup: True
                        center: self.parent.center
                        pos: self.parent.pos
                        height: self.parent.height
                        on_press: root.load_file_now()
                        background_normal: "./asmcnc/apps/systemTools_app/img/word_button.png"
                        background_down: "./asmcnc/apps/systemTools_app/img/word_button.png"
                        border: [dp(7.5)]*4
                        
                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        id: check_gcode_button
                        color: color_provider.get_rgba("near_white")
                        markup: True
                        center: self.parent.center
                        pos: self.parent.pos
                        height: self.parent.height
                        on_press: root.check_gcode()
                        background_normal: "./asmcnc/apps/systemTools_app/img/word_button.png"
                        background_down: "./asmcnc/apps/systemTools_app/img/word_button.png"
                        border: [dp(7.5)]*4
                             
"""
)


class CheckingScreen(Screen):
    job_checking_checked = StringProperty()
    check_outcome = StringProperty()
    display_output = StringProperty()
    exit_label = StringProperty()
    entry_screen = StringProperty()
    job_ok = False
    error_log = []
    error_out_event = None
    job_box = job_envelope.BoundingBox()
    flag_min_feed_rate = False
    as_low_as = 100
    flag_max_feed_rate = False
    as_high_as = 5000
    flag_spindle_off = True
    serial_function_called = False

    def __init__(self, **kwargs):
        super(CheckingScreen, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.m = kwargs["machine"]
        self.l = kwargs["localization"]
        self.jd = kwargs["job"]
        self.gcode_preview_widget = widget_gcode_view.GCodeView(job=self.jd)
        self.m.s.bind(on_check_job_finished=lambda instance, error_log: self.update_error_log(error_log))

    def on_pre_enter(self):
        self.toggle_boundary_buttons(True)

    def on_enter(self):
        self.job_checking_checked = self.l.get_str("Getting ready") + "..."
        self.m.set_pause(False)
        self.filename_label.text = self.jd.job_name
        self.exit_label = self.l.get_str("Unload job")
        if self.entry_screen == "file_loading":
            try:
                self.boundary_check()
            except:
                self.toggle_boundary_buttons(True)
                self.job_checking_checked = self.l.get_str("Cannot Check Job")
                self.check_outcome = (
                    self.l.get_str("Cannot check job")
                    + ": "
                    + self.l.get_str("Unable to run boundary check on file.")
                    + " "
                    + self.l.get_str("Please make sure file is in recognisable format.")
                )
                self.jd.reset_values()
        else:
            self.try_gcode_check()

    def update_error_log(self, error_log):
        self.error_log = error_log

    def try_gcode_check(self):
        try:
            self.check_gcode()
        except:
            self.toggle_boundary_buttons(True)
            self.job_checking_checked = self.l.get_str("Cannot Check Job")
            self.check_outcome = (
                self.l.get_str("Cannot check job")
                + ": "
                + self.l.get_str("Unable to run g-code check on file.")
                + " "
                + self.l.get_str("Please make sure file is in recognisable format.")
            )
            self.jd.reset_values()

    def boundary_check(self):
        bounds_output = self.is_job_within_bounds()
        if bounds_output == "job is within bounds":
            Logger.debug("In bounds...")
            self.check_outcome = self.l.get_str("Job is within bounds.")
            Clock.schedule_once(lambda dt: self.try_gcode_check(), 0.4)
        else:
            Logger.debug("Out of bounds...")
            self.job_checking_checked = self.l.get_str("Boundary issue!")
            self.toggle_boundary_buttons(False)
            self.check_outcome = (
                self.l.get_str(
                    "The job would exceed the working volume of the machine in one or more axes."
                )
                + "\n\n"
                + self.l.get_str("See help notes (right).")
            )
            self.jd.check_warning = self.l.get_str(
                "The job would exceed the working volume of the machine in one or more axes."
            )
            self.jd.checked = True
            self.write_boundary_output(bounds_output)

    def is_job_within_bounds(self):
        errorfound = 0
        error_message = ""
        job_box = self.sm.get_screen("home").job_box
        if (
            -(self.m.x_wco() + job_box.range_x[0])
            >= self.m.grbl_x_max_travel - self.m.limit_switch_safety_distance
        ):
            error_message = error_message + (
                "\n\n\t"
                + self.l.get_str(
                    "The job extent over-reaches the N axis at the home end."
                ).replace("N", "X")
                + "\n\n\t"
                + self.l.get_bold(
                    "Try positioning the machine's N datum further away from home."
                ).replace("N", "X")
            )
            errorfound += 1
        if (
            -(self.m.y_wco() + job_box.range_y[0])
            >= self.m.grbl_y_max_travel - self.m.limit_switch_safety_distance
        ):
            error_message = error_message + (
                "\n\n\t"
                + self.l.get_str(
                    "The job extent over-reaches the N axis at the home end."
                ).replace("N", "Y")
                + "\n\n\t"
                + self.l.get_bold(
                    "Try positioning the machine's N datum further away from home."
                ).replace("N", "Y")
            )
            errorfound += 1
        if (
            -(self.m.z_wco() + job_box.range_z[0])
            >= self.m.grbl_z_max_travel - self.m.limit_switch_safety_distance
        ):
            error_message = error_message + (
                "\n\n\t"
                + self.l.get_str(
                    "The job extent over-reaches the Z axis at the lower end."
                )
                + "\n\n\t"
                + self.l.get_bold("Try positioning the machine's Z datum higher up.")
            )
            errorfound += 1
        if self.m.x_wco() + job_box.range_x[1] >= -self.m.limit_switch_safety_distance:
            error_message = error_message + (
                "\n\n\t"
                + self.l.get_str(
                    "The job extent over-reaches the N axis at the far end."
                ).replace("N", "X")
                + "\n\n\t"
                + self.l.get_bold(
                    "Try positioning the machine's N datum closer to home."
                ).replace("N", "X")
            )
            errorfound += 1
        if self.m.y_wco() + job_box.range_y[1] >= -self.m.limit_switch_safety_distance:
            error_message = error_message + (
                "\n\n\t"
                + self.l.get_str(
                    "The job extent over-reaches the N axis at the far end."
                ).replace("N", "Y")
                + "\n\n\t"
                + self.l.get_bold(
                    "Try positioning the machine's N datum closer to home."
                ).replace("N", "Y")
            )
            errorfound += 1
        if self.m.z_wco() + job_box.range_z[1] >= -self.m.limit_switch_safety_distance:
            error_message = error_message + (
                "\n\n\t"
                + self.l.get_str(
                    "The job extent over-reaches the Z axis at the upper end."
                )
                + "\n\n\t"
                + self.l.get_bold("Try positioning the machine's Z datum lower down.")
            )
            errorfound += 1
        if errorfound > 0:
            return error_message
        else:
            return "job is within bounds"

    def write_boundary_output(self, bounds_output):
        self.display_output = (
            self.l.get_bold("BOUNDARY CONFLICT HELP")
            + "\n\n"
            + self.l.get_str("It looks like your job exceeds the bounds of the machine")
            + ":\n\n"
            + bounds_output
            + "\n\n"
            + self.l.get_str("The job datum is set in the wrong place.")
            + " "
            + self.l.get_str(
                "Press Adjust datums and then reposition the X, Y or Z datums as suggested above so that the job box is within the machine's boundaries."
            ).replace(self.l.get_str("Adjust datums"), self.l.get_bold("Adjust datums"))
            + " "
            + self.l.get_str(
                "Use the manual move controls and set datum buttons to achieve this."
            ).replace(self.l.get_str("set datum"), self.l.get_bold("set datum"))
            + " "
            + self.l.get_str("You should then reload the job and re-run this check.")
            + "\n\n"
            + self.l.get_str(
                "If you have already tried to reposition the datum, but cannot get the job to fit within the machine bounds, your job may simply be set up incorrectly in your CAD/CAM software."
            )
            + " "
            + self.l.get_str(
                "Common causes include setting the CAD/CAM job datum far away from the actual design, or exporting the job from the CAM software in the wrong units."
            )
            + " "
            + self.l.get_str("Check your design and export settings.")
            + " "
            + self.l.get_str("You should then reload the job and re-run the check.")
            + "\n\n"
            + self.l.get_str(
                "Finally, if you have already tried to reposition the datum, or if the graphics on the job previews do not look normal, your G-code may be corrupt."
            )
            + " "
            + self.l.get_str(
                "If this is the case, you may want to press Check G-code."
            ).replace(self.l.get_str("Check G-code"), self.l.get_bold("Check G-code"))
            + "\n\n"
            + self.l.get_bold("WARNING")
            + "[b]:[/b] "
            + self.l.get_bold(
                "Checking the job's G-code when it is outside of the machine bounds may trigger an alarm screen."
            )
            + "\n\n"
        )

    def toggle_boundary_buttons(self, hide_boundary_buttons):
        if hide_boundary_buttons:
            self.check_gcode_button.text = ""
            self.check_gcode_button.disabled = True
            self.check_gcode_button.opacity = 0
            self.check_gcode_button.size_hint_y = None
            self.check_gcode_button.size_hint_x = None
            self.check_gcode_button.height = "0dp"
            self.check_gcode_button.width = "0dp"
            self.load_file_now_button.text = ""
            self.load_file_now_button.disabled = True
            self.load_file_now_button.opacity = 0
            self.load_file_now_button.size_hint_y = None
            self.load_file_now_button.size_hint_x = None
            self.load_file_now_button.height = "0dp"
            self.load_file_now_button.width = "0dp"
        else:
            self.check_gcode_button.text = self.l.get_str("Check G-code")
            self.check_gcode_button.disabled = False
            self.check_gcode_button.opacity = 1
            self.check_gcode_button.size_hint_y = 1
            self.check_gcode_button.size_hint_x = 1
            self.check_gcode_button.height = "0dp"
            self.check_gcode_button.width = "0dp"
            self.load_file_now_button.text = self.l.get_str("Adjust datums")
            if len(self.load_file_now_button.text) > 30:
                self.load_file_now_button.font_size = str(11.0/800.0*Window.width) + "sp"
            elif len(self.load_file_now_button.text) > 25:
                self.load_file_now_button.font_size = str(14.0/800.0*Window.width) + "sp"
            else:
                self.load_file_now_button.font_size = str(15.0/800.0*Window.width) + "sp"
            self.load_file_now_button.disabled = False
            self.load_file_now_button.opacity = 1
            self.load_file_now_button.size_hint_y = 1
            self.load_file_now_button.size_hint_x = 1
            self.load_file_now_button.height = "0dp"
            self.load_file_now_button.width = "0dp"

    def check_gcode(self):
        self.toggle_boundary_buttons(True)
        if self.m.is_connected():
            self.display_output = ""
            if self.m.state() == "Idle":
                self.job_checking_checked = self.l.get_str("Starting Check") + "..."
                self.check_outcome = self.l.get_str("Looking for gcode errors") + "..."
                Clock.schedule_once(
                    partial(self.check_grbl_stream, self.jd.job_gcode), 0.1
                )
            else:
                self.job_checking_checked = self.l.get_str("Cannot check job")
                self.check_outcome = (
                    self.l.get_str("Cannot check job")
                    + ": "
                    + self.l.get_str("machine is not idle.")
                    + " "
                    + self.l.get_str(
                        "Please ensure machine is in idle state before attempting to reload the file."
                    )
                )
                self.jd.reset_values()
        else:
            self.job_checking_checked = self.l.get_str("Cannot check job")
            self.check_outcome = (
                self.l.get_str("Cannot check job")
                + ": "
                + self.l.get_str("no serial connection.")
                + " "
                + self.l.get_str(
                    "Please ensure your machine is connected, and reload the file."
                )
            )
            self.jd.reset_values()

    loop_for_job_progress = None

    def check_grbl_stream(self, objectifile, dt):
        if self.sm.current == "check_job":
            self.serial_function_called = True
            self.m.s.check_job(objectifile)
            self.loop_for_job_progress = Clock.schedule_interval(
                self.poll_for_gcode_check_progress, 0.6
            )
            self.error_out_event = Clock.schedule_interval(
                partial(self.get_error_log), 0.1
            )

    def poll_for_gcode_check_progress(self, dt):
        percent_thru_job = int(
            round(self.m.s.g_count * 1.0 / (len(self.jd.job_gcode) + 4) * 1.0 * 100.0)
        )
        if percent_thru_job > 100:
            percent_thru_job = 100
        self.job_checking_checked = (
            self.l.get_str("Checking job") + ": " + str(percent_thru_job) + " %"
        )

    def get_error_log(self, dt):
        if self.error_log != []:
            Clock.unschedule(self.error_out_event)
            if self.loop_for_job_progress != None:
                self.loop_for_job_progress.cancel()
            if any("error" in listitem for listitem in self.error_log):
                self.job_checking_checked = self.l.get_str("Errors found!")
                if self.entry_screen == "file_loading":
                    self.check_outcome = (
                        self.l.get_str("Errors found in G-code.")
                        + "\n\n"
                        + self.l.get_str(
                            "Please review your job before attempting to reload it."
                        )
                    )
                    self.jd.check_warning = self.l.get_str("Errors found in G-code.")
                    self.jd.checked = True
                elif self.entry_screen == "home":
                    self.check_outcome = (
                        self.l.get_str("Errors found in G-code.")
                        + "\n\n"
                        + self.l.get_str(
                            "Please review and re-load your job before attempting to run it."
                        )
                    )
                    self.jd.check_warning = self.l.get_str("Errors found in G-code.")
                    self.jd.checked = True
                self.job_ok = False
            elif (
                self.flag_min_feed_rate
                or self.flag_max_feed_rate
                or self.flag_spindle_off
            ):
                self.job_checking_checked = self.l.get_str("Advisories")
                self.check_outcome = (
                    self.l.get_str(
                        "This file will run, but it might not run in the way you expect."
                    )
                    + "\n\n"
                    + self.l.get_str("Please review your job before running it.")
                )
                self.jd.check_warning = self.l.get_str(
                    "This file will run, but it might not run in the way you expect."
                )
                self.jd.checked = True
                self.job_ok = True
                self.sm.get_screen("home").gcode_has_been_checked_and_its_ok = True
            else:
                self.job_checking_checked = self.l.get_str("File is OK!")
                self.check_outcome = self.l.get_str(
                    "No errors found. You're good to go!"
                )
                self.jd.check_warning = self.l.get_str("File is OK!")
                self.jd.checked = True
                self.job_ok = True
                self.sm.get_screen("home").gcode_has_been_checked_and_its_ok = True
            self.write_error_output(self.error_log)
            if self.job_ok == False:
                self.jd.reset_values()
            Logger.info("File has been checked!")
            self.exit_label = self.l.get_str("Finish")

    def write_error_output(self, error_log):
        self.display_output = ""
        if self.flag_spindle_off:
            self.display_output = (
                self.display_output + self.l.get_bold("SPINDLE WARNING") + "\n\n"
            )
            self.display_output = (
                self.display_output
                + self.l.get_str("This file has no command to turn the spindle on.")
                + "\n\n"
                + self.l.get_str(
                    "This may be intended behaviour, but if you are trying to do a cut you should review your file before trying to run it!"
                )
                + "\n\n"
            )
        if self.flag_max_feed_rate or self.flag_min_feed_rate:
            self.display_output = (
                self.display_output + self.l.get_bold("FEED RATE WARNING") + "\n\n"
            )
            if self.flag_min_feed_rate:
                self.display_output = self.display_output + (
                    self.l.get_str(
                        "This file contains feed rate commands as low as N00 mm/min."
                    ).replace("N00", str(self.as_low_as))
                    + "\n\n"
                    + self.l.get_str("The recommended minimum feed rate is 100 mm/min.")
                    + "\n\n"
                )
            if self.flag_max_feed_rate:
                self.display_output = self.display_output + (
                    self.l.get_str(
                        "This file contains feed rate commands as high as N00 mm/min."
                    ).replace("N00", str(self.as_high_as))
                    + "\n\n"
                    + self.l.get_str(
                        "The recommended maximum feed rate is 5000 mm/min."
                    )
                    + "\n\n"
                )
        error_summary = []
        no_empties = list(
            filter(lambda x: x != ("ok", ""), zip(error_log, self.jd.job_gcode))
        )
        for idx, f in enumerate(no_empties):
            if f[0].find("error") != -1:
                error_description = self.l.get_str(ERROR_CODES.get(f[0], ""))
                error_summary.append(
                    self.l.get_bold("Line") + "[b] " + str(idx) + ":[/b]"
                )
                error_summary.append(
                    f[0]
                    .replace(":", " ")
                    .replace("error", self.l.get_str("error"))
                    .capitalize()
                    + ": "
                    + error_description
                    + "\n\n"
                )
                error_summary.append('G-code: "' + f[1] + '"\n\n')
        if error_summary == []:
            self.display_output = self.display_output + ""
        else:
            self.display_output = (
                self.display_output
                + self.l.get_bold("ERROR SUMMARY")
                + "\n\n"
                + "\n\n".join(map(str, error_summary))
            )

    def stop_check_in_serial(self, pass_no):
        check_again = False
        pass_no += 1
        if self.m.s.check_streaming_started:
            if self.m.s.is_job_streaming:
                self.m.s.cancel_stream()
            else:
                check_again = True
        elif pass_no > 2 and self.m.state() == "Check" and not check_again:
            self.m.disable_check_mode()
        if check_again or pass_no < 3:
            Clock.schedule_once(lambda dt: self.stop_check_in_serial(pass_no), 1)

    def quit_to_home(self):
        if self.job_ok:
            self.sm.get_screen("home").z_datum_reminder_flag = True
            self.sm.current = "home"
        else:
            self.jd.reset_values()
            self.sm.current = "home"

    def load_file_now(self):
        self.sm.get_screen("home").z_datum_reminder_flag = True
        self.sm.current = "home"

    def on_pre_leave(self, *args):
        if self.serial_function_called:
            self.stop_check_in_serial(0)
            self.serial_function_called = False
        if self.error_out_event != None:
            Clock.unschedule(self.error_out_event)
        self.job_checking_checked = ""
        self.check_outcome = ""
        self.display_output = ""
        self.job_ok = False
        self.flag_min_feed_rate = False
        self.as_low_as = 100
        self.flag_max_feed_rate = False
        self.as_high_as = 5000
        self.flag_spindle_off = True
        self.error_log = []
        if self.loop_for_job_progress != None:
            self.loop_for_job_progress.cancel()
        self.jd.update_changeables_in_gcode_summary_string()
        self.toggle_boundary_buttons(True)
