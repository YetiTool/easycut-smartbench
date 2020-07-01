'''
Created on 19 Aug 2017

@author: Ed
'''
# config

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, StringProperty # @UnresolvedImport
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from __builtin__ import file, True, False
from kivy.clock import Clock, mainthread
from datetime import datetime


import os, sys, time

from asmcnc.skavaUI import widget_virtual_bed, widget_status_bar, widget_z_move, widget_xy_move, widget_common_move, widget_feed_override, widget_speed_override # @UnresolvedImport
from asmcnc.skavaUI import widget_quick_commands, widget_virtual_bed_control, widget_gcode_monitor, widget_network_setup, widget_z_height, popup_stop_press # @UnresolvedImport
from asmcnc.geometry import job_envelope # @UnresolvedImport
from kivy.properties import ObjectProperty, NumericProperty, StringProperty # @UnresolvedImport


# from asmcnc.skavaUI import widget_tabbed_panel


Builder.load_string("""

#:import hex kivy.utils.get_color_from_hex


<GoScreen>:

    status_container:status_container
    z_height_container:z_height_container
    job_progress_container:job_progress_container
    feed_override_container:feed_override_container
    speed_override_container:speed_override_container
    start_or_pause_button_image:start_or_pause_button_image
#     grbl_serial_char_capacity:grbl_serial_char_capacity
#     grbl_serial_line_capacity:grbl_serial_line_capacity
    btn_back: btn_back
    stop_start:stop_start
    file_data_label:file_data_label
    run_time_label:run_time_label
    progress_percentage_label:progress_percentage_label
    btn_back_img:btn_back_img
    overload_status_label:overload_status_label
    spindle_overload_container:spindle_overload_container
    
    BoxLayout:
        padding: 0
        spacing: 10
        orientation: "vertical"

        BoxLayout:
            size_hint_y: 0.9
            padding: 0
            spacing: 10
            orientation: "horizontal"

            BoxLayout:
                size_hint_x: 0.9
                padding: 20
                spacing: 20
                orientation: "horizontal"

                canvas:
                    Color:
                        rgba: hex('#E5E5E5FF')
                    Rectangle:
                        size: self.size
                        pos: self.pos

                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: 0.8
                    spacing: 20

                    BoxLayout:
                        size_hint_y: 0.3
                        padding: 20
                        canvas:
                            Color:
                                rgba: hex('#FFFFFFFF')
                            RoundedRectangle:
                                size: self.size
                                pos: self.pos
                        BoxLayout:
                            orientation: 'horizontal'
                            padding: 0
                            spacing: 10
                            Button:
                                id: btn_back
                                size_hint_x: 1
                                background_color: hex('#F4433600')
                                on_press:
                                    root.return_to_app()
                                BoxLayout:
                                    padding: 0
                                    size: self.parent.size
                                    pos: self.parent.pos
                                    Image:
                                        id: btn_back_img
                                        # source: "./asmcnc/skavaUI/img/back.png"
                                        center_x: self.parent.center_x
                                        y: self.parent.y
                                        size: self.parent.width, self.parent.height
                                        allow_stretch: True
                            
                            Label:
                                size_hint_x: 5
                                text_size: self.size
                                font_size: '20sp'
                                markup: True
                                text: 'Load a file...'
                                halign: 'center'
                                valign: 'middle'
                                id: file_data_label
                                
                            Button:
                                id: stop_start
                                size_hint_x: 1
                                disabled: False
                                background_color: hex('#F4433600')
                                on_release:
                                    self.background_color = hex('#F4433600')
                                on_press:
                                    root.start_or_pause_button_press()
                                    self.background_color = hex('#F44336FF')
                                BoxLayout:
                                    padding: 0
                                    size: self.parent.size
                                    pos: self.parent.pos
                                    Image:
                                        id: start_or_pause_button_image
                                        # source: "./asmcnc/skavaUI/img/go.png"
                                        center_x: self.parent.center_x
                                        y: self.parent.y
                                        size: self.parent.width, self.parent.height
                                        allow_stretch: True

                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: 0.7
                        padding: 00
                        spacing: 20

                        BoxLayout:
                            orientation: 'vertical'
                            padding: 10
                            spacing: 10
                            size_hint_x: 0.2
                            canvas:
                                Color:
                                    rgba: hex('#FFFFFFFF')
                                RoundedRectangle:
                                    size: self.size
                                    pos: self.pos

                            BoxLayout:
                                size_hint_y: 1.5
                                orientation: 'vertical'
                                padding: 00
                                spacing: 00
                                canvas:
                                    Color:
                                        rgba: hex('#FFFFFFFF')
                                    RoundedRectangle:
                                        size: self.size
                                        pos: self.pos
                                Label:
                                    text: '[color=808080]Feed[/color]'
                                    markup: True
                                    font_size: '16px' 
                                    valign: 'middle'
                                    halign: 'center'
                                    size:self.texture_size
                                    text_size: self.size
                                Label:
                                    text: '[color=808080]rate[/color]'
                                    markup: True
                                    font_size: '16px' 
                                    valign: 'middle'
                                    halign: 'center'
                                    size:self.texture_size
                                    text_size: self.size

                            BoxLayout:
                                id: feed_override_container
                                padding: 0
                                size_hint_y: 9
                                canvas:
                                    Color:
                                        rgba: hex('#FFFFFFFF')
                                    RoundedRectangle:
                                        size: self.size
                                        pos: self.pos
    

                        BoxLayout:
                            orientation: 'vertical'
                            padding: 10
                            spacing: 10
                            size_hint_x: 0.2
                            canvas:
                                Color:
                                    rgba: hex('#FFFFFFFF')
                                RoundedRectangle:
                                    size: self.size
                                    pos: self.pos

                            BoxLayout:
                                size_hint_y: 1.5
                                orientation: 'vertical'
                                padding: 00
                                spacing: 00
                                canvas:
                                    Color:
                                        rgba: hex('#FFFFFFFF')
                                    RoundedRectangle:
                                        size: self.size
                                        pos: self.pos
                                Label:
                                    text: '[color=808080]Spindle[/color]'
                                    markup: True
                                    font_size: '16px' 
                                    valign: 'middle'
                                    halign: 'center'
                                    size:self.texture_size
                                    text_size: self.size
                                Label:
                                    text: '[color=808080]speed[/color]'
                                    markup: True
                                    font_size: '16px' 
                                    valign: 'middle'
                                    halign: 'center'
                                    size:self.texture_size
                                    text_size: self.size

                            BoxLayout:
                                id: speed_override_container
                                padding: 0
                                size_hint_y: 9
                                canvas:
                                    Color:
                                        rgba: hex('#FFFFFFFF')
                                    RoundedRectangle:
                                        size: self.size
                                        pos: self.pos
    

                        BoxLayout:
                            id: job_progress_container
                            size_hint_x: 0.8
                            orientation: 'vertical'
                            padding: 20
                            spacing: 00

                            canvas:
                                Color:
                                    rgba: hex('#FFFFFFFF')
                                RoundedRectangle:
                                    size: self.size
                                    pos: self.pos

                            Label:
                                size_hint_y: 1
                                text: '[color=808080]File lines streamed:[/color]'
                                markup: True                           
                                font_size: '16px'
                                valign: 'middle'
                                halign: 'left'
                                size:self.texture_size
                                text_size: self.size 
                            Label:
                                size_hint_y: 3
                                id: progress_percentage_label
                                text: '[color=333333]0[size=70px] %[/size][/color]'
                                markup: True                           
                                font_size: '100px' 
                                valign: 'middle'
                                halign: 'left'
                                size:self.texture_size
                                text_size: self.size 
                            Label:
                                size_hint_y: 1
                                text: '[color=808080]Job time:[/color]'
                                markup: True                           
                                font_size: '16px' 
                                valign: 'middle'
                                halign: 'left'
                                size:self.texture_size
                                text_size: self.size 
                            Label:
                                size_hint_y: 1
                                id: run_time_label
                                text: '[color=333333]99 hours 59 mins 59 secs[/color]'
                                markup: True                           
                                font_size: '20px'
                                valign: 'middle'
                                halign: 'left'
                                size:self.texture_size
                                text_size: self.size 

                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: 0.15
                    padding: 20
                    spacing: 20

                    canvas:
                        Color:
                            rgba: hex('#FFFFFFFF')
                        RoundedRectangle:
                            size: self.size
                            pos: self.pos

                    BoxLayout:
                        size_hint_y: 0.95
                        id: z_height_container


                    BoxLayout:
                        id: spindle_overload_container
                        orientation: 'vertical'
                        size_hint_y: 0.25
                        padding: 00
                        spacing: 10
 
                        Label:
                            halign: 'center'
                            font_size: '16px' 
                            text: '[color=808080]Spindle\\noverload:[/color]'
                            markup: True
                        
                        Label:
                            font_size: '32px' 
                            id: overload_status_label
                            halign: 'center'
                            text: '[color=333333]0 %[/color]'
                            markup: True
                    

#                     BoxLayout:
#                         orientation: 'vertical'
#                         size_hint_y: 0.15
#                         padding: 00
#                         spacing: 00
# 
#                         Label:
#                             text: '[color=808080]Comms buffer:[/color]'
#                             markup: True
# 
#                         BoxLayout:
#                             orientation: 'horizontal'
#                             padding: 00
#                             spacing: 00
# 
#                             Label:
#                                 id: grbl_serial_char_capacity
#                                 text: '[color=808080]A[/color]'
#                                 markup: True
#                             Label:
#                                 id: grbl_serial_line_capacity
#                                 text: '[color=808080]B[/color]'
#                                 markup: True
    

        BoxLayout:
            size_hint_y: 0.08
            id: status_container

""")


