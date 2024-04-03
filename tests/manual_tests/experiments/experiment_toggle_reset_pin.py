 # -*- coding: utf-8 -*-

'''
########################################################
IMPORTANT!!
Run from easycut-smartbench folder, with 
python -m tests.manual_tests.experiments.experiment_toggle_reset_pin
'''

import sys, os, subprocess

from asmcnc.comms.logging_system.logging_system import Logger

sys.path.append('./src')
os.chdir('./src')

from kivy.config import Config
from kivy.clock import Clock
Config.set('kivy', 'keyboard_mode', 'systemanddock')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
Config.set('graphics', 'maxfps', '60')
Config.set('kivy', 'KIVY_CLOCK', 'interrupt')
Config.write()

from mock import Mock

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.lang import Builder

# COMMS IMPORTS
from asmcnc.comms import router_machine

# NB: router_machine imports serial_connection
from settings import settings_manager
from asmcnc.comms import localization
from asmcnc.job import job_data
from asmcnc.comms.yeti_grbl_protocol.c_defines import *
from asmcnc.apps.systemTools_app.screens.calibration import widget_sg_status_bar

Cmport = 'COM3'

Builder.load_string("""
<TestScreen>:

    threshold_to_set : threshold_to_set
    register_label : register_label
    status_container : status_container

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            size_hint_y: 0.92
            orientation: 'vertical'

            GridLayout:
                cols:2

                Label: 
                    id: register_label
                    text: "X1 threshold"


                Button:
                    text: "GRBL reset"
                    on_press: root.grbl_reset()

                BoxLayout: 
                    orientation: 'horizontal'
    

                    TextInput: 
                        id: threshold_to_set
                        text: ''
                        multiline: False
                        input_filter: 'int'

                    Button: 
                        text: "set"
                        on_press: root.set_threshold()

                Button: 
                    text: "Get registers"
                    on_press: root.get_registers()


                Button:
                    text: 'Serial comms off'
                    on_press: root.comms_off()


                Button:
                    text: 'Serial comms on'
                    on_press: root.comms_on()


                Button:
                    text: 'Toggle pin'
                    on_press: root.toggle_pin()

                Button:
                    text: 'Set pin mode'
                    on_press: root.set_pin_mode()
                
                Button:
                    text: 'Store params'
                    on_press: root.store_params()

                Button:
                    text: 'Test FW update W toggle'
                    on_press: root.fw_update_w_toggle()

                Button:
                    text: 'Test FW update WO toggle'
                    on_press: root.fw_update_wo_toggle()

                Button:
                    text: "Test FW update WO comms break"
                    on_press: root.fw_update_wo_comms_break()


                Button: 
                    text: "Check all"
                    on_press: root.check_all()
                Button: 
                    text: "Check ZH"
                    on_press: root.check_zh()
                Button: 
                    text: "Check Y"
                    on_press: root.check_y()




        BoxLayout:
            size_hint_y: 0.08
            id: status_container
""")

# Declare both screens
class TestScreen(Screen):

    common_move_widget = Mock()
    do_toggle = False

    def __init__(self, **kwargs):
        super(TestScreen, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']
        self.db = kwargs['db']
        self.status_container.add_widget(widget_sg_status_bar.SGStatusBar(machine=self.m, screen_manager=self.sm))

    def check_all(self): self.m.check_x_y_z_calibration()
    def check_zh(self): self.m.check_x_z_calibration()
    def check_y(self): self.m.check_y_calibration()


    def toggle_pin(self):
        self.m.toggle_reset_pin()

    def set_pin_mode(self):
        self.m.set_mode_of_reset_pin()

    def comms_off(self):
        self.m.stop_serial_comms()

    def comms_on(self):
        self.m.do_connection()

    def get_registers(self):
        self.m.tmc_handshake()
        self.update_label()

    def update_label(self):

        if self.m.TMC_registers_have_been_read_in():
            self.register_label.text = "X1 threshold: " + str(self.m.TMC_motor[TMC_X1].stallGuardAlarmThreshold)

        else: 
            Clock.schedule_once(lambda dt: self.update_label(), 1)

    def store_params(self):
        self.m.store_tmc_params_in_eeprom_and_handshake()
        self.update_label()

    def set_threshold(self):
        self.m.set_threshold_for_axis("X", self.threshold_to_set.text)

    def grbl_reset(self):
        self.m.resume_from_alarm()

    def fw_update_w_toggle(self):
        self.do_toggle = True
        self.test_fw_update()

    def fw_update_wo_toggle(self):
        self.do_toggle = False
        self.test_fw_update()

    def fw_update_wo_comms_break(self):

        cmd = "grbl_file=/home/pi/GRBL*.hex && avrdude -patmega2560 -cwiring -P/dev/ttyAMA0 -b115200 -D -Uflash:w:$(echo $grbl_file):i"
        proc = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = True)
        stdout, stderr = proc.communicate()
        exit_code = int(proc.returncode)

        if exit_code == 0: 
            did_fw_update_succeed = "Success!"

        else: 
            did_fw_update_succeed = "Update failed."

        Logger.info(did_fw_update_succeed)
        Logger.info(str(stdout))


    def test_fw_update(self):

        Logger.info("Updating")

        def disconnect_and_update():
            self.m.s.grbl_scanner_running = False
            Clock.schedule_once(self.m.close_serial_connection, 0.1)
            Clock.schedule_once(nested_do_fw_update, 1)

        def nested_do_fw_update(dt):

            if self.do_toggle: self.m.set_mode_of_reset_pin()

            cmd = "grbl_file=/home/pi/GRBL*.hex && avrdude -patmega2560 -cwiring -P/dev/ttyAMA0 -b115200 -D -Uflash:w:$(echo $grbl_file):i"
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

            Logger.info(did_fw_update_succeed)
            Logger.info(str(self.stdout))

        disconnect_and_update()





























class ScreenTest(App):

    def build(self):

        Logger.info("Starting App:")

        # Establish screens
        sm = ScreenManager(transition=NoTransition())

        # Localization/language object
        l = localization.Localization()

        # Initialise settings object
        sett = settings_manager.Settings(sm)

        # Initialise 'j'ob 'd'ata object
        jd = job_data.JobData(localization = l, settings_manager = sett)

        m = router_machine.RouterMachine(Cmport, sm, sett, l, jd)

        # Create database object to talk to
        db = Mock()

        # Alarm screens are set up in serial comms, need access to the db object
        m.s.alarm.db = db
        m.s.alarm = Mock()

        sm.add_widget(TestScreen(name='door', sm=sm, m=m, db=db))
        sm.add_widget(TestScreen(name='home', sm=sm, m=m, db=db))

        if "darwin" in sys.platform: m.s.s = Mock()
        m.s.start_services(0)

        sm.current = "door"

        return sm

ScreenTest().run()