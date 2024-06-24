"""
Created on 18 November 2020
Menu screen for system tools app

@author: Letty
"""
import os
import sys

from asmcnc.comms.logging_system.logging_system import Logger
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.spinner import Spinner
from asmcnc.skavaUI import popup_info
from asmcnc.apps.systemTools_app.screens import popup_factory_settings
from asmcnc.apps.systemTools_app.screens import popup_system
from asmcnc.apps.systemTools_app.screens.calibration.screen_calibration_test import (
    CalibrationTesting,
)
from asmcnc.apps.systemTools_app.screens.calibration.screen_overnight_test import (
    OvernightTesting,
)
from asmcnc.apps.systemTools_app.screens.calibration.screen_current_adjustment import (
    CurrentAdjustment,
)
from asmcnc.apps.systemTools_app.screens.calibration.screen_serial_numbers import (
    UploadSerialNumbersScreen,
)
from asmcnc.apps.systemTools_app.screens.calibration import screen_stall_jig
from asmcnc.apps.systemTools_app.screens.calibration import screen_set_thresholds
from asmcnc.apps.systemTools_app.screens.calibration import screen_general_measurement
from asmcnc.production.database.calibration_database import CalibrationDatabase

from asmcnc.comms.model_manager import ModelManagerSingleton, ProductCodes

from asmcnc.core_UI import console_utils

