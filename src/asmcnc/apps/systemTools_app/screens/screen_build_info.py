# -*- coding: utf-8 -*-
'''
Created on 18 November 2020
Build info screen for system tools app

@author: Letty
'''
import os, sys

from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.clock import Clock
from kivy.metrics import dp

from asmcnc.skavaUI import popup_info
from asmcnc.apps.systemTools_app.screens import popup_system
from asmcnc.apps.start_up_sequence.data_consent_app import screen_manager_data_consent

Builder.load_string("""

#:import Factory kivy.factory.Factory


<SystemToolsLanguageSpinner@SpinnerOption>

    background_normal: ''
    background_color: [1,1,1,1]
    height: dp(40)
    color: 0,0,0,1
    halign: 'left'
    markup: 'True'
    font_size: 18

<BuildInfoScreen>

    header: header
    serial_number_header: serial_number_header
    console_serial_number_header: console_serial_number_header
    software_header: software_header
    platform_header: platform_header
    firmware_header: firmware_header
    zhead_header: zhead_header
    hardware_header: hardware_header
    language_button: language_button

    sw_version_label: sw_version_label
    pl_version_label: pl_version_label
    fw_version_label: fw_version_label
    hw_version_label: hw_version_label
    zh_version_label: zh_version_label
    smartbench_name : smartbench_name
    smartbench_name_label : smartbench_name_label
    smartbench_name_input : smartbench_name_input
    smartbench_location: smartbench_location
    smartbench_location_label : smartbench_location_label
    smartbench_location_buffer : smartbench_location_buffer
    smartbench_location_input: smartbench_location_input
    smartbench_model_header : smartbench_model_header
    smartbench_model: smartbench_model
    machine_serial_number_label: machine_serial_number_label
    language_button: language_button
    data_and_wifi_button : data_and_wifi_button
    advanced_button : advanced_button
    show_more_info: show_more_info
    console_serial_number: console_serial_number

    BoxLayout:
        height: dp(800)
        width: dp(480)
        canvas.before:
            Color: 
                rgba: hex('#e5e5e5ff')
            Rectangle: 
                size: self.size
                pos: self.pos

        BoxLayout:
            padding: 0
            spacing: 10
            orientation: "vertical"
            BoxLayout:
                padding: 0
                spacing: 0
                canvas:
                    Color:
                        rgba: hex('#1976d2ff')
                    Rectangle:
                        pos: self.pos
                        size: self.size
                Label:
                    id: header
                    size_hint: (None,None)
                    height: dp(60)
                    width: dp(800)
                    text: "System Information"
                    color: hex('#f9f9f9ff')
                    # color: hex('#333333ff') #grey
                    font_size: 30
                    halign: "center"
                    valign: "bottom"
                    markup: True
                   
                    
            BoxLayout:
                size_hint: (None,None)
                width: dp(780)
                height: dp(320)
                padding: [dp(20), dp(0)]
                spacing: 0
                orientation: 'horizontal'

                BoxLayout:
                    orientation: 'vertical'
                    size_hint: (None, None)
                    height: dp(350)
                    width: dp(550)
                    padding: [dp(0), dp(20), dp(0), dp(0)]

                    Button:
                        id: smartbench_name
                        background_color: hex('#e5e5e5ff')
                        background_normal: ""
                        background_down: ""
                        opacity: 1
                        on_press: root.open_rename()
                        focus_next: smartbench_name_input
                        size_hint_y: None
                        height: dp(40)
                        BoxLayout:
                            pos: self.parent.pos
                            size: self.parent.size
                            orientation: 'horizontal'
                            padding: [dp(5), dp(0)]

                            BoxLayout: 
                                size_hint_x: None
                                width: dp(30)
                                Image:
                                    source: "./asmcnc/apps/systemTools_app/img/tiny_pencil.png"
                                    allow_stretch: True
                            Label:
                                id: smartbench_name_label
                                text: "The text"
                                text_size: self.size
                                halign: "left"
                                valign: "middle"
                                markup: True
                                font_size: 30
                                color: hex('#333333ff')
                                multiline: False
                                shorten: True
                    TextInput:
                        padding: [4, 2]
                        id: smartbench_name_input
                        text: 'My SmartBench'
                        color: hex('#333333ff')
                        text_size: self.size
                        halign: "left"
                        valign: "middle"
                        markup: True
                        font_size: 24
                        size_hint_y: None
                        height: dp(0)
                        size_hint_x: None
                        width: dp(500)
                        opacity: 0
                        on_text_validate: root.save_new_name()
                        # unfocus_on_touch: True
                        disabled: True
                        multiline: False

                    Button:
                        id: smartbench_location
                        background_color: hex('#e5e5e5ff')
                        background_normal: ""
                        background_down: ""
                        size_hint_y: None
                        height: dp(30)
                        opacity: 1
                        on_press: root.open_rename_location()
                        focus_next: smartbench_location_input

                        BoxLayout:
                            pos: self.parent.pos
                            size: self.parent.size
                            orientation: 'horizontal'
                            padding: [dp(5), dp(0)]

                            Label:
                                id: smartbench_location_label
                                size_hint_x: None
                                color: hex('#333333ff')
                                text_size: self.size
                                halign: "left"
                                valign: "middle"
                                markup: True
                                font_size: 24
                                shorten_from: 'right'
                                shorten: True

                            BoxLayout: 
                                size_hint_x: None
                                width: dp(24)
                                Image:
                                    source: "./asmcnc/apps/systemTools_app/img/tiny_pencil.png"
                                    allow_stretch: True

                            Label: 
                                id: smartbench_location_buffer
                                size_hint_x: None



                    TextInput:
                        padding: [4, 2]
                        id: smartbench_location_input
                        text: 'SmartBench location'
                        color: hex('#333333ff')
                        text_size: self.size
                        halign: "left"
                        valign: "middle"
                        markup: True
                        font_size: 20
                        size_hint_y: None
                        height: dp(0)
                        size_hint_x: None
                        width: dp(500)
                        opacity: 0
                        on_text_validate: root.save_new_location()
                        # unfocus_on_touch: True
                        disabled: True
                        multiline: False



                    GridLayout:
                        size: self.parent.size
                        pos: self.parent.pos
                        cols: 2
                        rows: 9
                        size_hint: (None, None)
                        height: dp(250)
                        width: dp(550)
                        cols_minimum: {0: dp(230), 1: dp(320)}

                        Label:
                            id: smartbench_model_header
                            text: '[b]SmartBench model[/b]'
                            color: hex('#333333ff')
                            text_size: self.size
                            halign: "left"
                            valign: "middle"
                            markup: True
                            font_size: 20

                        Label:
                            id: smartbench_model
                            text: '-'
                            color: hex('#333333ff')
                            text_size: self.size
                            halign: "left"
                            valign: "middle"
                            markup: True
                            font_size: 20

                        # Label:
                        #     text: ''
                        #     color: hex('#333333ff')
                        #     text_size: self.size
                        #     halign: "left"
                        #     valign: "middle"
                        #     markup: True
                        #     font_size: 20
                        Label:
                            id: serial_number_header
                            text: '[b]Serial number[/b]'
                            color: hex('#333333ff')
                            text_size: self.size
                            halign: "left"
                            valign: "middle"
                            markup: True
                            font_size: 20
                        Label:
                            id: machine_serial_number_label
                            color: hex('#333333ff')
                            text: ''
                            text_size: self.size
                            halign: "left"
                            valign: "middle"
                            markup: True
                            font_size: 20

                        Label:
                            id: console_serial_number_header
                            color: hex('#333333ff')
                            text_size: self.size
                            halign: "left"
                            valign: "middle"
                            markup: True
                            font_size: 20
                        Label:
                            id: console_serial_number
                            text: '-'
                            color: hex('#333333ff')
                            text_size: self.size
                            halign: "left"
                            valign: "middle"
                            markup: True
                            font_size: 20
                        Label: 
                            id: software_header
                            text: '[b]Software[/b]'
                            color: hex('#333333ff')
                            text_size: self.size
                            halign: "left"
                            valign: "middle"
                            markup: True
                            font_size: 20
                        Label:
                            id: sw_version_label
                            color: hex('#333333ff')
                            text: 'SW_version'
                            halign: "left"
                            valign: "middle"
                            markup: True
                            text_size: self.size
                            markup: 'True'
                            font_size: 20
                        Label: 
                            id: platform_header
                            text: '[b]Platform[/b]'
                            color: hex('#333333ff')
                            text_size: self.size
                            halign: "left"
                            valign: "middle"
                            markup: True
                            font_size: 20
                        Label: 
                            id: pl_version_label
                            color: hex('#333333ff')
                            text: 'PL_version'
                            halign: "left"
                            valign: "middle"
                            markup: True
                            text_size: self.size
                            markup: 'True'
                            font_size: 20
                        Label: 
                            id: firmware_header
                            text: '[b]Firmware[/b]'
                            color: hex('#333333ff')
                            text_size: self.size
                            halign: "left"
                            valign: "middle"
                            markup: True
                            font_size: 20
                        Label: 
                            id: fw_version_label
                            color: hex('#333333ff')
                            text: 'FW_version'
                            halign: "left"
                            valign: "middle"
                            markup: True
                            text_size: self.size
                            markup: 'True'
                            font_size: 20
                        Label: 
                            id: zhead_header
                            text: '[b]Z head[/b]'
                            color: hex('#333333ff')
                            text_size: self.size
                            halign: "left"
                            valign: "middle"
                            markup: True
                            font_size: 20
                        Label: 
                            id: zh_version_label
                            color: hex('#333333ff')
                            text: 'ZH_version'
                            halign: "left"
                            valign: "middle"
                            markup: True
                            text_size: self.size
                            markup: 'True'
                            font_size: 20
                        Label: 
                            id: hardware_header
                            text: '[b]Hardware[/b]'
                            color: hex('#333333ff')
                            text_size: self.size
                            halign: "left"
                            valign: "middle"
                            markup: True
                            font_size: 20
                        Label: 
                            id: hw_version_label
                            color: hex('#333333ff')
                            text: 'HW_version'
                            halign: "left"
                            valign: "middle"
                            markup: True
                            text_size: self.size
                            markup: 'True'
                            font_size: 20

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(210)
                    height: dp(280)
                    padding: 0
                    spacing: 20
                    orientation: 'vertical'

                    # canvas:
                    #     Color:
                    #         rgba: [1,1,1,1]
                    #     Rectangle:
                    #         pos: self.pos
                    #         size: self.size

                    Spinner:
                        id: language_button
                        size_hint: (None,None)
                        height: dp(35)
                        width: dp(180)
                        background_normal: "./asmcnc/apps/systemTools_app/img/word_button.png"
                        background_down: ""
                        border: [dp(7.5)]*4
                        center: self.parent.center
                        pos: self.parent.pos
                        text: 'Choose language...'
                        color: hex('#f9f9f9ff')
                        markup: True
                        option_cls: Factory.get("SystemToolsLanguageSpinner")
                        on_text: root.choose_language()

                    Button:
                        id: data_and_wifi_button
                        size_hint: (None,None)
                        height: dp(35)
                        width: dp(180)
                        background_normal: "./asmcnc/apps/systemTools_app/img/word_button.png"
                        background_down: "./asmcnc/apps/systemTools_app/img/word_button.png"
                        border: [dp(7.5)]*4
                        center: self.parent.center
                        pos: self.parent.pos
                        on_press: root.open_data_consent_app()
                        color: hex('#f9f9f9ff')
                        markup: True

                    ToggleButton:
                        id: advanced_button
                        size_hint: (None,None)
                        height: dp(35)
                        width: dp(180)
                        background_normal: "./asmcnc/apps/systemTools_app/img/word_button.png"
                        background_down: "./asmcnc/apps/systemTools_app/img/word_button.png"
                        border: [dp(7.5)]*4
                        center: self.parent.center
                        pos: self.parent.pos
                        on_press: root.do_show_more_info()
                        color: hex('#f9f9f9ff')
                        markup: True

                    BoxLayout: 
                        size_hint: (None, None)
                        height: dp(115)
                        width: dp(210)
                        padding: [0,0]

                        Label: 
                            id: show_more_info
                            text: ''
                            opacity: 0
                            color: hex('#333333ff')




                    # BoxLayout: 
                    #     size_hint: (None, None)
                    #     height: dp(10)
                    #     width: dp(210)

            BoxLayout:
                size_hint: (None,None)
                width: dp(800)
                height: dp(80)
                padding: 0
                spacing: 10
                orientation: 'horizontal'

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(80)
                    height: dp(80)
                    padding: 0
                    spacing: 0

                    BoxLayout: 
                        size_hint: (None, None)
                        height: dp(80)
                        width: dp(80)
                        padding: [10, 10, 10, 10]
                        Button:
                            size_hint: (None,None)
                            height: dp(52)
                            width: dp(60)
                            background_color: hex('#F4433600')
                            center: self.parent.center
                            pos: self.parent.pos
                            on_press: root.go_back()
                            BoxLayout:
                                padding: 0
                                size: self.parent.size
                                pos: self.parent.pos
                                Image:
                                    source: "./asmcnc/apps/systemTools_app/img/back_to_menu.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(620)
                    height: dp(80)
                    padding: 10
                    spacing: 0
                    orientation: 'vertical'

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(80)
                    height: dp(80)
                    padding: 0
                    spacing: 0

                    BoxLayout: 
                        size_hint: (None, None)
                        height: dp(80)
                        width: dp(80)
                        padding: [19, 10, 10, 10]
                        Button:
                            size_hint: (None,None)
                            height: dp(60)
                            width: dp(51)
                            background_color: hex('#F4433600')
                            center: self.parent.center
                            pos: self.parent.pos
                            on_press: root.exit_app()
                            BoxLayout:
                                padding: 0
                                size: self.parent.size
                                pos: self.parent.pos
                                Image:
                                    source: "./asmcnc/apps/systemTools_app/img/back_to_lobby.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True
""")