def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))


class GoScreen(Screen):

    job_filename = ""
    job_gcode = []

    btn_back = ObjectProperty()
    btn_back_img = ObjectProperty()
    start_or_pause_button_image = ObjectProperty()


    is_job_started_already = False
       
    return_to_screen = 'home' # screen to go to after job runs
    cancel_to_screen = 'home' # screen to go back to before job runs, or set to return to after job started
    loop_for_job_progress = None
    lift_z_on_job_pause = False


    def __init__(self, **kwargs):

        super(GoScreen, self).__init__(**kwargs)

        self.m=kwargs['machine']
        self.sm=kwargs['screen_manager']
        self.job_gcode=kwargs['job']
        
        self.feedOverride = widget_feed_override.FeedOverride(machine=self.m, screen_manager=self.sm)
        self.speedOverride = widget_speed_override.SpeedOverride(machine=self.m, screen_manager=self.sm)

        # Graphics commands
        self.z_height_container.add_widget(widget_z_height.VirtualZ(machine=self.m, screen_manager=self.sm))
        self.feed_override_container.add_widget(self.feedOverride)
        self.speed_override_container.add_widget(self.speedOverride)
        
        # Status bar
        self.status_container.add_widget(widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm))


### PRE-ENTER CONTEXTS: Call one before switching to screen

    def on_pre_enter(self, *args):

        self.sm.get_screen('jobdone').return_to_screen = self.return_to_screen

        # get initial values on screen loading
        self.poll_for_job_progress(0)

        # show overload status if running precision pro
        if self.m.product_code() == '12' or self.sm.get_screen('developer').developer_mode == True: # proxy product code for now
            self.update_overload_label(self.m.s.overload_state)
            self.spindle_overload_container.size_hint_y = 0.25
            self.spindle_overload_container.opacity = 1
        else: 
            self.spindle_overload_container.size_hint_y = 0
            self.spindle_overload_container.opacity = 0




        self.loop_for_job_progress = Clock.schedule_interval(self.poll_for_job_progress, 1)  # then poll repeatedly

        if self.is_job_started_already: 
            pass
        else: 
            self.reset_go_screen_prior_to_job_start()


