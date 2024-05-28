import logging
"""
Created on 1 Aug 2022
@author: Letty
"""
import os
import sys
from asmcnc.comms.logging_system.logging_system import Logger
from tests import test_utils
sys.path.append('./src')
try:
    import unittest
    import pytest
    from mock import Mock, MagicMock
except:
    Logger.info("Can't import mocking packages, are you on a dev machine?")
from asmcnc.comms import router_machine
from asmcnc.comms import localization
from asmcnc.comms.yeti_grbl_protocol.c_defines import *
from kivy.clock import Clock
"""
######################################
RUN FROM easycut-smartbench FOLDER WITH: 
python -m pytest tests/automated_unit_tests/comms/test_router_machine_units.py
######################################
"""
test_utils.create_app()


@pytest.fixture
def m():
    l = localization.Localization()
    screen_manager = Mock()
    settings_manager = Mock()
    jd = Mock()
    m = router_machine.RouterMachine('COM', screen_manager,
        settings_manager, l, jd)
    m.s.next_poll_time = 0
    m.s.write_direct = Mock()
    m.s.s = MagicMock()
    m.clear_motor_registers = Mock()
    m.is_machines_fw_version_equal_to_or_greater_than_version = Mock(
        return_value=True)
    m.s.m_state = 'Idle'
    return m


def test_close_serial_connection(m):
    m.close_serial_connection(0)
    m.clear_motor_registers.assert_called()


def test_reconnect_serial_connection(m):
    m.reconnect_serial_connection()
    m.clear_motor_registers.assert_called()


def test_construct_calibration_check_file_path(m):
    X_file = m.construct_calibration_check_file_path('X')
    Y_file = m.construct_calibration_check_file_path('Y')
    Z_file = m.construct_calibration_check_file_path('Z')
    assert os.path.exists('./src/' + X_file.strip('.'))
    assert os.path.exists('./src/' + Y_file.strip('.'))
    assert os.path.exists('./src/' + Z_file.strip('.'))


def assert_current_sent_to_motor(machine, axis, motors, current):
    expected_kwargs = []
    for motor in motors:
        expected_kwargs.append({'command': SET_ACTIVE_CURRENT, 'motor':
            motor, 'value': current})
        expected_kwargs.append({'command': SET_IDLE_CURRENT, 'motor': motor,
            'value': current})
    machine.send_command_to_motor = Mock()
    assert machine.set_motor_current(axis, current)
    assert len(machine.send_command_to_motor.call_args_list) == len(
        expected_kwargs)
    for idx, call in enumerate(machine.send_command_to_motor.call_args_list):
        assert call.kwargs == expected_kwargs[idx]


def test_set_X_motor_current_for_axis(m):
    axis = 'X'
    motor_1 = TMC_X1
    motor_2 = TMC_X2
    current = 26
    assert_current_sent_to_motor(m, axis, [motor_1, motor_2], current)


def test_set_X1_motor_current_for_individual_motor(m):
    axis = 'X1'
    motor = TMC_X1
    current = 23
    assert_current_sent_to_motor(m, axis, [motor], current)


def test_set_X2_motor_current_for_individual_motor(m):
    axis = 'X2'
    motor = TMC_X2
    current = 11
    assert_current_sent_to_motor(m, axis, [motor], current)


def test_set_Y_motor_current_for_axis(m):
    axis = 'Y'
    motor_1 = TMC_Y1
    motor_2 = TMC_Y2
    current = 0
    assert_current_sent_to_motor(m, axis, [motor_1, motor_2], current)


def test_set_Y1_motor_current_for_individual_motor(m):
    axis = 'Y1'
    motor = TMC_Y1
    current = 1
    assert_current_sent_to_motor(m, axis, [motor], current)


def test_set_Y2_motor_current_for_individual_motor(m):
    axis = 'Y2'
    motor = TMC_Y2
    current = 14
    assert_current_sent_to_motor(m, axis, [motor], current)


def test_set_Z_motor_current_for_individual_motor(m):
    axis = 'Z'
    motor = TMC_Z
    current = 15
    assert_current_sent_to_motor(m, axis, [motor], current)


def test_multiple_motor_currents(m):
    axis = 'X1YZ'
    motors = [TMC_Z, TMC_X1, TMC_Y1, TMC_Y2]
    current = 9
    assert_current_sent_to_motor(m, axis, motors, current)


