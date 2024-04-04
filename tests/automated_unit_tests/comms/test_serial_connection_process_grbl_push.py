'''
Created on 17 Aug 2022
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

'''
######################################
RUN FROM easycut-smartbench FOLDER WITH: 
python -m pytest tests/automated_unit_tests/comms/test_serial_connection_process_grbl_push.py
To run individual tests add < -k 'test_name_here' >, where test_name_here can be a partial string (that will then match as many tests as it's in)
######################################
'''
test_utils.create_app()

@pytest.fixture
def sc():

    l = localization.Localization()
    machine = Mock()
    screen_manager = Mock()
    settings_manager = Mock()
    job = Mock()
    sc_obj = serial_connection.SerialConnection(machine, screen_manager, settings_manager, l, job)
    sc_obj.s = MagicMock()
    return sc_obj


@pytest.fixture
def m():
    l = localization.Localization()
    screen_manager = Mock()
    settings_manager = Mock()
    job = Mock()
    m = router_machine.RouterMachine("COM", screen_manager, settings_manager, l, job)
    m.s.s = MagicMock()
    m.temp_sg_array = []
    return m


## TEST SG VALUES READ IN PROPERLY 
## --------------------------------

def construct_status_with_sg_values(z_motor_axis = None, x_motor_axis = None, y_axis = None, y1_motor = None, y2_motor = None, x1_motor = None, x2_motor = None):

    # Use this to construct the test status passed out by mock serial object

    if z_motor_axis == None:

        status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822|Sp:1,2,3,4,5,6,7>"

    elif x1_motor == None:

        status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Ld:0|SG:" + \
            str(z_motor_axis) + "," + \
            str(x_motor_axis) + "," + \
            str(y_axis) + "," + \
            str(y1_motor) + "," + \
            str(y2_motor) + \
            "|Sp:1,2,3,4,5,6,7>"

    else:

        status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Ld:0|SG:" + \
            str(z_motor_axis) + "," + \
            str(x_motor_axis) + "," + \
            str(y_axis) + "," + \
            str(y1_motor) + "," + \
            str(y2_motor) + "," + \
            str(x1_motor) + "," + \
            str(x2_motor) + \
            "|Sp:1,2,3,4,5,6,7>"

    return status


def assert_all_sg_values_equal(serial_comms, z_motor_axis = None, x_motor_axis = None, y_axis = None, y1_motor = None, y2_motor = None, x1_motor = None, x2_motor = None):
    
    if z_motor_axis: assert serial_comms.sg_z_motor_axis == z_motor_axis
    if x_motor_axis: assert serial_comms.sg_x_motor_axis == x_motor_axis
    if y_axis: assert serial_comms.sg_y_axis == y_axis
    if y1_motor: assert serial_comms.sg_y1_motor == y1_motor
    if y2_motor: assert serial_comms.sg_y2_motor == y2_motor
    if x1_motor: assert serial_comms.sg_x1_motor == x1_motor
    if x2_motor: assert serial_comms.sg_x2_motor == x2_motor


def test_read_in_no_SG_values(sc):
    status = construct_status_with_sg_values()
    sc.process_grbl_push(status)
    assert_all_sg_values_equal(sc)
    assert sc.spindle_mains_frequency_hertz == 7 # ensures that function has continued processing status parts

def test_read_in_SG_values_upto_y_motors(sc):
    # This is relevant to 4 driver PCBs, which DO NOT report individual x motor loads
    sg_z_motor_axis = 40
    sg_x_motor_axis = 41
    sg_y_axis = 42
    sg_y1_motor = 43
    sg_y2_motor = 44
    status = construct_status_with_sg_values(sg_z_motor_axis, sg_x_motor_axis, sg_y_axis, sg_y1_motor, sg_y2_motor)
    sc.process_grbl_push(status)
    assert_all_sg_values_equal(sc, sg_z_motor_axis, sg_x_motor_axis, sg_y_axis, sg_y1_motor, sg_y2_motor)
    assert sc.spindle_mains_frequency_hertz == 7 # ensures that function has continued processing status parts

def test_read_in_SG_values_for_dual_x_drivers(sc):
    # This is relevant to 5 driver PCBs, which DO report individual x motor loads
    sg_z_motor_axis = 50
    sg_x_motor_axis = 51
    sg_y_axis = 52
    sg_y1_motor = 53
    sg_y2_motor = 54
    sg_x1_motor = 55
    sg_x2_motor = 56
    status = construct_status_with_sg_values(sg_z_motor_axis, sg_x_motor_axis, sg_y_axis, sg_y1_motor, sg_y2_motor, sg_x1_motor, sg_x2_motor)
    sc.process_grbl_push(status)
    assert_all_sg_values_equal(sc, sg_z_motor_axis, sg_x_motor_axis, sg_y_axis, sg_y1_motor, sg_y2_motor, sg_x1_motor, sg_x2_motor)
    assert sc.spindle_mains_frequency_hertz == 7 # ensures that function has continued processing status parts

def test_invalid_values_handled_for_4_drivers(sc):
    sg_z_motor_axis = 30
    sg_x_motor_axis = 31
    sg_y_axis = 32
    sg_y1_motor = 33
    sg_y2_motor = "boop"
    status = construct_status_with_sg_values(sg_z_motor_axis, sg_x_motor_axis, sg_y_axis, sg_y1_motor, sg_y2_motor)
    sc.process_grbl_push(status)
    assert sc.spindle_mains_frequency_hertz == None # ensures that function has stopped processing status parts

def test_invalid_values_handled_for_5_drivers(sc):
    sg_z_motor_axis = 70
    sg_x_motor_axis = 71
    sg_y_axis = 72
    sg_y1_motor = 73
    sg_y2_motor = 71
    sg_x1_motor = "BOOP"
    sg_x2_motor = 76
    status = construct_status_with_sg_values(sg_z_motor_axis, sg_x_motor_axis, sg_y_axis, sg_y1_motor, sg_y2_motor, sg_x1_motor, sg_x2_motor)
    sc.process_grbl_push(status)
    assert sc.spindle_mains_frequency_hertz == None # ensures that function has stopped processing status parts

def test_temp_sg_array_append_5_drivers(m):
    sg_z_motor_axis = 80
    sg_x_motor_axis = 81
    sg_y_axis = 82
    sg_y1_motor = 83
    sg_y2_motor = 84
    sg_x1_motor = 88
    sg_x2_motor = 86
    five_driver_list = [sg_z_motor_axis, sg_x_motor_axis, sg_y_axis, sg_y1_motor, sg_y2_motor, sg_x1_motor, sg_x2_motor]
    status = construct_status_with_sg_values(*five_driver_list)
    m.s.record_sg_values_flag = True
    m.s.process_grbl_push(status)
    assert m.temp_sg_array[0] == five_driver_list

def test_temp_sg_array_append_4_drivers(m):
    sg_z_motor_axis = 62
    sg_x_motor_axis = 63
    sg_y_axis = 64
    sg_y1_motor = 65
    sg_y2_motor = 66
    four_driver_list = [sg_z_motor_axis, sg_x_motor_axis, sg_y_axis, sg_y1_motor, sg_y2_motor, None, None]
    status = construct_status_with_sg_values(*four_driver_list)
    m.s.record_sg_values_flag = True
    m.s.process_grbl_push(status)
    assert m.temp_sg_array[0] == four_driver_list


## TEST MACHINE COORD VALUE CHANGE
## --------------------------------

def default_pos_values(serial_comms):
    serial_comms.x_change = False
    serial_comms.y_change = False
    serial_comms.z_change = False
    serial_comms.m_x = 0.0
    serial_comms.m_y = 0.0
    serial_comms.m_z = 0.0

def test_value_change_x(sc):
    default_pos_values(sc)
    sc.process_grbl_push("<Idle|MPos:4.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ>")
    assert sc.x_change
    assert not sc.y_change
    assert not sc.z_change

def test_value_change_y(sc):
    default_pos_values(sc)
    sc.process_grbl_push("<Idle|MPos:0.000,6.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ>")
    assert not sc.x_change
    assert sc.y_change
    assert not sc.z_change

def test_value_change_z(sc):
    default_pos_values(sc)
    sc.process_grbl_push("<Idle|MPos:0.000,0.000,6.000|Bf:35,255|FS:0,0|Pn:PxXyYZ>")
    assert not sc.x_change
    assert not sc.y_change
    assert sc.z_change

def test_value_no_change_x(sc):
    default_pos_values(sc)
    sc.process_grbl_push("<Idle|MPos:0.000,7.000,8.000|Bf:35,255|FS:0,0|Pn:PxXyYZ>")
    assert not sc.x_change
    assert sc.y_change
    assert sc.z_change

def test_value_no_change_y(sc):
    default_pos_values(sc)
    sc.process_grbl_push("<Idle|MPos:5.000,0.000,6.000|Bf:35,255|FS:0,0|Pn:PxXyYZ>")
    assert sc.x_change
    assert not sc.y_change
    assert sc.z_change

def test_value_no_change_z(sc):
    default_pos_values(sc)
    sc.process_grbl_push("<Idle|MPos:2.000,6.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ>")
    assert sc.x_change
    assert sc.y_change
    assert not sc.z_change
    sc.process_grbl_push("<Idle|MPos:2.000,6.000,8.000|Bf:35,255|FS:0,0|Pn:PxXyYZ>")
    assert sc.z_change
    sc.process_grbl_push("<Idle|MPos:2.000,6.000,8.000|Bf:35,255|FS:0,0|Pn:PxXyYZ>")
    assert not sc.z_change

## TEST PIN VALUES READ IN PROPERLY 
## --------------------------------

def construct_status_with_pns(pins = None):

    # Use this to construct the test status passed out by mock serial object
    status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Ld:0"
    if pins: 
        pin_appendage = "|Pn:" + pins
        status += pin_appendage

    status += ">"

    return status

def assert_pns_neutral(serial_comms, pns):
    if "x" in pns: assert serial_comms.limit_x
    else: assert not serial_comms.limit_x
    if "X" in pns: assert serial_comms.limit_X
    else: assert not serial_comms.limit_X
    if "Z" in pns: assert serial_comms.limit_z
    else: assert not serial_comms.limit_z
    if "P" in pns: assert serial_comms.probe
    else: assert not serial_comms.probe
    if "G" in pns: assert serial_comms.dust_shoe_cover
    else: assert not serial_comms.dust_shoe_cover
    if "g" in pns: assert serial_comms.spare_door
    else: assert not serial_comms.spare_door


def assert_pns_v12(serial_comms, pns):

    assert_pns_neutral(serial_comms, pns)

    if "y" in pns: assert serial_comms.limit_y
    if "Y" in pns: assert serial_comms.limit_Y

    assert not serial_comms.limit_Y_axis
    assert not serial_comms.stall_X
    assert not serial_comms.stall_Z
    assert not serial_comms.stall_Y


def assert_pns_v13(serial_comms, pns):

    assert_pns_neutral(serial_comms, pns)

    if "y" in pns: assert serial_comms.limit_Y_axis
    else: assert not serial_comms.limit_Y_axis
    if "Y" in pns: assert serial_comms.stall_Y
    else: assert not serial_comms.stall_Y
    if "S" in pns: assert serial_comms.stall_X
    else: assert not serial_comms.stall_X
    if "z" in pns: assert serial_comms.stall_Z
    else: assert not serial_comms.stall_Z

def test_pin_selection_together_v12(sc):
    sc.fw_version = "1.4.0"
    pins = "xXZPGgyY"
    status = construct_status_with_pns(pins)
    sc.process_grbl_push(status)
    assert_pns_v12(sc, pins)
    pins = ""
    status = construct_status_with_pns(pins)
    sc.process_grbl_push(status)
    assert_pns_v12(sc, pins)

def test_pin_selection_together_v13(sc):
    sc.fw_version = "2.4.0"
    pins = "xXZPGgyYSz"
    status = construct_status_with_pns(pins)
    sc.process_grbl_push(status)
    assert_pns_v13(sc, pins)
    pins = ""
    status = construct_status_with_pns(pins)
    sc.process_grbl_push(status)
    assert_pns_v13(sc, pins)

def test_pin_selection_singles_v12(sc):
    sc.fw_version = "1.4.0"
    pins = "x"
    status = construct_status_with_pns(pins)
    sc.process_grbl_push(status)
    assert_pns_v12(sc, pins)
    pins = "X"
    status = construct_status_with_pns(pins)
    sc.process_grbl_push(status)
    assert_pns_v12(sc, pins)
    pins = "Z"
    status = construct_status_with_pns(pins)
    sc.process_grbl_push(status)
    assert_pns_v12(sc, pins)
    pins = "P"
    status = construct_status_with_pns(pins)
    sc.process_grbl_push(status)
    assert_pns_v12(sc, pins)
    pins = "G"
    status = construct_status_with_pns(pins)
    sc.process_grbl_push(status)
    assert_pns_v12(sc, pins)
    pins = "g"
    status = construct_status_with_pns(pins)
    sc.process_grbl_push(status)
    assert_pns_v12(sc, pins)
    pins = "y"
    status = construct_status_with_pns(pins)
    sc.process_grbl_push(status)
    assert_pns_v12(sc, pins)
    pins = "Y"
    status = construct_status_with_pns(pins)
    sc.process_grbl_push(status)
    assert_pns_v12(sc, pins)
    pins = ""
    status = construct_status_with_pns(pins)
    sc.process_grbl_push(status)
    assert_pns_v12(sc, pins)


def test_pin_selection_singles_v13(sc):
    sc.fw_version = "2.4.0"
    pins = "x"
    status = construct_status_with_pns(pins)
    sc.process_grbl_push(status)
    assert_pns_v13(sc, pins)
    pins = "X"
    status = construct_status_with_pns(pins)
    sc.process_grbl_push(status)
    assert_pns_v13(sc, pins)
    pins = "Z"
    status = construct_status_with_pns(pins)
    sc.process_grbl_push(status)
    assert_pns_v13(sc, pins)
    pins = "P"
    status = construct_status_with_pns(pins)
    sc.process_grbl_push(status)
    assert_pns_v13(sc, pins)
    pins = "G"
    status = construct_status_with_pns(pins)
    sc.process_grbl_push(status)
    assert_pns_v13(sc, pins)
    pins = "g"
    status = construct_status_with_pns(pins)
    sc.process_grbl_push(status)
    assert_pns_v13(sc, pins)
    pins = "y"
    status = construct_status_with_pns(pins)
    sc.process_grbl_push(status)
    assert_pns_v13(sc, pins)
    pins = "Y"
    status = construct_status_with_pns(pins)
    sc.process_grbl_push(status)
    assert_pns_v13(sc, pins)
    pins = "S"
    status = construct_status_with_pns(pins)
    sc.process_grbl_push(status)
    assert_pns_v13(sc, pins)
    pins = "z"
    status = construct_status_with_pns(pins)
    sc.process_grbl_push(status)
    assert_pns_v13(sc, pins)
    pins = ""
    status = construct_status_with_pns(pins)
    sc.process_grbl_push(status)
    assert_pns_v13(sc, pins)

## TEST OVERRIDE READ IN
## --------------------------------

def construct_status_with_override(feed_ov = None, rapid_ov = None, speed_ov = None):

    # Use this to construct the test status passed out by mock serial object
    status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Ld:0"
    if feed_ov or rapid_ov or speed_ov:

        if feed_ov == None: feed_ov = 100
        if rapid_ov == None: rapid_ov = 100
        if speed_ov == None: speed_ov = 100

        override_appendage = "|Ov:" + str(feed_ov) + "," + str(rapid_ov) + "," + str(speed_ov)
        status += override_appendage

    status += "|TC:1,2>"

    return status

def assert_status_end_processed(serial_comms):
    assert serial_comms.motor_driver_temp == 1
    assert serial_comms.pcb_temp == 2


def test_feed_override_read_in(sc):
    ov = 123
    status = construct_status_with_override(feed_ov=ov)
    sc.process_grbl_push(status)
    assert sc.feed_override_percentage == ov
    assert_status_end_processed(sc)

def test_not_feed_override_read_in(sc):
    ov = 123
    status = construct_status_with_override(rapid_ov=ov, speed_ov=ov)
    sc.process_grbl_push(status)
    assert sc.feed_override_percentage != ov
    assert_status_end_processed(sc)

def test_feed_override_read_in_fails_if_bad(sc):
    ov = ";"
    status = construct_status_with_override(feed_ov=ov)
    sc.process_grbl_push(status)
    assert sc.feed_override_percentage != ov
    assert sc.motor_driver_temp != 1
    assert sc.pcb_temp != 2


def test_speed_override_read_in(sc):
    ov = 123
    status = construct_status_with_override(speed_ov=ov)
    sc.process_grbl_push(status)
    assert sc.speed_override_percentage == ov
    assert_status_end_processed(sc)

def test_not_speed_override_read_in(sc):
    ov = 123
    status = construct_status_with_override(rapid_ov=ov, feed_ov=ov)
    sc.process_grbl_push(status)
    assert sc.speed_override_percentage != ov
    assert_status_end_processed(sc)

def test_speed_override_read_in_fails_if_bad(sc):
    ov = ";"
    status = construct_status_with_override(speed_ov=ov)
    sc.process_grbl_push(status)
    assert sc.feed_override_percentage != ov
    assert sc.motor_driver_temp != 1
    assert sc.pcb_temp != 2

## TEST LINE NUMBER READ IN

def construct_status_with_line_numbers(l=None):

    # Use this to construct the test status passed out by mock serial object
    status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255"

    if l: 
        line_appendage = "|Ln:" + str(l)
        status+=line_appendage

    status += "|FS:0,0|Ld:0|TC:1,2>"

    return status

def test_line_number_read_in(sc):
    status = construct_status_with_line_numbers(123)
    sc.remove_from_g_mode_tracker = Mock()
    sc.process_grbl_push(status)
    assert sc.grbl_ln == 123
    assert_status_end_processed(sc)

def test_line_number_read_in_when_nonsense(sc):
    status = construct_status_with_line_numbers("nonsense")
    sc.process_grbl_push(status)
    assert sc.grbl_ln == None
    assert sc.motor_driver_temp != 1
    assert sc.pcb_temp != 2

def test_line_number_read_in_when_no_number(sc):
    status = construct_status_with_line_numbers()
    sc.process_grbl_push(status)
    assert sc.grbl_ln == None
    assert_status_end_processed(sc)

# TEST INRUSH COUNTER

def construct_status_with_load_string(load_string = ""):
    # Use this to construct the test status passed out by mock serial object
    status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0" + load_string
    status += "|TC:1,2>"
    return status

def test_inrush_counter_0_when_no_load(sc):
    status = construct_status_with_load_string()
    sc.process_grbl_push(status)
    assert sc.inrush_counter == 0

def test_inrush_counter_1_when_1_load(sc):
    sc.inrush_counter == 0
    status = construct_status_with_load_string("|Ld:12,11,1,3")
    sc.process_grbl_push(status)
    assert sc.inrush_counter == 1

def test_inrush_counter_increases_to_max_and_stops(sc):
    sc.inrush_counter = 0
    status = construct_status_with_load_string("|Ld:12,11,1,3")
    for _ in range(sc.inrush_max):
        sc.process_grbl_push(status)
    assert sc.inrush_counter == sc.inrush_max

def test_inrush_counter_resets_after_no_comms(sc):
    sc.inrush_counter = 3
    status = construct_status_with_load_string()
    sc.process_grbl_push(status)
    assert sc.inrush_counter == 0

