'''
Created on 14 Feb 2022
@author: Letty
'''
from asmcnc.comms.logging_system.logging_system import Logger

try: 
    import unittest
    from mock import Mock, MagicMock
    from serial_mock.mock import MockSerial, DummySerial
    from serial_mock.decorators import serial_query

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


########################################################
# IMPORTANT!!
# Run from easycut-smartbench folder, with 
# python -m test.protocol_tests.send_motor_commands_test

Cmport = 'COM3'

class MotorCommandsTest(unittest.TestCase):

    status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822>"
    fw_version = '2.3.1'

    def give_me_a_PCB(outerSelf):

        class YETIPCB(MockSerial):
            simple_queries = {
                "$I":"[ASM CNC; SW Ver:"+outerSelf.fw_version+";HW Ver:32]",
                "?": outerSelf.status,
                "\x18": ""

            }

        return YETIPCB

    def status_and_PCB_constructor(self, ver='2.3.1'):

        self.fw_version = ver
        self.m = router_machine.RouterMachine(Cmport, self.sm, self.sett, self.l, self.jd)
        self.m.s.s = DummySerial(self.give_me_a_PCB())
        self.m.s.s.fd = 1 # this is needed to force it to run
        self.m.s.fw_version = ver
        self.m.s.start_services(1)
        sleep(0.02)

    def setUp(self):
        # If the set_up method raises an exception while the test is running, 
        # the framework will consider the test to have suffered an error, 
        # and the runTest (or test_X_Name) method will not be executed.

        self.sm = Mock()
        self.sett = Mock()
        self.sett.ip_address = ''
        self.l = localization.Localization()
        self.jd = Mock()

    def tearDown(self):
      self.m.s.__del__()

    def test_does_serial_think_its_connected(self):
        """Test that serial module thinks it is connected"""
        self.status_and_PCB_constructor()
        assert self.m.s.is_connected(), 'not connected'

    def test_the_mock_interface(self):
        """Test that we're getting statuses back"""
        self.status_and_PCB_constructor()
        assert self.m.s.m_state == "Idle", 'not idle'


    # def test_tmc_handshake_with_old_fw(self):
    #     """Test handshake with old FW"""
    #     self.status_and_PCB_constructor(ver='1.1.2')
    #     self.m.tmc_handshake()


    # def test_tmc_handshake_with_new_fw(self):
    #     """Test handshake with new FW"""
    #     self.status_and_PCB_constructor(ver='2.3.1')
    #     self.m.tmc_handshake()


    def test_tmc_handshake_with_no_fw(self):
        """Test handshake with no FW"""
        self.status_and_PCB_constructor(ver='')
        self.m.tmc_handshake()


    # def test_fw_check(self):
    #     """Test handshake with no FW"""
    #     self.status_and_PCB_constructor(ver='2.3.1')
    #     Logger.info("FW VERSION: " + self.m.s.fw_version)
    #     self.assertEqual(self.m.is_machines_fw_version_equal_to_or_greater_than_version('2.2.8', "just checkin"), True)

if __name__ == "__main__":
    #import sys;sys.argv = get('', 'Test.)estName']
    unittest.main()
