'''
Created on 19 Aug 2017

@author: Ed
'''
# config

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty # @UnresolvedImport
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.clock import Clock


import sys, os
from os.path import expanduser
from shutil import copy
from asmcnc.comms import usb_storage


Builder.load_string("""

<LobbyScreen>:

    carousel:carousel

    canvas.before:
        Color: 
            rgba: hex('#0d47a1FF')
        Rectangle: 
            size: self.size
            pos: self.pos

    BoxLayout:
        orientation: 'vertical'
        size: self.parent.size
        pos: self.parent.pos
        padding: 0
        spacing: 0

        Carousel:
            size_hint_y: 340
            id: carousel
            loop: True
                            
            BoxLayout:
                orientation: 'horizontal'
                padding: 70
                spacing: 70

                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: 1
                    spacing: 20
    
                    Button:
                        size_hint_y: 8
                        id: load_button
                        disabled: False
                        background_color: hex('#FFFFFF00')
                        on_release: 
#                             root.go_to_initial_screen(1)
                            root.quit_to_home()
                            self.background_color = hex('#FFFFFF00')
                        on_press:
                            self.background_color = hex('#FFFFFF00')
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                id: image_select
#                                source: "./asmcnc/skavaUI/img/lobby_app_freecut.png"
                                source: "./asmcnc/skavaUI/img/lobby_pro.png"
                                center_x: self.parent.center_x
                                center_y: self.parent.center_y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True 
                    Label:
                        size_hint_y: 1
                        font_size: '25sp'
                        text: 'CAD / CAM'
                        
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: 1
                    spacing: 20
                                            
                    Button:
                        id: load_button
                        disabled: True
                        size_hint_y: 8
                        background_color: hex('#FFFFFF00')
                        on_release: 
#                             root.go_to_initial_screen(1)
#                            root.manager.current = 'template'
#                            root.manager.current = 'vj_polygon'
                            self.background_color = hex('#FFFFFF00')
                        on_press:
                            self.background_color = hex('#FFFFFF00')
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                id: image_select
                                source: "./asmcnc/skavaUI/img/lobby_app_virtualjig_comingsoon.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True 
                    Label:
                        size_hint_y: 1
                        font_size: '25sp'
                        text: 'Virtual Jig'
                        
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: 1
                    spacing: 20

                    Button:
                        id: load_button
                        disabled: True
                        size_hint_y: 8
                        background_color: hex('#FFFFFF00')
                        on_release: 
#                             root.go_to_initial_screen(1)
                            self.background_color = hex('#FFFFFF00')
                        on_press:
                            self.background_color = hex('#FFFFFF00')
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                id: image_select
#                                source: "./asmcnc/skavaUI/img/lobby_app_cadcam.png"
                                source: "./asmcnc/skavaUI/img/lobby_door_hole_driller_comingsoon.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True 
                    Label:
                        size_hint_y: 1
                        font_size: '25sp'
                        text: 'Door Holer'
                        
            # Carousel pane 2
        
            BoxLayout:
                orientation: 'horizontal'
                padding: 70
                spacing: 70

                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: 1
                    spacing: 20
    
                    Button:
                        size_hint_y: 8
                        id: load_button
                        disabled: False
                        background_color: hex('#FFFFFF00')
                        on_release: 
#                             root.go_to_initial_screen(1)
                            self.background_color = hex('#FFFFFF00')
                        on_press:
                            self.background_color = hex('#FFFFFF00')
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                id: image_select
#                                source: "./asmcnc/skavaUI/img/lobby_app_signwriter.png"
                                source: "./asmcnc/skavaUI/img/lobby_sign_writer.png"
                                center_x: self.parent.center_x
                                center_y: self.parent.center_y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True 
                    Label:
                        size_hint_y: 1
                        font_size: '25sp'
                        text: 'Sign Writer'
                        
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: 1
                    spacing: 20
                                            
                    Button:
                        id: load_button
                        disabled: False
                        size_hint_y: 8
                        background_color: hex('#FFFFFF00')
                        on_release: 
#                             root.go_to_initial_screen(1)
                            self.background_color = hex('#FFFFFF00')
                        on_press:
                            self.background_color = hex('#FFFFFF00')
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                id: image_select
#                                source: "./asmcnc/skavaUI/img/lobby_app_pillardrill.png"
                                source: "./asmcnc/skavaUI/img/lobby_jointer.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True 
                    Label:
                        size_hint_y: 1
                        font_size: '25sp'
                        text: 'Jointer'
                        
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: 1
                    spacing: 20

                    Button:
                        id: load_button
                        disabled: False
                        size_hint_y: 8
                        background_color: hex('#FFFFFF00')
                        on_release: 
#                             root.go_to_initial_screen(1)
                            self.background_color = hex('#FFFFFF00')
                        on_press:
                            self.background_color = hex('#FFFFFF00')
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                id: image_select
#                                source: "./asmcnc/skavaUI/img/lobby_app_counterwiz.png"
                                source: "./asmcnc/skavaUI/img/lobby_counter_wiz.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True 
                    Label:
                        size_hint_y: 1
                        font_size: '25sp'
                        text: 'Counter Wiz'

        BoxLayout:
            size_hint_y: 6
            size: self.parent.size
            pos: self.parent.pos
          
            Image:
                source: "./asmcnc/skavaUI/img/lobby_separator.png"


        BoxLayout:
            size_hint_y: 134
            size: self.parent.size
            pos: self.parent.pos
            padding: 40
            orientation: 'horizontal'
            
            Button:
                disabled: False
                size_hint_y: 1
                background_color: hex('#FFFFFF00')
                on_release: 
                    carousel.load_previous()
                    self.background_color = hex('#FFFFFF00')
                on_press:
                    self.background_color = hex('#FFFFFF00')
                BoxLayout:
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        id: image_cancel
                        source: "./asmcnc/skavaUI/img/lobby_scrollleft.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True 

            Label:
                size_hint_y: 1

#             Button:
#                 id: load_button
#                 disabled: False
#                 size_hint_y: 1
#                 background_color: hex('#FFFFFF00')
#                 on_release: 
#                     root.quit_to_home()
#                     self.background_color = hex('#FFFFFF00')
#                 on_press:
#                     self.background_color = hex('#FFFFFF00')
#                 BoxLayout:
#                     size: self.parent.size
#                     pos: self.parent.pos
#                     Image:
#                         id: image_select
#                         source: "./asmcnc/skavaUI/img/lobby_expert.png"
#                         center_x: self.parent.center_x
#                         y: self.parent.y
#                         size: self.parent.width, self.parent.height
#                         allow_stretch: True 

#             Button:
#                 disabled: False
#                 size_hint_y: 1
#                 background_color: hex('#FFFFFF00')
#                 on_release: 
#                     self.background_color = hex('#FFFFFF00')
#                 on_press:
#                     self.background_color = hex('#FFFFFF00')
#                 BoxLayout:
#                     size: self.parent.size
#                     pos: self.parent.pos
#                     Image:
#                         id: image_cancel
#                         source: "./asmcnc/skavaUI/img/lobby_settings.png"
#                         center_x: self.parent.center_x
#                         y: self.parent.y
#                         size: self.parent.width, self.parent.height
#                         allow_stretch: True 

            Button:
                disabled: False
                size_hint_y: 1
                background_color: hex('#FFFFFF00')
                on_release: 
                    self.background_color = hex('#FFFFFF00')
                on_press:
                    self.background_color = hex('#FFFFFF00')
                BoxLayout:
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        id: image_cancel
                        source: "./asmcnc/skavaUI/img/lobby_help.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True 

            Label:
                size_hint_y: 1

            Button:
                id: load_button
                disabled: False
                size_hint_y: 1
                background_color: hex('#FFFFFF00')
                on_release: 
                    carousel.load_next(mode='next')
                    self.background_color = hex('#FFFFFF00')
                on_press:
                    self.background_color = hex('#FFFFFF00')
                BoxLayout:
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        id: image_select
                        source: "./asmcnc/skavaUI/img/lobby_scrollright.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True 

                
""")


job_cache_dir = './jobCache/'    # where job files are cached for selection (for last used history/easy access)
job_q_dir = './jobQ/'            # where file is copied if to be used next in job
ftp_file_dir = '/home/sysop/router_ftp'   # Linux location where incoming files are FTP'd to

class LobbyScreen(Screen):

    no_preview_found_img_path = './asmcnc/skavaUI/img/image_preview_inverted_large.png'
    
    
    def __init__(self, **kwargs):
        super(LobbyScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
 
# FLAG
    def on_enter(self):
        if not sys.platform == "win32":
            self.m.set_led_blue()
 

    def quit_to_home(self):
        #self.sm.transition = SlideTransition()
        #self.sm.transition.direction = 'up' 
        self.sm.current = 'home'
    
    
    def go_to_initial_screen(self, dt):
        #self.sm.transition = NoTransition()
        self.sm.current = 'initial'   
        
