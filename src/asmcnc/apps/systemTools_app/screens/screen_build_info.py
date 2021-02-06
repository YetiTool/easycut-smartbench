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

from asmcnc.skavaUI import popup_info
from asmcnc.apps.systemTools_app.screens import popup_system

Builder.load_string("""

#:import Factory kivy.factory.Factory


<LanguageSpinner@SpinnerOption>

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
    smartbench_model: smartbench_model
    machine_serial_number_label: machine_serial_number_label
    show_more_info: show_more_info
    more_info_button: more_info_button
    language_button: language_button
    console_serial_number: console_serial_number

    BoxLayout:
        height: dp(800)
        width: dp(480)
        canvas.before:
            Color: 
                rgba: hex('#f9f9f9ff')
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
                padding: 20
                spacing: 0
                orientation: 'horizontal'

                BoxLayout:
                    orientation: 'vertical'
                    size_hint: (None, None)
                    height: dp(280)
                    width: dp(550)

                    Label:
                        id: smartbench_model
                        text: '-'
                        color: hex('#333333ff')
                        text_size: self.size
                        halign: "left"
                        valign: "middle"
                        markup: True
                        font_size: 24

                    GridLayout:
                        size: self.parent.size
                        pos: self.parent.pos
                        cols: 2
                        rows: 8
                        size_hint: (None, None)
                        height: dp(240)
                        width: dp(550)
                        cols_minimum: {0: dp(230), 1: dp(320)}

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
                            text: '[b]Console serial number[/b]'
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
                    spacing: 0
                    orientation: 'vertical'

                    # canvas:
                    #     Color:
                    #         rgba: [1,1,1,1]
                    #     Rectangle:
                    #         pos: self.pos
                    #         size: self.size


                    BoxLayout: 
                        size_hint: (None, None)
                        height: dp(35)
                        width: dp(180)
                        # padding: [30,0]
                        ToggleButton:
                            id: more_info_button
                            size_hint: (None,None)
                            height: dp(35)
                            width: dp(180)
                            background_normal: "./asmcnc/apps/systemTools_app/img/word_button.png"
                            background_down: "./asmcnc/apps/systemTools_app/img/word_button.png"
                            border: [dp(7.5)]*4
                            center: self.parent.center
                            pos: self.parent.pos
                            on_press: root.do_show_more_info()
                            text: 'More info...'
                            color: hex('#f9f9f9ff')
                            markup: True
                    BoxLayout: 
                        size_hint: (None, None)
                        height: dp(200)
                        width: dp(210)
                        padding: [0,0]

                        Label: 
                            id: show_more_info
                            text: ''
                            opacity: 0
                            color: hex('#333333ff')


                    BoxLayout: 
                        size_hint: (None, None)
                        height: dp(35)
                        width: dp(180)
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
                            option_cls: Factory.get("LanguageSpinner")
                            on_text: root.choose_language()

                    BoxLayout: 
                        size_hint: (None, None)
                        height: dp(10)
                        width: dp(210)





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

    smartbench_model_path = '/home/pi/smartbench_model_name.txt'
    language_list = []
    reset_language = False

    def __init__(self, **kwargs):
        super(BuildInfoScreen, self).__init__(**kwargs)
        self.systemtools_sm = kwargs['system_tools']
        self.m = kwargs['machine']
        self.set = kwargs['settings']
        self.l = kwargs['localization']

        self.update_strings()
        self.language_button.values = self.l.supported_languages

        self.sw_version_label.text = self.set.sw_version
        self.pl_version_label.text = self.set.platform_version
        self.latest_sw_version = self.set.latest_sw_version
        self.latest_platform_version = self.set.latest_platform_version

        self.hw_version_label.text = self.m.s.hw_version
        self.zh_version_label.text = str(self.m.z_head_version())
        try: self.machine_serial_number_label.text = 'YS6' + str(self.m.serial_number())[0:4]
        except: self.machine_serial_number_label.text = '-'

        self.console_serial_number.text = (os.popen('hostname').read()).split('.')[0]

        self.get_smartbench_model()

    ## EXIT BUTTONS
    def go_back(self):
        self.systemtools_sm.back_to_menu()

    def exit_app(self):
        self.systemtools_sm.exit_app()

    ## GET BUILD INFO
    def on_pre_enter(self, *args):
        # check if language is up to date, if it isn't update all screen strings
        if self.serial_number_header.text != str(self.l.dictionary['Serial number']):
            self.update_strings()

        self.m.send_any_gcode_command('$I')

    def on_enter(self, *args):
        self.scrape_fw_version()

    def scrape_fw_version(self):
        self.fw_version_label.text = str((str(self.m.s.fw_version)).split('; HW')[0])

    def do_show_more_info(self):
        if self.more_info_button.state == 'normal':
            self.show_more_info.opacity = 0
        if self.more_info_button.state == 'down':
            self.show_more_info.opacity = 1

    def get_smartbench_model(self):
        try:
            file = open(self.smartbench_model_path, 'r')
            self.smartbench_model.text = '[b]' + str(file.read()) + '[/b]'
            file.close()
        except: 
            self.smartbench_model.text = '[b]SmartBench CNC Router[/b]'

    def get_ip_address(self):

        ip_address = ''

        if sys.platform == "win32":
            try:
                hostname=socket.gethostname()
                IPAddr=socket.gethostbyname(hostname)
                ip_address = str(IPAddr)

            except:
                ip_address = ''
        else:
            try:
                f = os.popen('hostname -I')
                first_info = f.read().strip().split(' ')[0]
                if len(first_info.split('.')) == 4:
                    ip_address = first_info

                else:
                    ip_address = ''

            except:
                ip_address = ''

        return ip_address

    ## LOCALIZATION TESTING

    def choose_language(self):
        chosen_lang = self.language_button.text
        self.l.load_in_new_language(chosen_lang)
        self.update_strings()
        self.restart_app()
        self.reset_language = True

    def update_strings(self):
        self.language_button.text = self.l.lang
        self.more_info_button.text = self.l.get_str('More info') + '...'
        self.header.text = self.l.get_str('System Information')
        self.serial_number_header.text = self.l.get_str('Serial number')
        self.console_serial_number_header.text = self.l.get_str('Console serial number')
        self.software_header.text = self.l.get_str('Software')
        self.platform_header.text = self.l.get_str('Platform')
        self.firmware_header.text = self.l.get_str('Firmware')
        self.zhead_header.text = self.l.get_str('Z head')
        self.hardware_header.text = self.l.get_str('Hardware')

        self.show_more_info.text = (
            self.l.get_str('Software') + '\n' + \
            self.set.sw_branch + '\n' + \
            self.set.sw_hash + '\n\n' + \
            self.l.get_str('Platform') + '\n' + \
            self.set.pl_branch + '\n' + \
            self.set.pl_hash + '\n\n' + \
            self.l.get_str('IP Address') + '\n' + \
            self.get_ip_address()
            )

    def restart_app(self):
        if self.reset_language == True: 
            popup_system.RebootAfterLanguageChange(self.systemtools_sm, self.l)

