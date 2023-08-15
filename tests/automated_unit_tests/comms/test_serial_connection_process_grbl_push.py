import logging

"""
Created on 17 Aug 2022
@author: Letty
"""
import sys

sys.path.append("./src")
try:
    import unittest
    import pytest
    from mock import Mock, MagicMock
except:
    print("Can't import mocking packages, are you on a dev machine?")
from asmcnc.comms import serial_connection
from asmcnc.comms import router_machine
from asmcnc.comms import localization

"""
######################################
RUN FROM easycut-smartbench FOLDER WITH: 
python -m pytest --show-capture=no --disable-pytest-warnings tests/automated_unit_tests/comms/test_serial_connection_process_grbl_push.py
To run individual tests add < -k 'test_name_here' >, where test_name_here can be a partial string (that will then match as many tests as it's in)
######################################
"""


@pytest.fixture
def sc():
    l = localization.Localization()
    machine = Mock()
    screen_manager = Mock()
    settings_manager = Mock()
    job = Mock()
    sc_obj = serial_connection.SerialConnection(
        machine,
        screen_manager,
        settings_manager,
        l,
        job,
        logging.Logger(name="__name__"),
    )
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


# weird test, check with Lettie
def construct_status_with_sg_values(
    z_motor_axis=None,
    x_motor_axis=None,
    y_axis=None,
    y1_motor=None,
    y2_motor=None,
    x1_motor=None,
    x2_motor=None,
):
    if z_motor_axis == None:
        status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822|Sp:1,2,3,4,5,6,7>"
    elif x1_motor == None:
        status = (
            "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Ld:0|SG:"
            + str(z_motor_axis)
            + ","
            + str(x_motor_axis)
            + ","
            + str(y_axis)
            + ","
            + str(y1_motor)
            + ","
            + str(y2_motor)
            + "|Sp:1,2,3,4,5,6,7>"
        )
    else:
        status = (
            "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Ld:0|SG:"
            + str(z_motor_axis)
            + ","
            + str(x_motor_axis)
            + ","
            + str(y_axis)
            + ","
            + str(y1_motor)
            + ","
            + str(y2_motor)
            + ","
            + str(x1_motor)
            + ","
            + str(x2_motor)
            + "|Sp:1,2,3,4,5,6,7>"
        )
    return status


def assert_all_sg_values_equal(
    serial_comms,
    z_motor_axis=None,
    x_motor_axis=None,
    y_axis=None,
    y1_motor=None,
    y2_motor=None,
    x1_motor=None,
    x2_motor=None,
):
    if z_motor_axis:
        assert serial_comms.stall_guard.z_motor_axis == z_motor_axis
    if x_motor_axis:
        assert serial_comms.stall_guard.x_motor_axis == x_motor_axis
    if y_axis:
        assert serial_comms.stall_guard.y_axis == y_axis
    if y1_motor:
        assert serial_comms.stall_guard.y1_motor == y1_motor
    if y2_motor:
        assert serial_comms.stall_guard.y2_motor == y2_motor
    if x1_motor:
        assert serial_comms.stall_guard.x1_motor == x1_motor
    if x2_motor:
        assert serial_comms.stall_guard.x2_motor == x2_motor


def test_read_in_no_SG_values(sc):
    status = construct_status_with_sg_values()
    sc.process_grbl_push(status)
    assert_all_sg_values_equal(sc)
    assert sc.spindle_statistics.mains_frequency_hertz == 7


def test_read_in_SG_values_upto_y_motors(sc):
    sg_z_motor_axis = 40
    sg_x_motor_axis = 41
    sg_y_axis = 42
    sg_y1_motor = 43
    sg_y2_motor = 44
    status = construct_status_with_sg_values(
        sg_z_motor_axis, sg_x_motor_axis, sg_y_axis, sg_y1_motor, sg_y2_motor
    )
    sc.process_grbl_push(status)
    assert_all_sg_values_equal(
        sc, sg_z_motor_axis, sg_x_motor_axis, sg_y_axis, sg_y1_motor, sg_y2_motor
    )
    assert sc.spindle_statistics.mains_frequency_hertz == 7


