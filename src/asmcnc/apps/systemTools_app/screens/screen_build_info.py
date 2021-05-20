'''
Created on 18 November 2020
Build info screen for system tools app

@author: Letty
'''
import os, sys

from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, Screen

from asmcnc.skavaUI import popup_info

Builder.load_string("""

<BuildInfoScreen>

    sw_version_label: sw_version_label
    pl_version_label: pl_version_label
    fw_version_label: fw_version_label
    hw_version_label: hw_version_label
    zh_version_label: zh_version_label
    smartbench_name : smartbench_name
    smartbench_name_input : smartbench_name_input
    smartbench_model: smartbench_model
    machine_serial_number_label: machine_serial_number_label
    show_more_info: show_more_info
    more_info_button: more_info_button
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
                    height: dp(300)
                    width: dp(550)

                    Button:
                        id: smartbench_name
                        text: '[b]My SmartBench[/b]'
                        background_color: hex('#f9f9f9ff')
                        background_normal: ""
                        background_down: ""
                        color: hex('#333333ff')
                        text_size: self.size
                        halign: "left"
                        valign: "middle"
                        markup: True
                        font_size: 28
                        size_hint_y: None
                        height: dp(40)
                        opacity: 1
                        on_press: root.open_rename()

                    TextInput:
                        id: smartbench_name_input
                        text: 'My SmartBench'
                        color: hex('#333333ff')
                        text_size: self.size
                        halign: "left"
                        valign: "middle"
                        markup: True
                        font_size: 28
                        size_hint_y: None
                        height: dp(0)
                        opacity: 0
                        on_text_validate: root.save_new_name()
                        disabled: True
                        multiline: False

                    Label:
                        id: smartbench_model
                        text: '-'
                        color: hex('#333333ff')
                        text_size: self.size
                        halign: "left"
                        valign: "middle"
                        markup: True
                        font_size: 22

                    GridLayout:
                        size: self.parent.size
                        pos: self.parent.pos
                        cols: 2
                        rows: 8
                        size_hint: (None, None)
                        height: dp(220)
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
                            text: '[b]Console hostname[/b]'
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
                    BoxLayout: 
                        size_hint: (None, None)
                        height: dp(35)
                        width: dp(150)
                        # padding: [30,0]
                        ToggleButton:
                            id: more_info_button
                            size_hint: (None,None)
                            height: dp(35)
                            width: dp(150)
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
                        height: dp(245)
                        width: dp(210)
                        padding: [0,0]

                        Label: 
                            id: show_more_info
                            text: ''
                            opacity: 0
                            color: hex('#333333ff')

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
    smartbench_name_filepath = '/home/pi/smartbench_name.txt'

    smartbench_name_unformatted = 'My SmartBench'


    def __init__(self, **kwargs):
        super(BuildInfoScreen, self).__init__(**kwargs)
        self.systemtools_sm = kwargs['system_tools']
        self.m = kwargs['machine']
        self.set = kwargs['settings']

        self.sw_version_label.text = self.set.sw_version
        self.pl_version_label.text = self.set.platform_version
        self.latest_sw_version = self.set.latest_sw_version
        self.latest_platform_version = self.set.latest_platform_version

        self.hw_version_label.text = self.m.s.hw_version
        self.zh_version_label.text = str(self.m.z_head_version())
        try: self.machine_serial_number_label.text = 'YS6' + str(self.m.serial_number())[0:4]
        except: self.machine_serial_number_label.text = '-'

        self.show_more_info.text = 'Software\n' + self.set.sw_branch + '\n' + self.set.sw_hash + \
        '\n\nPlatform\n' + self.set.pl_branch + '\n' + self.set.pl_hash + \
        '\n\nIP address\n' + self.get_ip_address()

        self.console_serial_number.text = (os.popen('hostname').read()).split('.')[0]

        self.get_smartbench_model()
        self.get_smartbench_name()


    ## EXIT BUTTONS
    def go_back(self):
        self.systemtools_sm.back_to_menu()

    def exit_app(self):
        self.systemtools_sm.exit_app()

    ## GET BUILD INFO
    def on_pre_enter(self, *args):
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


    ## SMARTBENCH NAMING

    def open_rename(self):
        self.smartbench_name.disabled = True
        self.smartbench_name_input.disabled = False
        self.smartbench_name.height = 0
        self.smartbench_name_input.height = 40
        self.smartbench_name.opacity = 0
        self.smartbench_name_input.opacity = 1

    def save_new_name(self):
        self.smartbench_name_unformatted = self.smartbench_name_input.text
        self.write_name_to_file()
        self.smartbench_name_input.disabled = True
        self.smartbench_name.disabled = False
        self.smartbench_name.height = 40
        self.smartbench_name_input.height = 0
        self.smartbench_name.opacity = 1
        self.smartbench_name_input.opacity = 0
        self.get_smartbench_name()

    def get_smartbench_name(self):
        try:
            file = open(self.smartbench_name_filepath, 'r')
            self.smartbench_name_unformatted = str(file.read())
            file.close()

        except: 
            self.smartbench_name_unformatted = 'My SmartBench'

        self.smartbench_name.text = '[b]' + self.smartbench_name_unformatted + '[/b]'
        self.smartbench_name_input.text = self.smartbench_name_unformatted

    def write_name_to_file(self):

        try:
            file_sb_name = open(self.smartbench_name_filepath, "w+")
            file_sb_name.write(str(self.smartbench_name_unformatted))
            file_sb_name.close()
            return True

        except: 
            warning_message = 'Problem saving nickname!!'
            popup_info.PopupWarning(self.systemtools_sm.sm, warning_message)
            return False