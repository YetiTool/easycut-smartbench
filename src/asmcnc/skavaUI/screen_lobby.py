# -*- coding: utf-8 -*-
'''
Created on 19 Aug 2017

@author: Ed
'''
# config

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty  
from kivy.uix.widget import Widget
from kivy.clock import Clock

import sys, os, textwrap
from os.path import expanduser
from shutil import copy

from asmcnc.core_UI import scaling_utils
from asmcnc.skavaUI import popup_info
from asmcnc.core_UI.popups import BasicPopup, PopupType
from asmcnc.core_UI import console_utils
from kivy.core.window import Window

from asmcnc.comms.model_manager import ModelManagerSingleton

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
    upgrade_app_label:upgrade_app_label

    carousel_pane_1:carousel_pane_1
    pro_app_container:pro_app_container
    shapecutter_container:shapecutter_container
    yeti_cut_apps_container:yeti_cut_apps_container
    drywall_app_container:drywall_app_container
    upgrade_app_container:upgrade_app_container

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
            padding: app.get_scaled_tuple([10.0, 10.0, 734.0, 0])
            orientation: 'horizontal'

        Carousel:
            size_hint_y: 270
            id: carousel
            loop: True
                            
            BoxLayout:
                id: carousel_pane_1
                orientation: 'horizontal'
                padding: app.get_scaled_tuple([100.0, 20.0, 100.0, 50.0])
                spacing: app.get_scaled_width(20.0)

                BoxLayout:
                    id: pro_app_container
                    orientation: 'vertical'
                    size_hint_x: 1
                    spacing: app.get_scaled_width(20.0)
    
                    Button:
                        font_size: app.get_scaled_sp('15.0sp')
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
                        font_size: app.get_scaled_sp('25.0sp')
                        text: 'CAD / CAM'


                   
                BoxLayout:
                    id: shapecutter_container
                    orientation: 'vertical'
                    size_hint_x: 1
                    spacing: app.get_scaled_width(20.0)
                                             
                    Button:
                        font_size: app.get_scaled_sp('15.0sp')
                        
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
                        font_size: app.get_scaled_sp('25.0sp')
                        text: 'Shape Cutter'

                BoxLayout:
                    id: yeti_cut_apps_container
                    orientation: 'vertical'
                    size_hint_x: 1
                    spacing: app.get_scaled_width(20.0)
                                             
                    Button:
                        font_size: app.get_scaled_sp('15.0sp')
                        disabled: False
                        size_hint_y: 8
                        background_color: hex('#FFFFFF00')
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                id: image_select
                                source: "./asmcnc/skavaUI/img/yeti_cut_apps_lobby_logo_coming_soon.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True 
                    Label:
                        size_hint_y: 1
                        font_size: app.get_scaled_sp('25.0sp')
                        text: 'YetiCut'

                BoxLayout:
                    id: drywall_app_container
                    orientation: 'vertical'
                    size_hint_x: 1
                    spacing: app.get_scaled_width(20.0)
                    padding: app.get_scaled_tuple([65.0, 0])

                    Button:
                        font_size: app.get_scaled_sp('15.0sp')
                        size_hint_y: 8
                        disabled: False
                        background_color: hex('#FFFFFF00')
                        on_release:
                            self.background_color = hex('#FFFFFF00')
                        on_press:
                            root.drywall_cutter_app()
                            self.background_color = hex('#FFFFFF00')
                        BoxLayout:
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                id: image_select
                                source: "./asmcnc/apps/drywall_cutter_app/img/lobby_logo.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True
                    Label:
                        size_hint_y: 1
                        font_size: app.get_scaled_sp('25.0sp')
                        text: 'Drywall cutter'
                        markup: True

                        
            # Carousel pane 2
            BoxLayout:
                orientation: 'horizontal'
                padding: app.get_scaled_tuple([100.0, 20.0, 100.0, 50.0])
                spacing: app.get_scaled_width(20.0)

                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: 1
                    spacing: app.get_scaled_width(20.0)
    
                    Button:
                        font_size: app.get_scaled_sp('15.0sp')
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
                        font_size: app.get_scaled_sp('25.0sp')
                        text: 'Wi-Fi'
                
                
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: 1
                    spacing: app.get_scaled_width(20.0)
    
                    Button:
                        font_size: app.get_scaled_sp('15.0sp')
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
                        font_size: app.get_scaled_sp('25.0sp')
                        text: 'Calibrate'
                        markup: True

            # Carousel pane 3
            BoxLayout:
                orientation: 'horizontal'
                padding: app.get_scaled_tuple([100.0, 20.0, 100.0, 50.0])
                spacing: app.get_scaled_width(20.0)

                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: 1
                    spacing: app.get_scaled_width(20.0)
    
                    Button:
                        font_size: app.get_scaled_sp('15.0sp')
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
                        font_size: app.get_scaled_sp('25.0sp')
                        text: 'Update'
                
                
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: 1
                    spacing: app.get_scaled_width(20.0)
    
                    Button:
                        font_size: app.get_scaled_sp('15.0sp')
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
                        font_size: app.get_scaled_sp('25.0sp')
                        text: 'Maintenance'

            # Carousel pane 4
            BoxLayout:
                orientation: 'horizontal'
                padding: app.get_scaled_tuple([100.0, 20.0, 100.0, 50.0])
                spacing: app.get_scaled_width(20.0)

                BoxLayout:
                    id: upgrade_app_container
                    orientation: 'vertical'
                    size_hint_x: 1
                    spacing: app.get_scaled_width(20.0)

                    Button:
                        font_size: app.get_scaled_sp('15.0sp')
                        size_hint_y: 8
                        disabled: False
                        background_color: hex('#FFFFFF00')
                        on_release: 
                            self.background_color = hex('#FFFFFF00')
                        on_press:
                            root.upgrade_app()
                            self.background_color = hex('#FFFFFF00')
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                id: image_select
                                source: "./asmcnc/apps/upgrade_app/img/lobby_upgrade.png"
                                center_x: self.parent.center_x
                                center_y: self.parent.center_y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True 
                    Label:
                        id: upgrade_app_label
                        size_hint_y: 1
                        font_size: app.get_scaled_sp('25.0sp')
                        text: 'Upgrade'
                        markup: True

                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: 1
                    spacing: app.get_scaled_width(20.0)
                
                    Button:
                        font_size: app.get_scaled_sp('15.0sp')
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
                        font_size: app.get_scaled_sp('25.0sp')
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
            orientation: 'horizontal'

            BoxLayout:
                size_hint_x: None
                width: app.get_scaled_width(720.0)
                height: self.parent.height
                padding: app.get_scaled_tuple([80.0, 40.0, 0, 40.0])
                orientation: 'horizontal'
                
                Button:
                    font_size: app.get_scaled_sp('15.0sp')
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
                    font_size: app.get_scaled_sp('15.0sp')
                    size_hint_y: 0.8

                Button:
                    font_size: app.get_scaled_sp('15.0sp')
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

                Label:
                    font_size: app.get_scaled_sp('15.0sp')
                    size_hint_y: 0.8

                Button:
                    font_size: app.get_scaled_sp('15.0sp')
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

            BoxLayout:
                size_hint: (None, None)
                size: app.get_scaled_tuple([80.0, 80.0])
                orientation: 'horizontal'
                padding: app.get_scaled_tuple([29.0, 29.0, 10.0, 10.0])
                Button:
                    font_size: app.get_scaled_sp('15.0sp')
                    disabled: False
                    background_color: hex('#FFFFFF00')
                    on_press: root.help_popup()
                    BoxLayout:
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            id: image_select
                            source: "./asmcnc/skavaUI/img/lobby_help.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True
                
