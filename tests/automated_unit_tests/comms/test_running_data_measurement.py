'''
Created August 2022
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
from asmcnc.comms import router_machine
from asmcnc.comms import localization
from datetime import datetime
from asmcnc.production.database.payload_publisher import DataPublisher
from asmcnc.production.database.calibration_database import CalibrationDatabase

'''
######################################
RUN FROM easycut-smartbench FOLDER WITH: 
python -m pytest tests/automated_unit_tests/comms/test_running_data_measurement.py
######################################
'''

test_utils.create_app()

# FIXTURES

# SERIAL CONNECTION
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
    return sc_obj

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
    return m

@pytest.fixture
def m_x():
    return -100.0

@pytest.fixture    
def m_y():
    return -200.0

@pytest.fixture    
def m_z():
    return -300.0

@pytest.fixture
def m_x_2():
    return -101.0
        
@pytest.fixture
def m_y_2():
    return -199.0

@pytest.fixture
def m_z_2():
    return -305.0

@pytest.fixture    
def sg_x_motor_axis():
    return 1

@pytest.fixture    
def sg_y_axis():
    return 2

@pytest.fixture    
def sg_y1_motor():
    return 3

@pytest.fixture    
def sg_y2_motor():
    return 4

@pytest.fixture    
def sg_z_motor_axis():
    return 5

@pytest.fixture    
def motor_driver_temp():
    return 6

@pytest.fixture    
def pcb_temp():
    return 7

@pytest.fixture    
def transistor_heatsink_temp():
    return 8

@pytest.fixture    
def feed_rate():
    return 3000

@pytest.fixture
def status_string(m_x, m_y, m_z, feed_rate, sg_z_motor_axis, sg_x_motor_axis, sg_y_axis, sg_y1_motor, sg_y2_motor, motor_driver_temp, pcb_temp, transistor_heatsink_temp):

    status = ('<Idle|MPos:' + \

        str(m_x) + "," + \
        str(m_y) + "," + \
        str(m_z) + "," + \
        "|Bf:35,255" + \
        "|FS:" + str(feed_rate) + ",0" + \
        "|SG:" + \
        str(sg_z_motor_axis) + "," + \
        str(sg_x_motor_axis) + "," + \
        str(sg_y_axis) + "," + \
        str(sg_y1_motor) + "," + \
        str(sg_y2_motor) + \
        "|TC:" + \
        str(motor_driver_temp) + "," + \
        str(pcb_temp) + "," + \
        str(transistor_heatsink_temp) + \
        ">")

    return status

@pytest.fixture
def running_data_element(sc, m_x, m_y, m_z, feed_rate, sg_z_motor_axis, sg_x_motor_axis, sg_y_axis, sg_y1_motor, sg_y2_motor, motor_driver_temp, pcb_temp, transistor_heatsink_temp):

    running_data_single_list = [
        9,
        m_x,
        m_y,
        m_z,
        sg_x_motor_axis,
        sg_y_axis,
        sg_y1_motor,
        sg_y2_motor,
        sg_z_motor_axis,
        motor_driver_temp,
        pcb_temp,
        transistor_heatsink_temp,
        datetime.now(),
        feed_rate
        ]

    return running_data_single_list

@pytest.fixture
def second_pos_data(m_x_2, m_y_2, m_z_2, feed_rate, sg_z_motor_axis, sg_x_motor_axis, sg_y_axis, sg_y1_motor, sg_y2_motor, motor_driver_temp, pcb_temp, transistor_heatsink_temp):

    data_list = [
        9,
        m_x_2,
        m_y_2,
        m_z_2,
        sg_x_motor_axis,
        sg_y_axis,
        sg_y1_motor,
        sg_y2_motor,
        sg_z_motor_axis,
        motor_driver_temp,
        pcb_temp,
        transistor_heatsink_temp,
        datetime.now(),
        feed_rate
        ]

    return data_list


@pytest.fixture
def running_data_element_dict(m_x, m_y, m_z, feed_rate, sg_z_motor_axis, sg_x_motor_axis, sg_y_axis, sg_y1_motor, sg_y2_motor, motor_driver_temp, pcb_temp, transistor_heatsink_temp):

    time_obj = datetime.now()

    status = {
        "Id": "",
        "FTID": 600009,
        "XCoordinate": m_x,
        "YCoordinate": m_y,
        "ZCoordinate": m_z,
        "XDirection": 0,
        "YDirection": 0,
        "ZDirection": 0,
        "XSG": sg_x_motor_axis,
        "YSG": sg_y_axis,
        "Y1SG": sg_y1_motor,
        "Y2SG": sg_y2_motor,
        "ZSG": sg_z_motor_axis,
        "TMCTemperature": motor_driver_temp,
        "PCBTemperature": pcb_temp,
        "MOTTemperature": transistor_heatsink_temp,
        "Timestamp": time_obj.strftime('%Y-%m-%d %H:%M:%S'),
        "Feedrate": feed_rate,
        "XWeight": 0,
        "YWeight": 0,
        "ZWeight": 2
        }

    return status

@pytest.fixture
def second_pos_data_dict(m_x_2, m_y_2, m_z_2, feed_rate, sg_z_motor_axis, sg_x_motor_axis, sg_y_axis, sg_y1_motor, sg_y2_motor, motor_driver_temp, pcb_temp, transistor_heatsink_temp):

    time_obj = datetime.now()

    status = {
        "Id": "",
        "FTID": 600009,
        "XCoordinate": m_x_2,
        "YCoordinate": m_y_2,
        "ZCoordinate": m_z_2,
        "XDirection": 1,
        "YDirection": -1,
        "ZDirection": -1,
        "XSG": sg_x_motor_axis,
        "YSG": sg_y_axis,
        "Y1SG": sg_y1_motor,
        "Y2SG": sg_y2_motor,
        "ZSG": sg_z_motor_axis,
        "TMCTemperature": motor_driver_temp,
        "PCBTemperature": pcb_temp,
        "MOTTemperature": transistor_heatsink_temp,
        "Timestamp": time_obj.strftime('%Y-%m-%d %H:%M:%S'),
        "Feedrate": feed_rate,
        "XWeight": 0,
        "YWeight": 0,
        "ZWeight": 2
        }

    return status

# CUSTOM ASSERTS

def assert_running_data_lists(expected_list, output_list, idx=0):

    assert expected_list[0] == output_list[idx][0]
    assert expected_list[1] == output_list[idx][1]
    assert expected_list[2] == output_list[idx][2]
    assert expected_list[3] == output_list[idx][3]
    assert expected_list[4] == output_list[idx][4]
    assert expected_list[5] == output_list[idx][5]
    assert expected_list[6] == output_list[idx][6]
    assert expected_list[7] == output_list[idx][7]
    assert expected_list[8] == output_list[idx][8]
    assert expected_list[9] == output_list[idx][9]
    assert expected_list[10] == output_list[idx][10]
    assert expected_list[11] == output_list[idx][11] 
    # assert expected_list[12] == output_list[idx][12] # THIS IS DATETIME!!
    assert expected_list[13] == output_list[idx][13] 

# TESTS

def test_process_grbl_push_parses_running_data(sc, status_string, running_data_element):
    sc.measurement_stage = 9
    sc.measure_running_data = True
    sc.process_grbl_push(status_string)
    assert_running_data_lists(running_data_element, sc.running_data)

def test_process_grbl_push_parses_running_data_with_scanner_run(sc, running_data_element):
    sc.s.readline = Mock(return_value = status_string)
    sc.s.inWaiting = Mock(return_value = True)
    sc.measurement_stage = 9
    sc.measure_running_data = True
    sc.grbl_scanner(run_grbl_scanner_once = True)
    assert_running_data_lists(running_data_element, sc.running_data)


def test_machine_starts_and_stops_measurement(m, status_string, running_data_element):
    m.s.s.readline = Mock(return_value = status_string)
    m.s.s.inWaiting = Mock(return_value = True)
    m.start_measuring_running_data(9)
    m.s.grbl_scanner(run_grbl_scanner_once = True)
    m.s.grbl_scanner(run_grbl_scanner_once = True)
    m.s.grbl_scanner(run_grbl_scanner_once = True)
    m.stop_measuring_running_data()
    assert_running_data_lists(running_data_element, m.measured_running_data())
    assert_running_data_lists(running_data_element, m.measured_running_data(), idx=1)
    assert_running_data_lists(running_data_element, m.measured_running_data(), idx=2)

@pytest.mark.xfail(raises=IndexError)
def test_indices_in_running_data(m, status_string, running_data_element):
    m.s.s.readline = Mock(return_value = status_string)
    m.s.s.inWaiting = Mock(return_value = True)
    m.start_measuring_running_data(9)
    m.s.grbl_scanner(run_grbl_scanner_once = True)
    m.s.grbl_scanner(run_grbl_scanner_once = True)
    m.s.grbl_scanner(run_grbl_scanner_once = True)
    m.stop_measuring_running_data()
    assert_running_data_lists(running_data_element, m.measured_running_data(), idx=2)
    m.measured_running_data()[4]

def test_machine_does_not_return_data_during_measurement(m):
    m.start_measuring_running_data()
    assert not m.measured_running_data()

def test_generate_directions(running_data_element, second_pos_data):
    running_data_list = [running_data_element, second_pos_data]
    cdb = CalibrationDatabase()
    x_dir, y_dir, z_dir = cdb.generate_directions(running_data_list,1)

    # -1    FORWARDS/DOWN (AWAY FROM HOME)
    # 0     NOT MOVING
    # 1     BACKWARDS/UP (TOWARDS HOME)

    assert x_dir == 1
    assert y_dir == -1
    assert z_dir == -1

@pytest.mark.skip(reason="Fails on timestamp if running a lot of tests")
def test_process_running_data(running_data_element_dict, running_data_element, second_pos_data, second_pos_data_dict):
    running_data_list = [running_data_element, second_pos_data]
    cdb = CalibrationDatabase()
    cdb._process_running_data(running_data_list, "YS60000")
    assert cdb.processed_running_data["9"][0][0] == running_data_element_dict
    assert cdb.processed_running_data["9"][0][1] == second_pos_data_dict
    assert not cdb.processing_running_data

@pytest.mark.skip(reason="Due to timings, sometimes just fails because thread has not finished yet")
def test_process_status_running_data_for_database_insert(running_data_element, second_pos_data,):
    running_data_list = [running_data_element, second_pos_data]
    cdb = CalibrationDatabase()
    cdb.process_status_running_data_for_database_insert(running_data_list,"YS61111")
    assert not cdb.processing_running_data

@pytest.mark.skip(reason="Takes a lot of time, only test if needed")
def test_process_many_statuses(running_data_element):
    running_data_list = [running_data_element]*10000000
    cdb = CalibrationDatabase()
    cdb._process_running_data(running_data_list, "YS61111")

@pytest.mark.skip(reason="Technically an integration test")
def test_get_stage_id_by_description():
    cdb = CalibrationDatabase()
    cdb.set_up_connection()
    output = cdb.get_stage_id_by_description("StallExperiment")
    assert output == 9

@pytest.mark.skip(reason="Technically an integration test")
def test_publishing_sample_data(running_data_element):
    running_data_list = [running_data_element]*10
    cdb = CalibrationDatabase()
    cdb._process_running_data(running_data_list, "ys60000")
    publisher = DataPublisher("ys60000")
    response_stall_data = publisher.run_data_send(*cdb.processed_running_data["9"])
    assert response_stall_data