class BuildInfoScreen(Screen):

    language_list = []
    reset_language = False

    smartbench_model_path = '/home/pi/smartbench_model_name.txt'
    smartbench_name_filepath = '/home/pi/smartbench_name.txt'
    smartbench_name_unformatted = 'My SmartBench'
    smartbench_name_formatted = 'My SmartBench'

    def __init__(self, **kwargs):
        super(BuildInfoScreen, self).__init__(**kwargs)
        self.systemtools_sm = kwargs['system_tools']
        self.m = kwargs['machine']
        self.set = kwargs['settings']
        self.l = kwargs['localization']

        self.smartbench_location_unformatted = self.l.get_str('SmartBench Location')
        self.smartbench_location_formatted = self.l.get_str('SmartBench Location')

        self.update_strings()
        self.language_button.values = self.l.supported_languages

        self.smartbench_name_input.bind(focus=self.on_focus)
        self.smartbench_location_input.bind(focus = self.on_focus_location)

        self.sw_version_label.text = self.set.sw_version
        self.pl_version_label.text = self.set.platform_version
        self.latest_sw_version = self.set.latest_sw_version
        self.latest_platform_version = self.set.latest_platform_version

        self.hw_version_label.text = self.m.s.hw_version
        self.zh_version_label.text = str(self.m.z_head_version())
        try: self.machine_serial_number_label.text = 'YS6' + str(self.m.serial_number())[0:4]
        except: self.machine_serial_number_label.text = '-'

        self.console_serial_number.text = self.set.console_hostname

        self.get_smartbench_model()
        self.get_smartbench_name()
        self.get_smartbench_location()


    ## EXIT BUTTONS
    def go_back(self):
        self.systemtools_sm.back_to_menu()

    def exit_app(self):
        self.systemtools_sm.exit_app()

    ## GET BUILD INFO
    def on_pre_enter(self, *args):
        # check if language is up to date, if it isn't update all screen strings
        if self.serial_number_header.text != self.l.get_str('Serial number'):
            self.update_strings()

        self.m.send_any_gcode_command('$I')

    def on_enter(self, *args):
        self.scrape_fw_version()

    def scrape_fw_version(self):
        self.fw_version_label.text = str((str(self.m.s.fw_version)).split('; HW')[0])

    
    def open_data_consent_app(self):

        wait_popup = popup_info.PopupWait(self.systemtools_sm.sm, self.l, self.l.get_str("Loading Data and Wi-Fi") + "...")

        def nested_open_data_consent_app(dt):
            self.data_consent_app = screen_manager_data_consent.ScreenManagerDataConsent(None, self.systemtools_sm.sm, self.l)
            self.data_consent_app.open_data_consent('build_info', 'build_info')
            wait_popup.popup.dismiss()

        Clock.schedule_once(nested_open_data_consent_app, 0.2)

    def do_show_more_info(self):
        if self.advanced_button.state == 'normal':
            self.show_more_info.opacity = 0
        if self.advanced_button.state == 'down':
            self.show_more_info.opacity = 1

    def get_smartbench_model(self):
        try:
            file = open(self.smartbench_model_path, 'r')
            self.smartbench_model.text = (str(file.read()).replace("SmartBench ", "")).replace("CNC Router", "")
            file.close()
        except: 
            self.smartbench_model.text = 'SmartBench CNC Router'

    ## LOCALIZATION TESTING

    def choose_language(self):
        chosen_lang = self.language_button.text
        self.l.load_in_new_language(chosen_lang)
        self.update_strings()
        self.restart_app()
        self.reset_language = True

    def update_strings(self):
        self.language_button.text = self.l.lang
        self.data_and_wifi_button.text = self.l.get_str('Data and Wi-Fi')
        self.advanced_button.text = self.l.get_str('Advanced') + '...'
        self.header.text = self.l.get_str('System Information')
        self.smartbench_model_header.text = self.l.get_str('SmartBench model')
        self.serial_number_header.text = self.l.get_str('Serial number')
        self.console_serial_number_header.text = self.l.get_str('Console hostname')
        self.software_header.text = self.l.get_str('Software')
        self.platform_header.text = self.l.get_str('Platform')
        self.firmware_header.text = self.l.get_str('Firmware')
        self.zhead_header.text = self.l.get_str('Z head')
        self.hardware_header.text = self.l.get_str('Hardware')

        self.show_more_info.text = (
            self.l.get_str('Software') + '\n' + \
            self.set.sw_branch + '\n' + \
            self.set.sw_hash + '\n\n' #+ \
            # self.l.get_str('Platform') + '\n' + \
            # self.set.pl_branch + '\n' + \
            # self.set.pl_hash + '\n\n' + \
            # self.l.get_str('IP Address') + '\n' + \
            # str(self.set.ip_address)
            )

    def restart_app(self):
        if self.reset_language == True: 
            popup_system.RebootAfterLanguageChange(self.systemtools_sm, self.l)

    ## SMARTBENCH NAMING

    def on_focus(self, instance, value):
        if not value:
            self.save_new_name()

    def set_focus_on_text_input(self, dt):
        self.smartbench_name_input.focus = True

    def open_rename(self):
        
        self.smartbench_name.disabled = True
        self.smartbench_name_input.disabled = False
        self.smartbench_name.height = 0
        self.smartbench_name.opacity = 0
        self.smartbench_name_input.height = 40
        self.smartbench_name_input.opacity = 1
        self.smartbench_name.focus = False

        Clock.schedule_once(self.set_focus_on_text_input, 0.3)
        

    def save_new_name(self):
        self.smartbench_name_unformatted = self.smartbench_name_input.text
        self.write_name_to_file()

        self.smartbench_name_input.focus = False

        self.smartbench_name_input.disabled = True
        self.smartbench_name.disabled = False
        self.smartbench_name_input.height = 0
        self.smartbench_name_input.opacity = 0
        self.smartbench_name.height = 40
        self.smartbench_name.opacity = 1

        self.get_smartbench_name()

    def get_smartbench_name(self):
        
        self.smartbench_name_unformatted = self.m.device_label

        # Remove newlines
        self.smartbench_name_formatted = self.smartbench_name_unformatted.replace('\n', ' ')
        # Remove trailing and leading whitespaces
        self.smartbench_name_formatted = self.smartbench_name_formatted.strip()

        self.smartbench_name_label.text = '[b]' + self.smartbench_name_formatted + '[/b]'
        self.smartbench_name_input.text = self.smartbench_name_formatted

    def write_name_to_file(self):

        if self.m.write_device_label(str(self.smartbench_name_unformatted)):
            return True

        else:
            warning_message = self.l.get_str('Problem saving nickname!')
            popup_info.PopupWarning(self.systemtools_sm.sm, warning_message)
            return False

    ## SMARTBENCH LOCATION NAMING

    def on_focus_location(self, instance, value):
        if not value:
            self.save_new_location()

    def set_focus_on_location_input(self, dt):
        self.smartbench_location_input.focus = True

    def open_rename_location(self):
        
        self.smartbench_location.disabled = True
        self.smartbench_location_input.disabled = False
        self.smartbench_location.height = 0
        self.smartbench_location.opacity = 0
        self.smartbench_location_input.height = 30
        self.smartbench_location_input.opacity = 1
        self.smartbench_location.focus = False

        Clock.schedule_once(self.set_focus_on_location_input, 0.3)

    def save_new_location(self):
        self.smartbench_location_unformatted = self.smartbench_location_input.text
        self.write_location_to_file()

        self.smartbench_location_input.focus = False
        self.smartbench_location_input.disabled = True
        self.smartbench_location.disabled = False
        self.smartbench_location_input.height = 0
        self.smartbench_location_input.opacity = 0
        self.smartbench_location.height = 30
        self.smartbench_location.opacity = 1
        self.get_smartbench_location()


    def get_smartbench_location(self):
        
        self.smartbench_location_unformatted = self.m.device_location

        # Remove newlines
        self.smartbench_location_formatted = self.smartbench_location_unformatted.replace('\n', ' ')
        # Remove trailing and leading whitespaces
        self.smartbench_location_formatted = self.smartbench_location_formatted.strip()

        if self.smartbench_location_formatted == 'SmartBench location':
            self.smartbench_location_formatted = self.l.get_str('SmartBench location')

        self.smartbench_location_label.text = '[b]' + self.smartbench_location_formatted + '[/b]'
        self.smartbench_location_input.text = self.smartbench_location_formatted

        self.smartbench_location_label.width = dp(len(self.smartbench_location_label.text)*10)
        self.smartbench_location_buffer.width = dp(self.smartbench_location.width) - dp(self.smartbench_location_label.width) - dp(24)
        self.smartbench_location_label.texture_update()

        print("*10, " + str(self.smartbench_location_label.is_shortened))

        if self.smartbench_location_label.is_shortened: 
            self.smartbench_location_label.width = dp(len(self.smartbench_location_label.text)*14)
            self.smartbench_location_buffer.width = dp(self.smartbench_location.width) - dp(self.smartbench_location_label.width) - dp(24)
            self.smartbench_location_label.texture_update()
            print("*14, " + str(self.smartbench_location_label.is_shortened))

        else: 
            return

        if self.smartbench_location_label.is_shortened: 
            self.smartbench_location_label.width = dp(len(self.smartbench_location_label.text)*18)
            self.smartbench_location_buffer.width = dp(self.smartbench_location.width) - dp(self.smartbench_location_label.width) - dp(24)
            self.smartbench_location_label.texture_update()
            print("*18, " + str(self.smartbench_location_label.is_shortened))
        else: 
            return

        if self.smartbench_location_label.is_shortened: 
            self.smartbench_location_label.width = dp(len(self.smartbench_location_label.text)*20)
            self.smartbench_location_buffer.width = dp(self.smartbench_location.width) - dp(self.smartbench_location_label.width) - dp(24)
            self.smartbench_location_label.texture_update()
            print("*20, " + str(self.smartbench_location_label.is_shortened))


    def write_location_to_file(self):

        if self.m.write_device_location(str(self.smartbench_location_unformatted)):
            return True

        else:
            warning_message = 'Problem saving location!!'
            popup_info.PopupWarning(self.systemtools_sm.sm, warning_message)
            return False