def test_read_in_SG_values_for_dual_x_drivers(sc):
    sg_z_motor_axis = 50
    sg_x_motor_axis = 51
    sg_y_axis = 52
    sg_y1_motor = 53
    sg_y2_motor = 54
    sg_x1_motor = 55
    sg_x2_motor = 56
    status = construct_status_with_sg_values(
        sg_z_motor_axis,
        sg_x_motor_axis,
        sg_y_axis,
        sg_y1_motor,
        sg_y2_motor,
        sg_x1_motor,
        sg_x2_motor,
    )
    sc.process_grbl_push(status)
    assert_all_sg_values_equal(
        sc,
        sg_z_motor_axis,
        sg_x_motor_axis,
        sg_y_axis,
        sg_y1_motor,
        sg_y2_motor,
        sg_x1_motor,
        sg_x2_motor,
    )
    assert sc.spindle_statistics.mains_frequency_hertz == 7


def test_invalid_values_handled_for_4_drivers(sc):
    sg_z_motor_axis = 30
    sg_x_motor_axis = 31
    sg_y_axis = 32
    sg_y1_motor = 33
    sg_y2_motor = "boop"
    status = construct_status_with_sg_values(
        sg_z_motor_axis, sg_x_motor_axis, sg_y_axis, sg_y1_motor, sg_y2_motor
    )

    with pytest.raises(ValueError):
        sc.process_grbl_push(status)


def test_invalid_values_handled_for_5_drivers(sc):
    sg_z_motor_axis = 70
    sg_x_motor_axis = 71
    sg_y_axis = 72
    sg_y1_motor = 73
    sg_y2_motor = 71
    sg_x1_motor = "BOOP"
    sg_x2_motor = 76
    status = construct_status_with_sg_values(
        sg_z_motor_axis,
        sg_x_motor_axis,
        sg_y_axis,
        sg_y1_motor,
        sg_y2_motor,
        sg_x1_motor,
        sg_x2_motor,
    )

    with pytest.raises(ValueError):
        sc.process_grbl_push(status)


def test_temp_sg_array_append_5_drivers(m):
    sg_z_motor_axis = 80
    sg_x_motor_axis = 81
    sg_y_axis = 82
    sg_y1_motor = 83
    sg_y2_motor = 84
    sg_x1_motor = 88
    sg_x2_motor = 86
    five_driver_list = [
        sg_z_motor_axis,
        sg_x_motor_axis,
        sg_y_axis,
        sg_y1_motor,
        sg_y2_motor,
        sg_x1_motor,
        sg_x2_motor,
    ]
    status = construct_status_with_sg_values(*five_driver_list)
    m.s.RECORD_SG_VALUES_FLAG = True
    m.s.process_grbl_push(status)
    assert m.temp_sg_array[0] == five_driver_list


def test_temp_sg_array_append_4_drivers(m):
    sg_z_motor_axis = 62
    sg_x_motor_axis = 63
    sg_y_axis = 64
    sg_y1_motor = 65
    sg_y2_motor = 66
    four_driver_list = [
        sg_z_motor_axis,
        sg_x_motor_axis,
        sg_y_axis,
        sg_y1_motor,
        sg_y2_motor,
        None,
        None,
    ]
    status = construct_status_with_sg_values(*four_driver_list)
    m.s.RECORD_SG_VALUES_FLAG = True
    m.s.process_grbl_push(status)
    assert m.temp_sg_array[0] == four_driver_list


def default_pos_values(serial_comms):
    serial_comms.machine_position.x_change = False
    serial_comms.machine_position.y_change = False
    serial_comms.machine_position.z_change = False
    serial_comms.machine_position.x = 0.0
    serial_comms.machine_position.y = 0.0
    serial_comms.machine_position.z = 0.0


def test_value_change_x(sc):
    default_pos_values(sc)
    sc.process_grbl_push("<Idle|MPos:4.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ>")
    assert sc.machine_position.x_change
    assert not sc.machine_position.y_change
    assert not sc.machine_position.z_change


def test_value_change_y(sc):
    default_pos_values(sc)
    sc.process_grbl_push("<Idle|MPos:0.000,6.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ>")
    assert not sc.machine_position.x_change
    assert sc.machine_position.y_change
    assert not sc.machine_position.z_change


def test_value_change_z(sc):
    default_pos_values(sc)
    sc.process_grbl_push("<Idle|MPos:0.000,0.000,6.000|Bf:35,255|FS:0,0|Pn:PxXyYZ>")
    assert not sc.machine_position.x_change
    assert not sc.machine_position.y_change
    assert sc.machine_position.z_change


