import logging
"""
Created on 25 Jan 2022
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
"""
- set up status constructor to take in temps/voltages, and a version, then can assert whether these come back out the other end 
"""


class TempsVoltagesTest(unittest.TestCase):
    status = (
        '<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822>'
        )
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

            @serial_query('?')
            def do_something(self):
                return outerSelf.status
        return YETIPCB

    def status_and_PCB_constructor(self, case=None, pcb_temp=0,
        motor_driver_temp=0, transistor_heatsink_temp=0, microcontroller_mV
        =0, LED_mV=0, PSU_mV=0, spindle_speed_monitor_mV=0):
        if case == 1 or case == None:
            self.status = (
                '<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822>'
                )
        elif case == 2:
            self.status = (
                '<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Ld:0|TC:' +
                str(motor_driver_temp) + ',' + str(pcb_temp) + '|V:' + str(
                microcontroller_mV) + ',' + str(LED_mV) + ',' + str(PSU_mV) +
                ',' + str(spindle_speed_monitor_mV) + '>')
        elif case == 3:
            self.status = (
                '<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Ld:0|TC:' +
                str(motor_driver_temp) + ',' + str(pcb_temp) + ',' + str(
                transistor_heatsink_temp) + '|V:' + str(microcontroller_mV) +
                ',' + str(LED_mV) + ',' + str(PSU_mV) + ',' + str(
                spindle_speed_monitor_mV) + '>')
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

    def test_pcb_temperature_case_107_112(self):
        """ 
        Test that PCB temperature is None, but that serial continues to work
        This is relevant to FW between v107 and v112
        """
        self.status_and_PCB_constructor(self.case_107_112)
        self.assertEqual(self.serial_module.pcb_temp, None
            ), 'pcb temp error, case 1'
        assert self.serial_module.is_connected(), 'not connected'

    def test_motor_driver_temperature_case_107_112(self):
        """ 
        Test that motor driver temperature is None, but that serial continues to work
        This is relevant to FW between v107 and v112
        """
        self.status_and_PCB_constructor(self.case_107_112)
        self.assertEqual(self.serial_module.motor_driver_temp, None
            ), 'motor_driver temp error, case 1'
        assert self.serial_module.is_connected(), 'not connected'

    def test_transistor_heatsink_temperature_case_107_112(self):
        """ 
        Test that transistor heatsink temperature is None, but that serial continues to work
        This is relevant to FW between v107 and v112
        """
        self.status_and_PCB_constructor(self.case_107_112)
        self.assertEqual(self.serial_module.transistor_heatsink_temp, None
            ), 'transistor heatsink temp error, case 1'
        assert self.serial_module.is_connected(), 'not connected'

    def test_microcontroller_voltage_case_107_112(self):
        """ 
        Test that microcontroller voltage is None, but that serial continues to work
        This is relevant to FW between v107 and v112
        """
        self.status_and_PCB_constructor(self.case_107_112)
        self.assertEqual(self.serial_module.microcontroller_mV, None
            ), 'microcontroller voltage error, case 1'
        assert self.serial_module.is_connected(), 'not connected'

    def test_LED_voltage_case_107_112(self):
        """ 
        Test that LED voltage is None, but that serial continues to work
        This is relevant to FW between v107 and v112
        """
        self.status_and_PCB_constructor(self.case_107_112)
        self.assertEqual(self.serial_module.LED_mV, None
            ), 'LED voltage error, case 1'
        assert self.serial_module.is_connected(), 'not connected'

    def test_PSU_voltage_case_107_112(self):
        """ 
        Test that PSU voltage is None, but that serial continues to work
        This is relevant to FW between v107 and v112
        """
        self.status_and_PCB_constructor(self.case_107_112)
        self.assertEqual(self.serial_module.PSU_mV, None
            ), 'PSU voltage error, case 1'
        assert self.serial_module.is_connected(), 'not connected'

    def test_spindle_speed_monitor_voltage_case_107_112(self):
        """ 
        Test that spindle speed monitor voltage is None, but that serial continues to work
        This is relevant to FW between v107 and v112
        """
        self.status_and_PCB_constructor(self.case_107_112)
        self.assertEqual(self.serial_module.spindle_speed_monitor_mV, None
            ), 'spindle speed monitor voltage error, case 1'
        assert self.serial_module.is_connected(), 'not connected'

    def test_pcb_temperature_case_136_140(self):
        """ 
        Test that PCB temperature works!
        This is relevant to FW between v136 and v140
        """
        self.status_and_PCB_constructor(self.case_136_140, pcb_temp=self.
            t_pcb_temp)
        self.assertEqual(self.serial_module.pcb_temp, self.t_pcb_temp
            ), 'pcb temp error, case 2'
        assert self.serial_module.is_connected(), 'not connected'

    def test_motor_driver_temperature_case_136_140(self):
        """ 
        Test that motor driver temperature works!
        This is relevant to FW between v136 and v140
        """
        self.status_and_PCB_constructor(self.case_136_140,
            motor_driver_temp=self.t_motor_driver_temp)
        self.assertEqual(self.serial_module.motor_driver_temp, self.
            t_motor_driver_temp), 'motor_driver temp error, case 2'
        assert self.serial_module.is_connected(), 'not connected'

    def test_transistor_heatsink_temperature_case_136_140(self):
        """ 
        Test that transistor heatsink temperature is None, but that serial is still connected.
        This is relevant to FW between v136 and v140
        """
        self.status_and_PCB_constructor(self.case_136_140)
        self.assertEqual(self.serial_module.transistor_heatsink_temp, None
            ), 'transistor heatsink temp error, case 2'
        assert self.serial_module.is_connected(), 'not connected'

    def test_microcontroller_voltage_case_136_140(self):
        """ 
        Test that microcontroller voltage works!
        This is relevant to FW between v136 and v140
        """
        self.status_and_PCB_constructor(self.case_136_140,
            microcontroller_mV=self.t_microcontroller_mV)
        self.assertEqual(self.serial_module.microcontroller_mV, self.
            t_microcontroller_mV), 'microcontroller voltage error, case 2'
        assert self.serial_module.is_connected(), 'not connected'

    def test_LED_voltage_case_136_140(self):
        """ 
        Test that LED voltage works!
        This is relevant to FW between v136 and v140
        """
        self.status_and_PCB_constructor(self.case_136_140, LED_mV=self.t_LED_mV
            )
        self.assertEqual(self.serial_module.LED_mV, self.t_LED_mV
            ), 'LED voltage error, case 2'
        assert self.serial_module.is_connected(), 'not connected'

    def test_PSU_voltage_case_136_140(self):
        """ 
        Test that PSU voltage works!
        This is relevant to FW between v136 and v140
        """
        self.status_and_PCB_constructor(self.case_136_140, PSU_mV=self.t_PSU_mV
            )
        self.assertEqual(self.serial_module.PSU_mV, self.t_PSU_mV
            ), 'PSU voltage error, case 2'
        assert self.serial_module.is_connected(), 'not connected'

    def test_spindle_speed_monitor_voltage_case_136_140(self):
        """ 
        Test that spindle speed monitor voltage works!
        This is relevant to FW between v136 and v140
        """
        self.status_and_PCB_constructor(self.case_136_140,
            spindle_speed_monitor_mV=self.t_spindle_speed_monitor_mV)
        self.assertEqual(self.serial_module.spindle_speed_monitor_mV, self.
            t_spindle_speed_monitor_mV
            ), 'spindle speed monitor voltage error, case 2'
        assert self.serial_module.is_connected(), 'not connected'

    def test_pcb_temperature_case_228_NOW(self):
        """ 
        Test that PCB temperature works!
        This is relevant to FW between v136 and v140
        """
        self.status_and_PCB_constructor(self.case_228_NOW, pcb_temp=self.
            t_pcb_temp)
        self.assertEqual(self.serial_module.pcb_temp, self.t_pcb_temp
            ), 'pcb temp error, case 3'
        assert self.serial_module.is_connected(), 'not connected'

    def test_motor_driver_temperature_case_228_NOW(self):
        """ 
        Test that motor driver temperature works!
        This is relevant to FW between v136 and v140
        """
        self.status_and_PCB_constructor(self.case_228_NOW,
            motor_driver_temp=self.t_motor_driver_temp)
        self.assertEqual(self.serial_module.motor_driver_temp, self.
            t_motor_driver_temp), 'motor_driver temp error, case 3'
        assert self.serial_module.is_connected(), 'not connected'

    def test_transistor_heatsink_temperature_case_228_NOW(self):
        """ 
        Test that transistor heatsink temperature works!
        This is relevant to FW between v136 and v140
        """
        self.status_and_PCB_constructor(self.case_228_NOW,
            transistor_heatsink_temp=self.t_transistor_heatsink_temp)
        self.assertEqual(self.serial_module.transistor_heatsink_temp, self.
            t_transistor_heatsink_temp
            ), 'transistor heatsink temp error, case 3'
        assert self.serial_module.is_connected(), 'not connected'

    def test_microcontroller_voltage_case_228_NOW(self):
        """ 
        Test that microcontroller voltage works!
        This is relevant to FW between v136 and v140
        """
        self.status_and_PCB_constructor(self.case_228_NOW,
            microcontroller_mV=self.t_microcontroller_mV)
        self.assertEqual(self.serial_module.microcontroller_mV, self.
            t_microcontroller_mV), 'microcontroller voltage error, case 3'
        assert self.serial_module.is_connected(), 'not connected'

    def test_LED_voltage_case_228_NOW(self):
        """ 
        Test that LED voltage works!
        This is relevant to FW between v136 and v140
        """
        self.status_and_PCB_constructor(self.case_228_NOW, LED_mV=self.t_LED_mV
            )
        self.assertEqual(self.serial_module.LED_mV, self.t_LED_mV
            ), 'LED voltage error, case 3'
        assert self.serial_module.is_connected(), 'not connected'

    def test_PSU_voltage_case_228_NOW(self):
        """ 
        Test that PSU voltage works!
        This is relevant to FW between v136 and v140
        """
        self.status_and_PCB_constructor(self.case_228_NOW, PSU_mV=self.t_PSU_mV
            )
        self.assertEqual(self.serial_module.PSU_mV, self.t_PSU_mV
            ), 'PSU voltage error, case 3'
        assert self.serial_module.is_connected(), 'not connected'

    def test_spindle_speed_monitor_voltage_case_228_NOW(self):
        """ 
        Test that spindle speed monitor voltage works!
        This is relevant to FW between v136 and v140
        """
        self.status_and_PCB_constructor(self.case_228_NOW,
            spindle_speed_monitor_mV=self.t_spindle_speed_monitor_mV)
        self.assertEqual(self.serial_module.spindle_speed_monitor_mV, self.
            t_spindle_speed_monitor_mV
            ), 'spindle speed monitor voltage error, case 3'
        assert self.serial_module.is_connected(), 'not connected'


if __name__ == '__main__':
    unittest.main()
