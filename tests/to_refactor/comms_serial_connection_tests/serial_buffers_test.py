import logging
"""
Created on 14 Feb 2022
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
from random import randint
import sys
sys.path.append('./src')
try:
    from asmcnc.comms import router_machine
    from asmcnc.comms import localization
except:
    pass
from asmcnc.comms.yeti_grbl_protocol.c_defines import *
Cmport = 'COM3'


class MotorCommandsTest(unittest.TestCase):
    status = (
        '<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822>'
        )
    max_count = 10
    command_buffer = ''
    run_buffer = ''
    realtime_buffer = ''
    protocol_buffer = ''
    job_object = []
    comparison_string = ''.join(map(str, list(range(max_count + 1))))

    def create_job_object(self, n_lines):
        for i in range(n_lines):
            self.job_object.append('count run ' + str(i))

    def give_me_a_PCB(outerSelf):


        class YETIPCB(MockSerial):
            simple_queries = {'?': outerSelf.status, '\x18': '',
                'G0 G53 Z-': 'ok', '*LFFFF00': 'ok'}

            @serial_query('count')
            def do_something(self, buffer_type, counter):
                if buffer_type == 'command':
                    outerSelf.command_buffer = outerSelf.command_buffer + str(
                        counter)
                    return 'ok'
                if buffer_type == 'run':
                    outerSelf.run_buffer = outerSelf.run_buffer + str(counter)
                    Logger.info(outerSelf.run_buffer)
                    return 'ok'
                if buffer_type == 'realtime':
                    outerSelf.realtime_buffer = (outerSelf.realtime_buffer +
                        str(counter))
                if buffer_type == 'protocol':
                    outerSelf.protocol_buffer = (outerSelf.protocol_buffer +
                        str(counter))
        return YETIPCB

    def setUp(self):
        self.sm = Mock()
        self.sett = Mock()
        self.sett.ip_address = ''
        self.l = localization.Localization()
        self.jd = Mock()
        self.m = router_machine.RouterMachine(Cmport, self.sm, self.sett,
            self.l, self.jd)
        self.m.s.s = DummySerial(self.give_me_a_PCB())
        self.m.s.s.fd = 1
        self.m.s.start_services(1)
        self.m.s.setting_27 = ''
        sleep(0.01)

    def tearDown(self):
        self.m.s.__del__()

    def test_does_serial_think_its_connected(self):
        """Test that serial module thinks it is connected"""
        assert self.m.s.is_connected(), 'not connected'

    def test_the_mock_interface(self):
        """Test that we're getting statuses back"""
        assert self.m.s.m_state == 'Idle', 'not idle'

    def test_buffer_stability(self):
        command_counter = 0
        run_counter = 0
        realtime_counter = 0
        protocol_counter = 0
        while True:
            decider = randint(1, 3)
            if decider == 1 and command_counter < self.max_count + 1:
                self.m.s.write_command('count command ' + str(command_counter))
                command_counter = command_counter + 1
            elif decider == 2 and realtime_counter < self.max_count + 1:
                self.m.s.write_realtime('count realtime ' + str(
                    realtime_counter))
                realtime_counter = realtime_counter + 1
            elif decider == 3 and protocol_counter < self.max_count + 1:
                self.m.s.write_protocol('count protocol ' + str(
                    protocol_counter), 'COUNTING ' + str(protocol_counter))
                protocol_counter = protocol_counter + 1
            elif self.command_buffer.endswith('10'
                ) and self.realtime_buffer.endswith('10'
                ) and self.protocol_buffer.endswith('10'):
                break
            sleep(0.01)
        self.assertEqual(self.command_buffer, self.comparison_string)
        self.assertEqual(self.protocol_buffer, self.comparison_string)
        self.assertEqual(self.realtime_buffer, self.comparison_string)


if __name__ == '__main__':
    unittest.main()
