'''
Created on 17 Aug 2022
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
from asmcnc.comms import router_machine
from asmcnc.comms import localization

'''
######################################
RUN FROM easycut-smartbench FOLDER WITH: 
python -m pytest --show-capture=no --disable-pytest-warnings tests/automated_unit_tests/comms/test_serial_connection_process_grbl_push.py
######################################
'''

def construct_status(z_motor_axis = None, x_motor_axis = None, y_axis = None, y1_motor = None, y2_motor = None, x1_motor = None, x2_motor = None):

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

def test_read_in_no_SG_values(sc):
    status = construct_status()
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
    status = construct_status(sg_z_motor_axis, sg_x_motor_axis, sg_y_axis, sg_y1_motor, sg_y2_motor)
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
    status = construct_status(sg_z_motor_axis, sg_x_motor_axis, sg_y_axis, sg_y1_motor, sg_y2_motor, sg_x1_motor, sg_x2_motor)
    sc.process_grbl_push(status)
    assert_all_sg_values_equal(sc, sg_z_motor_axis, sg_x_motor_axis, sg_y_axis, sg_y1_motor, sg_y2_motor, sg_x1_motor, sg_x2_motor)
    assert sc.spindle_mains_frequency_hertz == 7 # ensures that function has continued processing status parts

def test_invalid_values_handled_for_4_drivers(sc):
    sg_z_motor_axis = 30
    sg_x_motor_axis = 31
    sg_y_axis = 32
    sg_y1_motor = 33
    sg_y2_motor = "boop"
    status = construct_status(sg_z_motor_axis, sg_x_motor_axis, sg_y_axis, sg_y1_motor, sg_y2_motor)
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
    status = construct_status(sg_z_motor_axis, sg_x_motor_axis, sg_y_axis, sg_y1_motor, sg_y2_motor, sg_x1_motor, sg_x2_motor)
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
    status = construct_status(*five_driver_list)
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
    status = construct_status(*four_driver_list)
    m.s.record_sg_values_flag = True
    m.s.process_grbl_push(status)
    assert m.temp_sg_array[0] == four_driver_list



