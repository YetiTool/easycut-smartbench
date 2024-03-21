'''
Created on 25 Jan 2022
@author: Letty
'''
from asmcnc.comms.logging_system.logging_system import Logger
from tests.automated_unit_tests.test_base import UnitTestBase

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
# python -m test.comms_serial_connection_tests.spindle_feedback_test
# OUTDATED


##########################################################

#  PLAN THE TEST:
#  
#  >>> GIVEN:
#    1    GIVEN an analogue feedback status that contains one value after Ld: <Run|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:pGg|Ld:4956>
#    2    GIVEN a digital feedback status that contains four values after Ld: <Run|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,20874|Pn:pGg|Ld:3000, 65, 255, 240> 
#         (Smart SC2 Mafell spindle with analogue speed control and digital feedback)

#  >>> WHEN:
#    *    WHEN serial comms module reads in a status that contains the Ld parameter
#  

#  >>> THEN:
#    *    THEN the serial comms module parses the ld either as overload (if one value, analogue)
#    *    OR the serial comms module parses the 4 ld values into variables, but currently doesn't do anything else 
#    *    AND doesn't overload!

##########################################################

class SpindleFeedbackTest(UnitTestBase):

    status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822>"

    test_spindle_load_voltage = 1789
    test_digital_spindle_ld_qdA = 100
    test_digital_spindle_temperature = 45
    test_digital_spindle_kill_time = 255
    test_digital_spindle_mains_voltage = 250


    def generate_overload_value(self, analogue_spindle_ld):

        if analogue_spindle_ld < 400 : overload_mV_equivalent_state = 0
        elif analogue_spindle_ld < 1000 : overload_mV_equivalent_state = 20
        elif analogue_spindle_ld < 1500 : overload_mV_equivalent_state = 40
        elif analogue_spindle_ld < 2000 : overload_mV_equivalent_state = 60
        elif analogue_spindle_ld < 2500 : overload_mV_equivalent_state = 80
        elif analogue_spindle_ld >= 2500 : overload_mV_equivalent_state = 100

        return overload_mV_equivalent_state



    def give_me_a_PCB(outerSelf):

        class YETIPCB(MockSerial):

            @serial_query("?")
            def do_something(self):
                return outerSelf.status

        return YETIPCB


    def status_and_PCB_constructor(self, case=None, 
                        spindle_load_voltage = 0,
                        digital_spindle_ld_qdA = 0,
                        digital_spindle_temperature = 0,
                        digital_spindle_kill_time = 0,
                        digital_spindle_mains_voltage = 0
                        ):

        # Use this to construct the test status passed out by mock serial object

        if case == 1 or case==None:

            self.status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822>"

        elif case == 2:

            self.status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Ld:" + \
            str(spindle_load_voltage) + ">"

        elif case == 3:

            self.status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Ld:" + \
                str(digital_spindle_ld_qdA) + "," + \
                str(digital_spindle_temperature) + "," + \
                str(digital_spindle_kill_time) + "," + \
                str(digital_spindle_mains_voltage) + ">"

            Logger.info(self.status)


        # Need to construct mock PCB after the status, otherwise it'll run something else:
        self.serial_module.s = DummySerial(self.give_me_a_PCB())
        self.serial_module.s.fd = 1 # this is needed to force it to run
        self.serial_module.start_services(1)
        sleep(0.01)

    def setUp(self):
        super(SpindleFeedbackTest, self).setUp()
        # If the set_up method raises an exception while the test is running, 
        # the framework will consider the test to have suffered an error, 
        # and the runTest (or test_X_Name) method will not be executed.

        self.m = Mock()
        self.sm = Mock()
        self.sett = Mock()
        self.l = localization.Localization()
        self.jd = Mock()

        self.serial_module = serial_connection.SerialConnection(self.m, self.sm, self.sett, self.l, self.jd)

    def tearDown(self):
        self.serial_module.__del__()


    def test_does_serial_think_its_connected(self):
        """Test that serial module thinks it is connected"""
        self.status_and_PCB_constructor()
        assert self.serial_module.is_connected(), 'not connected'

    def test_the_mock_interface(self):
        """Test that we're getting statuses back"""
        self.status_and_PCB_constructor(2)
        assert self.serial_module.m_state == "Idle", 'not idle'

# ANALOGUE SPINDLE FEEDBACK READ IN AND OVERLOAD - CASE 2

    def test_does_serial_read_in_analogue_spindle_load(self):
        self.status_and_PCB_constructor(case=2, spindle_load_voltage = self.test_spindle_load_voltage)
        self.assertEqual(self.serial_module.spindle_load_voltage, self.test_spindle_load_voltage), 'Analogue spindle load voltage wrong'

    def test_does_serial_give_correct_overload_value(self):
        self.status_and_PCB_constructor(case=2, spindle_load_voltage = self.test_spindle_load_voltage)
        self.assertEqual(self.serial_module.overload_state, self.generate_overload_value(self.test_spindle_load_voltage)), 'Analogue spindle load overload wrong'

# ANALOGUE SPINDLE FEEDBACK READ IN AND OVERLOAD - CASE 3

    def test_does_serial_not_read_in_digital_status_as_analogue_spindle_load(self):
        """If serial comms receives a 4 value Ld report, then analogue spindle ld voltage should be None"""
        self.status_and_PCB_constructor(case=3, spindle_load_voltage = self.test_spindle_load_voltage, digital_spindle_ld_qdA = self.test_digital_spindle_ld_qdA)
        self.assertNotEqual(self.serial_module.spindle_load_voltage, self.test_spindle_load_voltage), 'Digital feedback reading into analogue load'

    def test_does_serial_not_overload_if_digital_readin(self):
        """If serial comms receives a 4 value Ld report, then overload should be 0"""
        self.status_and_PCB_constructor(case=3, spindle_load_voltage = self.test_spindle_load_voltage, digital_spindle_ld_qdA = self.test_digital_spindle_ld_qdA)
        self.assertEqual(self.serial_module.overload_state, 0), 'Digital feedback causing analogue overload'

# DIGITAL SPINDLE FEEDBACK READ IN

    def test_does_serial_read_in_digital_spindle_ld(self):
        self.status_and_PCB_constructor(case=3, digital_spindle_ld_qdA = self.test_digital_spindle_ld_qdA)
        self.assertEqual(self.serial_module.digital_spindle_ld_qdA, self.test_digital_spindle_ld_qdA), 'Digital spindle ld wrong'

    def test_does_serial_read_in_digital_spindle_temp(self):
        self.status_and_PCB_constructor(case=3, digital_spindle_temperature = self.test_digital_spindle_temperature)
        self.assertEqual(self.serial_module.digital_spindle_temperature, self.test_digital_spindle_temperature), 'Digital spindle temp wrong'

    def test_does_serial_read_in_digital_spindle_kill_time(self):
        self.status_and_PCB_constructor(case=3, digital_spindle_kill_time = self.test_digital_spindle_kill_time)
        self.assertEqual(self.serial_module.digital_spindle_kill_time, self.test_digital_spindle_kill_time), 'Digital spindle kill time wrong'

    def test_does_serial_read_in_digital_spindle_mains_voltage(self):
        self.status_and_PCB_constructor(case=3, digital_spindle_mains_voltage = self.test_digital_spindle_mains_voltage)
        self.assertEqual(self.serial_module.digital_spindle_mains_voltage, self.test_digital_spindle_mains_voltage), 'Digital spindle mains voltage wrong'


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()