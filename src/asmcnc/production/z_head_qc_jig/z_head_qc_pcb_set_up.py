import re
from functools import partial
import glob
import os, subprocess
from asmcnc.comms.logging_system.logging_system import Logger
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock
from asmcnc.comms.yeti_grbl_protocol.c_defines import *
from datetime import datetime
from asmcnc.skavaUI import widget_status_bar

Builder.load_string(
    """
<ZHeadPCBSetUp>:

    status_container : status_container
    hw_info_label : hw_info_label
    connection_button : connection_button
    recommended_firmware_label : recommended_firmware_label
    recommended_firmware_checkbox : recommended_firmware_checkbox
    alt_v3_firmware_label :  alt_v3_firmware_label
    alt_v3_firmware_checkbox :  alt_v3_firmware_checkbox
    alt_v2_firmware_label :  alt_v2_firmware_label
    alt_v2_firmware_checkbox :  alt_v2_firmware_checkbox
    single_stack_x_current_label :  single_stack_x_current_label
    single_stack_x_current_checkbox :  single_stack_x_current_checkbox
    double_stack_x_current_label :  double_stack_x_current_label
    double_stack_x_current_checkbox :  double_stack_x_current_checkbox
    other_x_current_label :  other_x_current_label
    other_x_current_checkbox :  other_x_current_checkbox
    other_x_current_textinput :  other_x_current_textinput
    recommended_z_current_label : recommended_z_current_label
    recommended_z_current_checkbox : recommended_z_current_checkbox
    other_z_current_label :  other_z_current_label
    other_z_current_checkbox :  other_z_current_checkbox
    other_z_current_textinput :  other_z_current_textinput
    thermal_coeff_x_label :  thermal_coeff_x_label
    thermal_coeff_x_textinput :  thermal_coeff_x_textinput
    thermal_coeff_y_label :  thermal_coeff_y_label
    thermal_coeff_y_textinput :  thermal_coeff_y_textinput
    thermal_coeff_z_label : thermal_coeff_z_label
    thermal_coeff_z_textinput : thermal_coeff_z_textinput
    ok_button : ok_button


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
                    on_press: root.go_to_qc_home()

                Label: 
                    id : hw_info_label
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]


                ToggleButton: 
                    id: connection_button
                    text: 'Disconnect'
                    text_size: self.size
                    markup: 'True'
                    halign: 'center'
                    valign: 'middle'
                    padding: [dp(10),0]
                    font_size: dp(20)
                    on_press: root.toggle_connection_to_z_head()

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
                                on_press: root.firmware_version = root.set_value_to_update_to(recommended_firmware_label, self)
                            Label:
                                id: recommended_firmware_label
                                size_hint_x: 0.8
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
                                on_press: root.firmware_version = root.set_value_to_update_to(alt_v3_firmware_label, self)
                            Label:
                                id: alt_v3_firmware_label
                                size_hint_x: 0.3
                                text_size: self.size
                                markup: 'True'
                                halign: 'left'
                                valign: 'middle'

                            CheckBox:
                                id: alt_v2_firmware_checkbox
                                size_hint_x: 0.2
                                group: "firmware" 
                                on_press: root.firmware_version = root.set_value_to_update_to(alt_v2_firmware_label, self)
                            Label:
                                id: alt_v2_firmware_label
                                size_hint_x: 0.3
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
                                id: double_stack_x_current_checkbox
                                size_hint_x: 0.2
                                group: "x_current"
                                on_press: root.x_current = root.set_value_to_update_to(double_stack_x_current_label, self)
                            Label:
                                id: double_stack_x_current_label
                                size_hint_x: 0.8
                                text_size: self.size
                                markup: 'True'
                                halign: 'left'
                                valign: 'middle'

                        BoxLayout: 
                            orientation: 'horizontal'
                            size_hint_y: 0.2
                            CheckBox:
                                id: single_stack_x_current_checkbox
                                size_hint_x: 0.2
                                group: "x_current" 
                                on_press: root.x_current = root.set_value_to_update_to(single_stack_x_current_label, self)
                            Label:
                                id: single_stack_x_current_label
                                size_hint_x: 0.8
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
                                on_press: root.x_current = root.set_value_to_update_to(other_x_current_textinput, self)
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
                                input_filter: "int"
                                multiline: False
                                font_size: "22sp"
                                padding: [dp(5), dp(5)]
                                on_text_validate: root.x_current = root.set_value_to_update_to(other_x_current_textinput, self)

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
                                on_press: root.z_current = root.set_value_to_update_to(recommended_z_current_label, self)
                            Label:
                                id: recommended_z_current_label
                                size_hint_x: 0.8
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
                                on_press: root.z_current = root.set_value_to_update_to(other_z_current_textinput, self)
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
                                input_filter: "int"
                                multiline: False
                                font_size: "22sp"
                                padding: [dp(5), dp(5)]
                                on_text_validate: root.z_current = root.set_value_to_update_to(other_z_current_textinput, self)
                        
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
                                on_text_validate: root.x_thermal_coefficient = root.set_value_to_update_to(self)
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
                                on_text_validate: root.y_thermal_coefficient = root.set_value_to_update_to(self)
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
                                on_text_validate: root.z_thermal_coefficient = root.set_value_to_update_to(self)

                        BoxLayout: 
                            size_hint_y: 0.4

            Button:
                id: ok_button
                text: 'OK'
                font_size: dp(30)
                size_hint_y: 0.2
                on_press: root.do_pcb_update_and_set_settings()

        BoxLayout:
            size_hint_y: 0.08
            id: status_container 
            pos: self.pos
"""
)