### COMMON SCREEN PREP METHOD

    def reset_go_screen_prior_to_job_start(self):

        print "RESET GO SCREEN FIRES"

        # Update images
        self.start_or_pause_button_image.source = "./asmcnc/skavaUI/img/go.png"

        #Show back button
        self.btn_back_img.source = "./asmcnc/skavaUI/img/back.png"
        self.btn_back.disabled = False

        # scrape filename title
        if sys.platform == 'win32':
            self.file_data_label.text = "[color=333333]" + self.job_filename.split("\\")[-1] + "[/color]"
        else:
            self.file_data_label.text = "[color=333333]" + self.job_filename.split("/")[-1] + "[/color]"
        
        # Reset flag & light
        self.is_job_started_already = False

        self.m.set_led_colour('BLUE')
        
        self.feedOverride.feed_norm()
        self.speedOverride.feed_norm()


### GENERAL ACTIONS
   
    def start_or_pause_button_press(self):

        log('start/pause button pressed')
        if self.is_job_started_already:
            self._pause_job()
        else:
            self._start_running_job()


    def _pause_job(self):

        self.sm.get_screen('spindle_shutdown').reason_for_pause = "job_pause"
        self.sm.get_screen('spindle_shutdown').return_screen = "go"
        self.sm.current = 'spindle_shutdown'


    def _start_running_job(self):

        self.is_job_started_already = True
        log('Starting job...')
        self.start_or_pause_button_image.source = "./asmcnc/skavaUI/img/pause.png"
        # Hide back button
        self.btn_back_img.source = './asmcnc/skavaUI/img/file_running.png'
        self.btn_back.disabled = True 

        # Vac_fix. Not very tidy but will probably work.
        # Also inject zUp-on-pause code if needed

        with_vac_job_gcode = []

        if self.lift_z_on_job_pause and self.m.fw_can_operate_zUp_on_pause():  # extra 'and' as precaution
            with_vac_job_gcode.append("M56")  #append cleaned up gcode to object
        with_vac_job_gcode.append("AE")  #append cleaned up gcode to object
        with_vac_job_gcode.append("G4 P2")  #append cleaned up gcode to object
        with_vac_job_gcode.extend(self.job_gcode)
        with_vac_job_gcode.append("G4 P2")  #append cleaned up gcode to object
        with_vac_job_gcode.append("AF")  #append cleaned up gcode to object  
        if self.lift_z_on_job_pause and self.m.fw_can_operate_zUp_on_pause():  # extra 'and' as precaution
            with_vac_job_gcode.append("M56 P0")  #append cleaned up gcode to object

        try:
            self.m.s.run_job(with_vac_job_gcode)
            log('Job started ok from go screen...')

        except:
            log('Job start from go screen failed!')


    def return_to_app(self):

        if self.m.fw_can_operate_zUp_on_pause():  # precaution
            self.m.send_any_gcode_command("M56 P0")  # disables Z lift on pause
        self.sm.current = self.cancel_to_screen


