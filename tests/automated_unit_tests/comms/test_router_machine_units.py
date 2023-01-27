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

from kivy.clock import Clock
from time import sleep


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


# SET MOTOR CURRENT TESTS

def assert_current_sent_to_motor(machine, axis, motors, current):
    # motors arg needs to contain the motors we expect to read :) 

    # SET UP LIST OF EXPECTED KEYWORD ARGUMENTS
    expected_kwargs = []
    for motor in motors: 
        expected_kwargs.append({'command': SET_ACTIVE_CURRENT, 'motor': motor, 'value': current})
        expected_kwargs.append({'command': SET_IDLE_CURRENT, 'motor': motor, 'value': current})

    # SET UP SEND_COMMAND_TO_MOTOR FUNCTION THAT WE CAN SPY ON
    machine.send_command_to_motor = Mock()
    assert machine.set_motor_current(axis, current)
    assert len(machine.send_command_to_motor.call_args_list) == len(expected_kwargs)

    # CHECK THAT THE KWARGS SENT MATCH THE EXPECTED ONES :)
    for idx, call in enumerate(machine.send_command_to_motor.call_args_list):
        assert call.kwargs == expected_kwargs[idx]

def test_set_X_motor_current_for_axis(m):
    axis = "X"
    motor_1 = TMC_X1
    motor_2 = TMC_X2
    current = 26
    assert_current_sent_to_motor(m, axis, [motor_1, motor_2], current)

def test_set_X1_motor_current_for_individual_motor(m):
    axis = "X1"
    motor = TMC_X1
    current = 23
    assert_current_sent_to_motor(m, axis, [motor], current)

def test_set_X2_motor_current_for_individual_motor(m):
    axis = "X2"
    motor = TMC_X2
    current = 11
    assert_current_sent_to_motor(m, axis, [motor], current)

def test_set_Y_motor_current_for_axis(m):
    axis = "Y"
    motor_1 = TMC_Y1
    motor_2 = TMC_Y2
    current = 0
    assert_current_sent_to_motor(m, axis, [motor_1, motor_2], current)

def test_set_Y1_motor_current_for_individual_motor(m):
    axis = "Y1"
    motor = TMC_Y1
    current = 1
    assert_current_sent_to_motor(m, axis, [motor], current)

def test_set_Y2_motor_current_for_individual_motor(m):
    axis = "Y2"
    motor = TMC_Y2
    current = 14
    assert_current_sent_to_motor(m, axis, [motor], current)

def test_set_Z_motor_current_for_individual_motor(m):
    axis = "Z"
    motor = TMC_Z
    current = 15
    assert_current_sent_to_motor(m, axis, [motor], current)

def test_multiple_motor_currents(m):
    axis = "X1YZ"
    motors = [TMC_Z, TMC_X1, TMC_Y1, TMC_Y2]
    current = 9
    assert_current_sent_to_motor(m, axis, motors, current)

def test_multiple_motor_currents_again(m):
    axis = "Y1Y2Xz" # note that "z" is lower case, and won't trigger
    motors = [TMC_X1, TMC_X2, TMC_Y1, TMC_Y2]
    current = 9
    assert_current_sent_to_motor(m, axis, motors, current)

def test_set_current_without_idle_state(m):
    axis = "Y"
    current = 4
    m.s.m_state = "Run"
    m.is_machines_fw_version_equal_to_or_greater_than_version = Mock(return_value=True)
    m.send_command_to_motor = Mock()
    assert not m.set_motor_current(axis, current)

def test_set_current_without_correct_FW(m):
    axis = "Y"
    current = 5
    m.s.m_state = "Idle"
    m.is_machines_fw_version_equal_to_or_greater_than_version = Mock(return_value=False)
    m.send_command_to_motor = Mock()
    assert not m.set_motor_current(axis, current)


# HOMING UNIT TESTS

def test_motor_self_adjustment_disables_y_motors(m):
    # spy on disable y motors
    pass

def test_start_homing(m):
    pass

def test_disable_stall_detection_before_auto_squaring(m):
    pass

def test_start_auto_squaring(m):
    pass

def test_start_calibrating_after_homing(m):
    pass

def test_enable_stall_detection_after_calibrating(m):
    pass

def test_move_to_accommodate_laser_offset(m):
    pass

# def test_schedule_home_seq_event(m):
#     m.next_homing_seq_event = None
#     def nested_func(): pass
#     m.next_homing_seq_event = m.schedule_event(nested_func, 10)
#     assert m.next_homing_seq_event != None


# def test_quick_clock():

#     def nested_func(a): return a
#     new_event = Clock.schedule_once(lambda dt: nested_func(1), 0.01)
#     # another_event = Clock.schedule_once(lambda dt: nested_func(1), 0.01)
#     assert new_event.get_callback() == nested_func
#     l = [new_event]
#     new = [ev for ev in l if nested_func == ev.get_callback()]
#     assert new == []



# def test_unschedule_home_seq_events(m):
#     m.next_homing_seq_event = None
#     def nested_func(): pass
#     m.schedule_event(nested_func, m.next_homing_seq_event, 10)
#     assert m.next_homing_seq_event is not None
#     m.clear_event(m.next_homing_seq_event)
#     assert m.next_homing_seq_event is None

# def test_reschedule_if_busy(m):
#     m.homing_sequence_clocks = []
#     def nested_func(): pass
#     m.smartbench_is_busy = Mock(return_value=True)
#     event = m.reschedule_if_busy(nested_func, delay=0.01)
#     assert event
#     assert event in m.homing_sequence_clocks
#     m.unschedule_home_seq_events()
#     assert m.homing_sequence_clocks == []

