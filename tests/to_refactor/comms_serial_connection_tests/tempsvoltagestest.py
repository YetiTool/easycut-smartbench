'''
Created on 25 Jan 2022
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
    from asmcnc.comms import serial_connection
    from asmcnc.comms import localization

except: 
    pass

########################################################
# IMPORTANT!!
# Run from easycut-smartbench folder, with 
# python -m test.comms_serial_connection_tests.tempsvoltagestest


##########################################################

#  PLAN THE TEST:
#  
#  >>> GIVEN:
#    1    GIVEN serial comms module is connected serial object connected to FW < 1.3.6 (no voltages or temps)
#    2    GIVEN serial comms module is connected serial object connected to 2.2.8 > FW > 1.3.6 (2 temps and all voltages)
#    3    GIVEN serial comms module is connected serial object connected to FW >= 2.2.8 (3 temps and all voltages)

#  >>> WHEN:
#    *    WHEN serial comms module reads in a status containing any number of temps or voltages
#  

#  >>> THEN:
#    *    THEN the serial comms module parses the status into corresponding variables in the serial comms module

##########################################################

# NEXT STEPS:


"""
- set up status constructor to take in temps/voltages, and a version, then can assert whether these come back out the other end 
"""


# class ParametrizedTestCase(unittest.TestCase):
#     """ TestCase classes that want to be parametrized should
#         inherit from this class.
#     """
#     def __init__(self, methodName='runTest', param=None):
#         super(ParametrizedTestCase, self).__init__(methodName)
#         self.param = param

#     @staticmethod
#     def parametrize(testcase_klass, param=None):
#         """ Create a suite containing all tests taken from the given
#             subclass, passing them the parameter 'param'.
#         """
#         testloader = unittest.TestLoader()
#         testnames = testloader.getTestCaseNames(testcase_klass)
#         suite = unittest.TestSuite()
#         for name in testnames:
#             suite.addTest(testcase_klass(name, param=param))
#         return suite


class TempsVoltagesTest(unittest.TestCase):

    status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822>"

    param = None

    case_107_112 = 1
    case_136_140 = 2
    case_228_NOW = 3

    t_pcb_temp = 20
    t_motor_driver_temp = 38
    t_transistor_heatsink_temp = 32
    t_microcontroller_mV = 5068
    t_LED_mV = 3000
    t_PSU_mV = 20242
    t_spindle_speed_monitor_mV = 1050

    def give_me_a_PCB(outerSelf):

        class YETIPCB(MockSerial):

            @serial_query("?")
            def do_something(self):
                return outerSelf.status

        return YETIPCB


    def status_and_PCB_constructor(self, case=None, 
                        pcb_temp=0,
                        motor_driver_temp=0,
                        transistor_heatsink_temp=0,
                        microcontroller_mV=0,
                        LED_mV=0,
                        PSU_mV=0,
                        spindle_speed_monitor_mV=0
                        ):

        # Use this to construct the test status passed out by mock serial object

        if case == 1 or case==None:

            self.status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822>"

        elif case == 2:

            self.status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Ld:0|TC:" + \
                str(motor_driver_temp) + "," + \
                str(pcb_temp) + "|V:" + \
                str(microcontroller_mV) + "," + \
                str(LED_mV) + "," + \
                str(PSU_mV) + "," + \
                str(spindle_speed_monitor_mV) + ">"

        elif case == 3:

            self.status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Ld:0|TC:" + \
                str(motor_driver_temp) + "," + \
                str(pcb_temp) + "," + \
                str(transistor_heatsink_temp) + "|V:" + \
                str(microcontroller_mV) + "," + \
                str(LED_mV) + "," + \
                str(PSU_mV) + "," + \
                str(spindle_speed_monitor_mV) + ">"


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


    ## CASE 1 TESTS:
    def test_pcb_temperature_case_107_112(self):
        """ 
        Test that PCB temperature is None, but that serial continues to work
        This is relevant to FW between v107 and v112
        """
        self.status_and_PCB_constructor(self.case_107_112)
        self.assertEqual(self.serial_module.pcb_temp, None), 'pcb temp error, case 1'
        assert self.serial_module.is_connected(), 'not connected'


    def test_motor_driver_temperature_case_107_112(self):
        """ 
        Test that motor driver temperature is None, but that serial continues to work
        This is relevant to FW between v107 and v112
        """
        self.status_and_PCB_constructor(self.case_107_112)
        self.assertEqual(self.serial_module.motor_driver_temp, None), 'motor_driver temp error, case 1'
        assert self.serial_module.is_connected(), 'not connected'

    def test_transistor_heatsink_temperature_case_107_112(self):
        """ 
        Test that transistor heatsink temperature is None, but that serial continues to work
        This is relevant to FW between v107 and v112
        """
        self.status_and_PCB_constructor(self.case_107_112)
        self.assertEqual(self.serial_module.transistor_heatsink_temp, None), 'transistor heatsink temp error, case 1'
        assert self.serial_module.is_connected(), 'not connected'

    def test_microcontroller_voltage_case_107_112(self):
        """ 
        Test that microcontroller voltage is None, but that serial continues to work
        This is relevant to FW between v107 and v112
        """
        self.status_and_PCB_constructor(self.case_107_112)
        self.assertEqual(self.serial_module.microcontroller_mV, None), 'microcontroller voltage error, case 1'
        assert self.serial_module.is_connected(), 'not connected'

    def test_LED_voltage_case_107_112(self):
        """ 
        Test that LED voltage is None, but that serial continues to work
        This is relevant to FW between v107 and v112
        """
        self.status_and_PCB_constructor(self.case_107_112)
        self.assertEqual(self.serial_module.LED_mV, None), 'LED voltage error, case 1'
        assert self.serial_module.is_connected(), 'not connected'

    def test_PSU_voltage_case_107_112(self):
        """ 
        Test that PSU voltage is None, but that serial continues to work
        This is relevant to FW between v107 and v112
        """
        self.status_and_PCB_constructor(self.case_107_112)
        self.assertEqual(self.serial_module.PSU_mV, None), 'PSU voltage error, case 1'
        assert self.serial_module.is_connected(), 'not connected'


    def test_spindle_speed_monitor_voltage_case_107_112(self):
        """ 
        Test that spindle speed monitor voltage is None, but that serial continues to work
        This is relevant to FW between v107 and v112
        """
        self.status_and_PCB_constructor(self.case_107_112)
        self.assertEqual(self.serial_module.spindle_speed_monitor_mV, None), 'spindle speed monitor voltage error, case 1'
        assert self.serial_module.is_connected(), 'not connected'


    ## CASE 2 TESTS:
    def test_pcb_temperature_case_136_140(self):
        """ 
        Test that PCB temperature works!
        This is relevant to FW between v136 and v140
        """
        self.status_and_PCB_constructor(self.case_136_140, pcb_temp = self.t_pcb_temp)
        self.assertEqual(self.serial_module.pcb_temp, self.t_pcb_temp), 'pcb temp error, case 2'
        assert self.serial_module.is_connected(), 'not connected'


    def test_motor_driver_temperature_case_136_140(self):
        """ 
        Test that motor driver temperature works!
        This is relevant to FW between v136 and v140
        """
        self.status_and_PCB_constructor(self.case_136_140, motor_driver_temp = self.t_motor_driver_temp)
        self.assertEqual(self.serial_module.motor_driver_temp, self.t_motor_driver_temp), 'motor_driver temp error, case 2'
        assert self.serial_module.is_connected(), 'not connected'

    def test_transistor_heatsink_temperature_case_136_140(self):
        """ 
        Test that transistor heatsink temperature is None, but that serial is still connected.
        This is relevant to FW between v136 and v140
        """
        self.status_and_PCB_constructor(self.case_136_140)
        self.assertEqual(self.serial_module.transistor_heatsink_temp, None), 'transistor heatsink temp error, case 2'
        assert self.serial_module.is_connected(), 'not connected'

    def test_microcontroller_voltage_case_136_140(self):
        """ 
        Test that microcontroller voltage works!
        This is relevant to FW between v136 and v140
        """
        self.status_and_PCB_constructor(self.case_136_140, microcontroller_mV = self.t_microcontroller_mV)
        self.assertEqual(self.serial_module.microcontroller_mV, self.t_microcontroller_mV), 'microcontroller voltage error, case 2'
        assert self.serial_module.is_connected(), 'not connected'

    def test_LED_voltage_case_136_140(self):
        """ 
        Test that LED voltage works!
        This is relevant to FW between v136 and v140
        """
        self.status_and_PCB_constructor(self.case_136_140, LED_mV = self.t_LED_mV)
        self.assertEqual(self.serial_module.LED_mV, self.t_LED_mV), 'LED voltage error, case 2'
        assert self.serial_module.is_connected(), 'not connected'

    def test_PSU_voltage_case_136_140(self):
        """ 
        Test that PSU voltage works!
        This is relevant to FW between v136 and v140
        """
        self.status_and_PCB_constructor(self.case_136_140, PSU_mV = self.t_PSU_mV)
        self.assertEqual(self.serial_module.PSU_mV, self.t_PSU_mV), 'PSU voltage error, case 2'
        assert self.serial_module.is_connected(), 'not connected'


    def test_spindle_speed_monitor_voltage_case_136_140(self):
        """ 
        Test that spindle speed monitor voltage works!
        This is relevant to FW between v136 and v140
        """
        self.status_and_PCB_constructor(self.case_136_140, spindle_speed_monitor_mV = self.t_spindle_speed_monitor_mV)
        self.assertEqual(self.serial_module.spindle_speed_monitor_mV, self.t_spindle_speed_monitor_mV), 'spindle speed monitor voltage error, case 2'
        assert self.serial_module.is_connected(), 'not connected'


    ## CASE 3 TESTS:
    def test_pcb_temperature_case_228_NOW(self):
        """ 
        Test that PCB temperature works!
        This is relevant to FW between v136 and v140
        """
        self.status_and_PCB_constructor(self.case_228_NOW, pcb_temp = self.t_pcb_temp)
        self.assertEqual(self.serial_module.pcb_temp, self.t_pcb_temp), 'pcb temp error, case 3'
        assert self.serial_module.is_connected(), 'not connected'


    def test_motor_driver_temperature_case_228_NOW(self):
        """ 
        Test that motor driver temperature works!
        This is relevant to FW between v136 and v140
        """
        self.status_and_PCB_constructor(self.case_228_NOW, motor_driver_temp = self.t_motor_driver_temp)
        self.assertEqual(self.serial_module.motor_driver_temp, self.t_motor_driver_temp), 'motor_driver temp error, case 3'
        assert self.serial_module.is_connected(), 'not connected'

    def test_transistor_heatsink_temperature_case_228_NOW(self):
        """ 
        Test that transistor heatsink temperature works!
        This is relevant to FW between v136 and v140
        """
        self.status_and_PCB_constructor(self.case_228_NOW, transistor_heatsink_temp = self.t_transistor_heatsink_temp)
        self.assertEqual(self.serial_module.transistor_heatsink_temp, self.t_transistor_heatsink_temp), 'transistor heatsink temp error, case 3'
        assert self.serial_module.is_connected(), 'not connected'

    def test_microcontroller_voltage_case_228_NOW(self):
        """ 
        Test that microcontroller voltage works!
        This is relevant to FW between v136 and v140
        """
        self.status_and_PCB_constructor(self.case_228_NOW, microcontroller_mV = self.t_microcontroller_mV)
        self.assertEqual(self.serial_module.microcontroller_mV, self.t_microcontroller_mV), 'microcontroller voltage error, case 3'
        assert self.serial_module.is_connected(), 'not connected'

    def test_LED_voltage_case_228_NOW(self):
        """ 
        Test that LED voltage works!
        This is relevant to FW between v136 and v140
        """
        self.status_and_PCB_constructor(self.case_228_NOW, LED_mV = self.t_LED_mV)
        self.assertEqual(self.serial_module.LED_mV, self.t_LED_mV), 'LED voltage error, case 3'
        assert self.serial_module.is_connected(), 'not connected'

    def test_PSU_voltage_case_228_NOW(self):
        """ 
        Test that PSU voltage works!
        This is relevant to FW between v136 and v140
        """
        self.status_and_PCB_constructor(self.case_228_NOW, PSU_mV = self.t_PSU_mV)
        self.assertEqual(self.serial_module.PSU_mV, self.t_PSU_mV), 'PSU voltage error, case 3'
        assert self.serial_module.is_connected(), 'not connected'


    def test_spindle_speed_monitor_voltage_case_228_NOW(self):
        """ 
        Test that spindle speed monitor voltage works!
        This is relevant to FW between v136 and v140
        """
        self.status_and_PCB_constructor(self.case_228_NOW, spindle_speed_monitor_mV = self.t_spindle_speed_monitor_mV)
        self.assertEqual(self.serial_module.spindle_speed_monitor_mV, self.t_spindle_speed_monitor_mV), 'spindle speed monitor voltage error, case 3'
        assert self.serial_module.is_connected(), 'not connected'



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
