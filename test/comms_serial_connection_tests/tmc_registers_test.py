'''
Created on 1 Feb 2022
@author: Letty
'''

try: 
    import unittest
    from mock import Mock, MagicMock
    from serial_mock.mock import MockSerial, DummySerial
    from serial_mock.decorators import serial_query

except: 
    print("Can't import mocking packages, are you on a dev machine?")

from time import sleep

import sys
sys.path.append('./src')

try:
    from asmcnc.comms import serial_connection
    from asmcnc.comms import localization

except: 
    pass

########################################################
# IMPORTANT!!
# Run from easycut-smartbench folder, with 
# python -m test.comms_serial_connection_tests.tmc_registers_test

class TMCRegisters(unittest.TestCase):

    status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822>"

    test_motor_id = 4
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

            @serial_query("?")
            def do_something(self):
                return outerSelf.status

        return YETIPCB


    def status_and_PCB_constructor(self, case=None, 
                        motor_id = 0,
                        register_DRVCTRL = 0,
                        register_CHOPCONF = 0,
                        register_SMARTEN = 0,
                        register_SGCSCONF = 0,
                        register_DRVCONF = 0,
                        active_current_scale = 0,
                        stand_still_current_scale = 0,
                        stall_guard_alarm_threshold = 0,
                        step_period_us_to_read_SG = 0,
                        gradient_per_celsius = 0):

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
        self.serial_module.s = DummySerial(self.give_me_a_PCB())
        self.serial_module.s.fd = 1 # this is needed to force it to run
        self.serial_module.start_services(1)
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

        self.serial_module = serial_connection.SerialConnection(self.m, self.sm, self.sett, self.l, self.jd)
        # self.serial_module.VERBOSE_ALL_RESPONSE = True

    def tearDown(self):
      self.serial_module.__del__()

    def test_does_serial_think_its_connected(self):
        """Test that serial module thinks it is connected"""
        self.status_and_PCB_constructor()
        assert self.serial_module.is_connected(), 'not connected'

    def test_the_mock_interface(self):
        """Test that we're getting statuses back"""
        self.status_and_PCB_constructor(1)
        assert self.serial_module.m_state == "Idle", 'not idle'

    def test_motor_id_read_in(self):
        """ 
        Test that motor id is expected value, and that serial continues to work
        This is relevant to FW between v228 onwards
        """
        self.status_and_PCB_constructor(2, motor_id = self.test_motor_id)
        self.assertEqual(self.serial_module.motor_id, self.test_motor_id), 'motor id error'
        assert self.serial_module.is_connected(), 'not connected'

    def test_register_DRVCTRL_read_in(self):
        """ 
        Test that register_DRVCTRL is expected value, and that serial continues to work
        This is relevant to FW between v228 onwards
        """
        self.status_and_PCB_constructor(2, register_DRVCTRL = self.test_register_DRVCTRL)
        self.assertEqual(self.serial_module.register_DRVCTRL, self.test_register_DRVCTRL), 'register_DRVCTRL error'
        assert self.serial_module.is_connected(), 'not connected'

    def test_register_CHOPCONF_read_in(self):
        """ 
        Test that register_CHOPCONF is expected value, and that serial continues to work
        This is relevant to FW between v228 onwards
        """
        self.status_and_PCB_constructor(2, register_CHOPCONF = self.test_register_CHOPCONF)
        self.assertEqual(self.serial_module.register_CHOPCONF, self.test_register_CHOPCONF), 'register_CHOPCONF error'
        assert self.serial_module.is_connected(), 'not connected'

    def test_register_SMARTEN_read_in(self):
        """ 
        Test that register_SMARTEN is expected value, and that serial continues to work
        This is relevant to FW between v228 onwards
        """
        self.status_and_PCB_constructor(2, register_SMARTEN = self.test_register_SMARTEN)
        self.assertEqual(self.serial_module.register_SMARTEN, self.test_register_SMARTEN), 'register_SMARTEN error'
        assert self.serial_module.is_connected(), 'not connected'

    def test_register_SGCSCONF_read_in(self):
        """ 
        Test that register_SGCSCONF is expected value, and that serial continues to work
        This is relevant to FW between v228 onwards
        """
        self.status_and_PCB_constructor(2, register_SGCSCONF = self.test_register_SGCSCONF)
        self.assertEqual(self.serial_module.register_SGCSCONF, self.test_register_SGCSCONF), 'register_SGCSCONF error'
        assert self.serial_module.is_connected(), 'not connected'

    def test_register_DRVCONF_read_in(self):
        """ 
        Test that register_DRVCONF is expected value, and that serial continues to work
        This is relevant to FW between v228 onwards
        """
        self.status_and_PCB_constructor(2, register_DRVCONF = self.test_register_DRVCONF)
        self.assertEqual(self.serial_module.register_DRVCONF, self.test_register_DRVCONF), 'register_DRVCONF error'
        assert self.serial_module.is_connected(), 'not connected'

    def test_active_current_scale_read_in(self):
        """ 
        Test that active_current_scale is expected value, and that serial continues to work
        This is relevant to FW between v228 onwards
        """
        self.status_and_PCB_constructor(2, active_current_scale = self.test_active_current_scale)
        self.assertEqual(self.serial_module.active_current_scale, self.test_active_current_scale), 'active_current_scale error'
        assert self.serial_module.is_connected(), 'not connected'

    def test_stand_still_current_scale_read_in(self):
        """ 
        Test that stand_still_current_scale is expected value, and that serial continues to work
        This is relevant to FW between v228 onwards
        """
        self.status_and_PCB_constructor(2, stand_still_current_scale = self.test_stand_still_current_scale)
        self.assertEqual(self.serial_module.stand_still_current_scale, self.test_stand_still_current_scale), 'stand_still_current_scale error'
        assert self.serial_module.is_connected(), 'not connected'


    def test_stall_guard_alarm_threshold_read_in(self):
        """ 
        Test that stall_guard_alarm_threshold is expected value, and that serial continues to work
        This is relevant to FW between v228 onwards
        """
        self.status_and_PCB_constructor(2, stall_guard_alarm_threshold = self.test_stall_guard_alarm_threshold)
        self.assertEqual(self.serial_module.stall_guard_alarm_threshold, self.test_stall_guard_alarm_threshold), 'stall_guard_alarm_threshold error'
        assert self.serial_module.is_connected(), 'not connected'

    def test_step_period_us_to_read_SG_read_in(self):
        """ 
        Test that step_period_us_to_read_SG is expected value, and that serial continues to work
        This is relevant to FW between v228 onwards
        """
        self.status_and_PCB_constructor(2, step_period_us_to_read_SG = self.test_step_period_us_to_read_SG)
        self.assertEqual(self.serial_module.step_period_us_to_read_SG, self.test_step_period_us_to_read_SG), 'step_period_us_to_read_SG error'
        assert self.serial_module.is_connected(), 'not connected'

    def test_gradient_per_celsius_read_in(self):
        """ 
        Test that gradient_per_celsius is expected value, and that serial continues to work
        This is relevant to FW between v228 onwards
        """
        self.status_and_PCB_constructor(2, gradient_per_celsius = self.test_gradient_per_celsius)
        self.assertEqual(self.serial_module.gradient_per_celsius, self.test_gradient_per_celsius), 'gradient_per_celsius error'
        assert self.serial_module.is_connected(), 'not connected'


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()