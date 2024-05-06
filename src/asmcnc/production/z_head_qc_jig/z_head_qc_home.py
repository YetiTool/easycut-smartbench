from asmcnc.comms.logging_system.logging_system import Logger
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.clock import Clock

from asmcnc.production.z_head_qc_jig import popup_z_head_qc
from asmcnc.core_UI import console_utils

import subprocess

import sys, os, re, glob

try: 
    import pigpio

except:
    pass

Builder.load_string("""
<ZHeadQCHome>:
    
    test_fw_update_button : test_fw_update_button

    BoxLayout:
        orientation: 'vertical'

        GridLayout:
            size: self.parent.size
            pos: self.parent.pos
            cols: 1
            rows: 3

            Label: 
                text: 'Have you just updated the FW on this Z Head?'
                color: color_provider.get_rgba("white")
                text_size: self.size
                markup: 'True'
                halign: 'center'
                valign: 'middle'
                font_size: dp(30)

            GridLayout: 
                cols: 2

                Button:
                    id: test_fw_update_button 
                    text: 'NO - Set up PCB & Flash FW'
                    font_size: dp(20)
                    on_press: root.go_back_to_pcb_setup()
                    markup: True
                    halign: "center"

                Button:
                    text: 'YES - Take me to QC! (For v1.3)'
                    font_size: dp(20)
                    on_press: root.enter_qc()

            GridLayout:
                cols: 2

                Button: 
                    text: 'Take me to WARRANTY QC! (For v1.2)'
                    font_size: dp(20)
                    on_press: root.secret_option_c()

                Button:
                    text: 'Shut down'
                    font_size: dp(20)
                    background_color: [1,0,0,1]
                    background_normal: ''
                    on_press: console_utils.shutdown()
""")


class ZHeadQCHome(Screen):

    fw_button_string = 'NO - Set up PCB & Flash FW'
    hw_version = 0

    def __init__(self, **kwargs):
        super(ZHeadQCHome, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']
        self.usb = kwargs['usb']

    def on_enter(self):
        try: 
            self.hw_version = int(self.m.s.hw_version)
            self.update_usb_button_label()

        except:
            Logger.exception("Can't get HW version or hex file")

    def go_back_to_pcb_setup(self):
        self.sm.current = "qcpcbsetup"  

    def get_fw_filepath(self):

        if int(self.hw_version) >= 34:
            return "/media/usb/GRBL*5.hex"

        elif int(self.hw_version) >= 20:
            if glob.glob("/media/usb/GRBL*4.hex"):
                return "/media/usb/GRBL*4.hex"

            # Allow for older FW versions, starting in 2 but not ending in 4
            return "/media/usb/GRBL23*.hex"

        return "/media/usb/GRBL1*.hex"

    def update_usb_button_label(self):
        try:
            self.fw_on_usb = "USB FW: " + re.split('GRBL|\.', str(glob.glob(self.get_fw_filepath())[0]))[1]
            self.test_fw_update_button.text = self.fw_button_string + "\n\n" + self.fw_on_usb

        except: 
            self.test_fw_update_button.text = "Looking for USB"
            self.usb.enable()
            Clock.schedule_once(lambda dt: self.update_usb_button_label(), 2)

    def enter_qc(self):
        self.sm.current = 'qc1'

    def test_fw_update(self):

        self.test_fw_update_button.text = "  Updating..."

        def disconnect_and_update():
            self.m.s.grbl_scanner_running = False
            Clock.schedule_once(self.m.close_serial_connection, 0.1)
            Clock.schedule_once(nested_do_fw_update, 1)

        def nested_do_fw_update(dt):
            pi = pigpio.pi()
            pi.set_mode(17, pigpio.ALT3)
            Logger.info(pi.get_mode(17))
            pi.stop()

            cmd = "grbl_file=" + self.get_fw_filepath() + " && avrdude -patmega2560 -cwiring -P/dev/ttyAMA0 -b115200 -D -Uflash:w:$(echo $grbl_file):i"
            proc = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = True)
            self.stdout, stderr = proc.communicate()
            self.exit_code = int(proc.returncode)

            connect()

        def connect():
            self.m.starting_serial_connection = True
            Clock.schedule_once(do_connection, 0.1)

        def do_connection(dt):
            self.m.reconnect_serial_connection()
            self.poll_for_reconnection = Clock.schedule_interval(try_start_services, 0.4)

        def try_start_services(dt):
            if self.m.s.is_connected():
                Clock.unschedule(self.poll_for_reconnection)
                Clock.schedule_once(self.m.s.start_services, 1)
                # hopefully 1 second should always be enough to start services
                Clock.schedule_once(update_complete, 2)

        def update_complete(dt):
            if self.exit_code == 0: 
                did_fw_update_succeed = "Success!"

            else: 
                did_fw_update_succeed = "Update failed."

            popup_z_head_qc.PopupFWUpdateDiagnosticsInfo(self.sm, did_fw_update_succeed, str(self.stdout))
            self.update_usb_button_label()

            self.sm.get_screen('qc1').reset_checkboxes()
            self.sm.get_screen('qc2').reset_checkboxes()
            self.sm.get_screen('qcW136').reset_checkboxes()
            self.sm.get_screen('qcW112').reset_checkboxes()
            self.sm.get_screen('qc3').reset_timer()

        disconnect_and_update()


    def secret_option_c(self):
        self.sm.current = 'qcWC'
