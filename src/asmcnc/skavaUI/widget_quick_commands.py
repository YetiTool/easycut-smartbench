"""
Created on 1 Feb 2018
@author: Ed
"""

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, FadeTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.base import runTouchApp
from kivy.clock import Clock
from asmcnc.skavaUI import popup_info
from kivy.core.window import Window
import sys, textwrap

Builder.load_string(
    """


<QuickCommands>

    stop_reset_button_image:stop_reset_button_image
    home_image:home_image
    home_button:home_button

    BoxLayout:
        size: self.parent.size
        pos: self.parent.pos      

        padding: 0
        spacing: 0.0208333333333333*app.height
        orientation: "vertical"

        Button:
            size_hint_y: 1
            background_color: hex('#F4433600')
            on_press: root.quit_to_lobby()
            BoxLayout:
                padding: 0
                size: self.parent.size
                pos: self.parent.pos
                Image:
                    source: "./asmcnc/skavaUI/img/quit_to_lobby_btn.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True   

        BoxLayout:
            size_hint_y: 1
            center: self.parent.center
            size: self.parent.size
            pos: self.parent.pos             
            Button:
                id:home_button
#                size_hint: None, None
                center: self.parent.center
    
                background_color: hex('#F4433600')
                on_press: root.home()
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        id: home_image
                        source: "./asmcnc/skavaUI/img/home.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True   

        Button:
            size_hint_y: 1
            background_color: hex('#F4433600')
            on_press: root.reset()
            BoxLayout:
                padding: 0
                size: self.parent.size
                pos: self.parent.pos
                Image:
                    source: "./asmcnc/skavaUI/img/reset.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True   
        
        Button:
            size_hint_y: 1
            background_color: hex('#F4433600')
            on_press:
                root.proceed_to_go_screen()
            BoxLayout:
                padding: 0
                size: self.parent.size
                pos: self.parent.pos
                Image:
                    source: "./asmcnc/skavaUI/img/resume.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True
  
        Button:
            size_hint_y: 1
            background_color: hex('#F4433600')
            on_press: root.stop()
            BoxLayout:
                padding: 0
                size: self.parent.size
                pos: self.parent.pos
                Image:
                    id: stop_reset_button_image
                    source: "./asmcnc/skavaUI/img/stop.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True   
  
        
"""
)