""")

job_cache_dir = './jobCache/'  # where job files are cached for selection (for last used history/easy access)
job_q_dir = './jobQ/'  # where file is copied if to be used next in job
ftp_file_dir = '/home/sysop/router_ftp'  # Linux location where incoming files are FTP'd to


class LobbyScreen(Screen):
    no_preview_found_img_path = './asmcnc/skavaUI/img/image_preview_inverted_large.png'
    trigger_update_popup = False
    welcome_popup_description = ''
    update_message = ''
    upgrade_app_hidden = False
    check_apps_on_pre_enter = False

    def __init__(self, **kwargs):
        super(LobbyScreen, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.am = kwargs['app_manager']
        self.l = kwargs['localization']
        self.model_manager = ModelManagerSingleton()
        self.show_desired_apps()
        self.update_strings()

    def show_desired_apps(self):
        # If it's a SmartCNC machine, then show the drywalltec app instead of shapecutter
        if self.model_manager.is_machine_drywall():
            self.remove_everything_but(self.drywall_app_container)
            self.put_drywall_app_first()
        # Check that window.height is valid & being read in - otherwise will default to SC
        elif type(Window.height) is not int and type(Window.height) is not float:
            self.check_apps_on_pre_enter = True
        # Else, show shapecutter
        else:
            self.remove_everything_but(self.shapecutter_container)

    def put_drywall_app_first(self):
        self.pro_app_container.parent.remove_widget(self.pro_app_container)
        self.drywall_app_container.parent.remove_widget(self.drywall_app_container)

        self.carousel_pane_1.add_widget(self.drywall_app_container)
        self.carousel_pane_1.add_widget(self.pro_app_container)

    def remove_everything_but(self, everything_but):
        containers = [
            self.drywall_app_container,
            self.yeti_cut_apps_container,
            self.shapecutter_container,
        ]
        containers.remove(everything_but)
        self.remove_container_from_parent(containers[0])
        self.remove_container_from_parent(containers[1])

    def remove_container_from_parent(self, container):
        container.parent.remove_widget(container)

    def on_pre_enter(self):
        if self.check_apps_on_pre_enter:
            self.show_desired_apps()
            self.check_apps_on_pre_enter = False
        # Hide upgrade app if machine is not upgradeable, and only if it has not been hidden already
        if not self.model_manager.is_machine_upgradeable() and not self.upgrade_app_hidden:
            self.remove_container_from_parent(self.upgrade_app_container)
            self.upgrade_app_hidden = True

    def on_enter(self):
        if not sys.platform == "win32":
            self.m.set_led_colour('GREEN')

        # Tell user to update if update is available
        if self.trigger_update_popup:
            popup_info.PopupInfo(self.sm, self.l, 450, self.update_message)

        # Trigger welcome popup is machine is being used for the first time
        if self.m.trigger_setup: self.help_popup()

    def set_trigger_to_false(self, *args):
        self.m.write_set_up_options(False)
        self.sm.get_screen('lobby').carousel.load_next(mode='next')

    def set_trigger_to_true(self, *args):
        self.m.write_set_up_options(True)

    def help_popup(self):
        # popup_info.PopupWelcome(self.sm, self.m, self.l, self.welcome_popup_description)
        welcome_popup = BasicPopup(sm=self.sm, m=self.m, l=self.l,
                                   title=self.l.get_str('Welcome to SmartBench'),
                                   main_string=self.welcome_popup_description,
                                   popup_type=PopupType.INFO,
                                   popup_width=500, popup_height=440, main_label_size_delta=80,
                                   main_label_padding=(0, 0), main_layout_padding=(10, 10, 10, 10),
                                   main_layout_spacing=10, button_layout_padding=(20, 10, 20, 0),
                                   button_layout_spacing=15,
                                   button_two_background_color=(76 / 255., 175 / 255., 80 / 255., 1.),
                                   button_one_background_color=(230 / 255., 74 / 255., 25 / 255., 1.),
                                   button_one_text="Remind me later", button_two_text="Ok",
                                   button_one_callback=self.set_trigger_to_true,
                                   button_two_callback=self.set_trigger_to_false)

        welcome_popup.open()

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

    def upgrade_app(self):
        # Need to set $51 on entry, requires idle
        if self.m.state().startswith('Idle'):
            self.am.start_upgrade_app()
        else:
            popup_info.PopupError(self.sm, self.l, self.l.get_str("Please ensure machine is idle before continuing."))

    def drywall_cutter_app(self):
        self.am.start_drywall_cutter_app()

    def shutdown_console(self):
        console_utils.shutdown()
        popup_info.PopupShutdown(self.sm, self.l)

    def update_strings(self):
        self.pro_app_label.text = self.l.get_str('CAD / CAM')
        self.shapecutter_app_label.text = self.l.get_str('Shape Cutter')
        self.wifi_app_label.text = self.l.get_str('Wifi')
        self.calibrate_app_label.text = self.l.get_str('Calibrate')
        self.update_app_label.text = self.l.get_str('Update')
        self.maintenance_app_label.text = self.l.get_str('Maintenance')
        self.system_tools_app_label.text = self.l.get_str('System Tools')
        self.upgrade_app_label.text = self.l.get_str('Upgrade')

        self.welcome_popup_description = (
                self.format_command(
                    self.l.get_str('Use the arrows to go through the menu, and select an app to get started.')
                ) + '\n\n' +
                self.format_command(
                    ((self.l.get_str('If this is your first time, make sure you use the Wifi, Maintenance, ' +
                                     'and Calibrate apps to set up SmartBench.'
                                     ).replace(self.l.get_str('Wifi'), self.l.get_bold('Wifi'))
                      ).replace(self.l.get_str('Maintenance'), self.l.get_bold('Maintenance'))
                     ).replace(self.l.get_str('Calibrate'), self.l.get_bold('Calibrate')
                               )
                ) + '\n\n' +
                self.format_command(
                    self.l.get_str('For more help, please visit:')
                ) + '\n' +
                '[b]https://www.yetitool.com/support[/b]' + '\n'
        )

        self.update_message = (
                self.l.get_str('New software update available for download!') + '\n\n' +
                self.l.get_str(
                    'Please use the Update app to get the latest version.'
                ).replace(self.l.get_str('Update'), self.l.get_bold('Update'))
        )

    def format_command(self, cmd):
        wrapped_cmd = textwrap.fill(cmd, width=50, break_long_words=False)
        return wrapped_cmd
