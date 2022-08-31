 # -*- coding: utf-8 -*-

'''
########################################################
IMPORTANT!!
Run from easycut-smartbench folder, with 
python -m tests.manual_tests.experiments.experiment_toggle_reset_pin
'''

import sys, os
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

import unittest
from mock import Mock, MagicMock, patch


import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from asmcnc.comms import localization
from kivy.lang import Builder

# COMMS IMPORTS
from asmcnc.comms import router_machine  # @UnresolvedImport
from asmcnc.comms import server_connection
from asmcnc.comms import smartbench_flurry_database_connection

# NB: router_machine imports serial_connection
from asmcnc.apps import app_manager # @UnresolvedImport
from settings import settings_manager # @UnresolvedImport
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
                    text: 'Store params'
                    on_press: root.store_params()

        BoxLayout:
            size_hint_y: 0.08
            id: status_container
""")

# Declare both screens
class TestScreen(Screen):

    def __init__(self, **kwargs):

        super(TestScreen, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']
        self.db = kwargs['db']
        self.status_container.add_widget(widget_sg_status_bar.SGStatusBar(machine=self.m, screen_manager=self.sm))

    def toggle_pin(self):
        self.m.toggle_reset_pin()

    def comms_off(self):
        self.m.stop_serial_comms()

    def comms_on(self):
        self.m.reconnect_serial_connection()

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

class ScreenTest(App):

    def build(self):

        print("Starting App:")

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