def test_value_no_change_x(sc):
    default_pos_values(sc)
    sc.process_grbl_push("<Idle|MPos:0.000,7.000,8.000|Bf:35,255|FS:0,0|Pn:PxXyYZ>")
    assert not sc.machine_position.x_change
    assert sc.machine_position.y_change
    assert sc.machine_position.z_change


def test_value_no_change_y(sc):
    default_pos_values(sc)
    sc.process_grbl_push("<Idle|MPos:5.000,0.000,6.000|Bf:35,255|FS:0,0|Pn:PxXyYZ>")
    assert sc.machine_position.x_change
    assert not sc.machine_position.y_change
    assert sc.machine_position.z_change


def test_value_no_change_z(sc):
    default_pos_values(sc)
    sc.process_grbl_push("<Idle|MPos:2.000,6.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ>")
    assert sc.machine_position.x_change
    assert sc.machine_position.y_change
    assert not sc.machine_position.z_change
    sc.process_grbl_push("<Idle|MPos:2.000,6.000,8.000|Bf:35,255|FS:0,0|Pn:PxXyYZ>")
    assert sc.machine_position.z_change
    sc.process_grbl_push("<Idle|MPos:2.000,6.000,8.000|Bf:35,255|FS:0,0|Pn:PxXyYZ>")
    assert not sc.machine_position.z_change


def construct_status_with_pns(pins=None):
    status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Ld:0"
    if pins:
        pin_appendage = "|Pn:" + pins
        status += pin_appendage
    status += ">"
    return status


def assert_pns_neutral(serial_comms, pns):
    if "x" in pns:
        assert serial_comms.pin_info.limit_x
    else:
        assert not serial_comms.pin_info.limit_x
    if "X" in pns:
        assert serial_comms.pin_info.limit_X
    else:
        assert not serial_comms.pin_info.limit_X
    if "Z" in pns:
        assert serial_comms.pin_info.limit_z
    else:
        assert not serial_comms.pin_info.limit_z
    if "P" in pns:
        assert serial_comms.pin_info.probe
    else:
        assert not serial_comms.pin_info.probe
    if "G" in pns:
        assert serial_comms.pin_info.dust_shoe_cover
    else:
        assert not serial_comms.pin_info.dust_shoe_cover
    if "g" in pns:
        assert serial_comms.pin_info.spare_door
    else:
        assert not serial_comms.pin_info.spare_door


def assert_pns_v12(serial_comms, pns):
    assert_pns_neutral(serial_comms, pns)
    if "y" in pns:
        assert serial_comms.pin_info.limit_y
    if "Y" in pns:
        assert serial_comms.pin_info.limit_Y
    assert not serial_comms.pin_info.limit_Y_axis
    assert not serial_comms.pin_info.stall_X
    assert not serial_comms.pin_info.stall_Z
    assert not serial_comms.pin_info.stall_Y


def assert_pns_v13(serial_comms, pns):
    assert_pns_neutral(serial_comms, pns)
    if "y" in pns:
        assert serial_comms.pin_info.limit_Y_axis
    else:
        assert not serial_comms.pin_info.limit_Y_axis
    if "Y" in pns:
        assert serial_comms.pin_info.stall_Y
    else:
        assert not serial_comms.pin_info.stall_Y
    if "S" in pns:
        assert serial_comms.pin_info.stall_X
    else:
        assert not serial_comms.pin_info.stall_X
    if "z" in pns:
        assert serial_comms.pin_info.stall_Z
    else:
        assert not serial_comms.pin_info.stall_Z


def test_pin_selection_together_v12(sc):
    sc.versions.firmware = "1.4.0"
    pins = "xXZPGgyY"
    status = construct_status_with_pns(pins)
    sc.process_grbl_push(status)
    assert_pns_v12(sc, pins)
    pins = ""
    status = construct_status_with_pns(pins)
    sc.process_grbl_push(status)
    assert_pns_v12(sc, pins)


def test_pin_selection_together_v13(sc):
    sc.versions.firmware = "2.4.0"
    pins = "xXZPGgyYSz"
    status = construct_status_with_pns(pins)
    sc.process_grbl_push(status)
    assert_pns_v13(sc, pins)
    pins = ""
    status = construct_status_with_pns(pins)
    sc.process_grbl_push(status)
    assert_pns_v13(sc, pins)