Builder.load_string(
    """

<FactorySettingsScreen>

    software_version_label: software_version_label
    platform_version_label: platform_version_label
    setting_54_label:setting_54_label
    latest_software_version: latest_software_version
    latest_platform_version: latest_platform_version
    z_touch_plate_entry: z_touch_plate_entry
    serial_prefix: serial_prefix
    serial_number_input: serial_number_input
    product_number_input: product_number_input
    machine_serial: machine_serial
    machine_touchplate_thickness: machine_touchplate_thickness
    maintenance_reminder_toggle: maintenance_reminder_toggle
    show_spindle_overload_toggle: show_spindle_overload_toggle
    setting_54_toggle:setting_54_toggle
    smartbench_model: smartbench_model
    console_update_button: console_update_button
    sc2_compatability_toggle:sc2_compatability_toggle

    on_touch_down: root.on_touch()

    BoxLayout:
        height: dp(1.66666666667*app.height)
        width: dp(0.6*app.width)
        canvas.before:
            Color: 
                rgba: hex('#f9f9f9ff')
            Rectangle: 
                size: self.size
                pos: self.pos

        BoxLayout:
            padding: 0
            spacing:0.0208333333333*app.height
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
                    height: dp(0.125*app.height)
                    width: dp(1.0*app.width)
                    text: "Factory settings"
                    color: hex('#f9f9f9ff')
                    font_size: 0.0375*app.width
                    halign: "center"
                    valign: "bottom"
                    markup: True
                   
            BoxLayout:
                size_hint: (None,None)
                width: dp(1.0*app.width)
                height: dp(0.666666666667*app.height)
                orientation: 'horizontal'
                BoxLayout:
                    size_hint: (None,None)
                    width: dp(0.721875*app.width)
                    height: dp(0.666666666667*app.height)
                    padding: 0
                    spacing:0.0208333333333*app.height
                    orientation: 'vertical'
                    BoxLayout:
                        size_hint: (None,None)
                        width: dp(0.721875*app.width)
                        height: dp(0.479166666667*app.height)
                        padding: 0
                        spacing: 0
                        orientation: 'vertical'

                        GridLayout: 
                            size: self.parent.size
                            pos: self.parent.pos
                            cols: 0
                            rows: 4
                            padding:[dp(0.0125)*app.width, dp(0.0208333333333)*app.height]
                            spacing:0.0104166666667*app.height
                            BoxLayout: 
                                orientation: 'vertical'
                                spacing:0.0104166666667*app.height
                                
                                BoxLayout:
                                    orientation: 'horizontal'
                                    spacing:0.00625*app.width
                                    
                                    Spinner:
                                        font_size: str(0.01875 * app.width) + 'sp'
                                        id: smartbench_model
                                        text: 'Choose model'
                                        values: root.latest_machine_model_values
                                        on_text: root.set_smartbench_model()
                                    
                                    ToggleButton:
                                        font_size: str(0.01875 * app.width) + 'sp'
                                        id: smartbench_model_button
                                        text: 'Show all models'
                                        on_press: root.show_all_smartbench_models()
                                        size_hint: 0.5, 1
                                    
                            BoxLayout: 
                                orientation: 'vertical'
                                spacing:0.0104166666667*app.height


                                GridLayout: 
                                    size: self.parent.size
                                    pos: self.parent.pos
                                    cols: 4
                                    rows: 0
                                    padding:[dp(0.00625)*app.width, dp(0.0104166666667)*app.height]
                                    spacing:0.0125*app.width
                                    Label:
                                        font_size: str(0.01875 * app.width) + 'sp'
                                        text: '[b]Serial number[/b]'
                                        color: [0,0,0,1]
                                        markup: True
                                    BoxLayout: 
                                        orientation: 'horizontal'

                                        TextInput:
                                            id: serial_prefix
                                            font_size: str(15.0/800.0 * app.width) + 'sp'
                                            text: 'YS6'
                                            color: [0,0,0,1]
                                            markup: True
                                            valign: 'middle'
                                            size_hint_x: 0.3
                                            multiline: False
                                        Label:
                                            font_size: str(0.01875 * app.width) + 'sp'
                                            text: ''
                                            color: [0,0,0,1]
                                            markup: True
                                            size_hint_x: 0.05

                                        TextInput:
                                            id: serial_number_input
                                            font_size: str(15.0/800.0 * app.width) + 'sp'
                                            text: '0000'
                                            color: [0,0,0,1]
                                            markup: True
                                            valign: 'middle'
                                            size_hint_x: 0.35
                                            input_filter: 'int'
                                            multiline: False

                                        Label:
                                            font_size: str(0.01875 * app.width) + 'sp'
                                            text: '.'
                                            color: [0,0,0,1]
                                            markup: True
                                            size_hint_x: 0.05

                                        TextInput:
                                            id: product_number_input
                                            font_size: str(15.0/800.0 * app.width) + 'sp'
                                            text: '00'
                                            color: [0,0,0,1]
                                            markup: True
                                            valign: 'middle'
                                            size_hint_x: 0.25
                                            input_filter: 'int'
                                            multiline: False

                                    Button:
                                        font_size: str(0.01875 * app.width) + 'sp'
                                        text: 'UPDATE'
                                        on_press: root.update_serial_number()

                                    Label:
                                        font_size: str(0.01875 * app.width) + 'sp'
                                        id: machine_serial
                                        text: 'machine serial'
                                        color: [0,0,0,1]
                                        markup: True

                            BoxLayout: 
                                orientation: 'vertical'
                                spacing:0.0104166666667*app.height

                                GridLayout: 
                                    size: self.parent.size
                                    pos: self.parent.pos
                                    cols: 4
                                    rows: 0
                                    padding:[dp(0.00625)*app.width, dp(0.0104166666667)*app.height]
                                    spacing:0.0125*app.width

                                    Label:
                                        font_size: str(0.01875 * app.width) + 'sp'
                                        text: '[b]Touchplate offset[/b]'
                                        color: [0,0,0,1]
                                        markup: True
                                    TextInput:
                                        id: z_touch_plate_entry
                                        font_size: str(15.0/800.0 * app.width) + 'sp'
                                        text: ''
                                        color: [0,0,0,1]
                                        markup: True
                                        valign: 'middle'
                                        input_filter: 'float'
                                        multiline: False
                                    Button:
                                        font_size: str(0.01875 * app.width) + 'sp'
                                        text: 'UPDATE'
                                        on_press: root.update_z_touch_plate_thickness()
    
                                    Label:
                                        font_size: str(0.01875 * app.width) + 'sp'
                                        id: machine_touchplate_thickness
                                        text: 'machine_tp'
                                        color: [0,0,0,1]
                                        markup: True

                        BoxLayout:
                            size_hint_y: 0.3
                            orientation: 'horizontal'
                            spacing:dp(0.0125)*app.width

                            Button:
                                font_size: str(0.01875 * app.width) + 'sp'
                                text: '$54 info'
                                on_press: root.setting_54_info()

                            ToggleButton:
                                font_size: str(0.01875 * app.width) + 'sp'
                                id: setting_54_toggle
                                text: 'Set $54=1'
                                on_press: root.toggle_setting_54()

                            Label:
                                font_size: str(0.01875 * app.width) + 'sp'
                                id: setting_54_label
                                size_hint_x: 0.7
                                text: '$54 = N/A'
                                color: [0,0,0,1]


                    BoxLayout:
                        size_hint: (None,None)
                        width: dp(0.721875*app.width)
                        height: dp(0.166666666667*app.height)
                        padding:[dp(0.00625)*app.width, dp(0.0104166666667)*app.height]
                        spacing: 0
                        orientation: 'vertical'

                        GridLayout: 
                            size: self.parent.size
                            pos: self.parent.pos
                            cols: 3
                            rows: 0
                            padding: 0
                            spacing:0.0125*app.width

                            Button:
                                font_size: str(0.01875 * app.width) + 'sp'
                                id: console_update_button
                                text: 'Full Console Update (wifi)'
                                on_press: root.full_console_update()

                            GridLayout: 
                                size: self.parent.size
                                pos: self.parent.pos
                                cols: 0
                                rows: 3
                                padding: 0
                                spacing:0.0025*app.width
                                Label:
                                    font_size: str(0.01875 * app.width) + 'sp'
                                    text: 'Current'
                                    color: [0,0,0,1]
                                    markup: True
                                Label:
                                    font_size: str(0.01875 * app.width) + 'sp'
                                    id: software_version_label
                                    text: 'SW'
                                    color: [0,0,0,1]
                                    markup: True
                                Label:
                                    font_size: str(0.01875 * app.width) + 'sp'
                                    id: platform_version_label
                                    text: 'PL'
                                    color: [0,0,0,1]
                                    markup: True
                            GridLayout: 
                                size: self.parent.size
                                pos: self.parent.pos
                                cols: 0
                                rows: 3
                                padding: 0
                                spacing:0.0025*app.width
                                Label:
                                    font_size: str(0.01875 * app.width) + 'sp'
                                    text: 'Available'
                                    color: [0,0,0,1]
                                    markup: True
                                Label:
                                    font_size: str(0.01875 * app.width) + 'sp'
                                    id: latest_software_version
                                    text: 'SW'
                                    color: [0,0,0,1]
                                    markup: True
                                Label:
                                    font_size: str(0.01875 * app.width) + 'sp'
                                    id: latest_platform_version
                                    text: 'PL'
                                    color: [0,0,0,1]
                                    markup: True

                GridLayout:
                    cols: 2
                    rows: 8
                    spacing:0.0025*app.width
                    ToggleButton:
                        font_size: str(0.01875 * app.width) + 'sp'
                        id: maintenance_reminder_toggle
                        text: 'Turn reminders off'
                        on_press: root.toggle_reminders()
                        text_size: self.size
                        halign: "center"
                        valign: "middle"

                    ToggleButton:
                        font_size: str(0.01875 * app.width) + 'sp'
                        id: show_spindle_overload_toggle
                        text: 'Show spindle overload'
                        on_press: root.toggle_spindle_mode()
                        text_size: self.size
                        halign: "center"
                        valign: "middle"

                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        text: 'Diagnostics'
                        on_press: root.diagnostics()
                        text_size: self.size
                        halign: "center"
                        valign: "middle"

                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        text: 'Current'
                        on_press: root.enter_current_adjustment()
                        text_size: self.size
                        halign: "center"
                        valign: "middle"

                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        text: 'FT B1'
                        background_normal: ''
                        background_color: [0.75,0.34,0.51,1]
                        on_press: root.final_test("pink")
                        text_size: self.size
                        halign: "center"
                        valign: "middle"

                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        text: 'FT B2'
                        background_normal: ''
                        background_color: [0.28,0.44,0.97,1]
                        on_press: root.final_test("blue")
                        text_size: self.size
                        halign: "center"
                        valign: "middle"

                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        text: 'FT B3'
                        background_normal: ''
                        background_color: [0.2,0.8,0.2,1]
                        on_press: root.final_test("green")
                        text_size: self.size
                        halign: "center"
                        valign: "middle"

                    ToggleButton:
                        font_size: str(0.01875 * app.width) + 'sp'
                        id: sc2_compatability_toggle
                        text: 'Enable SC2 compatability'
                        on_press: root.show_sc2_decision_popup()
                        text_size: self.size
                        halign: "center"
                        valign: "middle"

                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        text: 'Retrieve LB cal data'
                        on_press: root.enter_serial_number_screen()
                        text_size: self.size
                        halign: "center"
                        valign: "middle"

                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        text: 'SG & Load test'
                        on_press: root.enter_calibration_test()
                        text_size: self.size
                        halign: "center"
                        valign: "middle"

                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        text: 'Overnight test'
                        on_press: root.enter_overnight_test()
                        text_size: self.size
                        halign: "center"
                        valign: "middle"

                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        text: 'Stall Jig'
                        on_press: root.enter_stall_jig()
                        text_size: self.size
                        halign: "center"
                        valign: "middle"

                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        text: 'SG thresh'
                        on_press: root.enter_set_thresholds()
                        text_size: self.size
                        halign: "center"
                        valign: "middle"

                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        text: 'Measure'
                        on_press: root.enter_general_measurement()
                        text_size: self.size
                        halign: "center"
                        valign: "middle"
                        
                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        text: 'SC2 spindle test'
                        on_press: root.digital_spindle_test_pressed()
                        text_size: self.size
                        halign: "center"
                        valign: "middle"
                            

            BoxLayout:
                size_hint: (None,None)
                width: dp(1.0*app.width)
                height: dp(0.166666666667*app.height)
                padding: 0
                spacing:0.0125*app.width
                orientation: 'horizontal'

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(0.1*app.width)
                    height: dp(0.166666666667*app.height)
                    padding: 0
                    spacing: 0

                    BoxLayout: 
                        size_hint: (None, None)
                        height: dp(0.166666666667*app.height)
                        width: dp(0.1*app.width)
                        padding:[dp(0.0125)*app.width, dp(0.0208333333333)*app.height, dp(0.0125)*app.width, dp(0.0208333333333)*app.height]
                        Button:
                            font_size: str(0.01875 * app.width) + 'sp'
                            size_hint: (None,None)
                            height: dp(0.108333333333*app.height)
                            width: dp(0.075*app.width)
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
                    width: dp(0.775*app.width)
                    height: dp(0.166666666667*app.height)
                    padding:[dp(0.2)*app.width, 0]
                    spacing: 0
                    orientation: 'vertical'
                    BoxLayout:
                        Button:
                            font_size: str(0.01875 * app.width) + 'sp'
                            text: 'FACTORY RESET'
                            on_press: root.factory_reset()

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(0.1*app.width)
                    height: dp(0.166666666667*app.height)
                    padding: 0
                    spacing: 0

                    BoxLayout: 
                        size_hint: (None, None)
                        height: dp(0.166666666667*app.height)
                        width: dp(0.1*app.width)
                        padding:[dp(0.02375)*app.width, dp(0.0208333333333)*app.height, dp(0.0125)*app.width, dp(0.0208333333333)*app.height]
                        Button:
                            font_size: str(0.01875 * app.width) + 'sp'
                            size_hint: (None,None)
                            height: dp(0.125*app.height)
                            width: dp(0.06375*app.width)
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


"""
)


