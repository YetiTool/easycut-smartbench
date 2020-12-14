'''
Created on 18 November 2020
Menu screen for system tools app

@author: Letty
'''

from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.spinner import Spinner

from asmcnc.skavaUI import popup_info

Builder.load_string("""

<FactorySettingsScreen>

    software_version_label: software_version_label
    platform_version_label: platform_version_label
    latest_software_version: latest_software_version
    latest_platform_version: latest_platform_version
    z_touch_plate_entry: z_touch_plate_entry
    serial_number_input: serial_number_input
    product_number_input: product_number_input
    machine_serial: machine_serial
    machine_touchplate_thickness: machine_touchplate_thickness
    maintenance_reminder_toggle: maintenance_reminder_toggle
    show_spindle_overload_toggle: show_spindle_overload_toggle
    smartbench_model: smartbench_model

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
                    text: "Factory settings"
                    color: hex('#f9f9f9ff')
                    font_size: 30
                    halign: "center"
                    valign: "bottom"
                    markup: True
                   
            BoxLayout:
                size_hint: (None,None)
                width: dp(800)
                height: dp(320)
                padding: 10
                spacing: 10
                orientation: 'horizontal'
                BoxLayout:
                    size_hint: (None,None)
                    width: dp(577.5)
                    height: dp(320)
                    padding: 0
                    spacing: 10
                    orientation: 'vertical'
                    BoxLayout:
                        size_hint: (None,None)
                        width: dp(577.5)
                        height: dp(210)
                        padding: 0
                        spacing: 0
                        orientation: 'vertical'

                        GridLayout: 
                            size: self.parent.size
                            pos: self.parent.pos
                            cols: 0
                            rows: 3
                            padding: 10
                            spacing: 5
                            BoxLayout: 
                                orientation: 'vertical'
                                spacing: 5

                                Spinner:
                                    id: smartbench_model
                                    text: 'Choose model'
                                    values: root.machine_model_values
                                    on_text: root.set_smartbench_model()

                            BoxLayout: 
                                orientation: 'vertical'
                                spacing: 5


                                GridLayout: 
                                    size: self.parent.size
                                    pos: self.parent.pos
                                    cols: 4
                                    rows: 0
                                    padding: 10
                                    spacing: 10
                                    Label:
                                        text: '[b]Serial number $50[/b]'
                                        color: [0,0,0,1]
                                        markup: True
                                    BoxLayout: 
                                        orientation: 'horizontal'

                                        TextInput:
                                            id: serial_number_input
                                            text: '1234'
                                            color: [0,0,0,1]
                                            markup: True
                                            valign: 'middle'
                                            size_hint_x: 0.6
                                            input_filter: 'int'
                                            multiline: False

                                        Label:
                                            text: '.'
                                            color: [0,0,0,1]
                                            markup: True
                                            size_hint_x: 0.1

                                        TextInput:
                                            id: product_number_input
                                            text: '01'
                                            color: [0,0,0,1]
                                            markup: True
                                            valign: 'middle'
                                            size_hint_x: 0.3
                                            input_filter: 'int'
                                            multiline: False

                                    Button:
                                        text: 'UPDATE'
                                        on_press: root.update_serial_number()

                                    Label:
                                        id: machine_serial
                                        text: 'machine serial'
                                        color: [0,0,0,1]
                                        markup: True

                            BoxLayout: 
                                orientation: 'vertical'
                                spacing: 5

                                GridLayout: 
                                    size: self.parent.size
                                    pos: self.parent.pos
                                    cols: 4
                                    rows: 0
                                    padding: 10
                                    spacing: 10

                                    Label:
                                        text: '[b]Touchplate thickness[/b]'
                                        color: [0,0,0,1]
                                        markup: True
                                    TextInput:
                                        id: z_touch_plate_entry
                                        text: ''
                                        color: [0,0,0,1]
                                        markup: True
                                        valign: 'middle'
                                        input_filter: 'float'
                                        multiline: False
                                    Button:
                                        text: 'UPDATE'
                                        on_press: root.update_z_touch_plate_thickness()
    
                                    Label:
                                        id: machine_touchplate_thickness
                                        text: 'machine_tp'
                                        color: [0,0,0,1]
                                        markup: True


                    BoxLayout:
                        size_hint: (None,None)
                        width: dp(577.5)
                        height: dp(100)
                        padding: 5
                        spacing: 0
                        orientation: 'vertical'

                        GridLayout: 
                            size: self.parent.size
                            pos: self.parent.pos
                            cols: 3
                            rows: 0
                            padding: 0
                            spacing: 10

                            Button:
                                text: 'Full Console Update (wifi)'

                            GridLayout: 
                                size: self.parent.size
                                pos: self.parent.pos
                                cols: 0
                                rows: 3
                                padding: 0
                                spacing: 2
                                Label:
                                    text: 'Current'
                                    color: [0,0,0,1]
                                    markup: True
                                Label:
                                    id: software_version_label
                                    text: 'SW'
                                    color: [0,0,0,1]
                                    markup: True
                                Label:
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
                                spacing: 2
                                Label:
                                    text: 'Available'
                                    color: [0,0,0,1]
                                    markup: True
                                Label:
                                    id: latest_software_version
                                    text: 'SW'
                                    color: [0,0,0,1]
                                    markup: True
                                Label:
                                    id: latest_platform_version
                                    text: 'PL'
                                    color: [0,0,0,1]
                                    markup: True



                BoxLayout:
                    size_hint: (None,None)
                    width: dp(192.5)
                    height: dp(320)
                    padding: 0
                    spacing: 0
                    orientation: 'vertical'

                    GridLayout: 
                        size: self.parent.size
                        pos: self.parent.pos
                        cols: 1
                        rows: 3
                        padding: 10
                        spacing: 10
                        ToggleButton:
                            id: maintenance_reminder_toggle
                            text: 'Reminders on'
                            on_press: root.toggle_reminders()
                        ToggleButton:
                            id: show_spindle_overload_toggle
                            text: 'Show spindle overload'
                            on_press: root.toggle_spindle_mode()
                        Button:
                            text: 'Diagnostics'
                            on_press: root.diagnostics()

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
                    padding: [160, 0]
                    spacing: 0
                    orientation: 'vertical'
                    BoxLayout:
                        Button:
                            text: 'FACTORY RESET'
                            on_press: root.factory_reset()

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

class FactorySettingsScreen(Screen):

    machine_model_values = ['SmartBench V1.2 Standard CNC Router', 'SmartBench V1.2 Precision CNC Router', 'SmartBench V1.2 PrecisionPro CNC Router']
    smartbench_model_path = '/home/pi/smartbench_model_name.txt'

    def __init__(self, **kwargs):
        super(FactorySettingsScreen, self).__init__(**kwargs)
        self.systemtools_sm = kwargs['system_tools']
        self.m = kwargs['machine']
        self.set = kwargs['settings']

        self.software_version_label.text = self.set.sw_version
        self.platform_version_label.text = self.set.platform_version
        self.latest_software_version.text = self.set.latest_sw_version
        self.latest_platform_version.text = self.set.latest_platform_version

        self.machine_serial.text = str(self.m.serial_number())
        self.machine_touchplate_thickness.text = str(self.m.z_touch_plate_thickness)


    ## EXIT BUTTONS
    def go_back(self):
        self.systemtools_sm.back_to_menu()

    def exit_app(self):
        self.systemtools_sm.exit_app()

    def on_enter(self):
        self.z_touch_plate_entry.text = str(self.m.z_touch_plate_thickness)

    def update_z_touch_plate_thickness(self):
        self.m.write_z_touch_plate_thickness(self.z_touch_plate_entry.text)
        self.machine_touchplate_thickness.text = str(self.m.z_touch_plate_thickness)

    def update_serial_number(self):
        full_serial_number = self.serial_number_input.text + "." + self.product_number_input.text
        self.m.write_dollar_50_setting(full_serial_number)
        self.machine_serial.text = 'updating...'

        def update_text_with_serial():
            self.machine_serial.text = str( self.m.serial_number())

        Clock.schedule_once(lambda dt: update_text_with_serial(), 1)

    def factory_reset(self):
        if self.m.serial_number() == 0:
            warning_message = 'Please ensure machine has a serial number before doing a factory reset.'
            popup_info.PopupWarning(self.systemtools_sm.sm, warning_message)
        elif self.smartbench_model.text == 'Choose Model':
            warning_message = 'Please ensure machine model is set before doing a factory reset.'
            popup_info.PopupWarning(self.systemtools_sm.sm, warning_message)
        elif self.software_version_label.text != self.latest_software_version.text:
            warning_message = 'Please ensure machine is fully updated before doing a factory reset.'
            popup_info.PopupWarning(self.systemtools_sm.sm, warning_message)
        elif self.platform_version_label.text != self.latest_platform_version.text:
            warning_message = 'Please ensure machine is fully updated before doing a factory reset.'
            popup_info.PopupWarning(self.systemtools_sm.sm, warning_message)
        else:
            lifetime = float(120*3600)
            self.m.write_spindle_brush_values(0, lifetime)
            self.m.write_z_head_maintenance_settings(0)
            self.m.write_calibration_settings(0, float(320*3600))
            self.m.reminders_enabled = True
            self.m.trigger_setup = True
            self.m.write_set_up_options(True) # use this to set warranty on restart?
            # partially - set this flag and then if it's set check for a file containing an activation code.
            # delete this file when it's been set. 

    def full_console_update(self):
        if self.set.get_sw_update_via_wifi():
            self.set.update_platform()
        else: 
            message = "Could not get software update, please check connection."
            popup_info.PopupWarning(self.sm, message)


    def toggle_reminders(self):
        if self.maintenance_reminder_toggle.state == 'normal':
            self.m.reminders_enabled = True
            self.maintenance_reminder_toggle.text = "Reminders on"

        elif self.maintenance_reminder_toggle.state == 'down':
            self.m.reminders_enabled = False
            self.maintenance_reminder_toggle.text = "Reminders off"

    def toggle_spindle_mode(self):
        if self.show_spindle_overload_toggle.state == 'normal':
            self.systemtools_sm.sm.get_screen('go').show_spindle_overload = False
            self.show_spindle_overload_toggle.text = 'Show spindle overload'
        elif self.show_spindle_overload_toggle.state == 'down':
            self.systemtools_sm.sm.get_screen('go').show_spindle_overload = True
            self.show_spindle_overload_toggle.text = 'Hide spindle overload'

    def diagnostics(self):
        self.systemtools_sm.open_diagnostics_screen()

    def set_smartbench_model(self):
        print('Writing ' + self.smartbench_model.text)
        file = open(self.smartbench_model_path, "w+")
        file.write(str(self.smartbench_model.text))
        file.close()

    def get_smartbench_model(self):
        try:
            file = open(self.smartbench_model_path, 'r')
            self.smartbench_model.text = str(file.read())
            file.close()
        except: 
            self.smartbench_model.text = 'Choose Model'


            