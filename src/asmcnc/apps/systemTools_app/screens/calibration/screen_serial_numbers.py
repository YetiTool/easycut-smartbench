from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from asmcnc.comms.yeti_grbl_protocol.c_defines import *
from kivy.properties import ObjectProperty
import re

Builder.load_string("""
<UploadSerialNumbersScreen>:

    machine_serial_input:machine_serial_input
    zhead_serial_input:zhead_serial_input
    lb_serial_input:lb_serial_input
    ub_serial_input:ub_serial_input
    console_serial_input:console_serial_input
    ybench_serial_input:ybench_serial_input
    spindle_serial_input:spindle_serial_input
    software_version_input:software_version_input
    firmware_version_input:firmware_version_input
    squareness_input:squareness_input
    main_button:main_button
    error_label:error_label

    BoxLayout:
        orientation: 'vertical'
        size_hint_y: 1.00

        Button:
            text: '<<< BACK'
            on_press: root.go_back()
            text_size: self.size
            markup: 'True'
            halign: 'left'
            valign: 'middle'
            padding: [dp(10),0]
            size_hint_y: 0.2
            size_hint_x: 0.5
            font_size: dp(20)

        GridLayout:
            cols: 3
            rows: 4

            GridLayout:
                cols: 1
                rows: 2

                Label: 
                    text: 'Machine Serial'
                    font_size: dp(25)

                TextInput:
                    id: machine_serial_input
                    font_size: dp(30)
                    multiline: False
            
            GridLayout:
                cols: 1
                rows: 2

                Label:
                    text: 'ZHead Serial'
                    font_size: dp(25)

                TextInput:
                    id: zhead_serial_input
                    font_size: dp(30)
                    multiline: False

            GridLayout:
                cols: 1
                rows: 2

                Label:
                    text: 'LB Serial'
                    font_size: dp(25)

                TextInput:
                    id: lb_serial_input
                    font_size: dp(30)
                    multiline: False

            GridLayout:
                cols: 1
                rows: 2

                Label:
                    text: 'UB Serial'
                    font_size: dp(25)

                TextInput:
                    id: ub_serial_input
                    font_size: dp(30)
                    multiline: False

            GridLayout:
                cols: 1
                rows: 2

                Label:
                    text: 'Console Serial'
                    font_size: dp(25)

                TextInput:
                    id: console_serial_input
                    font_size: dp(30)
                    multiline: False

            GridLayout:
                cols: 1
                rows: 2

                Label:
                    text: 'YBench Serial'
                    font_size: dp(25)

                TextInput:
                    id: ybench_serial_input
                    font_size: dp(30)
                    multiline: False

            GridLayout:
                cols: 1
                rows: 2

                Label:
                    text: 'Spindle Serial'
                    font_size: dp(25)

                TextInput:
                    id: spindle_serial_input
                    font_size: dp(30)
                    multiline: False

            GridLayout:
                cols: 1
                rows: 2

                Label:
                    text: 'Software Version'
                    font_size: dp(25)

                TextInput:
                    id: software_version_input
                    font_size: dp(30)
                    multiline: False

            GridLayout:
                cols: 1
                rows: 2

                Label:
                    text: 'Firmware Version'
                    font_size: dp(25)

                TextInput:
                    id: firmware_version_input
                    font_size: dp(30)
                    multiline: False

            GridLayout:
                cols: 1
                rows: 2

                Label:
                    text: 'Squareness'
                    font_size: dp(25)

                TextInput:
                    id: squareness_input
                    font_size: dp(30)
                    multiline: False
                    
        Label:
            id: error_label
            text: 'Ensure all fields are entered accurately'
            font_size: dp(30)
            size_hint_y: 0.2

        Button:
            id: main_button
            on_press: root.validate_and_download()
            text: 'Download'
            font_size: dp(30)
            size_hint_y: 0.2
                

""")

class UploadSerialNumbersScreen(Screen):

    system_tools = ObjectProperty()
    m = ObjectProperty()
    calibration_db = ObjectProperty()

    def __init__(self, **kwargs):
        super(UploadSerialNumbersScreen, self).__init__(**kwargs)

    def validate_and_download(self):
        regex_check = self.check_valid_inputs_regex()
        valid_check = self.check_valid_inputs()

        if not regex_check or not valid_check:
            return

        # @lettie may be worth you doing this part as i'm not sure what happens after the download
        # download logic here

    def check_valid_inputs(self):
        validated = True

        if len(self.spindle_serial_input.text) < 7:
            self.error_label.text = 'Spindle serial invalid'
            validated = False

        if len(self.squareness_input.text) < 1:
            self.error_label.text = 'Squareness invalid'
            validated = False

        if len(self.software_version_input.text) < 1:
            self.error_label.text = 'Software version invalid'
            validated = False

        if len(self.firmware_version_input.text) < 1:
            self.error_label.text = 'Firmware version invalid'
            validated = False
        
        return validated

    def check_valid_inputs_regex(self):
        regex = '^({start})\d{4}$'

        machine_expression = regex.replace('{start}', 'ys6')
        zhead_expression = regex.replace('{start}', 'zh')
        lb_expression = regex.replace('{start}', 'xl')
        ub_expression = regex.replace('{start}', 'xu')
        console_expression = regex.replace('{start}', 'cs')
        ybench_expression = regex.replace('{start}', 'yb')

        machine_pattern = re.compile(machine_expression)
        zhead_pattern = re.compile(zhead_expression)
        lb_pattern = re.compile(lb_expression)
        ub_pattern = re.compile(ub_expression)
        console_pattern = re.compile(console_expression)
        ybench_pattern = re.compile(ybench_expression)

        machine_match = bool(machine_pattern.match(self.machine_serial_input.text))
        zhead_match = bool(zhead_pattern.match(self.zhead_serial_input.text))
        lb_match = bool(lb_pattern.match(self.lb_serial_input.text))
        ub_match = bool(ub_pattern.match(self.ub_serial_input.text))
        console_match = bool(console_pattern.match(self.console_serial_input.text))
        ybench_match = bool(ybench_pattern.match(self.ybench_serial_input.text))

        validated = True

        if not machine_match:
            self.error_label.text = 'Machine serial invalid'
            validated = False
        
        if not zhead_match:
            self.error_label.text = 'ZHead serial invalid'
            validated = False

        if not lb_match:
            self.error_label.text = 'LB serial invalid'
            validated = False
        
        if not ub_match:
            self.error_label.text = 'UB serial invalid'
            validated = False

        if not console_match:
            self.error_label.text = 'Console serial invalid'
            validated = False

        if not ybench_match:
            self.error_label.text = 'YBench serial invalid'
            validated = False

        return validated

        
