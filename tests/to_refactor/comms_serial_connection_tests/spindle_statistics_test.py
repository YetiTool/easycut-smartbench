import logging
"""
Created on 4 Feb 2022
@author: Letty
"""
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


class SpindleStatisticsTest(unittest.TestCase):
    status = (
        '<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822>'
        )
    test_spindle_serial_number = 10517
    test_spindle_production_year = 21
    test_spindle_production_week = 15
    test_spindle_firmware_version = 8
    test_spindle_total_run_time_seconds = 89324
    test_spindle_brush_run_time_seconds = 7
    test_spindle_mains_frequency_hertz = 50

    def give_me_a_PCB(outerSelf):


        class YETIPCB(MockSerial):

            @serial_query('?')
            def do_something(self):
                return outerSelf.status
        return YETIPCB

    def status_and_PCB_constructor(self, case=None, spindle_serial_number=0,
        spindle_production_year=0, spindle_production_week=0,
        spindle_firmware_version=0, spindle_total_run_time_seconds=0,
        spindle_brush_run_time_seconds=0, spindle_mains_frequency_hertz=0):
        if case == 1 or case == None:
            self.status = (
                '<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822>'
                )
        elif case == 2:
            self.status = (
                '<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Sp:' + str(
                spindle_serial_number) + ',' + str(spindle_production_year) +
                ',' + str(spindle_production_week) + ',' + str(
                spindle_firmware_version) + ',' + str(
                spindle_total_run_time_seconds) + ',' + str(
                spindle_brush_run_time_seconds) + ',' + str(
                spindle_mains_frequency_hertz) + '>')
        self.serial_module.s = DummySerial(self.give_me_a_PCB())
        self.serial_module.s.fd = 1
        self.serial_module.start_services(1)
        sleep(0.01)

    def setUp(self):
        self.m = Mock()
        self.sm = Mock()
        self.sett = Mock()
        self.l = localization.Localization()
        self.jd = Mock()
        self.serial_module = serial_connection.SerialConnection(self.m,
            self.sm, self.sett, self.l, self.jd, logging.Logger(name=
            '__name__'))

    def tearDown(self):
        self.serial_module.__del__()

    def test_does_serial_think_its_connected(self):
        """Test that serial module thinks it is connected"""
        self.status_and_PCB_constructor()
        assert self.serial_module.is_connected(), 'not connected'

    def test_the_mock_interface(self):
        """Test that we're getting statuses back"""
        self.status_and_PCB_constructor(1)
        assert self.serial_module.m_state == 'Idle', 'not idle'

    def test_does_serial_read_in_spindle_serial_number(self):
        """Test spindle serial number read-in"""
        self.status_and_PCB_constructor(case=2, spindle_serial_number=self.
            test_spindle_serial_number)
        self.assertEqual(self.serial_module.spindle_serial_number, self.
            test_spindle_serial_number), 'Serial number wrong'

    def test_does_serial_read_in_spindle_production_year(self):
        """Test spindle production year read-in"""
        self.status_and_PCB_constructor(case=2, spindle_production_year=
            self.test_spindle_production_year)
        self.assertEqual(self.serial_module.spindle_production_year, self.
            test_spindle_production_year), 'Production year wrong'

    def test_does_serial_read_in_spindle_production_week(self):
        """Test spindle production week read-in"""
        self.status_and_PCB_constructor(case=2, spindle_production_week=
            self.test_spindle_production_week)
        self.assertEqual(self.serial_module.spindle_production_week, self.
            test_spindle_production_week), 'Production week wrong'

    def test_does_serial_read_in_spindle_firmware_version(self):
        """Test spindle firmware version read-in"""
        self.status_and_PCB_constructor(case=2, spindle_firmware_version=
            self.test_spindle_firmware_version)
        self.assertEqual(self.serial_module.spindle_firmware_version, self.
            test_spindle_firmware_version), 'Firmware version wrong'

    def test_does_serial_read_in_spindle_total_run_time_seconds(self):
        """Test spindle total run time read-in"""
        self.status_and_PCB_constructor(case=2,
            spindle_total_run_time_seconds=self.
            test_spindle_total_run_time_seconds)
        self.assertEqual(self.serial_module.spindle_total_run_time_seconds,
            self.test_spindle_total_run_time_seconds), 'Total run time wrong'

    def test_does_serial_read_in_spindle_brush_run_time_seconds(self):
        """Test spindle brush run time read-in"""
        self.status_and_PCB_constructor(case=2,
            spindle_brush_run_time_seconds=self.
            test_spindle_brush_run_time_seconds)
        self.assertEqual(self.serial_module.spindle_brush_run_time_seconds,
            self.test_spindle_brush_run_time_seconds), 'Brush run time wrong'

    def test_does_serial_read_in_spindle_mains_frequency_hertz(self):
        """Test spindle mains frequency read-in"""
        self.status_and_PCB_constructor(case=2,
            spindle_mains_frequency_hertz=self.
            test_spindle_mains_frequency_hertz)
        self.assertEqual(self.serial_module.spindle_mains_frequency_hertz,
            self.test_spindle_mains_frequency_hertz), 'Mains frequency wrong'


if __name__ == '__main__':
    unittest.main()
