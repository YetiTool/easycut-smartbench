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
from kivy.uix.widget import Widget
from kivy.clock import Clock


import sys, os, textwrap
from os.path import expanduser
from shutil import copy
from asmcnc.comms import usb_storage

from asmcnc.skavaUI import popup_info


Builder.load_string("""

<LobbyScreen>:

    carousel:carousel

    pro_app_label: pro_app_label
    shapecutter_app_label: shapecutter_app_label
    wifi_app_label: wifi_app_label
    calibrate_app_label: calibrate_app_label
    update_app_label: update_app_label
    maintenance_app_label: maintenance_app_label
    system_tools_app_label: system_tools_app_label


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

        BoxLayout:
            size_hint_y: 70
            padding: [10, 10, 734, 0]
            orientation: 'horizontal'

            Button:
                id: shutdown_button
                size_hint_y: 1
                background_color: hex('#FFFFFF00')
                on_press: root.shutdown_console()

                BoxLayout:
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        id: image_select
                        source: "./asmcnc/skavaUI/img/shutdown.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True 

        Carousel:
            size_hint_y: 270
            id: carousel
            loop: True
                            
            BoxLayout:
                orientation: 'horizontal'
                padding: [100, 20, 100, 50]
                spacing: 20

                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: 1
                    spacing: 20
    
                    Button:
                        size_hint_y: 8
                        disabled: False
                        background_color: hex('#FFFFFF00')
                        on_release: 
                            self.background_color = hex('#FFFFFF00')
                        on_press:
                            root.pro_app()
                            self.background_color = hex('#FFFFFF00')
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                id: image_select
                                source: "./asmcnc/skavaUI/img/lobby_pro.png"
                                center_x: self.parent.center_x
                                center_y: self.parent.center_y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True 
                    Label:
                        id: pro_app_label
                        size_hint_y: 1
                        font_size: '25sp'
                        text: 'CAD / CAM'


                   
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: 1
                    spacing: 20
                                             
                    Button:
                        
                        disabled: False
                        size_hint_y: 8
                        background_color: hex('#FFFFFF00')
                        on_release:                 
                            self.background_color = hex('#FFFFFF00')
                        on_press:
                            root.shapecutter_app()
                            self.background_color = hex('#FFFFFF00')
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                id: image_select
                                source: "./asmcnc/skavaUI/img/lobby_app_shapecutter.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True 
                    Label:
                        id: shapecutter_app_label
                        size_hint_y: 1
                        font_size: '25sp'
                        text: 'Shape Cutter'
                        
            # Carousel pane 2
            BoxLayout:
                orientation: 'horizontal'
                padding: [100, 20, 100, 50]
                spacing: 20

                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: 1
                    spacing: 20
    
                    Button:
                        size_hint_y: 8
                        disabled: False
                        background_color: hex('#FFFFFF00')
                        on_release: 
                            self.background_color = hex('#FFFFFF00')
                        on_press:
                            root.wifi_app()
                            self.background_color = hex('#FFFFFF00')
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                id: image_select
                                source: "./asmcnc/skavaUI/img/lobby_app_wifi.png"
                                center_x: self.parent.center_x
                                center_y: self.parent.center_y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True 
                    Label:
                        id: wifi_app_label
                        size_hint_y: 1
                        font_size: '25sp'
                        text: 'Wifi'
                
                
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: 1
                    spacing: 20
    
                    Button:
                        size_hint_y: 8
                        disabled: False
                        background_color: hex('#FFFFFF00')
                        on_release: 
                            self.background_color = hex('#FFFFFF00')
                        on_press:
                            root.calibrate_smartbench()
                            self.background_color = hex('#FFFFFF00')
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                id: image_select
                                source: "./asmcnc/skavaUI/img/lobby_app_calibrate.png"
                                center_x: self.parent.center_x
                                center_y: self.parent.center_y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True 
                    Label:
                        id: calibrate_app_label
                        size_hint_y: 1
                        font_size: '25sp'
                        text: 'Calibrate'
                        markup: True

            # Carousel pane 3
            BoxLayout:
                orientation: 'horizontal'
                padding: [100, 20, 100, 50]
                spacing: 20

                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: 1
                    spacing: 20
    
                    Button:
                        size_hint_y: 8
                        disabled: False
                        background_color: hex('#FFFFFF00')
                        on_release: 
                            self.background_color = hex('#FFFFFF00')
                        on_press:
                            root.update_app()
                            self.background_color = hex('#FFFFFF00')
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                id: image_select
                                source: "./asmcnc/skavaUI/img/lobby_update.png"
                                center_x: self.parent.center_x
                                center_y: self.parent.center_y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True 
                    Label:
                        id: update_app_label
                        size_hint_y: 1
                        font_size: '25sp'
                        text: 'Update'
                
                
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: 1
                    spacing: 20
    
                    Button:
                        size_hint_y: 8
                        disabled: False
                        background_color: hex('#FFFFFF00')
                        on_release: 
                            self.background_color = hex('#FFFFFF00')
                        on_press:
                            root.maintenance_app()
                            self.background_color = hex('#FFFFFF00')
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                id: image_select
                                source: "./asmcnc/apps/maintenance_app/img/lobby_maintenance.png"
                                center_x: self.parent.center_x
                                center_y: self.parent.center_y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True 
                    Label:
                        id: maintenance_app_label
                        size_hint_y: 1
                        font_size: '25sp'
                        text: 'Maintenance'

            # Carousel pane 4
            BoxLayout:
                orientation: 'horizontal'
                padding: [100, 20, 100, 50]
                spacing: 20

                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: 1
                    spacing: 20
                
                    Button:
                        size_hint_y: 8
                        disabled: False
                        background_color: hex('#FFFFFF00')
                        on_release: 
                            self.background_color = hex('#FFFFFF00')
                        on_press:
                            root.developer_app()
                            self.background_color = hex('#FFFFFF00')
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                id: image_select
                                source: "./asmcnc/apps/systemTools_app/img/lobby_system.png"
                                center_x: self.parent.center_x
                                center_y: self.parent.center_y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True 
                    Label:
                        id: system_tools_app_label
                        size_hint_y: 1
                        font_size: '25sp'
                        text: 'System Tools'
                        markup: True
                       
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

            Button:
                disabled: False
                size_hint_y: 1
                background_color: hex('#FFFFFF00')
                on_release: 
                    self.background_color = hex('#FFFFFF00')
                on_press:
                    root.help_popup()
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
    trigger_update_popup = False
    welcome_popup_description = ''
    update_message = ''
    
    def __init__(self, **kwargs):
        super(LobbyScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        self.am=kwargs['app_manager']
        self.l=kwargs['localization']
# FLAG
    def on_pre_enter(self):
        # if self.update_app_label.text != self.l.dictionary['Update']:
        self.update_strings()

    def on_enter(self):
        if not sys.platform == "win32":
            self.m.set_led_colour('GREEN')

        # Tell user to update if update is available
        if self.trigger_update_popup:
            popup_info.PopupInfo(self.sm, self.l, 450, self.update_message)

        # Trigger welcome popup is machine is being used for the first time
        if self.m.trigger_setup: self.help_popup()

    def help_popup(self):
        popup_info.PopupWelcome(self.sm, self.m, self.l, self.welcome_popup_description)
 
    def pro_app(self):
        self.am.start_pro_app()
        self.sm.current = 'home'
    
    def shapecutter_app(self):
        self.m.run_led_rainbow_ending_green()
        self.am.start_shapecutter_app()
    
    def calibrate_smartbench(self):
        self.am.start_calibration_app('lobby')
    
    def wifi_app(self):
        self.am.start_wifi_app()
    
    def update_app(self):
        self.am.start_update_app()    
    
    def developer_app(self):
        # popup_info.PopupDeveloper(self.sm)
        self.am.start_systemtools_app()

    def maintenance_app(self):
        self.am.start_maintenance_app('laser_tab') 

    def shutdown_console(self):
        if sys.platform != 'win32' and sys.platform != 'darwin': 
            os.system('sudo shutdown -h')
        popup_info.PopupShutdown(self.sm, self.l)

    def update_strings(self):
        self.pro_app_label.text = self.l.get_str('CAD / CAM')
        self.shapecutter_app_label.text = self.l.get_str('Shape Cutter')
        self.wifi_app_label.text = self.l.get_str('Wifi')
        self.calibrate_app_label.text = self.l.get_str('Calibrate')
        self.update_app_label.text = self.l.get_str('Update')
        self.maintenance_app_label.text = self.l.get_str('Maintenance')
        self.system_tools_app_label.text = self.l.get_str('System Tools')

        self.welcome_popup_description = (
            self.format_command(
                self.l.get_str('Use the arrows to go through the menu, and select an app to get started.')
                ) + '\n\n' + \
            self.format_command(
                self.l.get_str('If this is your first time, make sure you use the') + ' ' + \
                self.l.get_bold('Wifi') + ', ' + \
                self.l.get_bold('Maintenance') + ', ' + \
                self.l.get_str('and') + ' ' + \
                self.l.get_bold('Calibrate') + ' ' + \
                self.l.get_str('apps to set up SmartBench.')
            ) + '\n\n' + \
            self.format_command(
                self.l.get_str('For more help, please visit:')
            ) + '\n' + \
            '[b]https://www.yetitool.com/support[/b]' + '\n'
            )

        self.update_message = (
            self.l.get_str('New software update available for download!') + '\n\n' + \
            self.l.get_str('Please use the') + ' ' + \
            self.l.get_bold('Update') + ' ' + \
            self.l.get_str('app to get the latest version.')
            )

    def format_command(self, cmd):
        wrapped_cmd = textwrap.fill(cmd, width=50, break_long_words=False)
        return wrapped_cmd