def test_multiple_motor_currents_again(m):
    axis = 'Y1Y2Xz'
    motors = [TMC_X1, TMC_X2, TMC_Y1, TMC_Y2]
    current = 9
    assert_current_sent_to_motor(m, axis, motors, current)


def test_set_current_without_idle_state(m):
    axis = 'Y'
    current = 4
    m.s.m_state = 'Run'
    m.is_machines_fw_version_equal_to_or_greater_than_version = Mock(
        return_value=True)
    m.send_command_to_motor = Mock()
    assert not m.set_motor_current(axis, current)


def test_set_current_without_correct_FW(m):
    axis = 'Y'
    current = 5
    m.s.m_state = 'Idle'
    m.is_machines_fw_version_equal_to_or_greater_than_version = Mock(
        return_value=False)
    m.send_command_to_motor = Mock()
    assert not m.set_motor_current(axis, current)


def make_smartbench_not_busy(m):
    m.state = Mock(return_value='Idle')
    m.s.is_sequential_streaming = False
    m.s.write_command_buffer = []
    m.s.write_realtime_buffer = []
    m.s.write_protocol_buffer = []
    m.s.serial_blocks_available = m.s.GRBL_BLOCK_SIZE
    m.s.serial_chars_available = m.s.RX_BUFFER_SIZE
    m.s.grbl_waiting_for_reset = False
    m.is_machine_paused = False


def test_smartbench_is_busy_in_alarm_state(m):
    m.state = Mock(return_value='Alarm')
    assert m.smartbench_is_busy()


def test_smartbench_is_busy_if_sequential_streaming(m):
    m.s.is_sequential_streaming = True
    assert m.smartbench_is_busy()


def test_smartbench_is_busy_if_job_streaming(m):
    m.s.is_job_streaming = True
    assert m.smartbench_is_busy()


def test_smartbench_is_busy_if_command_buffer_full(m):
    m.s.write_command_buffer = ['GRBL']
    assert m.smartbench_is_busy()


def test_smartbench_is_busy_if_realtime_buffer_full(m):
    m.s.write_realtime_buffer = ['GRBL']
    assert m.smartbench_is_busy()


def test_smartbench_is_busy_if_protocol_buffer_full(m):
    m.s.write_protocol_buffer = ['GRBL']
    assert m.smartbench_is_busy()


def test_smartbench_is_busy_if_serial_blocks_not_empty(m):
    m.s.serial_blocks_available = str('14')
    assert m.smartbench_is_busy()


def test_smartbench_is_busy_if_serial_chars_not_empty(m):
    m.s.serial_chars_available = str('20')
    assert m.smartbench_is_busy()


def test_smartbench_is_busy_if_grbl_waiting_for_reset(m):
    m.s.grbl_waiting_for_reset = True
    assert m.smartbench_is_busy()


def test_smartbench_is_busy_if_machine_paused(m):
    m.is_machine_paused = True
    assert m.smartbench_is_busy()


def test_smartbench_is_not_busy(m):
    make_smartbench_not_busy(m)
    assert not m.smartbench_is_busy()


def test_get_grbl_motion_mode_when_G0(m):
    m.jd.grbl_mode_tracker = [(0, 4, 5)]
    assert m.get_grbl_motion_mode() == 0


def test_get_grbl_motion_mode_when_empty_list(m):
    m.jd.grbl_mode_tracker = []
    assert m.get_grbl_motion_mode() is None


def test_get_grbl_motion_mode_when_empty_string(m):
    m.jd.grbl_mode_tracker = [('', 4, 5), (0, 0, 0), (1, 6, 7)]
    assert m.get_grbl_motion_mode() == ''


def test_get_grbl_motion_mode_when_G2(m):
    m.jd.grbl_mode_tracker = [(2, 4, 5), (0, 0, 0), (1, 6, 7)]
    assert m.get_grbl_motion_mode() == 2


def test_get_setting_53_when_does_not_exist(m):
    assert m.get_dollar_setting(53) == 0


def test_get_setting_53_when_1(m):
    m.s.setting_53 = 1
    assert m.get_dollar_setting(53) == 1


def test_get_setting_53_when_0(m):
    m.s.setting_53 = 0
    assert m.get_dollar_setting(53) == 0


def test_start_homing(m):
    m.reschedule_homing_task_if_busy = Mock(return_value=False)
    m.start_homing()


