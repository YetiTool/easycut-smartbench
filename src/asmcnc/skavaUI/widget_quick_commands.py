'''
Created on 1 Feb 2018
@author: Ed
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, FadeTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty # @UnresolvedImport
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.base import runTouchApp
from kivy.clock import Clock
from asmcnc.skavaUI import popup_info

import sys

Builder.load_string("""


<QuickCommands>

    stop_reset_button_image:stop_reset_button_image
    home_image:home_image
    home_button:home_button

    BoxLayout:
        size: self.parent.size
        pos: self.parent.pos      

        padding: 0
        spacing: 10
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
  
        
""")
    
# Valid states types: Idle, Run, Hold, Jog, Alarm, Door, Check, Home, Sleep



class QuickCommands(Widget):



    def __init__(self, **kwargs):
    
        super(QuickCommands, self).__init__(**kwargs)
        self.m=kwargs['machine']
        self.sm=kwargs['screen_manager']
      
    def quit_to_lobby(self):
        self.sm.current = 'lobby'
            
    def home(self):
        self.m.request_homing_procedure('home','home')

    def reset(self):
        self.m.stop_from_quick_command_reset()
    
    def stop(self):
        popup_info.PopupStop(self.m, self.sm)

    def proceed_to_go_screen(self):
        
        # NON-OPTIONAL CHECKS (bomb if non-satisfactory)
        
        # GCode must be loaded.
        # Machine state must be idle.
        # Machine must be homed.
        # Job must be within machine bounds.

        if self.sm.get_screen('home').job_gcode ==[]:
            info = "Before running, a file needs to be loaded. \n\nTap the file chooser in the first tab (top left) to load a file." \

            popup_info.PopupInfo(self.sm, 400, info)

        elif not self.m.state().startswith('Idle'):
            self.sm.current = 'mstate'
                
        elif self.is_job_within_bounds() == False and sys.platform != "win32":                   
            self.sm.current = 'boundary'

        elif self.m.is_machine_homed == False and sys.platform != "win32":
            self.m.request_homing_procedure('home','home')

        elif self.sm.get_screen('home').z_datum_reminder_flag and not self.sm.get_screen('home').has_datum_been_reset:
                z_datum_reminder_message = 'You may need to set a new Z datum\nbefore you start a new job!\n\nPress [b]Ok[/b] to clear this reminder.'
                popup_info.PopupWarning(self.sm, z_datum_reminder_message)
                self.sm.get_screen('home').z_datum_reminder_flag = False

        else:

            # clear to proceed
            self.sm.get_screen('go').job_gcode = self.sm.get_screen('home').job_gcode
            self.sm.get_screen('go').job_filename  = self.sm.get_screen('home').job_filename
            self.sm.get_screen('go').return_to_screen = 'home'
            self.sm.get_screen('go').cancel_to_screen = 'home'
            
            # is fw capable of auto Z lift?
            if self.m.fw_can_operate_zUp_on_pause():
                self.sm.current = 'lift_z_on_pause_or_not'
            else:
                self.sm.current = 'jobstart_warning'



        
    def is_job_within_bounds(self):

        errorfound = 0
        job_box = self.sm.get_screen('home').job_box
        
        # Mins
        
        if -(self.m.x_wco()+job_box.range_x[0]) >= (self.m.grbl_x_max_travel - self.m.limit_switch_safety_distance):
            self.sm.get_screen('boundary').job_box_details.append('[color=#FFFFFF]' + \
            "The job extent over-reaches the X axis at the home end. Try positioning the machine's [b]X datum further away from home[/b]." + '\n\n[/color]')
            errorfound += 1 
        if -(self.m.y_wco()+job_box.range_y[0]) >= (self.m.grbl_y_max_travel - self.m.limit_switch_safety_distance):
            self.sm.get_screen('boundary').job_box_details.append('[color=#FFFFFF]' + \
            "The job extent over-reaches the Y axis at the home end. Try positioning the machine's [b]Y datum further away from home[/b]." + '\n\n[/color]')
            errorfound += 1 
        if -(self.m.z_wco()+job_box.range_z[0]) >= (self.m.grbl_z_max_travel - self.m.limit_switch_safety_distance):
            self.sm.get_screen('boundary').job_box_details.append('[color=#FFFFFF]' + \
            "The job extent over-reaches the Z axis at the lower end. Try positioning the machine's [b]Z datum higher up[/b]." + '\n\n[/color]')
            errorfound += 1 
            
        # Maxs

        if self.m.x_wco()+job_box.range_x[1] >= -self.m.limit_switch_safety_distance:
            self.sm.get_screen('boundary').job_box_details.append('[color=#FFFFFF]' + \
            "The job extent over-reaches the X axis at the far end. Try positioning the machine's [b]X datum closer to home[/b]." + '\n\n[/color]') 
            errorfound += 1 
        if self.m.y_wco()+job_box.range_y[1] >= -self.m.limit_switch_safety_distance:
            self.sm.get_screen('boundary').job_box_details.append('[color=#FFFFFF]' + \
            "The job extent over-reaches the Y axis at the far end. Try positioning the machine's [b]Y datum closer to home[/b]." + '\n\n[/color]') 
            errorfound += 1 
        if self.m.z_wco()+job_box.range_z[1] >= -self.m.limit_switch_safety_distance:
            self.sm.get_screen('boundary').job_box_details.append('[color=#FFFFFF]' + \
            "The job extent over-reaches the Z axis at the upper end. Try positioning the machine's [b]Z datum lower down[/b]." + '\n\n[/color]')
            errorfound += 1 

        if errorfound > 0: return False
        else: return True

        
