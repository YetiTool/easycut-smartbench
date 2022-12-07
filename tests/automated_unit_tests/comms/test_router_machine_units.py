'''
Created on 1 Aug 2022
@author: Letty
'''

import sys, os
sys.path.append('./src')

try: 
    import unittest
    import pytest
    from mock import Mock, MagicMock

except: 
    print("Can't import mocking packages, are you on a dev machine?")


from asmcnc.comms import router_machine
from asmcnc.comms import localization
from datetime import datetime
from asmcnc.comms.yeti_grbl_protocol.c_defines import *


'''
######################################
RUN FROM easycut-smartbench FOLDER WITH: 
python -m pytest --show-capture=no --disable-pytest-warnings tests/automated_unit_tests/comms/test_router_machine_units.py
######################################
'''

# FIXTURES
@pytest.fixture
def m():
    l = localization.Localization()

    screen_manager = Mock()
    settings_manager = Mock()
    job = Mock()
    m = router_machine.RouterMachine("COM", screen_manager, settings_manager, l, job)
    m.s.next_poll_time = 0
    m.s.write_direct = Mock()
    m.s.s = MagicMock()
    m.clear_motor_registers = Mock()
    m.is_machines_fw_version_equal_to_or_greater_than_version = Mock(return_value=True)
    m.s.m_state = "Idle"
    return m

def test_close_serial_connection(m):
    m.close_serial_connection(0)
    m.clear_motor_registers.assert_called()

def test_reconnect_serial_connection(m):
    m.reconnect_serial_connection()
    m.clear_motor_registers.assert_called()

def test_construct_calibration_check_file_path(m):
    X_file = m.construct_calibration_check_file_path("X")
    Y_file = m.construct_calibration_check_file_path("Y")
    Z_file = m.construct_calibration_check_file_path("Z")
    assert os.path.exists("./src/" + X_file.strip("."))
    assert os.path.exists("./src/" + Y_file.strip("."))
    assert os.path.exists("./src/" + Z_file.strip("."))


# Set motor current tests

def generate_idle_current_text(axis, motor, current):
    altDisplayText = 'SET IDLE CURRENT: ' + axis + ': ' + "TMC: " + str(motor) + ", I: " + str(current)
    return altDisplayText

def generate_active_current_text(axis, motor, current):
    altDisplayText = 'SET ACTIVE CURRENT: ' + axis + ': ' + "TMC: " + str(motor) + ", I: " + str(current)
    return altDisplayText

def assert_current_sent_to_motor(machine, axis, motor, current):
    machine.send_command_to_motor = Mock()
    assert machine.set_motor_current(axis, current)
    machine.send_command_to_motor.assert_any_call(generate_active_current_text(axis, motor, current), motor=motor, command=SET_ACTIVE_CURRENT, value=current)
    machine.send_command_to_motor.assert_any_call(generate_idle_current_text(axis, motor, current), motor=motor, command=SET_IDLE_CURRENT, value=current)

# def assert_current_NOT_sent_to_motor(machine, axis, motor, current):
#     machine.send_command_to_motor = Mock()
#     assert machine.set_motor_current(axis, current)
#     machine.send_command_to_motor.assert_any_call(generate_active_current_text(axis, motor, current), motor=motor, command=SET_ACTIVE_CURRENT, value=current)
#     machine.send_command_to_motor.assert_any_call(generate_idle_current_text(axis, motor, current), motor=motor, command=SET_IDLE_CURRENT, value=current)


def test_set_X_motor_current(m):

    axis = "X"
    motor_1 = TMC_X1
    motor_2 = TMC_X2
    current = 26
    assert_current_sent_to_motor(m, axis, motor_1, current)
    assert_current_sent_to_motor(m, axis, motor_2, current)






