 # -*- coding: utf-8 -*-

from kivy.config import Config
from kivy.clock import Clock
Config.set('kivy', 'keyboard_mode', 'systemanddock')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
Config.set('graphics', 'maxfps', '60')
Config.set('kivy', 'KIVY_CLOCK', 'interrupt')
Config.write()


########################################################
# IMPORTANT!!
# Run from easycut-smartbench folder, with 
# python -m test.screen_tests.alarm_screen_tests

# Would be good to make this more of a unit test system

import sys, os
sys.path.append('./src')
os.chdir('./src')

import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from asmcnc.comms import localization
from asmcnc.comms import router_machine
from settings import settings_manager
from asmcnc.skavaUI import screen_home

try: 
    from mock import Mock, MagicMock
    from serial_mock.mock import MockSerial, DummySerial
    from random import randint

except: 
    pass


from asmcnc.comms.yeti_grbl_protocol.c_defines import *

Cmport = 'COM3'

class ScreenTest(App):

    lang_idx = 0
    
    fw_version = "2.4.2"
    alarm_pin = "Y"

    stall_pin = "YSz"
    motor_id = 0
    step_size = 75
    sg_val = 151
    thresh = 150
    distance = 42103020
    x_coord = -1084.997
    y_coord = -2487.003
    z_coord = -99.954


    alarm_message = "ALARM:1\n"

    status = "<Alarm|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:" + alarm_pin + "|WCO:-166.126,-213.609,-21.822|SG:-999,-20,15,-20,-2>"
    sg_alarm_status = "<Alarm|MPos:-685.008,-2487.003,-100.752|Bf:34,255|FS:0,0|Pn:G" + \
        stall_pin + \
        "|SGALARM:" + \
        str(motor_id) + "," + \
        str(step_size) + "," + \
        str(sg_val) + "," + \
        str(thresh) + "," + \
        str(distance) + "," + \
        str(x_coord) + "," + \
        str(y_coord) + "," + \
        str(z_coord) + ">\n"

    def give_status(self):

        status = self.sg_alarm_status
        # status = self.status
        return status

    def give_me_a_PCB(outerSelf):

        class YETIPCB(MockSerial):
            simple_queries = {
                "?": outerSelf.give_status(),
                "\x18": "",
                "*LFFFF00": "ok",
                "$$": outerSelf.alarm_message
            }

        return YETIPCB

    def build(self):

        # Establish screens
        sm = ScreenManager(transition=NoTransition())

        systemtools_sm = Mock()
        systemtools_sm.sm = sm

        # Localization/language object
        l = localization.Localization()
        l.load_in_new_language(l.approved_languages[self.lang_idx])

        # Initialise settings object
        sett = settings_manager.Settings(sm)
        # sett.ip_address = ''

        # Initialise 'j'ob 'd'ata object
        jd = Mock()
        jd.job_name = ""
        jd.gcode_summary_string = ""

        # Initialise 'm'achine object
        m = router_machine.RouterMachine(Cmport, sm, sett, l, jd)

        m.s.s = DummySerial(self.give_me_a_PCB())
        m.s.s.fd = 1 # this is needed to force it to run
        m.s.fw_version = self.fw_version

        home_screen = screen_home.HomeScreen(name='home', screen_manager = sm, machine = m, job = jd, settings = sett, localization = l)
        sm.add_widget(home_screen)
        sm.current = 'home'
        
        Clock.schedule_once(m.s.start_services, 0.1)

        return sm

ScreenTest().run()