class FactorySettingsScreen(Screen):
    latest_machine_model_values = [
        "SmartBench V1.3 PrecisionPro CNC Router",
        "SmartBench V1.3 PrecisionPro",
        "SmartBench V1.3 PrecisionPro Plus",
        "SmartBench V1.3 PrecisionPro X",
        "DRYWALLTEC SmartCNC",
    ]
    old_machine_model_values = [
        "SmartBench V1.0 CNC Router",
        "SmartBench V1.1 CNC Router",
        "SmartBench V1.2 Standard CNC Router",
        "SmartBench V1.2 Precision CNC Router",
        "SmartBench V1.2 PrecisionPro CNC Router",
    ]
    smartbench_model_path = "/home/pi/smartbench_model_name.txt"
    machine_serial_number_filepath = "/home/pi/smartbench_serial_number.txt"
    dev_mode = False
    poll_for_creds_file = None

    def __init__(self, **kwargs):
        super(FactorySettingsScreen, self).__init__(**kwargs)
        self.systemtools_sm = kwargs["system_tools"]
        self.m = kwargs["machine"]
        self.set = kwargs["settings"]
        self.l = kwargs["localization"]
        self.kb = kwargs["keyboard"]
        self.usb_stick = kwargs["usb_stick"]
        self.model_manager = ModelManagerSingleton()
        self.software_version_label.text = self.set.sw_version
        self.platform_version_label.text = self.set.platform_version
        self.latest_software_version.text = self.set.latest_sw_version
        self.latest_platform_version.text = self.set.latest_platform_version
        self.machine_serial.text = "$50 = " + str(self.m.serial_number())
        self.machine_touchplate_thickness.text = str(self.m.z_touch_plate_thickness)
        self.calibration_db = CalibrationDatabase()
        try:
            serial_number_string = self.get_serial_number()
            self.serial_prefix.text = serial_number_string[0:3]
            self.serial_number_input.text = serial_number_string[3:7]
            self.product_number_input.text = str(self.m.serial_number()).split(".")[1]
            if self.serial_prefix.text == "":
                self.serial_prefix.text = "YS6"
            if self.serial_number_input.text == "":
                self.serial_number_input.text = "0000"
            if self.product_number_input.text == "":
                self.product_number_input.text = "00"
        except:
            self.serial_prefix.text = "YS6"
            self.serial_number_input.text = "0000"
            self.product_number_input.text = "00"
        self.usb_stick.usb_notifications = False
        self.usb_stick.enable()
        self.poll_for_creds_file = Clock.schedule_interval(
            self.connect_to_db_when_creds_loaded, 1
        )
        if self.m.theateam():
            self.sc2_compatability_toggle.state = "down"
            self.sc2_compatability_toggle.text = "Disable SC2 compatability"
        self.text_inputs = [
            self.z_touch_plate_entry,
            self.serial_prefix,
            self.serial_number_input,
            self.product_number_input,
        ]

    def connect_to_db_when_creds_loaded(self, dt):
        try:
            if "credentials.py" in os.listdir("/media/usb/"):
                if self.poll_for_creds_file != None:
                    Clock.unschedule(self.poll_for_creds_file)
                os.system(
                    "cp /media/usb/credentials.py ./asmcnc/production/database/credentials.py"
                )
                Logger.info("Credentials file found on USB")
                self.calibration_db.set_up_connection()
        except:
            Logger.exception("No /media/usb/ folder found")

    def go_back(self):
        self.systemtools_sm.back_to_menu()
        self.stop_usb_doing_stuff()

    def exit_app(self):
        self.systemtools_sm.exit_app()
        self.stop_usb_doing_stuff()

    def stop_usb_doing_stuff(self):
        self.usb_stick.usb_notifications = True
        self.usb_stick.disable()
        if self.poll_for_creds_file != None:
            Clock.unschedule(self.poll_for_creds_file)

    def on_enter(self):
        self.usb_stick.usb_notifications = False
        self.z_touch_plate_entry.text = str(self.m.z_touch_plate_thickness)
        self.set_toggle_buttons()
        self.get_smartbench_model()
        self.kb.setup_text_inputs(self.text_inputs)
        csv_path = "./asmcnc/production/database/csvs"
        if not os.path.exists(csv_path):
            os.mkdir(csv_path)
        if self.m.is_machines_fw_version_equal_to_or_greater_than_version(
            "2.5.0", "Get $54 state"
        ):
            if self.m.s.setting_54:
                self.setting_54_label.text = "$54 = 1"
                self.setting_54_toggle.state = "down"
                self.setting_54_toggle.text = "Set $54=0"
            else:
                self.setting_54_label.text = "$54 = 0"
                self.setting_54_toggle.state = "normal"
                self.setting_54_toggle.text = "Set $54=1"
        else:
            self.setting_54_label.text = "$54 = N/A"

    def on_touch(self):
        for text_input in self.text_inputs:
            text_input.focus = False

    def set_toggle_buttons(self):
        if self.systemtools_sm.sm.get_screen("go").show_spindle_overload == False:
            self.show_spindle_overload_toggle.state = "normal"
            self.show_spindle_overload_toggle.text = "Show spindle overload"
        elif self.systemtools_sm.sm.get_screen("go").show_spindle_overload == True:
            self.show_spindle_overload_toggle.state = "down"
            self.show_spindle_overload_toggle.text = "Hide spindle overload"
        if self.m.reminders_enabled == True:
            self.maintenance_reminder_toggle.state = "normal"
            self.maintenance_reminder_toggle.text = "Turn reminders off"
        elif self.m.reminders_enabled == False:
            self.maintenance_reminder_toggle.state = "down"
            self.maintenance_reminder_toggle.text = "Turn reminders on"

    def validate_touch_plate_thickness(self):
        try:
            float(self.z_touch_plate_entry.text)
        except:
            warning_message = "Touchplate offset should be between 1.00 and 2.00 mm"
            popup_info.PopupWarning(self.systemtools_sm.sm, self.l, warning_message)
            return False
        if (
            float(self.z_touch_plate_entry.text) < 1
            or float(self.z_touch_plate_entry.text) > 2
        ):
            warning_message = "Touchplate offset should be between 1.00 and 2.00 mm"
            popup_info.PopupWarning(self.systemtools_sm.sm, self.l, warning_message)
            return False
        else:
            return True

    def update_z_touch_plate_thickness(self):
        if self.validate_touch_plate_thickness():
            self.m.write_z_touch_plate_thickness(self.z_touch_plate_entry.text)
            self.machine_touchplate_thickness.text = str(self.m.z_touch_plate_thickness)

    def validate_serial_number(self):
        if (
            str(self.serial_number_input.text) == ""
            or str(self.product_number_input.text) == ""
            or str(self.serial_prefix.text) == ""
        ):
            warning_message = "Serial number format should be: YS6-0000-.00"
            popup_info.PopupWarning(self.systemtools_sm.sm, self.l, warning_message)
            return False
        elif len(str(self.serial_number_input.text)) != 4:
            warning_message = (
                "Second part of the serial number should be 4 digits long."
            )
            popup_info.PopupWarning(self.systemtools_sm.sm, self.l, warning_message)
            return False
        elif int(self.product_number_input.text) not in [pc.value for pc in ProductCodes]:
            warning_message = "Product code should be 01 to 06."
            popup_info.PopupWarning(self.systemtools_sm.sm, self.l, warning_message)
            return False
        elif len(str(self.serial_prefix.text)) != 3:
            warning_message = (
                "First part of the serial number should be 3 characters long."
            )
            popup_info.PopupWarning(self.systemtools_sm.sm, self.l, warning_message)
            return False
        elif (
            len(
                str(self.serial_prefix.text)
                + str(self.serial_number_input.text)
                + "."
                + str(self.product_number_input.text)
            )
            != 10
        ):
            warning_message = "Serial number format should be: YS6-0000-.00"
            popup_info.PopupWarning(self.systemtools_sm.sm, self.l, warning_message)
            return False
        else:
            return True

    def update_serial_number(self):
        self.serial_prefix.focus = False
        self.serial_number_input.focus = False
        self.product_number_input.focus = False
        if self.validate_serial_number():
            full_serial_number = (
                str(self.serial_number_input.text)
                + "."
                + str(self.product_number_input.text)
            )
            # Do specific tasks for setting up the machine model (e.g. splash screen)
            pc = ProductCodes(int(self.product_number_input.text))
            self.model_manager.set_machine_type(pc, True)
            self.m.write_dollar_setting(50, full_serial_number)
            if pc is ProductCodes.DRYWALLTEC:  # set max z travel to 120mm because of the rubber bellow
                Logger.info("Z max travel ($132) is set to 120 for Drywalltec machine.")
                self.m.write_dollar_setting(132, 120)
            elif pc in [ProductCodes.PRECISION_PRO, ProductCodes.PRECISION_PRO_X, ProductCodes.PRECISION_PRO_PLUS]:
                Logger.info("Z max travel ($132) is set to 130 for double stack motors.")
                self.m.write_dollar_setting(132, 130)
            self.machine_serial.text = "updating..."

            def update_text_with_serial():
                self.machine_serial.text = "$50 = " + str(self.m.serial_number())
                self.write_serial_number_to_file()

            Clock.schedule_once(lambda dt: update_text_with_serial(), 1)

    def check_serial_number_for_factory_reset(self):
        if not (
            str(self.serial_number_input.text)
            + "."
            + str(self.product_number_input.text)
        ).endswith(str(self.m.serial_number())):
            return False
        elif (
            len(
                str(self.serial_prefix.text)
                + str(self.serial_number_input.text)
                + "."
                + str(self.product_number_input.text)
            )
            != 10
        ):
            return False
        else:
            return True

    def remove_creds_file(self):
        try:
            os.system("rm ./asmcnc/production/database/credentials.py")
            os.system("rm ./asmcnc/production/database/credentials.pyc")
        except:
            pass

    def remove_csv_files(self):
        try:
            os.system("rm -r ./asmcnc/production/database/csvs")
        except:
            pass

    def factory_reset(self):
        def nested_factory_reset():
            if not self.set.do_git_fsck():
                message = "git FSCK errors found! repo corrupt."
                popup_system.PopupFSCKErrors(
                    self.systemtools_sm.sm, self.l, message, self.set.details_of_fsck
                )
                return False
            if (
                self.write_activation_code_to_file()
                and self.write_serial_number_to_file()
            ):
                self.remove_creds_file()
                self.remove_csv_files()
                self.set.disable_ssh()
                lifetime = float(120 * 3600)
                self.m.write_spindle_brush_values(0, lifetime)
                self.m.write_z_head_maintenance_settings(0)
                self.m.write_calibration_settings(0, float(320 * 3600))
                self.m.write_spindle_cooldown_rpm_override_settings(False)
                self.m.reminders_enabled = True
                self.m.trigger_setup = True
                self.m.write_set_up_options(True)
                self.set_user_to_view_privacy_notice()
                self.welcome_user_to_smartbench()
                self.set_check_config_flag()
                self.set_wifi_never_connected()
                return True
            else:
                return False

        if self.dev_mode:
            if nested_factory_reset():
                Logger.info("doing factory reset...")
                Clock.schedule_once(self.close_sw, 5)
        else:
            try:
                if self.m.s.setting_54:
                    warning_message = (
                        "Please ensure $54 is set to 0 before doing a factory reset."
                    )
                    popup_info.PopupWarning(
                        self.systemtools_sm.sm, self.l, warning_message
                    )
                    return
            except:
                pass
            if self.smartbench_model.text == "SmartBench model detection failed":
                warning_message = (
                    "Please ensure machine model is set before doing a factory reset."
                )
                popup_info.PopupWarning(self.systemtools_sm.sm, self.l, warning_message)
            elif not self.check_serial_number_for_factory_reset():
                warning_message = "Please ensure machine has a serial number before doing a factory reset."
                popup_info.PopupWarning(self.systemtools_sm.sm, self.l, warning_message)
            elif self.software_version_label.text != self.latest_software_version.text:
                warning_message = "Please ensure machine is fully updated before doing a factory reset."
                popup_info.PopupWarning(self.systemtools_sm.sm, self.l, warning_message)
            elif self.platform_version_label.text != self.latest_platform_version.text:
                warning_message = "Please ensure machine is fully updated before doing a factory reset."
                popup_info.PopupWarning(self.systemtools_sm.sm, self.l, warning_message)
            elif nested_factory_reset():
                reset_warning = (
                    "FACTORY RESET TRIGGERED\n\n"
                    + """Maintenance reminders set and enabled.

"""
                    + """[b]VERY VERY IMPORTANT[/b]:
ALLOW THE CONSOLE TO SHUTDOWN COMPLETELY, AND WAIT 30 SECONDS BEFORE SWITCHING OFF THE MACHINE.

"""
                    + "Not doing this may corrupt the warranty registration start up sequence."
                )
                popup_info.PopupInfo(self.systemtools_sm.sm, self.l, 700, reset_warning)
                Clock.schedule_once(console_utils.shutdown, 5)
            else:
                warning_message = (
                    "There was an issue doing the factory reset! Get Letty for help."
                )
                popup_info.PopupWarning(self.systemtools_sm.sm, self.l, warning_message)

    def close_sw(self, dt):
        sys.exit()

    def full_console_update(self):
        try:
            if self.m.s.setting_54:
                warning_message = (
                    "Please ensure $54 is set to 0 before doing an update."
                )
                popup_info.PopupWarning(self.systemtools_sm.sm, self.l, warning_message)
                return
        except:
            pass
        self.console_update_button.text = "Doing update,\nplease wait..."
        self.remove_csv_files()
        self.remove_creds_file()

        def nested_full_console_update(dt):
            if not self.set.do_git_fsck():
                message = "git FSCK errors found! repo corrupt."
                popup_system.PopupFSCKErrors(
                    self.systemtools_sm.sm, self.l, message, self.set.details_of_fsck
                )
                self.console_update_button.text = "Full Console Update (wifi)"
                return False
            if self.set.get_sw_update_via_wifi():
                self.set.fetch_platform_tags()
                self.set.update_platform()
            else:
                message = "Could not get software update, please check connection."
                popup_info.PopupWarning(self.systemtools_sm.sm, self.l, message)
                self.console_update_button.text = "Full Console Update (wifi)"

        Clock.schedule_once(nested_full_console_update, 1)

    def toggle_reminders(self):
        if self.maintenance_reminder_toggle.state == "normal":
            self.m.reminders_enabled = True
            self.maintenance_reminder_toggle.text = "Turn reminders off"
        elif self.maintenance_reminder_toggle.state == "down":
            self.m.reminders_enabled = False
            self.maintenance_reminder_toggle.text = "Turn reminders on"

    def toggle_spindle_mode(self):
        if self.show_spindle_overload_toggle.state == "normal":
            self.systemtools_sm.sm.get_screen("go").show_spindle_overload = False
            self.show_spindle_overload_toggle.text = "Show spindle overload"
        elif self.show_spindle_overload_toggle.state == "down":
            self.systemtools_sm.sm.get_screen("go").show_spindle_overload = True
            self.show_spindle_overload_toggle.text = "Hide spindle overload"

    def toggle_setting_54(self):
        if self.m.is_machines_fw_version_equal_to_or_greater_than_version(
            "2.5.0", "Toggle $54"
        ):
            if self.setting_54_toggle.state == "normal":
                self.setting_54_label.text = "$54 = 0"
                self.m.write_dollar_setting(54, 0)
                self.setting_54_toggle.text = "Set $54=1"
            else:
                self.setting_54_label.text = "$54 = 1"
                self.m.write_dollar_setting(54, 1)
                self.setting_54_toggle.text = "Set $54=0"
        else:
            self.setting_54_label.text = "$54 = N/A"
            self.setting_54_toggle.state = "normal"
            popup_info.PopupError(self.systemtools_sm, self.l, "FW not compatible!")

    def setting_54_info(self):
        info = (
            "$54 available on FW 2.5 and up\n\n"
            + """$54 should be set to 1 for all final test procedures

"""
            + "$54 should be set to 0 when SB is ready to be factory reset and packed"
        )
        popup_info.PopupInfo(self.systemtools_sm.sm, self.l, 700, info)

    def diagnostics(self):
        self.systemtools_sm.open_diagnostics_screen()

    def update_product_code_with_model(self):
        if (
            self.smartbench_model.text == "SmartBench V1.2 Standard CNC Router"
            or self.smartbench_model.text == "SmartBench V1.2 Precision CNC Router"
        ):
            self.product_number_input.text = "02"
        elif "DRYWALLTEC SmartCNC" in self.smartbench_model.text:
            self.product_number_input.text = "06"
        elif "PrecisionPro X" in self.smartbench_model.text:
            self.product_number_input.text = "05"
        elif "PrecisionPro Plus" in self.smartbench_model.text:
            self.product_number_input.text = "04"
        elif "PrecisionPro" in self.smartbench_model.text:
            self.product_number_input.text = "03"
        elif "Precision/Standard" in self.smartbench_model.text:
            self.product_number_input.text = "03"
        else:
            self.product_number_input.text = "01"

    def set_smartbench_model(self):
        self.update_product_code_with_model()

    def get_smartbench_model(self):
        self.smartbench_model.text = self.m.smartbench_model()
        self.set_smartbench_model()

    def generate_activation_code(self):
        ActiveTempNoOnly = int(
            "".join(
                filter(
                    str.isdigit,
                    str(self.serial_prefix.text) + str(self.serial_number_input.text),
                )
            )
        )
        ActiveTempStart = str(ActiveTempNoOnly * 76289103623 + 20)
        ActiveTempStartReduce = ActiveTempStart[0:15]
        Activation_Code_1 = int(ActiveTempStartReduce[0]) * 171350
        Activation_Code_2 = int(ActiveTempStartReduce[3]) * 152740
        Activation_Code_3 = int(ActiveTempStartReduce[5]) * 213431
        Activation_Code_4 = int(ActiveTempStartReduce[7]) * 548340
        Activation_Code_5 = int(ActiveTempStartReduce[11]) * 115270
        Activation_Code_6 = int(ActiveTempStartReduce[2]) * 4670334
        Activation_Code_7 = int(ActiveTempStartReduce[7]) * 789190
        Activation_Code_8 = int(ActiveTempStartReduce[6]) * 237358903
        Activation_Code_9 = int(ActiveTempStartReduce[6]) * 937350
        Activation_Code_10 = int(ActiveTempStartReduce[6]) * 105430
        Activation_Code_11 = int(ActiveTempStartReduce[6]) * 637820
        Activation_Code_12 = int(ActiveTempStartReduce[6]) * 67253489
        Activation_Code_13 = int(ActiveTempStartReduce[6]) * 53262890
        Activation_Code_14 = int(ActiveTempStartReduce[6]) * 89201233
        Final_Activation_Code = (
            Activation_Code_1
            + Activation_Code_2
            + Activation_Code_3
            + Activation_Code_4
            + Activation_Code_5
            + Activation_Code_6
            + Activation_Code_7
            + Activation_Code_8
            + Activation_Code_9
            + Activation_Code_10
            + Activation_Code_11
            + Activation_Code_12
            + Activation_Code_13
            + Activation_Code_14
        )
        Logger.info(str(Final_Activation_Code) + "\n")
        return Final_Activation_Code

    def show_sc2_decision_popup(self):
        if self.m.state().startswith("Idle"):
            if self.sc2_compatability_toggle.state == "normal":
                message = """This will disable SC2 compatability, are you sure you want to continue?

$51 is currently set to """
            else:
                message = """This will enable SC2 compatability, are you sure you want to continue?

$51 is currently set to """
            if self.m.get_dollar_setting(51) != -1:
                message += str(int(self.m.s.setting_51))
            else:
                message += "N/A"
            popup_factory_settings.PopupSC2Decision(
                self.systemtools_sm.sm, self.l, message
            )
        else:
            popup_info.PopupError(
                self.systemtools_sm,
                self.l,
                "Please ensure machine is idle before continuing",
            )
            self.undo_toggle()

    def toggle_sc2_compatability(self):
        if self.sc2_compatability_toggle.state == "normal":
            self.sc2_compatability_toggle.text = "Enable SC2 compatability"
            try:
                self.m.disable_theateam()
            except:
                warning_message = "Problem removing SC2 compatability file!!"
                popup_info.PopupWarning(self.systemtools_sm.sm, self.l, warning_message)
        else:
            self.sc2_compatability_toggle.text = "Disable SC2 compatability"
            try:
                self.m.enable_theateam()
            except:
                warning_message = "Problem creating SC2 compatability file!!"
                popup_info.PopupWarning(self.systemtools_sm.sm, self.l, warning_message)

    def undo_toggle(self):
        if self.sc2_compatability_toggle.state == "normal":
            self.sc2_compatability_toggle.state = "down"
        else:
            self.sc2_compatability_toggle.state = "normal"

    def write_serial_number_to_file(self):
        try:
            file_ser = open(self.machine_serial_number_filepath, "w+")
            file_ser.write(
                str(self.serial_prefix.text) + str(self.serial_number_input.text)
            )
            file_ser.close()
            return True
        except:
            warning_message = "Problem saving serial number!!"
            popup_info.PopupWarning(self.systemtools_sm.sm, self.l, warning_message)
            return False

    def write_activation_code_to_file(self):
        activation_code_filepath = "/home/pi/smartbench_activation_code.txt"
        try:
            file_act = open(activation_code_filepath, "w+")
            file_act.write(str(self.generate_activation_code()))
            file_act.close()
            return True
        except:
            warning_message = "Problem saving activation code!!"
            popup_info.PopupWarning(self.systemtools_sm.sm, self.l, warning_message)
            return False

    def get_serial_number(self):
        serial_number_from_file = ""
        try:
            file = open(self.machine_serial_number_filepath, "r")
            serial_number_from_file = str(file.read())
            file.close()
        except:
            Logger.exception("Could not get serial number! Please contact YetiTool support!")
        return str(serial_number_from_file)

    def final_test(self, board):
        self.systemtools_sm.open_final_test_screen(board)

    def set_user_to_view_privacy_notice(self):
        user_has_seen_privacy_notice = os.popen(
            'grep "user_has_seen_privacy_notice" /home/pi/easycut-smartbench/src/config.txt'
        ).read()
        if not user_has_seen_privacy_notice:
            os.system(
                "sudo sed -i -e '$auser_has_seen_privacy_notice=False' /home/pi/easycut-smartbench/src/config.txt"
            )
        elif "True" in user_has_seen_privacy_notice:
            os.system(
                'sudo sed -i "s/user_has_seen_privacy_notice=True/user_has_seen_privacy_notice=False/" /home/pi/easycut-smartbench/src/config.txt'
            )

    def welcome_user_to_smartbench(self):
        show_user_welcome_app = os.popen(
            'grep "show_user_welcome_app" /home/pi/easycut-smartbench/src/config.txt'
        ).read()
        if not show_user_welcome_app:
            os.system(
                "sudo sed -i -e '$ashow_user_welcome_app=True' /home/pi/easycut-smartbench/src/config.txt"
            )
        elif "False" in show_user_welcome_app:
            os.system(
                'sudo sed -i "s/show_user_welcome_app=False/show_user_welcome_app=True/" /home/pi/easycut-smartbench/src/config.txt'
            )

    def set_check_config_flag(self):
        os.system('sudo sed -i "s/check_config=False/check_config=True/" config.txt')

    def set_wifi_never_connected(self):
        wifi_connected_before = os.popen(
            'grep "wifi_connected_before" /home/pi/easycut-smartbench/src/config.txt'
        ).read()
        if not wifi_connected_before:
            os.system(
                "sudo sed -i -e '$awifi_connected_before=False' /home/pi/easycut-smartbench/src/config.txt"
            )
        elif "True" in wifi_connected_before:
            os.system(
                'sudo sed -i "s/wifi_connected_before=True/wifi_connected_before=False/" config.txt'
            )

    def enter_serial_number_screen(self):
        if self.calibration_db.conn != None:
            if not self.systemtools_sm.sm.has_screen("serial_input_screen"):
                serial_input_screen = UploadSerialNumbersScreen(
                    name="serial_input_screen",
                    m=self.m,
                    systemtools=self.systemtools_sm,
                    calibration_db=self.calibration_db,
                    settings=self.set,
                    l=self.l,
                    keyboard=self.kb,
                )
                self.systemtools_sm.sm.add_widget(serial_input_screen)
            self.systemtools_sm.sm.current = "serial_input_screen"
        else:
            popup_info.PopupError(
                self.systemtools_sm, self.l, "Database not connected!"
            )

    def enter_calibration_test(self):
        if self.calibration_db.conn != None:
            if self.get_serial_number():
                if not self.systemtools_sm.sm.has_screen("calibration_testing"):
                    calibration_testing = CalibrationTesting(
                        name="calibration_testing",
                        m=self.m,
                        systemtools=self.systemtools_sm,
                        calibration_db=self.calibration_db,
                        sm=self.systemtools_sm.sm,
                        l=self.l,
                    )
                    self.systemtools_sm.sm.add_widget(calibration_testing)
                self.systemtools_sm.sm.current = "calibration_testing"
            else:
                popup_info.PopupError(
                    self.systemtools_sm, self.l, "Serial number has not been entered!"
                )
        else:
            popup_info.PopupError(
                self.systemtools_sm, self.l, "Database not connected!"
            )

    def enter_overnight_test(self):
        if self.calibration_db.conn != None:
            if self.get_serial_number():
                if not self.systemtools_sm.sm.has_screen("overnight_testing"):
                    overnight_testing = OvernightTesting(
                        name="overnight_testing",
                        m=self.m,
                        systemtools=self.systemtools_sm,
                        calibration_db=self.calibration_db,
                        sm=self.systemtools_sm.sm,
                        l=self.l,
                    )
                    self.systemtools_sm.sm.add_widget(overnight_testing)
                self.systemtools_sm.sm.current = "overnight_testing"
            else:
                popup_info.PopupError(
                    self.systemtools_sm, self.l, "Serial number has not been entered!"
                )
        else:
            popup_info.PopupError(
                self.systemtools_sm, self.l, "Database not connected!"
            )

    def enter_current_adjustment(self):
        if not self.systemtools_sm.sm.has_screen("current_adjustment"):
            current_adjustment = CurrentAdjustment(
                name="current_adjustment",
                m=self.m,
                systemtools=self.systemtools_sm,
                l=self.l,
                keyboard=self.kb,
            )
            self.systemtools_sm.sm.add_widget(current_adjustment)
        self.systemtools_sm.sm.current = "current_adjustment"

    def enter_stall_jig(self):
        if self.calibration_db.conn != None:
            if self.get_serial_number():
                if not self.systemtools_sm.sm.has_screen("stall_jig"):
                    stall_jig_screen = screen_stall_jig.StallJigScreen(
                        name="stall_jig",
                        systemtools=self.systemtools_sm,
                        machine=self.m,
                        localization=self.l,
                        calibration_db=self.calibration_db,
                    )
                    self.systemtools_sm.sm.add_widget(stall_jig_screen)
                self.systemtools_sm.sm.current = "stall_jig"
            else:
                popup_info.PopupError(
                    self.systemtools_sm, self.l, "Serial number has not been entered!"
                )
        else:
            popup_info.PopupError(
                self.systemtools_sm, self.l, "Database not connected!"
            )

    def enter_set_thresholds(self):
        if not self.systemtools_sm.sm.has_screen("set_thresholds"):
            set_thresholds_screen = screen_set_thresholds.SetThresholdsScreen(
                name="set_thresholds",
                systemtools=self.systemtools_sm,
                m=self.m,
                l=self.l,
                keyboard=self.kb,
            )
            self.systemtools_sm.sm.add_widget(set_thresholds_screen)
        self.systemtools_sm.sm.current = "set_thresholds"

    def enter_general_measurement(self):
        if not self.systemtools_sm.sm.has_screen("general_measurement"):
            general_measurement_screen = (
                screen_general_measurement.GeneralMeasurementScreen(
                    name="general_measurement",
                    systemtools=self.systemtools_sm,
                    machine=self.m,
                )
            )
            self.systemtools_sm.sm.add_widget(general_measurement_screen)
        self.systemtools_sm.sm.current = "general_measurement"

    def digital_spindle_test_pressed(self):
        from asmcnc.production.z_head_qc_jig.z_head_qc_2 import ZHeadQC2

        zhqc2 = ZHeadQC2(m=self.m, l=self.l, sm=self.systemtools_sm.sm)
        confirm_func = zhqc2.run_digital_spindle_test
        confirm_popup = popup_system.PopupConfirmSpindleTest(confirm_func=confirm_func)
        confirm_popup.open()

    def show_all_smartbench_models(self):
        if self.ids.smartbench_model_button.state == "normal":
            self.ids.smartbench_model.values = self.latest_machine_model_values
            self.ids.smartbench_model_button.text = "Show all models"
        else:
            self.ids.smartbench_model.values = (
                self.old_machine_model_values + self.latest_machine_model_values
            )
            self.ids.smartbench_model_button.text = "Hide all models"
