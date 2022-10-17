import re
from functools import partial

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock
from asmcnc.comms.yeti_grbl_protocol.c_defines import *
from datetime import datetime
from kivy.uix.spinner import Spinner

from asmcnc.skavaUI import widget_status_bar

Builder.load_string("""
<ZHeadPCBSetUp>:

    status_container : status_container
    hw_info_label : hw_info_label
    recommended_firmware_label : recommended_firmware_label
    recommended_firmware_checkbox : recommended_firmware_checkbox
    alt_v3_firmware_label :  alt_v3_firmware_label
    alt_v3_firmware_checkbox :  alt_v3_firmware_checkbox
    alt_v2_firmware_label :  alt_v2_firmware_label
    alt_v2_firmware_checkbox :  alt_v2_firmware_checkbox
    recommended_z_current_label : recommended_z_current_label
    recommended_z_current_checkbox : recommended_z_current_checkbox
    other_z_current_label :  other_z_current_label
    other_z_current_checkbox :  other_z_current_checkbox
    other_z_current_textinput :  other_z_current_textinput
    single_stack_x_current_label :  single_stack_x_current_label
    single_stack_x_current_checkbox :  single_stack_x_current_checkbox
    double_stack_x_current_label :  double_stack_x_current_label
    double_stack_x_current_checkbox :  double_stack_x_current_checkbox
    other_x_current_label :  other_x_current_label
    other_x_current_checkbox :  other_x_current_checkbox
    other_x_current_textinput :  other_x_current_textinput
    thermal_coeff_x_label :  thermal_coeff_x_label
    thermal_coeff_x_textinput :  thermal_coeff_x_textinput
    thermal_coeff_y_label :  thermal_coeff_y_label
    thermal_coeff_y_textinput :  thermal_coeff_y_textinput
    thermal_coeff_z_label : thermal_coeff_z_label
    thermal_coeff_z_textinput : thermal_coeff_z_textinput

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.92

            BoxLayout:
                orientation: 'horizontal'
                size_hint_y: 0.2

                Button:
                    text: '<<< Home'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]

                Label: 
                    id : hw_info_label
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]

                Button:
                    text: 'Disconnect'
                    text_size: self.size
                    markup: 'True'
                    halign: 'center'
                    valign: 'middle'
                    padding: [dp(10),0]

            BoxLayout: 
                orientation: 'horizontal'
                size_hint_y: 0.6

                BoxLayout: 
                    orientation: 'vertical'
                    padding: [dp(5),dp(10)]

                    BoxLayout: 
                        size_hint_y: 0.2
                        canvas:
                            Color: 
                                rgba: hex('#566573')
                            Rectangle: 
                                size: self.size
                                pos: self.pos

                        Label: 
                            text: "FW version"
                            text_size: self.size
                            markup: 'True'
                            halign: 'left'
                            valign: 'middle'
                            padding: [dp(10),0]

                    BoxLayout: 
                        orientation: 'vertical'
                        size_hint_y: 0.8
                        padding: [dp(5),0]

                        Label: 
                            size_hint_y: 0.2
                            text: "Recommended: "
                            text_size: self.size
                            markup: 'True'
                            halign: 'left'
                            valign: 'middle'

                        BoxLayout: 
                            orientation: 'horizontal'
                            size_hint_y: 0.2
                            CheckBox:
                                id: recommended_firmware_checkbox
                                size_hint_x: 0.2
                                group: "firmware"
                                on_press: root.set_value_to_update_to(recommended_firmware_label, root.firmware_version, self)
                            Label:
                                id: recommended_firmware_label
                                size_hint_x: 0.8
                                text: "2.5.5"
                                text_size: self.size
                                markup: 'True'
                                halign: 'left'
                                valign: 'middle'

                        Label: 
                            size_hint_y: 0.2
                            text: "Alternative & available: "
                            text_size: self.size
                            markup: 'True'
                            halign: 'left'
                            valign: 'middle'

                        BoxLayout: 
                            orientation: 'horizontal'
                            size_hint_y: 0.2

                            CheckBox:
                                id: alt_v3_firmware_checkbox
                                size_hint_x: 0.2
                                group: "firmware" 
                                on_press: root.set_value_to_update_to(alt_v3_firmware_label, root.firmware_version, self)
                            Label:
                                id: alt_v3_firmware_label
                                size_hint_x: 0.3
                                text: "2.5.4"
                                text_size: self.size
                                markup: 'True'
                                halign: 'left'
                                valign: 'middle'

                            CheckBox:
                                id: alt_v2_firmware_checkbox
                                size_hint_x: 0.2
                                group: "firmware" 
                                on_press: root.set_value_to_update_to(alt_v2_firmware_label, root.firmware_version, self)
                            Label:
                                id: alt_v2_firmware_label
                                size_hint_x: 0.3
                                text: "1.4.0"
                                text_size: self.size
                                markup: 'True'
                                halign: 'left'
                                valign: 'middle'

                        BoxLayout: 
                            size_hint_y: 0.2

                BoxLayout: 
                    orientation: 'vertical'
                    padding: [dp(5),dp(10)]

                    BoxLayout: 
                        size_hint_y: 0.2
                        canvas:
                            Color: 
                                rgba: hex('#566573')
                            Rectangle: 
                                size: self.size
                                pos: self.pos

                        Label: 
                            text: "Z current (v1.3)"
                            text_size: self.size
                            markup: 'True'
                            halign: 'left'
                            valign: 'middle'
                            padding: [dp(10),0]

                    BoxLayout: 
                        orientation: 'vertical'
                        size_hint_y: 0.8
                        padding: [dp(5),0]

                        BoxLayout: 
                            orientation: 'horizontal'
                            size_hint_y: 0.2
                            CheckBox:
                                id: recommended_z_current_checkbox
                                size_hint_x: 0.2
                                group: "z_current" 
                                on_press: root.set_value_to_update_to(recommended_z_current_label, root.z_current, self)
                            Label:
                                id: recommended_z_current_label
                                size_hint_x: 0.8
                                text: "25"
                                text_size: self.size
                                markup: 'True'
                                halign: 'left'
                                valign: 'middle'

                        BoxLayout: 
                            orientation: 'horizontal'
                            size_hint_y: 0.2
                            CheckBox:
                                id: other_z_current_checkbox
                                size_hint_x: 0.2
                                group: "z_current" 
                                on_press: root.set_value_to_update_to(other_z_current_textinput, root.z_current, self)
                            Label:
                                id: other_z_current_label
                                size_hint_x: 0.4
                                text: "Other"
                                text_size: self.size
                                markup: 'True'
                                halign: 'left'
                                valign: 'middle'

                            TextInput:
                                id: other_z_current_textinput
                                size_hint_x: 0.4
                                text: "25"
                                input_filter: "int"
                                multiline: False
                                font_size: "22sp"
                                padding: [dp(5), dp(5)]
                        
                        BoxLayout: 
                            size_hint_y: 0.6



                BoxLayout: 
                    orientation: 'vertical'
                    padding: [dp(5),dp(10)]

                    BoxLayout: 
                        size_hint_y: 0.2
                        canvas:
                            Color: 
                                rgba: hex('#566573')
                            Rectangle: 
                                size: self.size
                                pos: self.pos

                        Label: 
                            text: "X current (v1.3)"
                            text_size: self.size
                            markup: 'True'
                            halign: 'left'
                            valign: 'middle'
                            padding: [dp(10),0]

                    BoxLayout: 
                        orientation: 'vertical'
                        size_hint_y: 0.8
                        padding: [dp(5),0]

                        BoxLayout: 
                            orientation: 'horizontal'
                            size_hint_y: 0.2
                            CheckBox:
                                id: single_stack_x_current_checkbox
                                size_hint_x: 0.2
                                group: "x_current" 
                                on_press: root.set_value_to_update_to(single_stack_x_current_label, root.x_current, self)
                            Label:
                                id: single_stack_x_current_label
                                size_hint_x: 0.8
                                text: "26 (single stack)"
                                text_size: self.size
                                markup: 'True'
                                halign: 'left'
                                valign: 'middle'

                        BoxLayout: 
                            orientation: 'horizontal'
                            size_hint_y: 0.2
                            CheckBox:
                                id: double_stack_x_current_checkbox
                                size_hint_x: 0.2
                                group: "x_current"
                                on_press: root.set_value_to_update_to(double_stack_x_current_label, root.x_current, self)
                            Label:
                                id: double_stack_x_current_label
                                size_hint_x: 0.8
                                text: "20 (double stack)"
                                text_size: self.size
                                markup: 'True'
                                halign: 'left'
                                valign: 'middle'

                        BoxLayout: 
                            orientation: 'horizontal'
                            size_hint_y: 0.2
                            CheckBox:
                                id: other_x_current_checkbox
                                size_hint_x: 0.2
                                group: "x_current" 
                                on_press: root.set_value_to_update_to(other_x_current_textinput, root.x_current, self)
                            Label:
                                id: other_x_current_label
                                size_hint_x: 0.4
                                text: "Other"
                                text_size: self.size
                                markup: 'True'
                                halign: 'left'
                                valign: 'middle'

                            TextInput:
                                id: other_x_current_textinput
                                size_hint_x: 0.4
                                text: "25"
                                input_filter: "int"
                                multiline: False
                                font_size: "22sp"
                                padding: [dp(5), dp(5)]

                        BoxLayout: 
                            size_hint_y: 0.4

                BoxLayout: 
                    orientation: 'vertical'
                    padding: [dp(5),dp(10)]

                    BoxLayout: 
                        size_hint_y: 0.2
                        canvas:
                            Color: 
                                rgba: hex('#566573')
                            Rectangle: 
                                size: self.size
                                pos: self.pos

                        Label: 
                            text: "Thermal coefficients (v1.3)"
                            text_size: self.size
                            markup: 'True'
                            halign: 'left'
                            valign: 'middle'
                            padding: [dp(10),0]

                    BoxLayout: 
                        orientation: 'vertical'
                        size_hint_y: 0.8
                        padding: [dp(5),0]

                        GridLayout: 
                            size_hint_y: 0.6
                            cols: 2
                            rows: 3
                            Label:
                                id: thermal_coeff_x_label
                                text: "X"
                            TextInput:
                                id: thermal_coeff_x_textinput
                                text: "5000"
                                input_filter: "int"
                                multiline: False
                                font_size: "22sp"
                                padding: [dp(5), dp(5)]
                            Label:
                                id: thermal_coeff_y_label
                                text: "Y"
                            TextInput:
                                id: thermal_coeff_y_textinput
                                text: "5000"
                                input_filter: "int"
                                multiline: False
                                font_size: "22sp"
                                padding: [dp(5), dp(5)]
                            Label:
                                id: thermal_coeff_z_label
                                text: "Z"
                            TextInput:
                                id: thermal_coeff_z_textinput
                                text: "10000"
                                input_filter: "int"
                                multiline: False
                                font_size: "22sp"
                                padding: [dp(5), dp(5)]
                                on_text_validate: root.set_value_to_update_to(self, root.z_thermal_coefficient)

                        BoxLayout: 
                            size_hint_y: 0.4

            Button:
                on_press: 
                text: 'OK'
                font_size: dp(30)
                size_hint_y: 0.2

        BoxLayout:
            size_hint_y: 0.08
            id: status_container 
            pos: self.pos
""")