class QuickCommands(Widget):

    def __init__(self, **kwargs):
        self.m = kwargs.pop("machine")
        self.sm = kwargs.pop("screen_manager")
        self.jd = kwargs.pop("job")
        self.l = kwargs.pop("localization")
        super(QuickCommands, self).__init__(**kwargs)

    def quit_to_lobby(self):
        self.sm.current = "lobby"

    def home(self):
        self.m.request_homing_procedure("home", "home")

    def reset(self):
        self.m.stop_from_quick_command_reset()

    def stop(self):
        popup_info.PopupStop(self.m, self.sm, self.l)

    def proceed_to_go_screen(self):
        if self.jd.job_gcode == []:
            info = (
                self.format_command(
                    self.l.get_str("Before running, a file needs to be loaded.")
                )
                + "\n\n"
                + self.format_command(
                    self.l.get_str(
                        "Tap the file chooser in the first tab (top left) to load a file."
                    )
                )
            )
            popup_info.PopupInfo(self.sm, self.l, 450, info)
        elif not self.m.state().startswith("Idle"):
            self.sm.current = "mstate"
        elif not self.is_job_within_bounds() and sys.platform != "win32":
            self.sm.current = "boundary"
        elif not self.m.is_machine_homed and self.m.is_connected:
            self.m.request_homing_procedure("home", "home")
        elif (
            self.sm.get_screen("home").z_datum_reminder_flag
            and not self.sm.get_screen("home").has_datum_been_reset
        ):
            z_datum_reminder_message = (
                self.format_command(
                    self.l.get_str(
                        "You may need to set a new Z datum before you start a new job!"
                    )
                )
                + "\n\n"
                + self.format_command(
                    self.l.get_str("Press Ok to clear this reminder.").replace(
                        self.l.get_str("Ok"), self.l.get_bold("Ok")
                    )
                )
            )
            popup_info.PopupWarning(self.sm, self.l, z_datum_reminder_message)
            self.sm.get_screen("home").z_datum_reminder_flag = False
        else:
            self.jd.screen_to_return_to_after_job = "home"
            self.jd.screen_to_cancel_to_after_job = "home"
            if self.m.is_stylus_enabled == True:
                self.sm.current = "tool_selection"
            else:
                self.m.stylus_router_choice = "router"
                if self.m.fw_can_operate_zUp_on_pause():
                    self.sm.current = "lift_z_on_pause_or_not"
                else:
                    self.sm.current = "jobstart_warning"

    def is_job_within_bounds(self):
        errorfound = 0
        job_box = self.sm.get_screen("home").job_box
        if (
            -(self.m.x_wco() + job_box.range_x[0])
            >= self.m.grbl_x_max_travel - self.m.limit_switch_safety_distance
        ):
            self.sm.get_screen("boundary").job_box_details.append(
                self.l.get_str(
                    "The job extent over-reaches the N axis at the home end."
                ).replace("N", "X")
                + "\n\n"
                + self.l.get_bold(
                    "Try positioning the machine's N datum further away from home."
                ).replace("N", "X")
                + "\n\n"
            )
            errorfound += 1
        if (
            -(self.m.y_wco() + job_box.range_y[0])
            >= self.m.grbl_y_max_travel - self.m.limit_switch_safety_distance
        ):
            self.sm.get_screen("boundary").job_box_details.append(
                self.l.get_str(
                    "The job extent over-reaches the N axis at the home end."
                ).replace("N", "Y")
                + "\n\n"
                + self.l.get_bold(
                    "Try positioning the machine's N datum further away from home."
                ).replace("N", "Y")
                + "\n\n"
            )
            errorfound += 1
        if (
            -(self.m.z_wco() + job_box.range_z[0])
            >= self.m.grbl_z_max_travel - self.m.limit_switch_safety_distance
        ):
            self.sm.get_screen("boundary").job_box_details.append(
                self.l.get_str(
                    "The job extent over-reaches the Z axis at the lower end."
                )
                + "\n\n"
                + self.l.get_bold("Try positioning the machine's Z datum higher up.")
                + "\n\n"
            )
            errorfound += 1
        if self.m.x_wco() + job_box.range_x[1] >= -self.m.limit_switch_safety_distance:
            self.sm.get_screen("boundary").job_box_details.append(
                self.l.get_str(
                    "The job extent over-reaches the N axis at the far end."
                ).replace("N", "X")
                + "\n\n"
                + self.l.get_bold(
                    "Try positioning the machine's N datum closer to home."
                ).replace("N", "X")
                + "\n\n"
            )
            errorfound += 1
        if self.m.y_wco() + job_box.range_y[1] >= -self.m.limit_switch_safety_distance:
            self.sm.get_screen("boundary").job_box_details.append(
                self.l.get_str(
                    "The job extent over-reaches the N axis at the far end."
                ).replace("N", "Y")
                + "\n\n"
                + self.l.get_bold(
                    "Try positioning the machine's N datum closer to home."
                ).replace("N", "Y")
                + "\n\n"
            )
            errorfound += 1
        if self.m.z_wco() + job_box.range_z[1] >= -self.m.limit_switch_safety_distance:
            self.sm.get_screen("boundary").job_box_details.append(
                self.l.get_str(
                    "The job extent over-reaches the Z axis at the upper end."
                )
                + "\n\n"
                + self.l.get_bold("Try positioning the machine's Z datum lower down.")
                + "\n\n"
            )
            errorfound += 1
        if errorfound > 0:
            return False
        else:
            return True

    def format_command(self, cmd):
        wrapped_cmd = textwrap.fill(
            cmd, width=0.0625 * Window.width, break_long_words=False
        )
        return wrapped_cmd
