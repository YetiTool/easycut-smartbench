import logging

"""
Created on 25 Jan 2022
@author: Letty
"""
try:
    import unittest
    from mock import Mock, MagicMock
    from serial_mock.mock import MockSerial, DummySerial
    from serial_mock.decorators import serial_query
except:
    print("Can't import mocking packages, are you on a dev machine?")
from time import sleep
import sys

sys.path.append("./src")
try:
    from asmcnc.comms import serial_connection
    from asmcnc.comms import localization
except:
    pass


class SpindleFeedbackTest(unittest.TestCase):
    status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822>"
    test_spindle_load_voltage = 1789
    test_digital_spindle_ld_qdA = 100
    test_digital_spindle_temperature = 45
    test_digital_spindle_kill_time = 255
    test_digital_spindle_mains_voltage = 250

    def generate_overload_value(self, analogue_spindle_ld):
        if analogue_spindle_ld < 400:
            overload_mV_equivalent_state = 0
        elif analogue_spindle_ld < 1000:
            overload_mV_equivalent_state = 20
        elif analogue_spindle_ld < 1500:
            overload_mV_equivalent_state = 40
        elif analogue_spindle_ld < 2000:
            overload_mV_equivalent_state = 60
        elif analogue_spindle_ld < 2500:
            overload_mV_equivalent_state = 80
        elif analogue_spindle_ld >= 2500:
            overload_mV_equivalent_state = 100
        return overload_mV_equivalent_state

    def give_me_a_PCB(outerSelf):
        class YETIPCB(MockSerial):
            @serial_query("?")
            def do_something(self):
                return outerSelf.status

        return YETIPCB

    def status_and_PCB_constructor(
        self,
        case=None,
        spindle_load_voltage=0,
        digital_spindle_ld_qdA=0,
        digital_spindle_temperature=0,
        digital_spindle_kill_time=0,
        digital_spindle_mains_voltage=0,
    ):
        if case == 1 or case == None:
            self.status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822>"
        elif case == 2:
            self.status = (
                "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Ld:"
                + str(spindle_load_voltage)
                + ">"
            )
        elif case == 3:
            self.status = (
                "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Ld:"
                + str(digital_spindle_ld_qdA)
                + ","
                + str(digital_spindle_temperature)
                + ","
                + str(digital_spindle_kill_time)
                + ","
                + str(digital_spindle_mains_voltage)
                + ">"
            )
            print(self.status)
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
        self.serial_module = serial_connection.SerialConnection(
            self.m, self.sm, self.sett, self.l, self.jd, logging.Logger(name="__name__")
        )

    def tearDown(self):
        self.serial_module.__del__()

    def test_does_serial_think_its_connected(self):
        """Test that serial module thinks it is connected"""
        self.status_and_PCB_constructor()
        assert self.serial_module.is_connected(), "not connected"

    def test_the_mock_interface(self):
        """Test that we're getting statuses back"""
        self.status_and_PCB_constructor(2)
        assert self.serial_module.m_state == "Idle", "not idle"

    def test_does_serial_read_in_analogue_spindle_load(self):
        self.status_and_PCB_constructor(
            case=2, spindle_load_voltage=self.test_spindle_load_voltage
        )
        self.assertEqual(
            self.serial_module.spindle_load_voltage, self.test_spindle_load_voltage
        ), "Analogue spindle load voltage wrong"

    def test_does_serial_give_correct_overload_value(self):
        self.status_and_PCB_constructor(
            case=2, spindle_load_voltage=self.test_spindle_load_voltage
        )
        self.assertEqual(
            self.serial_module.overload_state,
            self.generate_overload_value(self.test_spindle_load_voltage),
        ), "Analogue spindle load overload wrong"

    def test_does_serial_not_read_in_digital_status_as_analogue_spindle_load(self):
        """If serial comms receives a 4 value Ld report, then analogue spindle ld voltage should be None"""
        self.status_and_PCB_constructor(
            case=3,
            spindle_load_voltage=self.test_spindle_load_voltage,
            digital_spindle_ld_qdA=self.test_digital_spindle_ld_qdA,
        )
        self.assertNotEqual(
            self.serial_module.spindle_load_voltage, self.test_spindle_load_voltage
        ), "Digital feedback reading into analogue load"

    def test_does_serial_not_overload_if_digital_readin(self):
        """If serial comms receives a 4 value Ld report, then overload should be 0"""
        self.status_and_PCB_constructor(
            case=3,
            spindle_load_voltage=self.test_spindle_load_voltage,
            digital_spindle_ld_qdA=self.test_digital_spindle_ld_qdA,
        )
        self.assertEqual(
            self.serial_module.overload_state, 0
        ), "Digital feedback causing analogue overload"

    def test_does_serial_read_in_digital_spindle_ld(self):
        self.status_and_PCB_constructor(
            case=3, digital_spindle_ld_qdA=self.test_digital_spindle_ld_qdA
        )
        self.assertEqual(
            self.serial_module.digital_spindle_ld_qdA, self.test_digital_spindle_ld_qdA
        ), "Digital spindle ld wrong"

    def test_does_serial_read_in_digital_spindle_temp(self):
        self.status_and_PCB_constructor(
            case=3, digital_spindle_temperature=self.test_digital_spindle_temperature
        )
        self.assertEqual(
            self.serial_module.digital_spindle_temperature,
            self.test_digital_spindle_temperature,
        ), "Digital spindle temp wrong"

    def test_does_serial_read_in_digital_spindle_kill_time(self):
        self.status_and_PCB_constructor(
            case=3, digital_spindle_kill_time=self.test_digital_spindle_kill_time
        )
        self.assertEqual(
            self.serial_module.digital_spindle_kill_time,
            self.test_digital_spindle_kill_time,
        ), "Digital spindle kill time wrong"

    def test_does_serial_read_in_digital_spindle_mains_voltage(self):
        self.status_and_PCB_constructor(
            case=3,
            digital_spindle_mains_voltage=self.test_digital_spindle_mains_voltage,
        )
        self.assertEqual(
            self.serial_module.digital_spindle_mains_voltage,
            self.test_digital_spindle_mains_voltage,
        ), "Digital spindle mains voltage wrong"


if __name__ == "__main__":
    unittest.main()