def test_start_auto_squaring(m):
    m.reschedule_homing_task_if_busy = Mock(return_value=False)
    m.start_auto_squaring()


def test_move_to_accommodate_laser_offset(m):
    m.reschedule_homing_task_if_busy = Mock(return_value=False)
    m.is_laser_enabled = True
    m.move_to_accommodate_laser_offset()


def test_schedule_homing_event_works_and_does_not_duplicate_callbacks(m):
    m.homing_seq_events = []

    def nested_func():
        pass
    m.schedule_homing_event(nested_func)
    m.schedule_homing_event(nested_func)
    assert len(m.homing_seq_events) == 1
    assert m.homing_seq_events[0].get_callback() == nested_func


def test_schedule_homing_event_works_and_holds_multiple_funcs(m):
    m.homing_seq_events = []

    def nested_func():
        pass

    def another_nested_func():
        pass
    m.schedule_homing_event(nested_func)
    m.schedule_homing_event(another_nested_func)
    m.schedule_homing_event(nested_func)
    assert len(m.homing_seq_events) == 2
    assert m.homing_seq_events[0].get_callback() == another_nested_func
    assert m.homing_seq_events[1].get_callback() == nested_func


def test_resched_homing_task_if_busy(m):
    m.homing_seq_events == []
    m.smartbench_is_busy = Mock(return_value=True)

    def nested_func():
        pass
    assert m.reschedule_homing_task_if_busy(nested_func, delay=1)
    assert m.homing_seq_events[0].get_callback() == nested_func


def test_resched_homing_task_if_busy_returns_false_if_not_busy(m):
    m.homing_seq_events == []
    m.smartbench_is_busy = Mock(return_value=False)

    def nested_func():
        pass
    assert not m.reschedule_homing_task_if_busy(nested_func, delay=1)
    assert m.homing_seq_events == []


def test_unschedule_homing_events(m):
    m.homing_seq_events = []

    def nested_func():
        pass

    def another_nested_func():
        pass
    m.schedule_homing_event(nested_func)
    m.unschedule_homing_events()
    assert m.homing_seq_events == []


def test_reset_homing_sequence_flags(m):
    m.completed_homing_tasks = [True] * 3
    m.homing_task_idx = 'Dogs'

    def nested_func(dt):
        pass
    m.homing_seq_events = [Clock.schedule_once(nested_func, 1)]
    m.reset_homing_sequence_flags()
    assert m.completed_homing_tasks == []
    assert m.homing_task_idx == 0
    assert m.homing_seq_events == []


def test_do_standard_homing_sequence_with_spys(m):
    m.homing_in_progress = False
    m.reset_homing_sequence_flags = Mock()
    m.reset_pre_homing = Mock()
    m.complete_homing_task = Mock()
    m.do_next_task_in_sequence = Mock()
    m.do_standard_homing_sequence()
    assert m.homing_in_progress
    m.reset_homing_sequence_flags.assert_called()
    m.reset_pre_homing.assert_called()


def test_do_standard_homing_sequence_with_actual_funcs(m):
    m.homing_in_progress = False
    m.do_standard_homing_sequence()
    assert m.homing_in_progress


def test_complete_homing_sequence(m):
    m.reset_homing_sequence_flags()
    m.homing_in_progress = True
    m.reset_homing_sequence_flags = Mock()
    m.complete_homing_sequence()
    m.reset_homing_sequence_flags.assert_called()
    assert not m.homing_in_progress


def test_complete_homing_task_when_busy(m):
    m.reset_homing_sequence_flags()
    m.setup_homing_funcs_list()
    m.homing_task_idx = 0
    m.smartbench_is_busy = Mock(return_value=True)
    m.complete_homing_task()
    assert not m.completed_homing_tasks[m.homing_task_idx]


def test_complete_homing_task_when_idle(m):
    m.reset_homing_sequence_flags()
    m.setup_homing_funcs_list()
    m.homing_task_idx = 3
    m.smartbench_is_busy = Mock(return_value=False)
    m.complete_homing_task()
    assert m.completed_homing_tasks[m.homing_task_idx]


def test_if_last_task_complete(m):
    i = 2
    m.homing_task_idx = i
    m.setup_homing_funcs_list()
    m.completed_homing_tasks[m.homing_task_idx] = True
    assert m.if_last_task_complete()
    assert m.homing_task_idx == i + 1


