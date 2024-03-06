'''
Created on 4 Mar 2022
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
# python -m test.protocol_tests.tmc_motor_objects_test

Cmport = 'COM3'

class MotorCommandsTest(unittest.TestCase):

    status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822>"
    fw_version = '2.3.1'

    TMC_X1                = 0
    TMC_X2                = 1
    TMC_Y1                = 2
    TMC_Y2                = 3
    TMC_Z                 = 4

    status_idx_0          = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:GrxXyZ|Ld:0|TREG:0,10,20,30,40,50,60,70,80,90,100>\n"
    status_idx_1          = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:GrxXyZ|Ld:0|TREG:1,11,21,31,41,51,61,71,81,91,101>\n"
    status_idx_2          = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:GrxXyZ|Ld:0|TREG:2,12,22,32,42,52,62,72,82,92,102>\n"
    status_idx_3          = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:GrxXyZ|Ld:0|TREG:3,13,23,33,43,53,63,73,83,93,103>\n"
    status_idx_4          = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:GrxXyZ|Ld:0|TREG:4,14,24,34,44,54,64,74,84,94,104>\n"


    def give_me_a_PCB(outerSelf):

        class YETIPCB(MockSerial):
            simple_queries = {
                "?": '',
                "\x18": "",
                "request registers 0": outerSelf.status_idx_0,
                "request registers 1": outerSelf.status_idx_1,
                "request registers 2": outerSelf.status_idx_2,
                "request registers 3": outerSelf.status_idx_3,
                "request registers 4": outerSelf.status_idx_4
            }

            # @serial_query("request registers")
            # def do_something(self, motor_id):

            #     if motor_id == "0": 
            #         return outerSelf.status_idx_0

            #     if motor_id == "1": 
            #         return outerSelf.status_idx_1

            #     if motor_id == "2": 
            #         return outerSelf.status_idx_2

            #     if motor_id == "3": 
            #         return outerSelf.status_idx_3

            #     if motor_id == "4": 
            #         return outerSelf.status_idx_4

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

    # def test_does_serial_think_its_connected(self):
    #     """Test that serial module thinks it is connected"""
    #     self.status_and_PCB_constructor()
    #     assert self.m.s.is_connected(), 'not connected'

    # def test_the_mock_interface(self):
    #     """Test that we're getting statuses back"""
    #     self.status_and_PCB_constructor()
    #     assert self.m.s.m_state == "Idle", 'not idle'

    def test_printing_tmc_registers(self):
        self.status_and_PCB_constructor()

        assert self.m.TMC_motor[1].got_registers == False

        self.m.s.write_command("request registers 0")
        sleep(0.01)
        self.m.s.write_command("request registers 1")
        sleep(0.01)
        self.m.s.write_command("request registers 2")
        sleep(0.01)
        self.m.s.write_command("request registers 3")
        sleep(0.01)
        self.m.s.write_command("request registers 4")
        sleep(0.01)

        self.m.print_tmc_registers(0)
        self.m.print_tmc_registers(1)
        self.m.print_tmc_registers(2)
        self.m.print_tmc_registers(3)
        self.m.print_tmc_registers(4)

        assert self.m.TMC_motor[1].got_registers == True

if __name__ == "__main__":
    #import sys;sys.argv = get('', 'Test.)estName']
    unittest.main()