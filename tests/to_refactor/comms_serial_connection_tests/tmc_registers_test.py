'''
Created on 1 Feb 2022
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

Cmport = 'COM3'
from asmcnc.comms.yeti_grbl_protocol.c_defines import *

########################################################
# IMPORTANT!!
# Run from easycut-smartbench folder, with 
# python -m test.comms_serial_connection_tests.tmc_registers_test

class TMCRegisters(unittest.TestCase):

    status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822>"

    test_register_DRVCTRL = 516
    test_register_CHOPCONF = 602832
    test_register_SMARTEN = 688384
    test_register_SGCSCONF = 853269
    test_register_DRVCONF = 978961
    test_active_current_scale = 21
    test_stand_still_current_scale = 21
    test_stall_guard_alarm_threshold = 150
    test_step_period_us_to_read_SG = 800
    test_gradient_per_celsius = 1000

    def give_me_a_PCB(outerSelf):

        class YETIPCB(MockSerial):
            simple_queries = {
                "?": outerSelf.status,
                "\x18": ""

            }

        return YETIPCB


    def status_and_PCB_constructor(self, case=None, 
                        motor_id = None,
                        register_DRVCTRL = test_register_DRVCTRL,
                        register_CHOPCONF = test_register_CHOPCONF,
                        register_SMARTEN = test_register_SMARTEN,
                        register_SGCSCONF = test_register_SGCSCONF,
                        register_DRVCONF = test_register_DRVCONF,
                        active_current_scale = test_active_current_scale,
                        stand_still_current_scale = test_stand_still_current_scale,
                        stall_guard_alarm_threshold = test_stall_guard_alarm_threshold,
                        step_period_us_to_read_SG = test_step_period_us_to_read_SG,
                        gradient_per_celsius = test_gradient_per_celsius):

        # Use this to construct the test status passed out by mock serial object

        if case == 1 or case==None:

            self.status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822>"

        elif case == 2:

            # <Run|MPos:-692.704,-2142.446,-39.392|Bf:0,121|FS:6060,0|Pn:G|SG:-12,-20,15,46,-2>

            self.status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|TREG:" + \
                    str(motor_id) + "," + \
                    str(register_DRVCTRL) + "," + \
                    str(register_CHOPCONF) + "," + \
                    str(register_SMARTEN) + "," + \
                    str(register_SGCSCONF) + "," + \
                    str(register_DRVCONF) + "," + \
                    str(active_current_scale) + "," + \
                    str(stand_still_current_scale) + "," + \
                    str(stall_guard_alarm_threshold) + "," + \
                    str(step_period_us_to_read_SG) + "," + \
                    str(gradient_per_celsius) + ">"

        # Need to construct mock PCB after the status, otherwise it'll run something else:
        
        self.m.s.s = DummySerial(self.give_me_a_PCB())
        self.m.s.s.fd = 1 # this is needed to force it to run
        self.m.s.start_services(1)
        sleep(0.01)

    def setUp(self):
        # If the set_up method raises an exception while the test is running, 
        # the framework will consider the test to have suffered an error, 
        # and the runTest (or test_X_Name) method will not be executed.

        self.m = Mock()
        self.sm = Mock()
        self.sett = Mock()
        self.l = localization.Localization()
        self.jd = Mock()

        self.m = router_machine.RouterMachine(Cmport, self.sm, self.sett, self.l, self.jd)

    def tearDown(self):
      self.m.s.__del__()

    def test_does_serial_think_its_connected(self):
        """Test that serial module thinks it is connected"""
        self.status_and_PCB_constructor()
        assert self.m.s.is_connected(), 'not connected'

    def test_the_mock_interface(self):
        """Test that we're getting statuses back"""
        self.status_and_PCB_constructor(1)
        assert self.m.s.m_state == "Idle", 'not idle'

    def test_motor_x1(self):
        """ 
        Test that motor registers are expected value for x1, and that serial continues to work
        This is relevant to FW between v228 onwards
        """
        self.status_and_PCB_constructor(case=2, motor_id = 0)
        self.assertEqual(self.m.TMC_motor[TMC_X1].index, TMC_X1), 'x1 motor id error'
        self.assertEqual(self.m.TMC_motor[TMC_X1].shadowRegisters[0], self.test_register_DRVCTRL), 'x1 test_register_DRVCTRL error'
        self.assertEqual(self.m.TMC_motor[TMC_X1].shadowRegisters[1], self.test_register_CHOPCONF), 'x1 test_register_CHOPCONF error'
        self.assertEqual(self.m.TMC_motor[TMC_X1].shadowRegisters[2], self.test_register_SMARTEN), 'x1 test_register_SMARTEN error'
        self.assertEqual(self.m.TMC_motor[TMC_X1].shadowRegisters[3], self.test_register_SGCSCONF), 'x1 test_register_SGCSCONF error'
        self.assertEqual(self.m.TMC_motor[TMC_X1].shadowRegisters[4], self.test_register_DRVCONF), 'x1 test_register_DRVCONF error'
        self.assertEqual(self.m.TMC_motor[TMC_X1].ActiveCurrentScale, self.test_active_current_scale), 'x1 test_active_current_scale error'
        self.assertEqual(self.m.TMC_motor[TMC_X1].standStillCurrentScale, self.test_stand_still_current_scale), 'x1 test_stand_still_current_scale error'
        self.assertEqual(self.m.TMC_motor[TMC_X1].stallGuardAlarmThreshold, self.test_stall_guard_alarm_threshold), 'x1 test_stall_guard_alarm_threshold error'
        self.assertEqual(self.m.TMC_motor[TMC_X1].max_step_period_us_SG, self.test_step_period_us_to_read_SG), 'x1 test_step_period_us_to_read_SG error'
        self.assertEqual(self.m.TMC_motor[TMC_X1].temperatureCoefficient, self.test_gradient_per_celsius), 'x1 test_gradient_per_celsius error'
        self.assertEqual(self.m.TMC_motor[TMC_X1].got_registers, True), 'not got registers!'

        assert self.m.s.is_connected(), 'not connected'

    def test_motor_x2(self):
        """ 
        Test that motor registers are expected value for x2, and that serial continues to work
        This is relevant to FW between v228 onwards
        """
        self.status_and_PCB_constructor(case=2, motor_id = 1)
        self.assertEqual(self.m.TMC_motor[TMC_X2].index, TMC_X2), 'x2 motor id error'
        self.assertEqual(self.m.TMC_motor[TMC_X2].shadowRegisters[0], self.test_register_DRVCTRL), 'x2 test_register_DRVCTRL error'
        self.assertEqual(self.m.TMC_motor[TMC_X2].shadowRegisters[1], self.test_register_CHOPCONF), 'x2 test_register_CHOPCONF error'
        self.assertEqual(self.m.TMC_motor[TMC_X2].shadowRegisters[2], self.test_register_SMARTEN), 'x2 test_register_SMARTEN error'
        self.assertEqual(self.m.TMC_motor[TMC_X2].shadowRegisters[3], self.test_register_SGCSCONF), 'x2 test_register_SGCSCONF error'
        self.assertEqual(self.m.TMC_motor[TMC_X2].shadowRegisters[4], self.test_register_DRVCONF), 'x2 test_register_DRVCONF error'
        self.assertEqual(self.m.TMC_motor[TMC_X2].ActiveCurrentScale, self.test_active_current_scale), 'x2 test_active_current_scale error'
        self.assertEqual(self.m.TMC_motor[TMC_X2].standStillCurrentScale, self.test_stand_still_current_scale), 'x2 test_stand_still_current_scale error'
        self.assertEqual(self.m.TMC_motor[TMC_X2].stallGuardAlarmThreshold, self.test_stall_guard_alarm_threshold), 'x2 test_stall_guard_alarm_threshold error'
        self.assertEqual(self.m.TMC_motor[TMC_X2].max_step_period_us_SG, self.test_step_period_us_to_read_SG), 'x2 test_step_period_us_to_read_SG error'
        self.assertEqual(self.m.TMC_motor[TMC_X2].temperatureCoefficient, self.test_gradient_per_celsius), 'x2 test_gradient_per_celsius error'
        self.assertEqual(self.m.TMC_motor[TMC_X2].got_registers, True), 'not got registers!'
        assert self.m.s.is_connected(), 'not connected'

    def test_motor_y1(self):
        """ 
        Test that motor id is expected value for y1, and that serial continues to work
        This is relevant to FW between v228 onwards
        """
        self.status_and_PCB_constructor(case=2, motor_id = 2)
        self.assertEqual(self.m.TMC_motor[TMC_Y1].index, TMC_Y1), 'y1 motor id error'
        self.assertEqual(self.m.TMC_motor[TMC_Y1].shadowRegisters[0], self.test_register_DRVCTRL), 'y1 test_register_DRVCTRL error'
        self.assertEqual(self.m.TMC_motor[TMC_Y1].shadowRegisters[1], self.test_register_CHOPCONF), 'y1 test_register_CHOPCONF error'
        self.assertEqual(self.m.TMC_motor[TMC_Y1].shadowRegisters[2], self.test_register_SMARTEN), 'y1 test_register_SMARTEN error'
        self.assertEqual(self.m.TMC_motor[TMC_Y1].shadowRegisters[3], self.test_register_SGCSCONF), 'y1 test_register_SGCSCONF error'
        self.assertEqual(self.m.TMC_motor[TMC_Y1].shadowRegisters[4], self.test_register_DRVCONF), 'y1 test_register_DRVCONF error'
        self.assertEqual(self.m.TMC_motor[TMC_Y1].ActiveCurrentScale, self.test_active_current_scale), 'y1 test_active_current_scale error'
        self.assertEqual(self.m.TMC_motor[TMC_Y1].standStillCurrentScale, self.test_stand_still_current_scale), 'y1 test_stand_still_current_scale error'
        self.assertEqual(self.m.TMC_motor[TMC_Y1].stallGuardAlarmThreshold, self.test_stall_guard_alarm_threshold), 'y1 test_stall_guard_alarm_threshold error'
        self.assertEqual(self.m.TMC_motor[TMC_Y1].max_step_period_us_SG, self.test_step_period_us_to_read_SG), 'y1 test_step_period_us_to_read_SG error'
        self.assertEqual(self.m.TMC_motor[TMC_Y1].temperatureCoefficient, self.test_gradient_per_celsius), 'y1 test_gradient_per_celsius error'
        self.assertEqual(self.m.TMC_motor[TMC_Y1].got_registers, True), 'not got registers!'
        assert self.m.s.is_connected(), 'not connected'

    def test_motor_y2(self):
        """ 
        Test that motor id is expected value for y2, and that serial continues to work
        This is relevant to FW between v228 onwards
        """
        self.status_and_PCB_constructor(case=2, motor_id = 3)
        self.assertEqual(self.m.TMC_motor[TMC_Y2].index, TMC_Y2), 'y2 motor id error'
        self.assertEqual(self.m.TMC_motor[TMC_Y2].shadowRegisters[0], self.test_register_DRVCTRL), 'x1 test_register_DRVCTRL error'
        self.assertEqual(self.m.TMC_motor[TMC_Y2].shadowRegisters[1], self.test_register_CHOPCONF), 'x1 test_register_CHOPCONF error'
        self.assertEqual(self.m.TMC_motor[TMC_Y2].shadowRegisters[2], self.test_register_SMARTEN), 'x1 test_register_SMARTEN error'
        self.assertEqual(self.m.TMC_motor[TMC_Y2].shadowRegisters[3], self.test_register_SGCSCONF), 'x1 test_register_SGCSCONF error'
        self.assertEqual(self.m.TMC_motor[TMC_Y2].shadowRegisters[4], self.test_register_DRVCONF), 'x1 test_register_DRVCONF error'
        self.assertEqual(self.m.TMC_motor[TMC_Y2].ActiveCurrentScale, self.test_active_current_scale), 'x1 test_active_current_scale error'
        self.assertEqual(self.m.TMC_motor[TMC_Y2].standStillCurrentScale, self.test_stand_still_current_scale), 'x1 test_stand_still_current_scale error'
        self.assertEqual(self.m.TMC_motor[TMC_Y2].stallGuardAlarmThreshold, self.test_stall_guard_alarm_threshold), 'x1 test_stall_guard_alarm_threshold error'
        self.assertEqual(self.m.TMC_motor[TMC_Y2].max_step_period_us_SG, self.test_step_period_us_to_read_SG), 'x1 test_step_period_us_to_read_SG error'
        self.assertEqual(self.m.TMC_motor[TMC_Y2].temperatureCoefficient, self.test_gradient_per_celsius), 'x1 test_gradient_per_celsius error'
        self.assertEqual(self.m.TMC_motor[TMC_Y2].got_registers, True), 'not got registers!'
        assert self.m.s.is_connected(), 'not connected'

    def test_motor_z(self):
        """ 
        Test that motor id is expected value for z, and that serial continues to work
        This is relevant to FW between v228 onwards
        """
        self.status_and_PCB_constructor(case=2, motor_id = 4)
        self.assertEqual(self.m.TMC_motor[TMC_Z].index, TMC_Z), 'z motor id error'
        self.assertEqual(self.m.TMC_motor[TMC_Z].shadowRegisters[0], self.test_register_DRVCTRL), 'x1 test_register_DRVCTRL error'
        self.assertEqual(self.m.TMC_motor[TMC_Z].shadowRegisters[1], self.test_register_CHOPCONF), 'x1 test_register_CHOPCONF error'
        self.assertEqual(self.m.TMC_motor[TMC_Z].shadowRegisters[2], self.test_register_SMARTEN), 'x1 test_register_SMARTEN error'
        self.assertEqual(self.m.TMC_motor[TMC_Z].shadowRegisters[3], self.test_register_SGCSCONF), 'x1 test_register_SGCSCONF error'
        self.assertEqual(self.m.TMC_motor[TMC_Z].shadowRegisters[4], self.test_register_DRVCONF), 'x1 test_register_DRVCONF error'
        self.assertEqual(self.m.TMC_motor[TMC_Z].ActiveCurrentScale, self.test_active_current_scale), 'x1 test_active_current_scale error'
        self.assertEqual(self.m.TMC_motor[TMC_Z].standStillCurrentScale, self.test_stand_still_current_scale), 'x1 test_stand_still_current_scale error'
        self.assertEqual(self.m.TMC_motor[TMC_Z].stallGuardAlarmThreshold, self.test_stall_guard_alarm_threshold), 'x1 test_stall_guard_alarm_threshold error'
        self.assertEqual(self.m.TMC_motor[TMC_Z].max_step_period_us_SG, self.test_step_period_us_to_read_SG), 'x1 test_step_period_us_to_read_SG error'
        self.assertEqual(self.m.TMC_motor[TMC_Z].temperatureCoefficient, self.test_gradient_per_celsius), 'x1 test_gradient_per_celsius error'
        self.assertEqual(self.m.TMC_motor[TMC_Z].got_registers, True), 'not got registers!'
        assert self.m.s.is_connected(), 'not connected'

    # def test_register_DRVCTRL_read_in(self):
    #     """ 
    #     Test that register_DRVCTRL is expected value, and that serial continues to work
    #     This is relevant to FW between v228 onwards
    #     """
    #     self.status_and_PCB_constructor(2, register_DRVCTRL = self.test_register_DRVCTRL)
    #     self.assertEqual(self.serial_module.register_DRVCTRL, self.test_register_DRVCTRL), 'register_DRVCTRL error'
    #     assert self.serial_module.is_connected(), 'not connected'

    # def test_register_CHOPCONF_read_in(self):
    #     """ 
    #     Test that register_CHOPCONF is expected value, and that serial continues to work
    #     This is relevant to FW between v228 onwards
    #     """
    #     self.status_and_PCB_constructor(2, register_CHOPCONF = self.test_register_CHOPCONF)
    #     self.assertEqual(self.serial_module.register_CHOPCONF, self.test_register_CHOPCONF), 'register_CHOPCONF error'
    #     assert self.serial_module.is_connected(), 'not connected'

    # def test_register_SMARTEN_read_in(self):
    #     """ 
    #     Test that register_SMARTEN is expected value, and that serial continues to work
    #     This is relevant to FW between v228 onwards
    #     """
    #     self.status_and_PCB_constructor(2, register_SMARTEN = self.test_register_SMARTEN)
    #     self.assertEqual(self.serial_module.register_SMARTEN, self.test_register_SMARTEN), 'register_SMARTEN error'
    #     assert self.serial_module.is_connected(), 'not connected'

    # def test_register_SGCSCONF_read_in(self):
    #     """ 
    #     Test that register_SGCSCONF is expected value, and that serial continues to work
    #     This is relevant to FW between v228 onwards
    #     """
    #     self.status_and_PCB_constructor(2, register_SGCSCONF = self.test_register_SGCSCONF)
    #     self.assertEqual(self.serial_module.register_SGCSCONF, self.test_register_SGCSCONF), 'register_SGCSCONF error'
    #     assert self.serial_module.is_connected(), 'not connected'

    # def test_register_DRVCONF_read_in(self):
    #     """ 
    #     Test that register_DRVCONF is expected value, and that serial continues to work
    #     This is relevant to FW between v228 onwards
    #     """
    #     self.status_and_PCB_constructor(2, register_DRVCONF = self.test_register_DRVCONF)
    #     self.assertEqual(self.serial_module.register_DRVCONF, self.test_register_DRVCONF), 'register_DRVCONF error'
    #     assert self.serial_module.is_connected(), 'not connected'

    # def test_active_current_scale_read_in(self):
    #     """ 
    #     Test that active_current_scale is expected value, and that serial continues to work
    #     This is relevant to FW between v228 onwards
    #     """
    #     self.status_and_PCB_constructor(2, active_current_scale = self.test_active_current_scale)
    #     self.assertEqual(self.serial_module.active_current_scale, self.test_active_current_scale), 'active_current_scale error'
    #     assert self.serial_module.is_connected(), 'not connected'

    # def test_stand_still_current_scale_read_in(self):
    #     """ 
    #     Test that stand_still_current_scale is expected value, and that serial continues to work
    #     This is relevant to FW between v228 onwards
    #     """
    #     self.status_and_PCB_constructor(2, stand_still_current_scale = self.test_stand_still_current_scale)
    #     self.assertEqual(self.serial_module.stand_still_current_scale, self.test_stand_still_current_scale), 'stand_still_current_scale error'
    #     assert self.serial_module.is_connected(), 'not connected'


    # def test_stall_guard_alarm_threshold_read_in(self):
    #     """ 
    #     Test that stall_guard_alarm_threshold is expected value, and that serial continues to work
    #     This is relevant to FW between v228 onwards
    #     """
    #     self.status_and_PCB_constructor(2, stall_guard_alarm_threshold = self.test_stall_guard_alarm_threshold)
    #     self.assertEqual(self.serial_module.stall_guard_alarm_threshold, self.test_stall_guard_alarm_threshold), 'stall_guard_alarm_threshold error'
    #     assert self.serial_module.is_connected(), 'not connected'

    # def test_step_period_us_to_read_SG_read_in(self):
    #     """ 
    #     Test that step_period_us_to_read_SG is expected value, and that serial continues to work
    #     This is relevant to FW between v228 onwards
    #     """
    #     self.status_and_PCB_constructor(2, step_period_us_to_read_SG = self.test_step_period_us_to_read_SG)
    #     self.assertEqual(self.serial_module.step_period_us_to_read_SG, self.test_step_period_us_to_read_SG), 'step_period_us_to_read_SG error'
    #     assert self.serial_module.is_connected(), 'not connected'

    # def test_gradient_per_celsius_read_in(self):
    #     """ 
    #     Test that gradient_per_celsius is expected value, and that serial continues to work
    #     This is relevant to FW between v228 onwards
    #     """
    #     self.status_and_PCB_constructor(2, gradient_per_celsius = self.test_gradient_per_celsius)
    #     self.assertEqual(self.serial_module.gradient_per_celsius, self.test_gradient_per_celsius), 'gradient_per_celsius error'
    #     assert self.serial_module.is_connected(), 'not connected'


if __name__ == "__main__":
    #import sys;sys.argv = get('', 'Test.)estName']
    unittest.main()