def log(message):
    timestamp = datetime.now()
    print ('Z Head Connecting Screen: ' + timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))

class ZHeadPCBSetUp(Screen):

    firmware_version = "2.5.5"
    x_current = "20"
    z_current = "25"
    x_thermal_coefficient = "5000"
    y_thermal_coefficient = "5000"
    z_thermal_coefficient = "10000"

    def __init__(self, **kwargs):

        super(ZHeadPCBSetUp, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']

        # Green status bar
        self.status_bar_widget = widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm)
        self.status_container.add_widget(self.status_bar_widget)

        self.other_x_current_textinput.bind(focus=partial(self.on_focus, self.x_current, self.other_x_current_checkbox))
        self.other_z_current_textinput.bind(focus=partial(self.on_focus, self.z_current, self.other_z_current_checkbox))

        self.thermal_coeff_x_textinput.bind(focus=partial(self.on_focus, self.x_thermal_coefficient, None))
        self.thermal_coeff_y_textinput.bind(focus=partial(self.on_focus, self.y_thermal_coefficient, None))
        self.thermal_coeff_z_textinput.bind(focus=partial(self.on_focus, self.z_thermal_coefficient, None))

    def on_enter(self):
        self.set_value_to_update_to(self.recommended_firmware_label, self.firmware_version, self.recommended_firmware_checkbox)
        self.set_value_to_update_to(self.recommended_z_current_label, self.z_current, self.recommended_z_current_checkbox)
        self.set_value_to_update_to(self.single_stack_x_current_label, self.x_current, self.single_stack_x_current_checkbox)
        self.scrape_fw_version()

    def on_focus(self, value_to_set, radio_button, instance, value):
        if not value:
            self.set_value_to_update_to(instance, value_to_set, radio_button)

    def set_value_to_update_to(self, text_obj, value_to_set, radio_button = None):
        if radio_button != None: radio_button.state ='down'
        value_to_set = re.findall('[0-9.]+', text_obj.text)[0]
        print(value_to_set)

    def scrape_fw_version(self):
        # try:

        fw_and_hw = str(self.m.s.fw_version).split('; HW:')

        no_drivers = 3

        self.hw_info_label.text = "HW version: " + fw_and_hw[1] + "\n" + "No. motor drivers: " + str(no_drivers) + "\n" + "FW version: " + fw_and_hw[0]
        
        # except:
        #     pass

