### GLOBAL ENTER/LEAVE ACTIONS

    def on_leave(self, *args):

        if self.loop_for_job_progress != None: self.loop_for_job_progress.cancel()

            
### SCREEN UPDATES
    
    def poll_for_job_progress(self, dt):

        # % progress    
        if len(self.job_gcode) != 0:
            percent_thru_job = int(round((self.m.s.g_count * 1.0 / (len(self.job_gcode) + 4) * 1.0)*100.0))
            if percent_thru_job > 100: percent_thru_job = 100
            self.progress_percentage_label.text = "[color=333333]" + str(percent_thru_job) + "[size=70px] %[/size][/color]"

        # Runtime
        if len(self.job_gcode) != 0 and self.m.s.g_count != 0 and self.m.s.stream_start_time != 0: 

            stream_end_time = time.time()
            time_taken_seconds = int(stream_end_time - self.m.s.stream_start_time)
            hours = int(time_taken_seconds / (60 * 60))
            seconds_remainder = time_taken_seconds % (60 * 60)
            minutes = int(seconds_remainder / 60)
            seconds = int(seconds_remainder % 60)
            
            if hours > 0:
                self.run_time_label.text = "[color=333333]" + str(hours) + " hrs " + str(minutes) + " mins " + str(seconds) + " secs" + "[/color]"
            elif minutes > 0:
                self.run_time_label.text = "[color=333333]" + str(minutes) + " mins " + str(seconds) + " secs" + "[/color]"
            else:
                self.run_time_label.text = "[color=333333]" + str(seconds) + " secs" + "[/color]"
        
        else:
            self.run_time_label.text = "[color=333333]" + "Waiting for job to be started" + "[/color]"
            

    # Called from serial_connection if change in state seen
    def update_overload_label(self, state):
        
        if state == 0: self.overload_status_label.text = "[color=4CA82B][b]" + str(state) + "[size=25px] %[/size][b][/color]"
        elif state == 20: self.overload_status_label.text = "[color=E6AA19][b]" + str(state) + "[size=25px] %[/size][/b][/color]"
        elif state == 40: self.overload_status_label.text = "[color=E27A1D][b]" + str(state) + "[size=25px] %[/size][/b][/color]"
        elif state == 60: self.overload_status_label.text = "[color=DE5003][b]" + str(state) + "[size=25px] %[/size][/b][/color]"
        elif state == 80: self.overload_status_label.text = "[color=DE5003][b]" + str(state) + "[size=25px] %[/size][/b][/color]"
        elif state == 90: self.overload_status_label.text = "[color=C11C17][b]" + str(state) + "[size=25px] %[/size][/b][/color]"
        elif state == 100: self.overload_status_label.text = "[color=C11C17][b]" + str(state) + "[size=25px] %[/size][/b][/color]"
        else: log('Overload state not recognised: ' + str(state))



            



        
        
        
