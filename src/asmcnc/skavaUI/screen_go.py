'''
Created on 19 Aug 2017

@author: Ed
'''
# config

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty # @UnresolvedImport
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from __builtin__ import file, True
from kivy.clock import Clock, mainthread


import os, sys

from asmcnc.skavaUI import widget_virtual_bed, widget_status_bar,\
    widget_z_move, widget_xy_move, widget_common_move,\
    widget_quick_commands, widget_virtual_bed_control, widget_gcode_monitor,\
    widget_network_setup, widget_z_height, popup_stop_press,\
    widget_feed_override
from asmcnc.geometry import job_envelope
from kivy.properties import ObjectProperty, NumericProperty, StringProperty # @UnresolvedImport


# from asmcnc.skavaUI import widget_tabbed_panel


Builder.load_string("""

#:import hex kivy.utils.get_color_from_hex


<GoScreen>:

    status_container:status_container
    z_height_container:z_height_container
    gcode_path_container:gcode_path_container
    feed_override_container:feed_override_container
    start_stop_button_image:start_stop_button_image
    grbl_serial_char_capacity:grbl_serial_char_capacity
    grbl_serial_line_capacity:grbl_serial_line_capacity
    btn_back: btn_back
    stop_start:stop_start
    btn_pause_play: btn_pause_play
    play_pause_button_image: play_pause_button_image

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
                            padding: 10
                            Button:
                                id: btn_back
                                size_hint_x: 1
                                background_color: hex('#F4433600')
                                on_release:
                                    root.manager.current = 'home'
                                    self.background_color = hex('#F4433600')
                                on_press:
                                    self.background_color = hex('#F44336FF')
                                BoxLayout:
                                    padding: 0
                                    size: self.parent.size
                                    pos: self.parent.pos
                                    Image:
                                        source: "./asmcnc/skavaUI/img/back.png"
                                        center_x: self.parent.center_x
                                        y: self.parent.y
                                        size: self.parent.width, self.parent.height
                                        allow_stretch: True
                            
                            Label:
                                size_hint_x: 5
                                text_size: self.size
                                color: 0,0,0,1
                                markup: True
                                text: 'Load a file...'
                                halign: 'center'
                                valign: 'middle'
                                id: file_data_label
                                text: root.job_filename
                                
                            Button:
                                id: btn_pause_play
                                size_hint_x: 1
                                background_color: hex('#F4433600')
                                on_release:
                                    root.play_pause_button_press()
                                    self.background_color = hex('#F4433600')
                                on_press:
                                    self.background_color = hex('#F44336FF')
                                BoxLayout:
                                    padding: 0
                                    size: self.parent.size
                                    pos: self.parent.pos
                                    Image:
                                        id: play_pause_button_image
                                        source: "./asmcnc/skavaUI/img/pause.png"
                                        center_x: self.parent.center_x
                                        y: self.parent.y
                                        size: self.parent.width, self.parent.height
                                        allow_stretch: True
                            Button:
                                id: stop_start
                                size_hint_x: 1
                                disabled: True
                                background_color: hex('#F4433600')
                                on_release:
                                    root.start_stop_button_press()
                                    self.background_color = hex('#F4433600')
                                on_press:
                                    self.background_color = hex('#F44336FF')
                                BoxLayout:
                                    padding: 0
                                    size: self.parent.size
                                    pos: self.parent.pos
                                    Image:
                                        id: start_stop_button_image
                                        source: "./asmcnc/skavaUI/img/go.png"
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
                            padding: 0
                            size_hint_x: 0.2
                            canvas:
                                Color:
                                    rgba: hex('#FFFFFFFF')
                                RoundedRectangle:
                                    size: self.size
                                    pos: self.pos

                            id: feed_override_container

                        BoxLayout:
                            padding: 0
                            canvas:
                                Color:
                                    rgba: hex('#FFFFFFFF')
                                RoundedRectangle:
                                    size: self.size
                                    pos: self.pos

                            id: gcode_path_container

                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: 0.15
                    padding: 00
                    spacing: 20

                    BoxLayout:
                        padding: 20
                        size_hint_y: 0.95

                        canvas:
                            Color:
                                rgba: hex('#FFFFFFFF')
                            RoundedRectangle:
                                size: self.size
                                pos: self.pos

                        id: z_height_container

                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: 0.05
                        padding: 00
                        spacing: 00
                        Label:
                            id: grbl_serial_char_capacity
                            text: 'A'
                            color: 0,0,0,1
                        Label:
                            id: grbl_serial_line_capacity
                            text: 'B'
                            color: 0,0,0,1


        BoxLayout:
            size_hint_y: 0.08
            id: status_container

""")


