'''
Created Aug 2022
@author: Letty
'''

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


from asmcnc.comms import serial_connection
from asmcnc.comms import localization
from asmcnc.job import job_data

'''
######################################
RUN FROM easycut-smartbench FOLDER WITH: 
python -m pytest --show-capture=no --disable-pytest-warnings tests/automated_unit_tests/comms/test_serial_connection_streaming_units.py

For me, this is:
python -m pytest tests/automated_unit_tests/comms/test_serial_connection_streaming_units.py
######################################
'''

test_utils.create_app()

@pytest.fixture
def sc():

    l = localization.Localization()
    machine = Mock()
    screen_manager = Mock()
    settings_manager = Mock()
    jd = job_data.JobData(localization = l, settings_manager = settings_manager)
    sc_obj = serial_connection.SerialConnection(machine, screen_manager, settings_manager, l, jd)
    sc_obj.next_poll_time = 0
    sc_obj.write_direct = Mock()
    sc_obj.s = MagicMock()
    sc_obj.s.inWaiting = Mock(return_value = True)
    sc_obj.s.readline = Mock(return_value = '<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0>')
    return sc_obj

def run_scanner(sc_obj):
    sc_obj.grbl_scanner(run_grbl_scanner_once = True)
    sc_obj.s.inWaiting = Mock(return_value = True)
    sc_obj.s.readline = Mock(return_value = 'ok')

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
    run_scanner(sc)
    sc._send_next_sequential_stream = Mock()
    sc.grbl_scanner(run_grbl_scanner_once = True)
    sc._send_next_sequential_stream.assert_called()

def test_clean_up_after_buffer_is_empty_after_reset_requested(sc):
    sc.start_sequential_stream(['a'], True)
    run_scanner(sc)
    run_scanner(sc)
    sc.grbl_scanner(run_grbl_scanner_once = True)
    assert sc._sequential_stream_buffer == []
    assert not sc.is_sequential_streaming
    assert not sc._reset_grbl_after_stream
    assert not sc._ready_to_send_first_sequential_stream
    assert not sc._process_oks_from_sequential_streaming

def test_clean_up_after_buffer_is_empty_after_end_dwell_requested(sc):
    sc.start_sequential_stream(['a'], end_dwell=True)
    run_scanner(sc)
    run_scanner(sc)
    sc.grbl_scanner(run_grbl_scanner_once = True)
    assert sc._sequential_stream_buffer == []
    assert not sc.is_sequential_streaming
    assert not sc._reset_grbl_after_stream
    assert not sc._ready_to_send_first_sequential_stream
    assert not sc._process_oks_from_sequential_streaming

def test_clean_up_after_sequential_streaming_is_cancelled(sc):
    sc.start_sequential_stream(['a'], True)
    sc.grbl_scanner(run_grbl_scanner_once = True)
    sc.cancel_sequential_stream()
    assert not sc.is_sequential_streaming
    assert sc._sequential_stream_buffer == []
    assert not sc._reset_grbl_after_stream
    assert not sc._ready_to_send_first_sequential_stream
    assert not sc._process_oks_from_sequential_streaming

def test_clean_up_after_sequential_streaming_is_cancelled_with_reset(sc):
    sc.start_sequential_stream(['a', 'b'])
    sc.grbl_scanner(run_grbl_scanner_once = True)
    sc.m._grbl_soft_reset = Mock()
    sc.cancel_sequential_stream(True)
    assert not sc.is_sequential_streaming
    assert sc._sequential_stream_buffer == []
    assert not sc._reset_grbl_after_stream
    assert not sc._ready_to_send_first_sequential_stream
    assert not sc._process_oks_from_sequential_streaming
    sc.m._grbl_soft_reset.assert_called()