class ZHeadPCBSetUp(Screen):
    usb_path = "/media/usb/"
    single_stack_single_driver_x_current = 26
    double_stack_single_driver_x_current = 31
    single_stack_dual_driver_x_current = 13
    double_stack_dual_driver_x_current = 27
    default_z_current = 31
    default_y_current = 28
    default_x_thermal_coefficient = 5000
    default_y_thermal_coefficient = 5000
    default_z_thermal_coefficient = 10000
    firmware_version = "2.5.5"
    number_of_drivers = 4
    x_current = str(single_stack_dual_driver_x_current)
    y_current = str(default_y_current)
    z_current = str(default_z_current)
    x_thermal_coefficient = str(default_x_thermal_coefficient)
    y_thermal_coefficient = str(default_y_thermal_coefficient)
    z_thermal_coefficient = str(default_z_thermal_coefficient)
    poll_for_reconnection = None
    x_current_single_driver_max = 31
    x_current_dual_driver_max = 31
    z_current_max = 31
    x_current_single_driver_min = 0
    x_current_dual_driver_min = 0
    z_current_min = 0
    x_thermal_coefficient_max = 65000
    y_thermal_coefficient_max = 65000
    z_thermal_coefficient_max = 65000
    x_thermal_coefficient_min = 0
    y_thermal_coefficient_min = 0
    z_thermal_coefficient_min = 0
    exit_code = None

    def __init__(self, **kwargs):
        self.sm = kwargs.pop("sm")
        self.m = kwargs.pop("m")
        super(ZHeadPCBSetUp, self).__init__(**kwargs)
        self.status_bar_widget = widget_status_bar.StatusBar(
            machine=self.m, screen_manager=self.sm
        )
        self.status_container.add_widget(self.status_bar_widget)
        self.x_current_checkbox_group = [
            self.other_x_current_checkbox,
            self.single_stack_x_current_checkbox,
            self.double_stack_x_current_checkbox,
        ]
        self.z_current_checkbox_group = [
            self.other_z_current_checkbox,
            self.recommended_z_current_checkbox,
        ]
        self.other_x_current_textinput.bind(
            focus=partial(self.on_focus, self.x_current_checkbox_group)
        )
        self.other_z_current_textinput.bind(
            focus=partial(self.on_focus, self.z_current_checkbox_group)
        )

    def on_pre_enter(self):
        self.ok_button.text = "Flash FW and set up PCB"
        self.exit_code = None
        self.set_default_thermal_coefficients()
        self.set_default_z_current()
        if not self.m.s.hw_version:
            self.hw_info_label.text = "Can't read HW version :("
            return
        self.number_of_drivers = self.generate_no_drivers_based_on_hw_version(
            self.m.s.hw_version
        )
        self.set_default_x_current(self.number_of_drivers)
        self.generate_hw_and_fw_info_label(
            self.m.s.hw_version, self.m.s.fw_version, self.number_of_drivers
        )
        self.set_default_firmware_version()

    def go_to_qc_home(self):
        self.sm.current = "qchome"

    def set_default_thermal_coefficients(self):
        self.x_thermal_coefficient = str(self.default_x_thermal_coefficient)
        self.y_thermal_coefficient = str(self.default_y_thermal_coefficient)
        self.z_thermal_coefficient = str(self.default_z_thermal_coefficient)
        self.thermal_coeff_x_textinput.text = str(self.x_thermal_coefficient)
        self.thermal_coeff_y_textinput.text = str(self.y_thermal_coefficient)
        self.thermal_coeff_z_textinput.text = str(self.z_thermal_coefficient)

    def set_default_z_current(self):
        self.recommended_z_current_checkbox.state = "normal"
        self.other_z_current_checkbox.state = "normal"
        self.recommended_z_current_label.text = str(self.default_z_current)
        self.other_z_current_textinput.text = str(self.z_current)
        self.z_current = self.set_value_to_update_to(
            self.recommended_z_current_label, self.recommended_z_current_checkbox
        )

    def set_default_x_current(self, number_of_drivers):
        self.double_stack_x_current_checkbox.state = "normal"
        self.single_stack_x_current_checkbox.state = "normal"
        self.other_x_current_checkbox.state = "normal"
        self.generate_recommended_x_currents(number_of_drivers)
        self.other_x_current_textinput.text = str(self.x_current)
        self.x_current = self.set_value_to_update_to(
            self.double_stack_x_current_label, self.double_stack_x_current_checkbox
        )

    def set_default_firmware_version(self):
        self.recommended_firmware_checkbox.state = "normal"
        self.alt_v3_firmware_checkbox.state = "normal"
        self.alt_v2_firmware_checkbox.state = "normal"
        try:
            self.get_fw_options_from_usb(self.usb_path)
            self.choose_recommended_firmware_from_available(self.m.s.hw_version)
            self.firmware_version = self.set_value_to_update_to(
                self.recommended_firmware_label, self.recommended_firmware_checkbox
            )
        except:
            self.hw_info_label.text = (
                self.hw_info_label.text
                + """
Problems getting available FW :("""
            )

    def on_focus(self, radio_button_group, instance, value):
        if value:
            radio_button_group[0].state = "down"
            try:
                radio_button_group[1].state = "normal"
                radio_button_group[2].state = "normal"
            except:
                pass

    def set_value_to_update_to(self, text_obj, radio_button):
        if radio_button != None:
            radio_button.state = "down"
            radio_button.active = True
        value_to_set = re.findall("[0-9.]+", text_obj.text)[0]
        return value_to_set

    def generate_no_drivers_based_on_hw_version(self, hw_version):
        """
        HW versions from 34 and up have a driver for each X motor (5 drivers in total)
        Hw versions 33 and under have a shared driver for both X motors (4 drivers in total)
        """
        if int(hw_version) > 33:
            return 5
        else:
            return 4

    def generate_hw_and_fw_info_label(self, hw, fw, no_drivers):
        self.hw_info_label.text = (
            "HW version: "
            + str(hw)
            + "\n"
            + "No. motor drivers: "
            + str(no_drivers)
            + "\n"
            + "FW version: "
            + str(fw)
        )

    def generate_recommended_x_currents(self, no_drivers):
        if no_drivers < 5:
            self.single_stack_x_current_label.text = (
                str(self.single_stack_single_driver_x_current) + " (single stack)"
            )
            self.double_stack_x_current_label.text = (
                str(self.double_stack_single_driver_x_current) + " (double_stack)"
            )
        else:
            self.single_stack_x_current_label.text = (
                str(self.single_stack_dual_driver_x_current) + " (single stack)"
            )
            self.double_stack_x_current_label.text = (
                str(self.double_stack_dual_driver_x_current) + " (double_stack)"
            )

    def choose_recommended_firmware_from_available(self, hw):
        if int(hw) > 33:
            self.recommended_firmware_label.text = self.ver_2_5_drivers_string
            self.alt_v3_firmware_label.text = self.ver_2_4_drivers_string
        elif int(hw) > 19:
            self.recommended_firmware_label.text = self.ver_2_4_drivers_string
            self.alt_v3_firmware_label.text = self.ver_2_5_drivers_string
        else:
            self.recommended_firmware_label.text = self.ver_1_string
            self.alt_v3_firmware_label.text = self.ver_2_4_drivers_string
        self.alt_v2_firmware_label.text = self.ver_1_string

    def get_fw_options_from_usb(self, usb_path):
        self.ver_2_5_drivers_filename = glob.glob(usb_path + "GRBL2_*_5.hex")[0]
        self.ver_2_4_drivers_filename = glob.glob(usb_path + "GRBL2_*_4.hex")[0]
        self.ver_1_filename = glob.glob(usb_path + "GRBL1_*.hex")[0]
        self.ver_2_5_drivers_string = self.generate_fw_string_from_path(
            self.ver_2_5_drivers_filename
        )
        self.ver_2_4_drivers_string = self.generate_fw_string_from_path(
            self.ver_2_4_drivers_filename
        )
        self.ver_1_string = self.generate_fw_string_from_path(self.ver_1_filename)

    def generate_fw_string_from_path(self, fw_path):
        just_numbers_and_underscores = re.findall("[0-9_]+", os.path.basename(fw_path))[
            0
        ]
        return ".".join(just_numbers_and_underscores.split("_"))

    def check_and_set_textinput_values(self):
        try:
            if (
                not self.x_thermal_coefficient_min
                <= int(self.thermal_coeff_x_textinput.text)
                <= self.x_thermal_coefficient_max
                or not self.y_thermal_coefficient_min
                <= int(self.thermal_coeff_y_textinput.text)
                <= self.y_thermal_coefficient_max
                or not self.z_thermal_coefficient_min
                <= int(self.thermal_coeff_z_textinput.text)
                <= self.z_thermal_coefficient_max
            ):
                return False
            self.x_thermal_coefficient = int(self.thermal_coeff_x_textinput.text)
            self.y_thermal_coefficient = int(self.thermal_coeff_y_textinput.text)
            self.z_thermal_coefficient = int(self.thermal_coeff_z_textinput.text)
            if self.other_x_current_checkbox.state == "down":
                if int(self.number_of_drivers) > 4:
                    x_min = self.x_current_dual_driver_min
                    x_max = self.x_current_dual_driver_max
                else:
                    x_min = self.x_current_single_driver_min
                    x_max = self.x_current_single_driver_max
                if not x_min <= int(self.other_x_current_textinput.text) <= x_max:
                    return False
                self.x_current = int(self.other_x_current_textinput.text)
            if self.other_z_current_checkbox.state == "down":
                if (
                    not self.z_current_min
                    <= int(self.other_z_current_textinput.text)
                    <= self.z_current_max
                ):
                    return False
                self.z_current = int(self.other_z_current_textinput.text)
            return True
        except:
            return False

    def print_settings_to_set(self):
        Logger.info("FW version " + str(self.firmware_version))
        Logger.info("X current: " + str(self.x_current))
        Logger.info("Y current: " + str(self.y_current))
        Logger.info("Z current: " + str(self.z_current))
        Logger.info("X thermal coefficient: " + str(self.x_thermal_coefficient))
        Logger.info("Y thermal coefficient: " + str(self.y_thermal_coefficient))
        Logger.info("Z thermal coefficient: " + str(self.z_thermal_coefficient))

    def toggle_connection_to_z_head(self):
        if self.connection_button.state == "normal":
            self.connection_button.text = "Reconnecting..."
            Clock.schedule_once(lambda dt: self.m.reconnect_serial_connection(), 0.2)
            self.poll_for_reconnection = Clock.schedule_interval(
                self.try_start_services, 1
            )
        else:
            self.connection_button.text = "Reconnect Z Head"
            self.m.s.grbl_scanner_running = False
            Clock.schedule_once(self.m.close_serial_connection, 0.2)

    def try_start_services(self, dt):
        if self.m.s.is_connected():
            Clock.unschedule(self.poll_for_reconnection)
            Clock.schedule_once(self.m.s.start_services, 1)
            self.connection_button.text = "Disconnect Z Head"
            self.sm.get_screen("qc1").reset_checkboxes()
            self.sm.get_screen("qc2").reset_checkboxes()
            self.sm.get_screen("qcW136").reset_checkboxes()
            self.sm.get_screen("qcW112").reset_checkboxes()
            self.sm.get_screen("qc3").reset_timer()
            self.sm.current = "qcconnecting"

    def do_pcb_update_and_set_settings(self):
        self.ok_button.text = "Updating firmware..."
        if not self.m.state().startswith("Idle"):
            self.ok_button.text = "Ensure Z Head connected and Idle!"
            return
        if not self.check_and_set_textinput_values():
            self.ok_button.text = "Check text inputs, something wrong"
            return
        self.print_settings_to_set()

        def disconnect_and_update():
            self.m.s.grbl_scanner_running = False
            Clock.schedule_once(self.m.close_serial_connection, 0.1)
            self.reset_screens()
            Clock.schedule_once(nested_do_fw_update, 1)

        def nested_do_fw_update(dt):
            if self.m.set_mode_of_reset_pin():
                cmd = (
                    "grbl_file="
                    + self.get_fw_path_from_string(self.firmware_version)
                    + " && avrdude -patmega2560 -cwiring -P/dev/ttyAMA0 -b115200 -D -Uflash:w:$(echo $grbl_file):i"
                )
                proc = subprocess.Popen(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True
                )
                self.stdout, stderr = proc.communicate()
                self.exit_code = int(proc.returncode)
            else:
                self.ok_button.text = "Check pigpiod and AMA0 port"
            connect()

        def connect():
            self.m.starting_serial_connection = True
            Clock.schedule_once(do_connection, 0.1)
            self.ok_button.text = "Reconnecting..."

        def do_connection(dt):
            self.m.reconnect_serial_connection()
            self.poll_for_reconnection = Clock.schedule_interval(
                try_start_services, 0.4
            )

        def try_start_services(dt):
            if self.m.s.is_connected():
                Clock.unschedule(self.poll_for_reconnection)
                Clock.schedule_once(self.m.s.start_services, 1)
                Clock.schedule_once(update_complete, 2)

        def update_complete(dt):
            try:
                if self.exit_code != 0:
                    self.sm.get_screen("qcpcbsetupoutcome").fw_update_success = False
                    self.ok_button.text = "Check pigpiod and AMA0 port"
                else:
                    set_settings_if_fw_version_high_enough()
            except:
                self.ok_button.text = "Check pigpiod and AMA0 port"

        def set_settings_if_fw_version_high_enough():
            if not self.m.s.fw_version:
                Clock.schedule_once(
                    lambda dt: set_settings_if_fw_version_high_enough(), 1
                )
                return
            if str(self.m.s.fw_version).startswith("2"):
                set_currents_and_coeffs()
            else:
                self.sm.get_screen("qcpcbsetupoutcome").x_current_correct = False
                self.sm.get_screen("qcpcbsetupoutcome").y_current_correct = False
                self.sm.get_screen("qcpcbsetupoutcome").z_current_correct = False
                self.sm.get_screen("qcpcbsetupoutcome").thermal_coefficients_correct = (
                    False
                )
                self.progress_to_next_screen()

        def set_currents_and_coeffs():
            if not self.m.TMC_registers_have_been_read_in():
                Clock.schedule_once(lambda dt: set_currents_and_coeffs(), 1)
                return
            self.ok_button.text = "Setting currents and coefficients..."
            if (
                self.m.set_thermal_coefficients("X", int(self.x_thermal_coefficient))
                and self.m.set_thermal_coefficients(
                    "Y", int(self.y_thermal_coefficient)
                )
                and self.m.set_thermal_coefficients(
                    "Z", int(self.z_thermal_coefficient)
                )
                and self.m.set_motor_current("Z", int(self.z_current))
                and self.m.set_motor_current("Y", int(self.y_current))
                and self.m.set_motor_current("X", int(self.x_current))
            ):
                Clock.schedule_once(lambda dt: store_params_and_progress(), 1.2)
            else:
                Logger.warning("Z Head not Idle yet, waiting...")
                Clock.schedule_once(lambda dt: set_currents_and_coeffs(), 0.5)

        def store_params_and_progress():
            self.ok_button.text = "Storing parameters..."
            Logger.info("Storing TMC params...")
            self.m.store_tmc_params_in_eeprom_and_handshake()
            check_registers_are_correct()

        def check_registers_are_correct():
            if not self.m.TMC_registers_have_been_read_in():
                Clock.schedule_once(lambda dt: check_registers_are_correct(), 0.5)
                return
            self.ok_button.text = "Checking registers..."
            outcome_screen = self.sm.get_screen("qcpcbsetupoutcome")
            outcome_screen.x_current_correct *= self.check_current(
                TMC_X1, self.x_current
            )
            outcome_screen.x_current_correct *= self.check_current(
                TMC_X2, self.x_current
            )
            outcome_screen.y_current_correct *= self.check_current(
                TMC_Y1, self.y_current
            )
            outcome_screen.y_current_correct *= self.check_current(
                TMC_Y2, self.y_current
            )
            outcome_screen.z_current_correct *= self.check_current(
                TMC_Z, self.z_current
            )
            outcome_screen.thermal_coefficients_correct *= self.check_temp_coeff(
                TMC_X1, self.x_thermal_coefficient
            )
            outcome_screen.thermal_coefficients_correct *= self.check_temp_coeff(
                TMC_X2, self.x_thermal_coefficient
            )
            outcome_screen.thermal_coefficients_correct *= self.check_temp_coeff(
                TMC_Y1, self.y_thermal_coefficient
            )
            outcome_screen.thermal_coefficients_correct *= self.check_temp_coeff(
                TMC_Y2, self.y_thermal_coefficient
            )
            outcome_screen.thermal_coefficients_correct *= self.check_temp_coeff(
                TMC_Z, self.z_thermal_coefficient
            )
            self.progress_to_next_screen()

        disconnect_and_update()

    def check_current(self, motor, expected_current):
        if int(self.m.TMC_motor[motor].ActiveCurrentScale) != int(expected_current):
            return False
        if int(self.m.TMC_motor[motor].standStillCurrentScale) != int(expected_current):
            return False
        return True

    def check_temp_coeff(self, motor, expected_coeff):
        if int(self.m.TMC_motor[motor].temperatureCoefficient) != int(expected_coeff):
            return False
        return True

    def get_fw_path_from_string(self, fw_string):
        return self.usb_path + "GRBL" + "_".join(fw_string.split(".")) + ".hex"

    def reset_screens(self):
        self.sm.get_screen("qc1").reset_checkboxes()
        self.sm.get_screen("qc2").reset_checkboxes()
        self.sm.get_screen("qcW136").reset_checkboxes()
        self.sm.get_screen("qcW112").reset_checkboxes()
        self.sm.get_screen("qc3").reset_timer()

    def progress_to_next_screen(self):
        self.ok_button.text = "OK"
        self.sm.current = "qcpcbsetupoutcome"
