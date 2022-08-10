'''
Created on 25 Jan 2022
@author: Letty
'''

import sys
sys.path.append('./src')

try: 
    import unittest
    import pytest
    from mock import Mock, MagicMock

except: 
    print("Can't import mocking packages, are you on a dev machine?")


from asmcnc.comms import serial_connection
from asmcnc.comms import localization

'''
######################################
RUN FROM easycut-smartbench FOLDER WITH: 
python -m pytest --show-capture=no --disable-pytest-warnings tests/automated_unit_tests/comms/test_serial_connection_sequential_streaming_units.py
######################################
'''

@pytest.fixture
def sc():

    l = localization.Localization()
    machine = Mock()
    screen_manager = Mock()
    settings_manager = Mock()
    job = Mock()
    sc_obj = serial_connection.SerialConnection(machine, screen_manager, settings_manager, l, job)
    sc_obj.next_poll_time = 0
    sc_obj.write_direct = Mock()
    sc_obj.s = MagicMock()
    sc_obj.s.inWaiting = Mock(return_value = True)
    sc_obj.s.readline = Mock(return_value = '<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0>')
    return sc_obj

def test_cancel_sequential_stream_clears_sequential_stream_buffer(sc):
    sc._sequential_stream_buffer = ['a']
    sc.cancel_sequential_stream()
    assert sc._sequential_stream_buffer == []

def test_send_next_sequential_stream_with_existing_buffer(sc):
    sc._sequential_stream_buffer = ['a']
    sc.write_direct = Mock()
    sc._send_next_sequential_stream()
    assert sc._sequential_stream_buffer == []

def test_start_sequential_stream(sc):
    sc.start_sequential_stream(['a'])
    assert sc._ready_to_send_first_sequential_stream

def test_grbl_scanner_runs_once_with_testing_flag(sc):
    sc.grbl_scanner(run_grbl_scanner_once = True)
    assert sc.m_state == "Off"

def test_is_buffer_clear(sc):
    sc.grbl_scanner(run_grbl_scanner_once = True)
    assert sc.is_buffer_clear()

def test_grbl_scanner_runs__send_next_sequential_stream(sc):
    sc._send_next_sequential_stream = Mock()
    sc.start_sequential_stream(['a'])
    sc.grbl_scanner(run_grbl_scanner_once = True)
    sc._send_next_sequential_stream.assert_called()

def test_process_grbl_response_calls_send_next_seq_stream(sc):
    sc.start_sequential_stream(['a'])
    sc.grbl_scanner(run_grbl_scanner_once = True)
    sc.s.inWaiting = Mock(return_value = True)
    sc.s.readline = Mock(return_value = 'ok')
    sc._send_next_sequential_stream = Mock()
    sc.grbl_scanner(run_grbl_scanner_once = True)
    sc._send_next_sequential_stream.assert_called()

def test_clean_up_after_buffer_is_empty(sc):
    sc.start_sequential_stream(['a'], True)
    sc.grbl_scanner(run_grbl_scanner_once = True)
    sc.s.inWaiting = Mock(return_value = True)
    sc.s.readline = Mock(return_value = 'ok')
    sc.grbl_scanner(run_grbl_scanner_once = True)
    assert sc._sequential_stream_buffer == []
    assert sc.is_sequential_streaming == False
    assert sc._reset_grbl_after_stream == False
    assert sc._ready_to_send_first_sequential_stream == False
    assert sc._process_oks_from_sequential_streaming == False

def test_clean_up_after_sequential_streaming_is_cancelled(sc):
    sc.start_sequential_stream(['a'], True)
    sc.grbl_scanner(run_grbl_scanner_once = True)
    sc.cancel_sequential_stream()
    assert sc.is_sequential_streaming == False
    assert sc._sequential_stream_buffer == []
    assert sc._reset_grbl_after_stream == False
    assert sc._ready_to_send_first_sequential_stream == False
    assert sc._process_oks_from_sequential_streaming == False

def test_clean_up_after_sequential_streaming_is_cancelled_with_reset(sc):
    sc.start_sequential_stream(['a'])
    sc.grbl_scanner(run_grbl_scanner_once = True)
    sc.m._grbl_soft_reset = Mock()
    sc.cancel_sequential_stream(True)
    assert sc.is_sequential_streaming == False
    assert sc._sequential_stream_buffer == []
    assert sc._reset_grbl_after_stream == False
    assert sc._ready_to_send_first_sequential_stream == False
    assert sc._process_oks_from_sequential_streaming == False
    sc.m._grbl_soft_reset.assert_called()

def test_clean_up_adter_sequential_streaming_is_immediately_cancelled(sc):
    sc.start_sequential_stream(['a'], True)
    sc.cancel_sequential_stream()
    assert sc.is_sequential_streaming == False
    assert sc._sequential_stream_buffer == []
    assert sc._reset_grbl_after_stream == False
    assert sc._ready_to_send_first_sequential_stream == False
    assert sc._process_oks_from_sequential_streaming == False

def test_that_seq_streaming_does_not_start_if_grbl_buffer_occupied(sc):
    sc.start_sequential_stream(['a'], True)
    sc.s.readline = Mock(return_value = '<Idle|MPos:0.000,0.000,0.000|Bf:35,200|FS:0,0>')
    sc._send_next_sequential_stream = Mock()
    sc.grbl_scanner(run_grbl_scanner_once = True)
    sc._send_next_sequential_stream.assert_not_called()

def test_process_grbl_push_detects_reset_has_happened(sc):
    sc.grbl_waiting_for_reset = True
    sc.process_grbl_push("Grbl 1.1f ['$' for help]")
    assert not sc.grbl_waiting_for_reset

def test_process_grbl_push_detects_reset_has_not_happened(sc):
    sc.grbl_waiting_for_reset = True
    sc.process_grbl_push("Grbl needs some help]")
    assert sc.grbl_waiting_for_reset