def test_clean_up_adter_sequential_streaming_is_immediately_cancelled(sc):
    sc.start_sequential_stream(['a'], True)
    sc.cancel_sequential_stream()
    assert not sc.is_sequential_streaming
    assert sc._sequential_stream_buffer == []
    assert not sc._reset_grbl_after_stream
    assert not sc._ready_to_send_first_sequential_stream
    assert not sc._process_oks_from_sequential_streaming

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

def test_dwell_appended_at_end_of_seq_stream_with_reset_requested(sc):
    sc.start_sequential_stream(['a'], True)
    run_scanner(sc)
    assert sc._sequential_stream_buffer == ["G4 P0.5"]
    assert sc.is_sequential_streaming
    assert sc._reset_grbl_after_stream
    assert not sc._ready_to_send_first_sequential_stream
    assert sc._process_oks_from_sequential_streaming

def test_dwell_appended_at_end_of_seq_stream_with_end_dwell_requested(sc):
    sc.start_sequential_stream(['a'], end_dwell=True)
    run_scanner(sc)
    assert sc._sequential_stream_buffer == ["G4 P0.01"]
    assert sc.is_sequential_streaming
    assert not sc._reset_grbl_after_stream
    assert not sc._ready_to_send_first_sequential_stream
    assert sc._process_oks_from_sequential_streaming

written_gcodes_list = []

@pytest.fixture
def sc_write_spy():

    def write_direct_spy(gcode, realtime = True, show_in_sys = False, show_in_console = False):
        global written_gcodes_list
        if gcode != '?':
            written_gcodes_list.append(gcode)

    l = localization.Localization()
    machine = Mock()
    screen_manager = Mock()
    settings_manager = Mock()
    jd = job_data.JobData(localization = l, settings_manager = settings_manager)
    sc_obj = serial_connection.SerialConnection(machine, screen_manager, settings_manager, l, jd)
    sc_obj.next_poll_time = 0
    sc_obj.write_direct = Mock(side_effect=write_direct_spy)
    sc_obj.s = MagicMock()
    sc_obj.s.inWaiting = Mock(return_value = True)
    sc_obj.s.readline = Mock(return_value = '<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0>')
    return sc_obj

def test_dwell_inserted_into_mixed_block(sc_write_spy):

    stream = ["G90","$1=1","$2=2","$3=3","G91","$2=6","XYZ"]
    expected_dwells = ["G90","$1=1","$2=2","$3=3","G4 P0.5","G91","$2=6","G4 P0.5","XYZ"]
    global written_gcodes_list
    written_gcodes_list = []

    sc_write_spy.start_sequential_stream(stream)
    run_scanner(sc_write_spy)
    run_scanner(sc_write_spy)
    run_scanner(sc_write_spy)
    run_scanner(sc_write_spy)
    run_scanner(sc_write_spy)
    run_scanner(sc_write_spy)
    run_scanner(sc_write_spy)
    run_scanner(sc_write_spy)
    run_scanner(sc_write_spy)

    assert written_gcodes_list == expected_dwells

def test_dwell_inserted_into_mixed_block_with_reset(sc_write_spy):

    stream = ["G90","$1=1","$2=2","$3=3","G91","$2=6","XYZ","$6=8"]
    expected_dwells = ["G90","$1=1","$2=2","$3=3","G4 P0.5","G91","$2=6","G4 P0.5","XYZ","$6=8","G4 P0.5"]
    global written_gcodes_list
    written_gcodes_list = []

    sc_write_spy.start_sequential_stream(stream, True)
    run_scanner(sc_write_spy)
    run_scanner(sc_write_spy)
    run_scanner(sc_write_spy)
    run_scanner(sc_write_spy)
    run_scanner(sc_write_spy)
    run_scanner(sc_write_spy)
    run_scanner(sc_write_spy)
    run_scanner(sc_write_spy)
    run_scanner(sc_write_spy)
    run_scanner(sc_write_spy)
    run_scanner(sc_write_spy)
    run_scanner(sc_write_spy)
    run_scanner(sc_write_spy)

    assert written_gcodes_list == expected_dwells