class GoScreen(Screen):

    no_image_preview_path = 'asmcnc/skavaUI/img/image_preview_inverted.png'
    job_q_dir = 'jobQ/'            # where file is copied if to be used next in job

    test_property = 0
    btn_back = ObjectProperty()
    no_job = True
    job_filename = StringProperty()
    start_stop_button_press_counter = 0
    paused = False
    started = False
    stopped = False
    

    def __init__(self, **kwargs):

        super(GoScreen, self).__init__(**kwargs)

        self.m=kwargs['machine']
        self.sm=kwargs['screen_manager']
        self.job_gcode=kwargs['job']

        # Graphics commands
        self.z_height_container.add_widget(widget_z_height.VirtualZ(machine=self.m, screen_manager=self.sm))
        self.feed_override_container.add_widget(widget_feed_override.FeedOverride(machine=self.m, screen_manager=self.sm))

        # Status bar
        self.status_container.add_widget(widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm))

        # self.job_gcode = self.sm.get_screen('home').job_gcode       
        
    def on_enter(self, *args):
        self.job_gcode = self.sm.get_screen('home').job_gcode
        self.job_filename = self.sm.get_screen('home').job_filename
        self.btn_pause_play.size_hint_y = None
        self.btn_pause_play.height = '0dp'
        self.paused = False
                        
        if self.job_gcode != []:
            print('Yo')
            print self.no_job
            self.no_job = False
            print self.no_job
            self.stop_start.disabled = False
            
        else:
            self.stop_start.disabled = True


    
    def start_stop_button_press(self):
       
        self.start_stop_button_press_counter += 1
        # self.started = not self.started

        if self.start_stop_button_press_counter == 1:
            self.stream_job()
            self.start_stop_button_image.source = "./asmcnc/skavaUI/img/stop.png"
            #Hide back button
            self.btn_back.size_hint_y = None
            self.btn_back.height = '0dp'
            self.btn_pause_play.size_hint_y = 1
            
        else:
            
            if self.paused == False:
                self.m.hold()
            
            self.m.s.is_job_streaming = False
            popup_stop_press.PopupStop(self.m, self.sm) # POPUP FLAG

    def play_pause_button_press(self):
        
        self.paused = not self.paused
        
        if self.paused == True:
            self.play_pause_button_image.source = "./asmcnc/skavaUI/img/resume.png"
            self.m.hold()
            self.m.s.is_job_streaming = False
            
        if self.paused == False: 
            self.play_pause_button_image.source = "./asmcnc/skavaUI/img/pause.png"
            self.m.resume()
            self.m.s.is_job_streaming = True


    @mainthread
    def reset_go_screen_after_job_finished(self):

        self.start_stop_button_press_counter = 0
        self.start_stop_button_image.source = "./asmcnc/skavaUI/img/go.png"
        self.play_pause_button_image.source = "./asmcnc/skavaUI/img/pause.png"
        #Show back button
        self.btn_back.size_hint_y = 1
        self.btn_pause_play.size_hint_y = None
        self.btn_pause_play.height = '0dp'


    def stream_job(self):
                
        if self.job_gcode:
          
            try:
                self.m.s.run_job(self.job_gcode)
                print('Streaming')
                print(self.job_gcode)
            except:
                print('Stream failed')
                print self.job_gcode
        else:
            print('No file loaded')
