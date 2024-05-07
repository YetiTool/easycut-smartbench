from asmcnc.comms.logging_system.logging_system import Logger
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.clock import Clock
import traceback, glob, os, re

from asmcnc.skavaUI import widget_status_bar

Builder.load_string("""
<ZHeadWarrantyChoice>:

    fw_version_label : fw_version_label
    connection_button : connection_button
    usb_change_button : usb_change_button
    status_container : status_container

    BoxLayout:
        orientation: 'vertical'

        GridLayout:
            size: self.parent.size
            pos: self.parent.pos
            cols: 1
            rows: 3

            GridLayout: 
                rows: 2

                Label: 
                    text: 'How old is this Z Head?'
                    color: 1,1,1,1
                    text_size: self.size
                    markup: 'True'
                    halign: 'center'
                    valign: 'bottom'
                    font_size: app.get_scaled_width(30.0)

                Label: 
                    id: fw_version_label
                    text: 'Detecting FW version...'
                    color: 1,1,1,1
                    text_size: self.size
                    markup: 'True'
                    halign: 'center'
                    valign: 'middle'
                    font_size: app.get_scaled_width(24.0)

            GridLayout: 
                cols: 2

                Button:
                    text: root.after_label
                    font_size: app.get_scaled_width(20.0)
                    color: 1,1,1,1
                    text_size: self.size
                    markup: 'True'
                    halign: 'center'
                    valign: 'middle'
                    on_press: root.after_apr21()

                Button:
                    text: root.before_label
                    font_size: app.get_scaled_width(20.0)
                    color: 1,1,1,1
                    text_size: self.size
                    markup: 'True'
                    halign: 'center'
                    valign: 'middle'
                    on_press: root.before_apr21()

            BoxLayout: 
                orientation: 'horizontal'

                Button: 
                    text: '<<< Back'
                    font_size: app.get_scaled_width(20.0)
                    on_press: root.back_to_home()

                ToggleButton: 
                    id: connection_button
                    text: "Disconnect Z Head"
                    font_size: app.get_scaled_width(20.0)
                    on_press: root.toggle_connection_to_z_head()


                ToggleButton:
                    id: usb_change_button
                    text: 'FW on USB: vx.x.x'
                    font_size: app.get_scaled_width(20.0)
                    on_press: root.toggle_usb_mounted()
                    markup: True
                    halign: "center"

        BoxLayout:
            size_hint_y: 0.08
            id: status_container 
            pos: self.pos

""")


class ZHeadWarrantyChoice(Screen):

    after_label = "Made AFTER April 2021\n\nFW version v1.3.6 or above"
    before_label = "Made BEFORE April 2021\n\nFW version v1.1.2 or below"

    poll_for_fw = None


    def __init__(self, **kwargs):
        super(ZHeadWarrantyChoice, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']
        self.usb = kwargs['usb']

        # Status bar
        self.status_bar_widget = widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm)
        self.status_container.add_widget(self.status_bar_widget)

    def on_enter(self):
        self.poll_for_fw = Clock.schedule_once(self.scrape_fw_version, 0.2)
        self.load_usb_stick_with_hex_file() 

    def scrape_fw_version(self, dt):
        try:
            self.fw_version_label.text = "Detected FW version: " + str((str(self.m.s.fw_version)).split('; HW')[0])
            if self.poll_for_fw != None: Clock.unschedule(self.poll_for_fw)
        
        except:
            Logger.exception("could not detect fw/update label")

    def after_apr21(self):
        self.sm.current = 'qcW136'

    def before_apr21(self):
        self.sm.current = 'qcW112'

    def back_to_home(self):
        self.sm.current = 'qchome'

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

    def toggle_usb_mounted(self):

        if self.usb_change_button.state == 'normal':
            self.load_usb_stick_with_hex_file() 

        else: 
            self.usb_change_button.text = "No USB\n\nReconnect?"
            self.usb.disable()

    def load_usb_stick_with_hex_file(self):

        if not self.usb.stick_enabled:
            self.usb.enable()

        if self.usb.is_available():
            try:
                self.fw_on_usb = re.split('GRBL|\.', str(glob.glob("/media/usb/GRBL*.hex")[0]))[1]
                self.usb_change_button.text = "FW on USB: " + self.fw_on_usb + "\n\n" + "Change USB?"
            except:
                Logger.exception('Failed to extract firmware name!')

            return

        Clock.schedule_once(lambda dt: self.load_usb_stick_with_hex_file(), 1)