@pytest.fixture
def sc_test_index_error():

    l = localization.Localization()
    machine = Mock()
    screen_manager = Mock()
    settings_manager = Mock()
    jd = job_data.JobData(localization = l, settings_manager = settings_manager)
    sc_obj = serial_connection.SerialConnection(machine, screen_manager, settings_manager, l, jd)
    sc_obj.next_poll_time = 0

    def write_direct_mock(gcode, realtime = True, show_in_sys = False, show_in_console = False):
        del sc_obj._sequential_stream_buffer

    sc_obj.write_direct = Mock(side_effect=write_direct_mock)
    sc_obj.s = MagicMock()
    sc_obj.s.inWaiting = Mock(return_value = True)
    sc_obj.s.readline = Mock(return_value = '<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0>')
    return sc_obj

def test_getting_index_error(sc_test_index_error):
    sc_test_index_error.start_sequential_stream(['a', 'b'])
    sc_test_index_error._after_grbl_settings_insert_dwell = Mock(return_value=False)
    run_scanner(sc_test_index_error)
    assert sc_test_index_error._sequential_stream_buffer == []
    sc_test_index_error._after_grbl_settings_insert_dwell.assert_not_called()

def test_after_grbl_settings_insert_dwell(sc):
    sc._sequential_stream_buffer = ["a$", "G"]
    assert not sc._after_grbl_settings_insert_dwell()
    sc._sequential_stream_buffer = ["$", "G"]
    assert sc._after_grbl_settings_insert_dwell()
    sc._sequential_stream_buffer = ["$"]
    assert sc._after_grbl_settings_insert_dwell()
    sc._sequential_stream_buffer = ["$","$"]
    assert not sc._after_grbl_settings_insert_dwell()
    sc._sequential_stream_buffer = ["G","$"]
    assert not sc._after_grbl_settings_insert_dwell()

# LINE COUNTING

def test_buffer_stuffer_with_line_number_tracking(sc_write_spy):
    test_gcode = ["G90", "G0X4Y5F100", "AE", "G1", "G91"]
    expected_line_count = ["N0G90", "N1G0X4Y5F100", "AE", "N3G1", "N4G91"]
    global written_gcodes_list
    written_gcodes_list = []

    sc_write_spy.l_count = 0
    sc_write_spy.c_line = []
    sc_write_spy.jd.job_gcode_running = test_gcode
    sc_write_spy.stuff_buffer()
    assert written_gcodes_list == expected_line_count

def test_gcode_line_is_excluded(sc):

    uncountable_gcodes = [
        '(',
        ')',
        '$',
        'AE',
        'AF',
        '*L'
    ]
    number_gcodes = 1
    for line in uncountable_gcodes:
        assert sc.gcode_line_is_excluded(line)
    assert sc.gcode_line_is_excluded("(AHHH)")

def test_gcode_line_is_not_excluded(sc):
    assert not sc.gcode_line_is_excluded("G90")
    assert not sc.gcode_line_is_excluded("GX1Y4F600")
    assert not sc.gcode_line_is_excluded("GX1Y4F600")

def test_add_line_number_to_gcode_line(sc):
    assert sc.add_line_number_to_gcode_line("G1", 4) == "N4G1"
    assert sc.add_line_number_to_gcode_line("AE", 2) == "AE"
    assert sc.add_line_number_to_gcode_line("*LFFFFFF", 3) == "*LFFFFFF"


# GRBL mode tracking

def construct_status_with_line_numbers_feeds_speeds(l=None, f=0, s=0):

    # Use this to construct the test status passed out by mock serial object
    status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255"

    if l != None: 
        line_appendage = "|Ln:" + str(l)
        status+=line_appendage

    status += "|FS:"+str(f)+","+str(s)+"|Ld:0|TC:1,2>"

    return status

