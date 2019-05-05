'''
Created on 19 Aug 2017

@author: Ed
'''
# config

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty  # @UnresolvedImport
from kivy.uix.widget import Widget
from kivy.clock import Clock

import sys, os
from os.path import expanduser
from shutil import copy
from asmcnc.comms import usb_storage

Builder.load_string("""

<TemplateScreen>:

    carousel:carousel

    BoxLayout:
        padding: 20
        spacing: 20
        size: root.size
        pos: root.pos
        orientation: "vertical"

        BoxLayout:
            size_hint_y: 1
            orientation: 'horizontal'
            size: self.parent.size
            pos: self.parent.pos
            padding: 15

            canvas.before:
                Color: 
                    rgba: 1,1,1,1
                RoundedRectangle: 
                    size: self.size
                    pos: self.pos

            Label:
                size_hint_x: 1
                text: 'Bit dia:'
                font_size:20
                color: 0,0,0,.8
            TextInput:
                size_hint_x: 1
                id: bit_dia_textinput
                font_size:24
                multiline: False

            Label:
                size_hint_x: 1
                text: 'Depth:'
                font_size:20
                color: 0,0,0,.8
            TextInput:
                size_hint_x: 1
                id: bit_dia_textinput
                font_size:24
                multiline: False

            Label:
                size_hint_x: 1
                text: 'A:'
                font_size:20
                color: 0,0,0,.8
            TextInput:
                size_hint_x: 1
                id: bit_dia_textinput
                font_size:24
                multiline: False

            Label:
                size_hint_x: 1
                text: 'B:'
                font_size:20
                color: 0,0,0,.8
            TextInput:
                size_hint_x: 1
                id: bit_dia_textinput
                font_size:24
                multiline: False

            Label:
                size_hint_x: 1
                text: 'C:'
                font_size:20
                color: 0,0,0,.8
            TextInput:
                size_hint_x: 1
                id: bit_dia_textinput
                font_size:24
                multiline: False

        BoxLayout:
            size_hint_y: 5
            orientation: 'horizontal'
            size: self.parent.size
            pos: self.parent.pos
            padding: 0
            spacing: 20
            
            BoxLayout:
                size_hint_x: 6
                size: self.parent.size
                pos: self.parent.pos
                padding: 20
                canvas:
                    Color: 
                        rgba: 1,1,1,1
                    RoundedRectangle: 
                        size: self.size
                        pos: self.pos
                Carousel:
                    id: carousel
                    Image:
                        source: "./asmcnc/skavaUI/v_jigs/hole.png"
                        allow_stretch: True 
                    Image:
                        source: "./asmcnc/skavaUI/v_jigs/slot.png"
                        allow_stretch: True 
                    Image:
                        source: "./asmcnc/skavaUI/v_jigs/rectangle.png"
                        allow_stretch: True 
                    Image:
                        source: "./asmcnc/skavaUI/v_jigs/rounded_rectangle.png"
                        allow_stretch: True 
                        
                    Image:
                        source: "./asmcnc/skavaUI/v_jigs/hockeystick.png"
                        allow_stretch: True 
                        
                    Image:
                        source: "./asmcnc/skavaUI/v_jigs/keyhole.png"
                        allow_stretch: True 
                        
                
            BoxLayout:
                size_hint_x: 1
                orientation: 'vertical'
                spacing: 10

                canvas:
                    Color: 
                        rgba: 1,1,1,1
                    RoundedRectangle: 
                        size: self.size
                        pos: self.pos


                Button:
                    disabled: False
                    size_hint_y: 1
                    background_color: hex('#FFFFFF00')
                    on_release: 
                        carousel.load_next(mode='next')
                        self.background_color = hex('#FFFFFF00')
                    on_press:
                        self.background_color = hex('#FFFFFFFF')
                    BoxLayout:
                        padding: 10
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            id: image_cancel
                            source: "./asmcnc/skavaUI/img/xy_arrow_right.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True 
                Button:
                    id: load_button
                    disabled: False
                    size_hint_y: 1
                    background_color: hex('#FFFFFF00')
                    on_release: 
#                        carousel.load_previous()
                        self.background_color = hex('#FFFFFF00')
                        root.manager.current = 'vj_polygon'
                    on_press:
                        self.background_color = hex('#FFFFFFFF')
                    BoxLayout:
                        padding: 10
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            id: image_select
                            source: "./asmcnc/skavaUI/img/xy_arrow_left.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True 

                Button:
                    disabled: False
                    size_hint_y: 1
                    background_color: hex('#FFFFFF00')
                    on_release: 
#                        root.quit_to_home()
                        root.manager.current = 'lobby'
                        self.background_color = hex('#FFFFFF00')
                    on_press:
                        self.background_color = hex('#FFFFFFFF')
                    BoxLayout:
                        padding: 20
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            id: image_cancel
                            source: "./asmcnc/skavaUI/img/template_cancel.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True 
                Button:
                    id: load_button
                    disabled: False
                    size_hint_y: 1
                    background_color: hex('#FFFFFF00')
                    on_release: 
#                        root.load_file(filechooser.selection[0])
                        self.background_color = hex('#FFFFFF00')
                    on_press:
                        self.background_color = hex('#FFFFFFFF')
                    BoxLayout:
                        padding: 20
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            id: image_select
                            source: "./asmcnc/skavaUI/img/file_select_select.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True 

                
""")

job_cache_dir = './jobCache/'    # where job files are cached for selection (for last used history/easy access)
job_q_dir = './jobQ/'            # where file is copied if to be used next in job
ftp_file_dir = '/home/sysop/router_ftp'   # Linux location where incoming files are FTP'd to


class TemplateScreen(Screen):

    no_preview_found_img_path = './asmcnc/skavaUI/img/image_preview_inverted_large.png'
    
    def __init__(self, **kwargs):

        super(TemplateScreen, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']
        
    def on_enter(self):

        pass

    def quit_to_home(self):

        self.manager.current = 'home'
        #self.manager.transition.direction = 'up'
        
