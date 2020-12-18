'''
Created on 18 November 2020
Menu screen for system tools app

@author: Letty
'''
import os

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
    serial_prefix: serial_prefix
    serial_number_input: serial_number_input
    product_number_input: product_number_input
    machine_serial: machine_serial
    machine_touchplate_thickness: machine_touchplate_thickness
    maintenance_reminder_toggle: maintenance_reminder_toggle
    show_spindle_overload_toggle: show_spindle_overload_toggle
    smartbench_model: smartbench_model
    console_update_button: console_update_button

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
                                            id: serial_prefix
                                            text: 'YS6'
                                            color: [0,0,0,1]
                                            markup: True
                                            valign: 'middle'
                                            size_hint_x: 0.3
                                            multiline: False
                                        Label:
                                            text: ''
                                            color: [0,0,0,1]
                                            markup: True
                                            size_hint_x: 0.05

                                        TextInput:
                                            id: serial_number_input
                                            text: '0000'
                                            color: [0,0,0,1]
                                            markup: True
                                            valign: 'middle'
                                            size_hint_x: 0.35
                                            input_filter: 'int'
                                            multiline: False

                                        Label:
                                            text: '.'
                                            color: [0,0,0,1]
                                            markup: True
                                            size_hint_x: 0.05

                                        TextInput:
                                            id: product_number_input
                                            text: '00'
                                            color: [0,0,0,1]
                                            markup: True
                                            valign: 'middle'
                                            size_hint_x: 0.25
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
                                        text: '[b]Touchplate offset[/b]'
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
                                id: console_update_button
                                text: 'Full Console Update (wifi)'
                                on_press: root.full_console_update()

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
                            text: 'Turn reminders off'
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
    machine_serial_number_filepath  = "/home/pi/smartbench_serial_number.txt"

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

        try: 
            serial_number_string = self.get_serial_number()
            self.serial_prefix.text = serial_number_string[0:3]
            self.serial_number_input.text = serial_number_string[3:7]
            self.product_number_input.text = str(self.m.serial_number()).split('.')[1]
        except: 
            self.serial_prefix.text = 'YS6'
            self.serial_number_input.text = '0000'
            self.product_number_input.text = '00'

    ## EXIT BUTTONS
    def go_back(self):
        self.systemtools_sm.back_to_menu()

    def exit_app(self):
        self.systemtools_sm.exit_app()

    def on_enter(self):
        self.z_touch_plate_entry.text = str(self.m.z_touch_plate_thickness)

    def validate_touch_plate_thickness(self):

        try: 
            float(self.z_touch_plate_entry.text)

        except: 
            warning_message = 'Touchplate offset should be between 1.00 and 2.00 mm'
            popup_info.PopupWarning(self.systemtools_sm.sm, warning_message)
            return False        

        if (float(self.z_touch_plate_entry.text) < 1) or (float(self.z_touch_plate_entry.text) > 2):
            warning_message = 'Touchplate offset should be between 1.00 and 2.00 mm'
            popup_info.PopupWarning(self.systemtools_sm.sm, warning_message)
            return False

        else: 
            return True

    def update_z_touch_plate_thickness(self):

        if self.validate_touch_plate_thickness():
            self.m.write_z_touch_plate_thickness(self.z_touch_plate_entry.text)
            self.machine_touchplate_thickness.text = str(self.m.z_touch_plate_thickness)

    def validate_serial_number(self):

        if ((str(self.serial_number_input.text) == '') or (str(self.product_number_input.text) == '') or
            (str(self.serial_prefix.text) == '')):
            warning_message = 'Serial number format should be: YS6-0000-.00'
            popup_info.PopupWarning(self.systemtools_sm.sm, warning_message)
            return False

        elif len(str(self.serial_number_input.text)) != 4:
            warning_message = 'Second part of the serial number should be 4 digits long.'
            popup_info.PopupWarning(self.systemtools_sm.sm, warning_message)
            return False

        elif not ((str(self.product_number_input.text) == '01') or (str(self.product_number_input.text) == '02') or 
            (str(self.product_number_input.text) == '03')):
            warning_message = 'Product code should 01, 02, or 03.'
            popup_info.PopupWarning(self.systemtools_sm.sm, warning_message)
            return False

        elif len(str(self.serial_prefix.text)) != 3: 
            warning_message = 'First part of the serial number should be 3 characters long.'
            popup_info.PopupWarning(self.systemtools_sm.sm, warning_message)
            return False

        else: 
            return True

    def update_serial_number(self):

        self.serial_prefix.focus = False
        self.serial_number_input.focus = False
        self.product_number_input.focus = False

        if self.validate_serial_number():
            full_serial_number = self.serial_number_input.text + "." + self.product_number_input.text
            self.m.write_dollar_50_setting(full_serial_number)
            self.machine_serial.text = 'updating...'

            def update_text_with_serial():
                self.machine_serial.text = str( self.m.serial_number())

            Clock.schedule_once(lambda dt: update_text_with_serial(), 1)

    def factory_reset(self):
        if len(str(self.m.serial_number())) < 7:
            warning_message = 'Please ensure machine has a serial number before doing a factory reset.'
            popup_info.PopupWarning(self.systemtools_sm.sm, warning_message)
        elif self.smartbench_model.text == 'Choose model':
            warning_message = 'Please ensure machine model is set before doing a factory reset.'
            popup_info.PopupWarning(self.systemtools_sm.sm, warning_message)
        # elif self.software_version_label.text != self.latest_software_version.text:
        #     warning_message = 'Please ensure machine is fully updated before doing a factory reset.'
        #     popup_info.PopupWarning(self.systemtools_sm.sm, warning_message)
        # elif self.platform_version_label.text != self.latest_platform_version.text:
        #     warning_message = 'Please ensure machine is fully updated before doing a factory reset.'
        #     popup_info.PopupWarning(self.systemtools_sm.sm, warning_message)
        else:

            def nested_factory_reset():
                if self.write_activation_code_and_serial_number_to_file():
                    lifetime = float(120*3600)
                    self.m.write_spindle_brush_values(0, lifetime)
                    self.m.write_z_head_maintenance_settings(0)
                    self.m.write_calibration_settings(0, float(320*3600))
                    self.m.reminders_enabled = True
                    self.m.trigger_setup = True
                    self.m.write_set_up_options(True)
                    return True
                else:
                    return False

            if nested_factory_reset():
                reset_warning = "FACTORY RESET TRIGGERED\n\n" + \
                "Maintenance reminders set and enabled.\n\n" + \
                "[b]VERY VERY IMPORTANT[/b]:\nALLOW THE CONSOLE TO SHUTDOWN COMPLETELY, AND WAIT 30 SECONDS BEFORE SWITCHING OFF THE MACHIN.\n\n" + \
                "Not doing this may corrupt the warranty registration start up sequence."
                popup_info.PopupInfo(self.systemtools_sm.sm, 700, reset_warning)

                Clock.schedule_once(self.shutdown_console, 5)

            else: 
                warning_message = 'There was an issue doing the factory reset! Get Letty for help.'
                popup_info.PopupWarning(self.systemtools_sm.sm, warning_message)



    def shutdown_console(self, dt):
        os.system('sudo shutdown -h now')

    def full_console_update(self):

        self.console_update_button.text = "Doing update,\nplease wait..."

        def nested_full_console_update(dt):

            if self.set.get_sw_update_via_wifi():
                self.set.update_platform()
            else: 
                message = "Could not get software update, please check connection."
                popup_info.PopupWarning(self.sm, message)

        Clock.schedule_once(nested_full_console_update, 1)


    def toggle_reminders(self):
        if self.maintenance_reminder_toggle.state == 'normal':
            self.m.reminders_enabled = True
            self.maintenance_reminder_toggle.text = "Turn reminders off"

        elif self.maintenance_reminder_toggle.state == 'down':
            self.m.reminders_enabled = False
            self.maintenance_reminder_toggle.text = "Turn reminders on"

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

    def generate_activation_code(self):
        ActiveTempNoOnly = int(''.join(filter(str.isdigit, str(self.serial_prefix.text) + str(self.serial_number_input.text))))
        ActiveTempStart = str(ActiveTempNoOnly * 76289103623 + 20)
        ActiveTempStartReduce = ActiveTempStart[0:15]
        Activation_Code_1 = int(ActiveTempStartReduce[0])*171350;
        Activation_Code_2 = int(ActiveTempStartReduce[3])*152740;
        Activation_Code_3 = int(ActiveTempStartReduce[5])*213431; 
        Activation_Code_4 = int(ActiveTempStartReduce[7])*548340;
        Activation_Code_5 = int(ActiveTempStartReduce[11])*115270;
        Activation_Code_6 = int(ActiveTempStartReduce[2])*4670334;
        Activation_Code_7 = int(ActiveTempStartReduce[7])*789190;
        Activation_Code_8 = int(ActiveTempStartReduce[6])*237358903;
        Activation_Code_9 = int(ActiveTempStartReduce[6])*937350;
        Activation_Code_10 = int(ActiveTempStartReduce[6])*105430;
        Activation_Code_11 = int(ActiveTempStartReduce[6])*637820;
        Activation_Code_12 = int(ActiveTempStartReduce[6])*67253489;
        Activation_Code_13 = int(ActiveTempStartReduce[6])*53262890;
        Activation_Code_14 = int(ActiveTempStartReduce[6])*89201233;
        Final_Activation_Code = Activation_Code_1 + Activation_Code_2 + Activation_Code_3 +Activation_Code_4 + Activation_Code_5 + Activation_Code_6 + Activation_Code_7 + Activation_Code_8 + Activation_Code_9 + Activation_Code_10 + Activation_Code_11 + Activation_Code_12 + Activation_Code_13 + Activation_Code_14
        print(str(Final_Activation_Code)+'\n')
        return Final_Activation_Code

    def write_activation_code_and_serial_number_to_file(self):
        activation_code_filepath = "/home/pi/smartbench_activation_code.txt"
        try: 
            file_act = open(activation_code_filepath, "w+")
            file_act.write(str(self.generate_activation_code()))
            file_act.close()
            file_ser = open(self.machine_serial_number_filepath, "w+")
            file_ser.write(str(self.serial_prefix.text) + str(self.serial_number_input.text))
            file_ser.close()
            return True
        except: 
            warning_message = 'Problem saving activation code!!'
            popup_info.PopupWarning(self.systemtools_sm.sm, warning_message)
            return False

    def get_serial_number(self):
        serial_number_from_file = ''

        try: 
            file = open(self.machine_serial_number_filepath, 'r')
            serial_number_from_file  = str(file.read())
            file.close()

        except: 
            print 'Could not get serial number! Please contact YetiTool support!'

        return str(serial_number_from_file)

            