'''
Created on 4 Feb 2022
@author: Letty
'''
from kivy import Logger

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
# python -m test.comms_serial_connection_tests.spindle_statistics_test


##########################################################

#  PLAN THE TEST:
#  
#  >>> GIVEN:
#    1    GIVEN a status with no spindle statistics
#    2    GIVEN a status that contains full spindle statistics
#
#  >>> WHEN:
#    *    WHEN serial comms module reads in a status that contains 'Sp:'
#  
#  >>> THEN:
#    *    THEN the serial comms module reads in the spindle statistics

##########################################################

class SpindleStatisticsTest(unittest.TestCase):

    status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822>"

    # Spindle serial number: 10517
    # Production year: 21
    # Production week: 15
    # Firmware version: 8
    # Total run time: 89324 seconds
    # Brush run time: 7 seconds (since last reset)
    # Mains frequency: 50Hz

    test_spindle_serial_number = 10517
    test_spindle_production_year = 21
    test_spindle_production_week = 15
    test_spindle_firmware_version = 8
    test_spindle_total_run_time_seconds = 89324
    test_spindle_brush_run_time_seconds = 7
    test_spindle_mains_frequency_hertz = 50


    def give_me_a_PCB(outerSelf):

        class YETIPCB(MockSerial):

            @serial_query("?")
            def do_something(self):
                return outerSelf.status

        return YETIPCB


    def status_and_PCB_constructor(self, case=None, 
                        spindle_serial_number = 0,
                        spindle_production_year = 0,
                        spindle_production_week = 0,
                        spindle_firmware_version = 0,
                        spindle_total_run_time_seconds = 0,
                        spindle_brush_run_time_seconds = 0,
                        spindle_mains_frequency_hertz = 0
                        ):

        # Use this to construct the test status passed out by mock serial object

        if case == 1 or case==None:

            self.status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822>"

        elif case == 2:

            self.status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Sp:" + \
                        str(spindle_serial_number) + "," + \
                        str(spindle_production_year) + "," + \
                        str(spindle_production_week) + "," + \
                        str(spindle_firmware_version) + "," + \
                        str(spindle_total_run_time_seconds) + "," + \
                        str(spindle_brush_run_time_seconds) + "," + \
                        str(spindle_mains_frequency_hertz) + ">"

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

    def test_does_serial_read_in_spindle_serial_number(self):
        """Test spindle serial number read-in"""
        self.status_and_PCB_constructor(case=2, spindle_serial_number = self.test_spindle_serial_number)
        self.assertEqual(self.serial_module.spindle_serial_number, self.test_spindle_serial_number), 'Serial number wrong'

    def test_does_serial_read_in_spindle_production_year(self):
        """Test spindle production year read-in"""
        self.status_and_PCB_constructor(case=2, spindle_production_year = self.test_spindle_production_year)
        self.assertEqual(self.serial_module.spindle_production_year, self.test_spindle_production_year), 'Production year wrong'

    def test_does_serial_read_in_spindle_production_week(self):
        """Test spindle production week read-in"""
        self.status_and_PCB_constructor(case=2, spindle_production_week = self.test_spindle_production_week)
        self.assertEqual(self.serial_module.spindle_production_week, self.test_spindle_production_week), 'Production week wrong'

    def test_does_serial_read_in_spindle_firmware_version(self):
        """Test spindle firmware version read-in"""
        self.status_and_PCB_constructor(case=2, spindle_firmware_version = self.test_spindle_firmware_version)
        self.assertEqual(self.serial_module.spindle_firmware_version, self.test_spindle_firmware_version), 'Firmware version wrong'

    def test_does_serial_read_in_spindle_total_run_time_seconds(self):
        """Test spindle total run time read-in"""
        self.status_and_PCB_constructor(case=2, spindle_total_run_time_seconds = self.test_spindle_total_run_time_seconds)
        self.assertEqual(self.serial_module.spindle_total_run_time_seconds, self.test_spindle_total_run_time_seconds), 'Total run time wrong'

    def test_does_serial_read_in_spindle_brush_run_time_seconds(self):
        """Test spindle brush run time read-in"""
        self.status_and_PCB_constructor(case=2, spindle_brush_run_time_seconds = self.test_spindle_brush_run_time_seconds)
        self.assertEqual(self.serial_module.spindle_brush_run_time_seconds, self.test_spindle_brush_run_time_seconds), 'Brush run time wrong'

    def test_does_serial_read_in_spindle_mains_frequency_hertz(self):
        """Test spindle mains frequency read-in"""
        self.status_and_PCB_constructor(case=2, spindle_mains_frequency_hertz = self.test_spindle_mains_frequency_hertz)
        self.assertEqual(self.serial_module.spindle_mains_frequency_hertz, self.test_spindle_mains_frequency_hertz), 'Mains frequency wrong'

    # Spindle serial number: 10517
    # Production year: 21
    # Production week: 15
    # Firmware version: 8
    # Total run time: 89324 seconds
    # Brush run time: 7 seconds (since last reset)
    # Mains frequency: 50Hz



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()




