def test_pin_selection_singles_v12(sc):
    sc.versions.firmware = "1.4.0"
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
    sc.versions.firmware = "2.4.0"
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


def construct_status_with_override(feed_ov=None, rapid_ov=None, speed_ov=None):
    status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Ld:0"
    if feed_ov or rapid_ov or speed_ov:
        if feed_ov == None:
            feed_ov = 100
        if rapid_ov == None:
            rapid_ov = 100
        if speed_ov == None:
            speed_ov = 100
        override_appendage = (
            "|Ov:" + str(feed_ov) + "," + str(rapid_ov) + "," + str(speed_ov)
        )
        status += override_appendage
    status += "|TC:1,2>"
    return status


def assert_status_end_processed(serial_comms):
    assert serial_comms.temperatures.motor_driver == 1
    assert serial_comms.temperatures.pcb == 2


def test_feed_override_read_in(sc):
    ov = 123
    status = construct_status_with_override(feed_ov=ov)
    sc.process_grbl_push(status)
    assert sc.feeds_and_speeds.feed_override == ov
    assert_status_end_processed(sc)


def test_not_feed_override_read_in(sc):
    ov = 123
    status = construct_status_with_override(rapid_ov=ov, speed_ov=ov)
    sc.process_grbl_push(status)
    assert sc.feeds_and_speeds.feed_override != ov
    assert_status_end_processed(sc)


def test_feed_override_read_in_fails_if_bad(sc):
    ov = ";"
    status = construct_status_with_override(feed_ov=ov)

    with pytest.raises(ValueError):
        sc.process_grbl_push(status)


def test_speed_override_read_in(sc):
    ov = 123
    status = construct_status_with_override(speed_ov=ov)
    sc.process_grbl_push(status)
    assert sc.feeds_and_speeds.speed_override == ov
    assert_status_end_processed(sc)


def test_not_speed_override_read_in(sc):
    ov = 123
    status = construct_status_with_override(rapid_ov=ov, feed_ov=ov)
    sc.process_grbl_push(status)
    assert sc.feeds_and_speeds.speed_override != ov
    assert_status_end_processed(sc)


def test_speed_override_read_in_fails_if_bad(sc):
    ov = ";"
    status = construct_status_with_override(speed_ov=ov)

    with pytest.raises(ValueError):
        sc.process_grbl_push(status)


def construct_status_with_line_numbers(l=None):
    status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255"
    if l:
        line_appendage = "|Ln:" + str(l)
        status += line_appendage
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

    with pytest.raises(ValueError):
        sc.process_grbl_push(status)
    assert sc.grbl_ln == None


def test_line_number_read_in_when_no_number(sc):
    status = construct_status_with_line_numbers()
    sc.process_grbl_push(status)
    assert sc.grbl_ln == None
    assert_status_end_processed(sc)


def construct_status_with_load_string(load_string=""):
    status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0" + load_string
    status += "|TC:1,2>"
    return status


def test_inrush_counter_0_when_no_load(sc):
    status = construct_status_with_load_string()
    sc.process_grbl_push(status)
    assert sc.digital_spindle.inrush_counter == 0


def test_inrush_counter_1_when_1_load(sc):
    sc.digital_spindle.inrush_counter = 0
    sc.digital_spindle.ld_qdA = 1
    status = construct_status_with_load_string("|Ld:12,11,1,3")
    sc.process_grbl_push(status)
    assert sc.digital_spindle.inrush_counter == 1


def test_inrush_counter_increases_to_max_and_stops(sc):
    sc.inrush_counter = 0
    status = construct_status_with_load_string("|Ld:12,11,1,3")
    for _ in range(sc.digital_spindle.inrush_max):
        sc.process_grbl_push(status)
    assert sc.digital_spindle.inrush_counter == sc.digital_spindle.inrush_max
    assert not sc.digital_spindle.in_inrush


def test_inrush_counter_resets_after_no_comms(sc):
    sc.digital_spindle.inrush_counter = 3
    status = construct_status_with_load_string()
    sc.process_grbl_push(status)
    assert sc.digital_spindle.inrush_counter == 0
