'''
Created on 18 November 2020
Menu screen for system tools app

@author: Letty
'''

from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

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

    BoxLayout:
        width: dp(800)
        height: dp(480)
        canvas.before:
            Color: 
                rgba: [226 / 255., 226 / 255., 226 / 255., 1.]
            Rectangle: 
                size: self.size
                pos: self.pos

        BoxLayout:
            padding: 10
            spacing: 10
            orientation: "vertical"
            BoxLayout:
                padding: 0
                spacing: 0
                canvas:
                    Color:
                        rgba: [1,1,1,1]
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                Label:
                    size_hint: (None,None)
                    height: dp(70)
                    width: dp(780)
                    text: "Factory Settings"
                    color: [0,0,0,1]
                    font_size: 30
                    halign: "center"
                    valign: "bottom"
                    markup: True

            BoxLayout:
                size_hint: (None,None)
                width: dp(780)
                height: dp(240)
                padding: 0
                spacing: 10
                orientation: 'horizontal'
                BoxLayout:
                    size_hint: (None,None)
                    width: dp(577.5)
                    height: dp(240)
                    padding: 0
                    spacing: 10
                    orientation: 'vertical'
                    BoxLayout:
                        size_hint: (None,None)
                        width: dp(577.5)
                        height: dp(155)
                        padding: 0
                        spacing: 0
                        orientation: 'vertical'
                        canvas:
                            Color:
                                rgba: [1,1,1,1]
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                        GridLayout: 
                            size: self.parent.size
                            pos: self.parent.pos
                            cols: 0
                            rows: 3
                            padding: [10,0]
                            spacing: 5
                            BoxLayout: 
                                orientation: 'vertical'
                                spacing: 5
                                Label:
                                    text: '[b]Serial number (e.g., 1234.01)[/b]'
                                    color: [0,0,0,1]
                                    markup: True
                                    text_size: self.size
                                    halign: 'left'
                                    size_hint_y: 0.8

                                GridLayout: 
                                    size: self.parent.size
                                    pos: self.parent.pos
                                    cols: 4
                                    rows: 0
                                    padding: 0
                                    spacing: 10
                                    Label:
                                        text: '$50 ='
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
                                Label:
                                    text: '[b]Touchplate thickness (default: 1.53)[/b]'
                                    color: [0,0,0,1]
                                    markup: True
                                    text_size: self.size
                                    halign: 'left'
                                    size_hint_y: 0.8

                                GridLayout: 
                                    size: self.parent.size
                                    pos: self.parent.pos
                                    cols: 4
                                    rows: 0
                                    padding: 0
                                    spacing: 10

                                    Label:
                                        text: 'Thickness = '
                                        color: [0,0,0,1]
                                        markup: True
                                    TextInput:
                                        id: z_touch_plate_entry
                                        text: ''
                                        color: [0,0,0,1]
                                        markup: True
                                        valign: 'middle'
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
                        height: dp(75)
                        padding: 5
                        spacing: 0
                        orientation: 'vertical'
                        canvas:
                            Color:
                                rgba: [1,1,1,1]
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                        GridLayout: 
                            size: self.parent.size
                            pos: self.parent.pos
                            cols: 3
                            rows: 0
                            padding: 0
                            spacing: 10

                            Button:
                                text: 'Full Console Update'

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
                    height: dp(240)
                    padding: 0
                    spacing: 0
                    orientation: 'vertical'
                    canvas:
                        Color:
                            rgba: [1,1,1,1]
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
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
                width: dp(780)
                height: dp(130)
                padding: 0
                spacing: 10
                orientation: 'horizontal'

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(192.5)
                    height: dp(130)
                    padding: 0
                    spacing: 0
                    canvas:
                        Color:
                            rgba: [1,1,1,1]
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                    BoxLayout: 
                        size_hint: (None, None)
                        height: dp(130)
                        width: dp(192.5)
                        padding: [52.25,31,52.25,31]
                        Button:
                            size_hint: (None,None)
                            height: dp(68)
                            width: dp(88)
                            background_color: hex('#F4433600')
                            center: self.parent.center
                            pos: self.parent.pos
                            on_press: root.go_back()
                            BoxLayout:
                                padding: 0
                                size: self.parent.size
                                pos: self.parent.pos
                                Image:
                                    source: "./asmcnc/apps/shapeCutter_app/img/arrow_back.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(375)
                    height: dp(130)
                    padding: 0
                    spacing: 0
                    orientation: 'vertical'
                    canvas:
                        Color:
                            rgba: [1,1,1,1]
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size

                    BoxLayout:
                        padding: [30, 10]
                        Button:
                            text: 'FACTORY RESET'
                            on_press: root.factory_reset()

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(192.5)
                    height: dp(130)
                    padding: 0
                    spacing: 0
                    canvas:
                        Color:
                            rgba: [1,1,1,1]
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size

                    BoxLayout: 
                        size_hint: (None, None)
                        height: dp(130)
                        width: dp(192.5)
                        padding: [40.25,9,40.25,9] 
                        Button:
                            size_hint: (None,None)
                            height: dp(112)
                            width: dp(112)
                            background_color: hex('#F4433600')
                            center: self.parent.center
                            pos: self.parent.pos
                            on_press: root.exit_app()
                            BoxLayout:
                                padding: 0
                                size: self.parent.size
                                pos: self.parent.pos
                                Image:
                                    source: "./asmcnc/apps/wifi_app/img/quit.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True


""")

class FactorySettingsScreen(Screen):

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
        lifetime = float(120*3600)
        self.m.write_spindle_brush_values(0, lifetime)
        self.m.write_z_head_maintenance_settings(0)
        self.m.write_calibration_settings(0, float(320*3600))
        self.m.reminders_enabled = True
        self.m.trigger_setup = True
        self.m.write_set_up_options(True)

    def full_console_update(self):
        pass
        # run mega update script

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
            