def test_if_last_task_complete_when_not_ready(m):
    i = 2
    m.homing_task_idx = i
    m.setup_homing_funcs_list()
    m.completed_homing_tasks[m.homing_task_idx] = False
    assert not m.if_last_task_complete()
    assert m.homing_task_idx == i


def test_do_next_task_in_sequence_when_ready(m):
    m.reset_homing_sequence_flags()
    m.setup_homing_funcs_list()
    m.homing_task_idx = 3
    m.if_last_task_complete = Mock(return_value=True)
    m.do_next_task_in_sequence()
    assert m.homing_seq_events[0].get_callback() == m.next_homing_task_wrapper
    assert m.homing_seq_events[1].get_callback() == m.complete_homing_task


def test_do_next_task_in_sequence_with_actual_funcs(m):
    m.reset_homing_sequence_flags()
    m.setup_homing_funcs_list()
    m.homing_task_idx = 4
    m.smartbench_is_busy = Mock(return_value=False)
    m.if_last_task_complete = Mock(return_value=True)
    m.do_next_task_in_sequence()
    assert m.homing_seq_events[1].get_callback() == m.complete_homing_task


def test_do_next_task_in_sequence_when_not_ready(m):
    m.reset_homing_sequence_flags()
    m.setup_homing_funcs_list()
    m.do_next_task_in_sequence()
    assert m.homing_seq_events[0].get_callback() == m.do_next_task_in_sequence


def test_get_is_constant_feed_rate_accel(m):
    feed_override_percentage = 100
    feed_rate = 6000
    last_feed_rate = 8000
    tolerance = 50
    val, last = m.get_is_constant_feed_rate(last_feed_rate,
        feed_override_percentage, feed_rate, tolerance)
    assert last == last_feed_rate
    assert not val


def test_get_is_constant_feed_rate_decel(m):
    feed_override_percentage = 100
    feed_rate = 6000
    last_feed_rate = 4000
    tolerance = 50
    val, last = m.get_is_constant_feed_rate(last_feed_rate,
        feed_override_percentage, feed_rate, tolerance)
    assert last == last_feed_rate
    assert not val


def test_get_is_constant_feed_rate_true_within_range(m):
    feed_override_percentage = 100
    feed_rate = 6000
    last_feed_rate = 6010
    tolerance = 50
    val, last = m.get_is_constant_feed_rate(last_feed_rate,
        feed_override_percentage, feed_rate, tolerance)
    assert last == last_feed_rate
    assert val


def test_get_is_constant_feed_rate_false_when_tolerance_small(m):
    feed_override_percentage = 100
    feed_rate = 6000
    last_feed_rate = 6010
    tolerance = 9
    val, last = m.get_is_constant_feed_rate(last_feed_rate,
        feed_override_percentage, feed_rate, tolerance)
    assert last == last_feed_rate
    assert not val


def test_get_is_constant_feed_rate_true_when_diff_equal_to_tolerance(m):
    feed_override_percentage = 100
    feed_rate = 6000
    tolerance = 10
    last_feed_rate = feed_rate + tolerance
    val, last = m.get_is_constant_feed_rate(last_feed_rate,
        feed_override_percentage, feed_rate, tolerance)
    assert last == last_feed_rate
    assert val


def test_get_z_max_travel_to_bake_when_fw_is_2_5(m):
    assert m.get_z_max_travel_to_bake(False, 27) == 150.0


def test_get_z_max_travel_to_bake_when_fw_is_2_6_but_current_is_low(m):
    assert m.get_z_max_travel_to_bake(True, 26) == 150.0


def test_get_z_max_travel_to_bake_when_fw_is_2_6_and_current_is_27(m):
    assert m.get_z_max_travel_to_bake(True, 27) == 130.0


def test_get_z_max_travel_to_bake_when_fw_is_2_6_and_current_is_0(m):
    assert not m.get_z_max_travel_to_bake(True, 0)


def test_get_z_max_travel_to_bake_when_fw_is_1_and_current_is_0(m):
    assert m.get_z_max_travel_to_bake(False, 0) == 150.0


def test_bake_default_grbl_settings_when_z_max_travel_value_is_false(m):
    m.get_z_max_travel_to_bake = Mock(return_value=False)
    assert not m.bake_default_grbl_settings()


def test_bake_default_grbl_settings_when_z_max_travel_value_is_true(m):
    m.get_z_max_travel_to_bake = Mock(return_value=True)
    assert m.bake_default_grbl_settings()