def assert_process_data_matches_ln(ser_con, modes, n):
    ser_con.process_grbl_push(construct_status_with_line_numbers_feeds_speeds(n, modes[n][1], modes[n][2]))
    assert ser_con.grbl_ln == n
    assert ser_con.jd.grbl_mode_tracker[0] == modes[n]


def test_grbl_mode_tracking_over_scanner_run(sc):

    expected_modes = [
                    (0,6,7),   #1
                    (1,6,8),   #2
                    (0,7,9),   #3
                    (2,8,9),   #4
                    (0,9,11),  #5
                    (0,10,19) #6
    ]

    test_gcode = [
                    "G0X4Y5F" + str(expected_modes[0][1]) + "S" + str(expected_modes[0][2]),
                    "G1X4Y5" + "S" + str(expected_modes[1][2]),
                    "G0X4Y5F" + str(expected_modes[2][1]) + "S" + str(expected_modes[2][2]),
                    "G02X4Y5F" + str(expected_modes[3][1]),
                    "F" + str(expected_modes[4][1]) + "G0X4Y5" + "S" + str(expected_modes[4][2]),
                    "G0X4Y5F" + str(expected_modes[5][1]) + "S" + str(expected_modes[5][2])
    ]

    sc.jd.grbl_mode_tracker = []
    sc.grbl_ln = None
    sc.last_sent_motion_mode = ""
    sc.last_sent_feed = 0
    sc.last_sent_speed = 0
    sc.jd.job_gcode_running = test_gcode
    sc._reset_counters()
    sc.stuff_buffer()

    # If it gets to here then the output has worked correctly
    assert sc.jd.grbl_mode_tracker == expected_modes

    # Now to test that line number read in is working as expected
    assert_process_data_matches_ln(sc, expected_modes, 0)
    assert_process_data_matches_ln(sc, expected_modes, 0)
    assert_process_data_matches_ln(sc, expected_modes, 0)
    assert_process_data_matches_ln(sc, expected_modes, 1)
    assert_process_data_matches_ln(sc, expected_modes, 1)
    assert_process_data_matches_ln(sc, expected_modes, 3)
    assert_process_data_matches_ln(sc, expected_modes, 4)

def test_grbl_mode_tracking_over_scanner_run_with_jump_from_no_ln_no_to_start(sc):

    expected_modes = [
                    (0,6,7),   #1
                    (0,6,8),   #2
                    (0,7,9),   #3
                    (0,8,9),   #4
                    (0,9,11),  #5
                    (0,10,19) #6
    ]

    test_gcode = [
                    "G0X4Y5F" + str(expected_modes[0][1]) + "S" + str(expected_modes[0][2]),
                    "G0X4Y5" + "S" + str(expected_modes[1][2]),
                    "G0X4Y5F" + str(expected_modes[2][1]) + "S" + str(expected_modes[2][2]),
                    "G0X4Y5F" + str(expected_modes[3][1]),
                    "G0X4Y5F" + str(expected_modes[4][1]) + "S" + str(expected_modes[4][2]),
                    "G0X4Y5F" + str(expected_modes[5][1]) + "S" + str(expected_modes[5][2])
    ]

    sc.jd.grbl_mode_tracker = []
    sc.grbl_ln = None
    sc.last_sent_motion_mode = ""
    sc.last_sent_feed = 0
    sc.last_sent_speed = 0
    sc.jd.job_gcode_running = test_gcode
    sc._reset_counters()
    sc.stuff_buffer()

    # If it gets to here then the output has worked correctly
    assert sc.jd.grbl_mode_tracker == expected_modes

    # Now to test that line number read in is working as expected
    assert_process_data_matches_ln(sc, expected_modes, 3)
    assert_process_data_matches_ln(sc, expected_modes, 4)
    assert_process_data_matches_ln(sc, expected_modes, 5)

