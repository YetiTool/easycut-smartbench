import re
from functools import partial
import glob
import os, subprocess

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock
from asmcnc.comms.yeti_grbl_protocol.c_defines import *
from datetime import datetime

from asmcnc.skavaUI import widget_status_bar

Builder.load_string("""
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
                                on_press: root.set_value_to_update_to(recommended_firmware_label, root.firmware_version, self)
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
                                on_press: root.set_value_to_update_to(alt_v3_firmware_label, root.firmware_version, self)
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
                                on_press: root.set_value_to_update_to(alt_v2_firmware_label, root.firmware_version, self)
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
                id: ok_button
                text: 'OK'
                font_size: dp(30)
                size_hint_y: 0.2
                on_press: root.do_pcb_update_and_set_settings()

        BoxLayout:
            size_hint_y: 0.08
            id: status_container 
            pos: self.pos
""")

def log(message):
    timestamp = datetime.now()
    print ('Z Head Connecting Screen: ' + timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))

class ZHeadPCBSetUp(Screen):

    usb_path = "/media/usb/"

    single_stack_single_driver_x_current = 26
    double_stack_single_driver_x_current = 26
    single_stack_dual_driver_x_current = 13
    double_stack_dual_driver_x_current = 20

    default_z_current = 25

    default_x_thermal_coefficient = 5000
    default_y_thermal_coefficient = 5000
    default_z_thermal_coefficient = 10000

    firmware_version = "2.5.5"
    number_of_drivers = 4

    x_current = str(double_stack_dual_driver_x_current)
    z_current = str(default_z_current)

    x_thermal_coefficient = str(default_x_thermal_coefficient)
    y_thermal_coefficient = str(default_y_thermal_coefficient)
    z_thermal_coefficient = str(default_z_thermal_coefficient)

    poll_for_reconnection = None

    def __init__(self, **kwargs):

        super(ZHeadPCBSetUp, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']

        # Green status bar
        self.status_bar_widget = widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm)
        self.status_container.add_widget(self.status_bar_widget)

        # Ensure that textinputs are auto-validated when user presses away from keyboard
        self.other_x_current_textinput.bind(focus=partial(self.on_focus, self.x_current, self.other_x_current_checkbox))
        self.other_z_current_textinput.bind(focus=partial(self.on_focus, self.z_current, self.other_z_current_checkbox))

        self.thermal_coeff_x_textinput.bind(focus=partial(self.on_focus, self.x_thermal_coefficient, None))
        self.thermal_coeff_y_textinput.bind(focus=partial(self.on_focus, self.y_thermal_coefficient, None))
        self.thermal_coeff_z_textinput.bind(focus=partial(self.on_focus, self.z_thermal_coefficient, None))

    def on_pre_enter(self):

        self.z_current = str(self.default_z_current)
    
        self.x_thermal_coefficient = str(self.default_x_thermal_coefficient)
        self.y_thermal_coefficient = str(self.default_y_thermal_coefficient)
        self.z_thermal_coefficient = str(self.default_z_thermal_coefficient)
    
        try:
            number_of_drivers = self.generate_no_drivers_based_on_hw_version(self.m.s.hw_version)
            self.generate_hw_and_fw_info_label(self.m.s.hw_version, self.m.s.fw_version, number_of_drivers)
            self.generate_recommended_x_currents(number_of_drivers)

        except: self.hw_info_label.text = "Can't read HW version :("
        else: 

            try:
                self.get_fw_options(self.usb_path)
                self.choose_recommended_firmware_from_available(hw)

            except: self.hw_info_label.text = self.hw_info_label.text.append("\nProblems getting available FW :(")
            else: self.set_and_select_defaults()

    def go_to_qc_home(self):
        self.sm.current = "qchome"

    # BUTTON HANDLING

    def on_focus(self, value_to_set, radio_button, instance, value):
        if not value:
            self.set_value_to_update_to(instance, value_to_set, radio_button)

    def set_value_to_update_to(self, text_obj, value_to_set, radio_button = None):
        if radio_button != None: radio_button.state ='down'
        value_to_set = re.findall('[0-9.]+', text_obj.text)[0]
        print(value_to_set)

    def set_and_select_defaults(self):
        self.set_value_to_update_to(self.recommended_firmware_label, self.firmware_version, self.recommended_firmware_checkbox)
        self.set_value_to_update_to(self.recommended_z_current_label, self.z_current, self.recommended_z_current_checkbox)
        self.set_value_to_update_to(self.single_stack_x_current_label, self.x_current, self.single_stack_x_current_checkbox)

    # VERSION HANDLING

    def generate_no_drivers_based_on_hw_version(self, hw_version):
        """
        HW versions from 34 and up have a driver for each X motor (5 drivers in total)
        Hw versions 33 and under have a shared driver for both X motors (4 drivers in total)
        """
        if int(hw_version) > 33: return 5
        else: return 4

    def generate_hw_and_fw_info_label(self, hw, fw, no_drivers):
        self.hw_info_label.text =   "HW version: " + str(hw) + "\n" + \
                                    "No. motor drivers: " + str(no_drivers) + "\n" + \
                                    "FW version: " + str(fw)

    def generate_recommended_x_currents(self, no_drivers):
        if no_drivers < 5: 
            self.single_stack_x_current_label.text = str(self.single_stack_single_driver_x_current)
            self.double_stack_x_current_label.text = str(self.double_stack_single_driver_x_current)

        else: 
            self.single_stack_x_current_label.text = str(self.single_stack_dual_driver_x_current)
            self.double_stack_x_current_label.text = str(self.double_stack_dual_driver_x_current)

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

    def get_fw_options(self, usb_path):

        self.ver_2_5_drivers_filename = glob.glob(usb_path + "GRBL2_*_5.hex")[0]
        self.ver_2_4_drivers_filename = glob.glob(usb_path + "GRBL2_*_4.hex")[0]
        self.ver_1_filename = glob.glob(usb_path + "GRBL1_*.hex")[0]

        self.ver_2_5_drivers_string = self.generate_fw_string_from_path(self.ver_2_5_drivers_filename)
        self.ver_2_4_drivers_string = self.generate_fw_string_from_path(self.ver_2_4_drivers_filename)
        self.ver_1_string = self.generate_fw_string_from_path(self.ver_1_filename)

    def generate_fw_string_from_path(self, fw_path):
        just_numbers_and_underscores = re.findall('[0-9_]+', os.path.basename(fw_path))[0]
        return (".".join(just_numbers_and_underscores.split("_")))


    ## Z HEAD DISCONNECT/RECONNECT

    def toggle_connection_to_z_head(self):

        if self.connection_button.state == 'normal': 
            self.connection_button.text = "Reconnecting..."
            Clock.schedule_once(lambda dt: self.m.reconnect_serial_connection(), 0.2)
            self.poll_for_reconnection = Clock.schedule_interval(self.try_start_services, 1)

        else: 
            self.connection_button.text = "Reconnect Z Head"
            self.m.s.grbl_scanner_running = False
            Clock.schedule_once(self.m.close_serial_connection, 0.2)

    def try_start_services(self, dt):
        if self.m.s.is_connected():
            Clock.unschedule(self.poll_for_reconnection)
            Clock.schedule_once(self.m.s.start_services, 1)
            self.connection_button.text = "Disconnect Z Head"
            self.sm.get_screen('qc1').reset_checkboxes()
            self.sm.get_screen('qc2').reset_checkboxes()
            self.sm.get_screen('qcW136').reset_checkboxes()
            self.sm.get_screen('qcW112').reset_checkboxes()
            self.sm.get_screen('qc3').reset_timer()
            self.sm.current = 'qcconnecting'


    ## DOING PCB FW UPDATE AND SETTINGS

    def do_pcb_update_and_set_settings(self):

        self.ok_button.text = "Updating firmware..."

        # DO FW UPDATE
        def disconnect_and_update():
            self.m.s.grbl_scanner_running = False
            Clock.schedule_once(self.m.close_serial_connection, 0.1)
            Clock.schedule_once(nested_do_fw_update, 1)

        def nested_do_fw_update(dt):
            if self.m.set_mode_of_reset_pin():

                cmd =   "grbl_file=" + self.get_fw_path_from_string(self.firmware_version) + \
                        " && avrdude -patmega2560 -cwiring -P/dev/ttyAMA0 -b115200 -D -Uflash:w:$(echo $grbl_file):i"
                proc = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = True)
                self.stdout, stderr = proc.communicate()
                self.exit_code = int(proc.returncode)

                connect()

        # RECONNECT
        def connect():
            self.m.starting_serial_connection = True
            Clock.schedule_once(do_connection, 0.1)
            self.OK_button.text = "Reconnecting..."

        def do_connection(dt):
            self.m.reconnect_serial_connection()
            self.poll_for_reconnection = Clock.schedule_interval(try_start_services, 0.4)

        def try_start_services(dt):
            if self.m.s.is_connected() and self.m.s.fw_version:
                Clock.unschedule(self.poll_for_reconnection)
                Clock.schedule_once(self.m.s.start_services, 1)
                # 1 second should always be enough to start services
                Clock.schedule_once(update_complete, 2)

        # CONFIRM THAT IT WAS SUCCESSFUL
        def update_complete(dt):
            if self.exit_code == 0: self.sm.get_screen("qcpcbsetupoutcome").fw_update_success = True
            else: self.sm.get_screen("qcpcbsetupoutcome").fw_update_success = False
            self.reset_screens()
            self.does_firmware_version_match()


        # CHECK FW VERSION MATCHES
        def does_firmware_version_match(self):
            fw_components = self.firmware_version.rsplit('.', 1)
            version = re.findall(fw_components[0] + ".\d." + fw_components[1] + ".\d", self.m.s.fw_version)
            if version: self.sm.get_screen("qcpcbsetupoutcome").fw_version_correct = True
            else: self.sm.get_screen("qcpcbsetupoutcome").fw_version_correct = False

            if version.startswith("2"):
                self.set_currents_and_coeffs()


        def set_currents_and_coeffs(self):

            if not self.m.TMC_registers_have_been_read_in():
                Clock.schedule_once(lambda dt: self.set_currents_and_coeffs(), 1)
                return

            self.OK_button.text = "Setting currents and coefficients..."

            # SET CURRENTS AND THERMAL COEFFICIENTS
            if  self.m.set_thermal_coefficients("X", x_thermal_coefficient) and \
                self.m.set_thermal_coefficients("Y", y_thermal_coefficient) and \
                self.m.set_thermal_coefficients("Z", z_thermal_coefficient) and \
                self.m.set_motor_current("Z", self.z_current) and \
                self.m.set_motor_current("X", self.x_current):

                # STORE PARAMETERS
                Clock.schedule_once(lambda dt: self.store_params_and_progress(), 1)

            else:
                log("Z Head not Idle yet, waiting...")
                Clock.schedule_once(lambda dt: self.set_currents_and_coeffs(), 0.5)


        def store_params_and_progress(self):
            log("Storing TMC params...")
            self.m.store_tmc_params_in_eeprom_and_handshake()
            self.check_registers_are_correct()


        def check_registers_are_correct(self):

            if not self.m.TMC_registers_have_been_read_in():
                Clock.schedule_once(lambda dt: self.check_registers_are_correct(), 0.5)
                return

            # CHECK REGISTERS
            if int(self.m.TMC_motor[TMC_X1].ActiveCurrentScale) != int(self.x_current): self.sm.get_screen("qcpcbsetupoutcome").x_current_correct = False
            if int(self.m.TMC_motor[TMC_X2].ActiveCurrentScale) != int(self.x_current): self.sm.get_screen("qcpcbsetupoutcome").x_current_correct = False
            if int(self.m.TMC_motor[TMC_X1].standStillCurrentScale) != int(self.x_current): self.sm.get_screen("qcpcbsetupoutcome").x_current_correct = False
            if int(self.m.TMC_motor[TMC_X2].standStillCurrentScale) != int(self.x_current): self.sm.get_screen("qcpcbsetupoutcome").x_current_correct = False

            if int(self.m.TMC_motor[TMC_Z].ActiveCurrentScale) != int(self.z_current): self.sm.get_screen("qcpcbsetupoutcome").z_current_correct = False
            if int(self.m.TMC_motor[TMC_Z].standStillCurrentScale) != int(self.z_current): self.sm.get_screen("qcpcbsetupoutcome").z_current_correct = False

            if int(self.m.TMC_motor[TMC_X1].temperatureCoefficient) != int(self.x_thermal_coefficient): self.sm.get_screen("qcpcbsetupoutcome").thermal_coefficients_correct = False
            if int(self.m.TMC_motor[TMC_X2].temperatureCoefficient) != int(self.x_thermal_coefficient): self.sm.get_screen("qcpcbsetupoutcome").thermal_coefficients_correct = False
            if int(self.m.TMC_motor[TMC_Y1].temperatureCoefficient) != int(self.y_thermal_coefficient): self.sm.get_screen("qcpcbsetupoutcome").thermal_coefficients_correct = False
            if int(self.m.TMC_motor[TMC_Y2].temperatureCoefficient) != int(self.y_thermal_coefficient): self.sm.get_screen("qcpcbsetupoutcome").thermal_coefficients_correct = False
            if int(self.m.TMC_motor[TMC_Z].temperatureCoefficient) != int(self.z_thermal_coefficient): self.sm.get_screen("qcpcbsetupoutcome").thermal_coefficients_correct = False

            self.progress_to_next_screen()

        disconnect_and_update()

    def get_fw_path_from_string(self, fw_string):
        return self.usb_path + "GRBL" + "_".join(fw_string.split(".")) + ".hex"

    def reset_screens(self):
        self.sm.get_screen('qc1').reset_checkboxes()
        self.sm.get_screen('qc2').reset_checkboxes()
        self.sm.get_screen('qcW136').reset_checkboxes()
        self.sm.get_screen('qcW112').reset_checkboxes()
        self.sm.get_screen('qc3').reset_timer()


    def progress_to_next_screen(self):
        # TAKE USER TO OUTCOME SCREEN 
        self.sm.current = "qcpcbsetupoutcome"














