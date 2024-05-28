import logging
"""
Created on 15 Feb 2022
@author: Letty
"""
from asmcnc.comms.logging_system.logging_system import Logger
try:
    import unittest
    from mock import Mock, MagicMock
    from serial_mock.mock import MockSerial, DummySerial
    from serial_mock.decorators import serial_query
    from random import randint
except:
    Logger.info("Can't import mocking packages, are you on a dev machine?")
from time import sleep
import sys
sys.path.append('./src')
try:
    from asmcnc.comms import router_machine
    from asmcnc.comms import localization
except:
    pass
from asmcnc.comms.yeti_grbl_protocol.c_defines import *
Cmport = 'COM3'


class MotorCommandsTest(unittest.TestCase):
    sg_values = [-12, -20, 15, 46, -2]
    normalized_SGs = (
        '<Run|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822|SG:-12,-20,15,-999,-2>'
        )
    raw_SGs = (
        '<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822|SG:500,500,500,500,500>'
        )
    temp_to_test_against = 45
    tuning_array_to_test = None
    status = normalized_SGs

    def give_status(self):
        if randint(0, 1) == 0:
            status = (
                '<Run|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822|SG:-999,-20,15,-20,-2>'
                )
        else:
            status = (
                '<Run|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822|SG:-999,-16,-15,-20,-2>'
                )
        return status
    test_arr = [[[832, 1023, -999, 1023, 1023], [838, 1023, -999, 1023, 
        1023], [841, 1023, -999, 1023, 1023], [847, 1023, -999, 1023, 1023],
        [846, 1023, -999, 1023, 1023], [843, 1023, -999, 1023, 1023], [829,
        1023, -999, 1023, 1023], [830, 1023, -999, 1023, 1023]] * 11] * 21

    def give_me_a_PCB(outerSelf):


        class YETIPCB(MockSerial):
            simple_queries = {'?': outerSelf.give_status(), '\x18': ''}
        return YETIPCB

    def setUp(self):
        self.sm = Mock()
        self.sett = Mock()
        self.sett.ip_address = ''
        self.l = localization.Localization()
        self.jd = Mock()
        self.m = router_machine.RouterMachine(Cmport, self.sm, self.sett,
            self.l, self.jd)
        self.m.s.s = DummySerial(self.give_me_a_PCB())
        self.m.s.s.fd = 1
        self.m.s.start_services(1)
        self.m.s.motor_driver_temp = self.temp_to_test_against
        sleep(0.01)

    def tearDown(self):
        self.m.s.__del__()

    def test_are_sg_values_in_range_after_calibration(self):
        self.m.temp_sg_array = []
        self.m.s.record_sg_values_flag = True
        sleep(3)
        self.m.s.record_sg_values_flag = False
        self.m.are_sg_values_in_range_after_calibration(['X', 'Y', 'Z'])
        Logger.info(self.m.checking_calibration_fail_info)
        assert self.m.checking_calibration_fail_info.startswith(
            'All values -999 for idx: 0')


if __name__ == '__main__':
    unittest.main()