def test_is_spindle_speed_in_line(sc):
    assert sc.get_grbl_float("GX1Y4S600F80", sc.speed_pattern) == 600

def test_is_spindle_speed_in_line_float(sc):
    assert sc.get_grbl_float("GX1Y4S80000.9876F90", sc.speed_pattern) == 80000.9876
    assert sc.get_grbl_float("M3S16000", sc.speed_pattern) == 16000
    assert sc.get_grbl_float("S18000M3", sc.speed_pattern) == 18000

def test_is_feed_rate_in_line(sc):
    assert sc.get_grbl_float("G0X1Y4F600Y9S0", sc.feed_pattern) == 600

def test_is_feed_rate_in_line_float(sc):
    assert sc.get_grbl_float("G91F9000.9876X6Y7S3", sc.feed_pattern) == 9000.9876

def test_get_motion_mode_for_line(sc):
    assert sc.get_grbl_mode("G1X6Y7", sc.g_motion_pattern) == 1
    assert sc.get_grbl_mode("G02X6Y7", sc.g_motion_pattern) == 2
    assert sc.get_grbl_mode("G00X6Y7", sc.g_motion_pattern) == 0
    assert sc.get_grbl_mode("G011X6Y7", sc.g_motion_pattern) == None
    assert sc.get_grbl_mode("G20X6Y7", sc.g_motion_pattern) == None
    assert sc.get_grbl_mode("GX4X6Y7", sc.g_motion_pattern) == None
    assert sc.get_grbl_mode("GX3X6Y7", sc.g_motion_pattern) == None
    assert sc.get_grbl_mode("G91F66X7Y7G2S20.67F600", sc.g_motion_pattern) == 2

def test_scrape_last_sent_modes_no_new_info(sc):
    sc.scrape_last_sent_modes("G91")
    assert sc.last_sent_feed == 0
    assert sc.last_sent_speed == 0
    assert sc.last_sent_motion_mode == ""

def test_scrape_last_sent_modes_changing_info(sc):
    sc.last_sent_feed = 6
    sc.last_sent_speed = 6
    sc.last_sent_motion_mode = 2
    sc.scrape_last_sent_modes("G3F700.89")
    assert sc.last_sent_feed == 700.89
    assert sc.last_sent_speed == 6
    assert sc.last_sent_motion_mode == 3
    sc.scrape_last_sent_modes("M3S23000")
    assert sc.last_sent_feed == 700.89
    assert sc.last_sent_speed == 23000
    assert sc.last_sent_motion_mode == 3
    sc.scrape_last_sent_modes("G0S0X1Y6")
    assert sc.last_sent_feed == 700.89
    assert sc.last_sent_speed == 0
    assert sc.last_sent_motion_mode == 0
    sc.scrape_last_sent_modes("G1S20.90F5000")
    assert sc.last_sent_feed == 5000
    assert sc.last_sent_speed == 20.90
    assert sc.last_sent_motion_mode == 1
    sc.scrape_last_sent_modes("G2X800Y700")
    assert sc.last_sent_feed == 5000
    assert sc.last_sent_speed == 20.90
    assert sc.last_sent_motion_mode == 2

def test_add_to_g_mode_tracker(sc):
    sc.jd.grbl_mode_tracker = []
    sc.add_to_g_mode_tracker(0,5,7)
    assert sc.jd.grbl_mode_tracker == [(0,5,7)]
    sc.add_to_g_mode_tracker(1,400,6)
    assert sc.jd.grbl_mode_tracker == [(0,5,7), (1,400,6)]
    assert sc.jd.grbl_mode_tracker[0][1] == 5

def test_remove_from_g_mode_tracker_with_change(sc):
    sc.jd.grbl_mode_tracker = [
                                (0,7,8),
                                (0,7,9),
                                (1,7,9),
    ]

    sc.remove_from_g_mode_tracker(4-3)
    assert sc.jd.grbl_mode_tracker == [
                                (0,7,9),
                                (1,7,9),
    ]

def test_remove_from_g_mode_tracker_with_0_to_1_change(sc):
    sc.jd.grbl_mode_tracker = [
                                (0,7,8),
                                (0,7,9),
                                (1,7,9),
    ]

    sc.remove_from_g_mode_tracker(1-0)
    assert sc.jd.grbl_mode_tracker == [
                                (0,7,9),
                                (1,7,9),
    ]

def test_remove_from_g_mode_tracker_with_no_change(sc):
    sc.jd.grbl_mode_tracker = [
                                (0,7,9),
                                (1,7,9),
    ]

    sc.remove_from_g_mode_tracker(10-10)
    assert sc.jd.grbl_mode_tracker == [
                                (0,7,9),
                                (1,7,9),
    ]


def test_remove_from_g_mode_tracker_with_line_skip(sc):
    sc.jd.grbl_mode_tracker = [
                                (0,7,8),
                                (0,7,9),
                                (1,7,9),
    ]

    sc.remove_from_g_mode_tracker(5-3)
    assert sc.jd.grbl_mode_tracker == [
                                (1,7,9),
    ]

def test_remove_from_g_mode_tracker_at_job_start(sc):
    sc.jd.grbl_mode_tracker = [
                                (0,7,8),
                                (0,7,9),
                                (1,7,9),
    ]

    sc.remove_from_g_mode_tracker(0-0)
    assert sc.jd.grbl_mode_tracker == [
                                (0,7,8),
                                (0,7,9),
                                (1,7,9),
    ]


# Test YP impartiality
## If serial comms is run from any production jigs, they don't use or need yp
## it's important that serial comms can still run even if yp == None. 

def test_yp_is_use_yp_when_yp_none(sc):
    sc.yp = None
    assert not sc.is_use_yp()

def test_yp_is_use_yp_when_yp_not_none(sc):
    sc.yp = Mock()
    sc.yp.use_yp = True
    assert sc.is_use_yp()

def test_yp_set_use_yp_false(sc):
    sc.yp = Mock()
    sc.yp.use_yp = True
    sc.set_use_yp(False)
    assert not sc.yp.use_yp

def test_yp_set_use_yp_true(sc):
    sc.yp = Mock()
    sc.yp.use_yp = False
    sc.set_use_yp(True)
    assert sc.yp.use_yp

def test_yp_grbl_scanner_when_yp_none(sc):
    # pass this: if (self.is_job_streaming and not self.m.is_machine_paused and not "Alarm" in self.m.state()):
    sc.is_job_streaming = True
    sc.m.is_machine_paused = False
    sc.m.state = Mock(return_value="Idle")

    sc.g_count = 0 # prevent end_stream from running
    sc.l_count = 1 # prevent end_stream from running

    sc.yp = None
    sc.grbl_scanner(run_grbl_scanner_once=True)

def test_yp_check_job_yp_is_none(sc):
    sc.yp = None
    sc.check_job([])

def test_yp_check_job_yp_exists(sc):
    sc.yp = Mock()
    sc.yp.use_yp = True
    sc.check_job([])
    assert not sc.yp.use_yp

def test_yp_end_stream_is_none(sc):
    sc.yp = None
    sc.update_machine_runtime = Mock()
    sc.end_stream()

def test_yp_cancel_stream_is_none(sc):
    sc.yp = None
    sc.update_machine_runtime = Mock()
    sc.cancel_stream()

def test_yp_end_stream_exists(sc):
    sc.yp = Mock()
    sc.yp.use_yp = True
    sc.update_machine_runtime = Mock()
    sc.end_stream()
    assert not sc.yp.use_yp

def test_yp_cancel_stream_exists(sc):
    sc.yp = Mock()
    sc.yp.use_yp = True
    sc.update_machine_runtime = Mock()
    sc.cancel_stream()
    assert not sc.yp.use_yp