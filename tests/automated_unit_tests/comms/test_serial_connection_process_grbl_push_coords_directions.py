'''
Created on 13 Sep 2022
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
python -m pytest --show-capture=no --disable-pytest-warnings tests/automated_unit_tests/comms/test_serial_connection_process_grbl_push_coords_directions.py
######################################
'''

def construct_status(x_pos=0.0,y_pos=0.0,z_pos=0.0,\
    z_motor_axis=0,x_motor_axis=0,y_axis=0,y1_motor=0,y2_motor=0,x1_motor=0,x2_motor=0):

	status = "<Idle|MPos:" + \
		str(x_pos) + ","+ \
		str(y_pos) + ","+ \
		str(z_pos) + ","+ \
		"|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822|SG:" + \
        str(z_motor_axis) + "," + \
        str(x_motor_axis) + "," + \
        str(y_axis) + "," + \
        str(y1_motor) + "," + \
        str(y2_motor) + "," + \
        str(x1_motor) + "," + \
        str(x2_motor) + \
        "|Sp:1,2,3,4,5,6,7>"

	return status


def construct_status_single_x_driver(x_pos=0.0,y_pos=0.0,z_pos=0.0,\
    z_motor_axis=0,x_motor_axis=0,y_axis=0,y1_motor=0,y2_motor=0):

    status = "<Idle|MPos:" + \
        str(x_pos) + ","+ \
        str(y_pos) + ","+ \
        str(z_pos) + ","+ \
        "|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822|SG:" + \
        str(z_motor_axis) + "," + \
        str(x_motor_axis) + "," + \
        str(y_axis) + "," + \
        str(y1_motor) + "," + \
        str(y2_motor) + \
        "|Sp:1,2,3,4,5,6,7>"

    return status

def assert_positions_equal(sc_obj, x_pos=0.0, y_pos=0.0, z_pos=0.0):
	assert sc_obj.m_x == str(x_pos)
	assert sc_obj.m_y == str(y_pos)
	assert sc_obj.m_z == str(z_pos)

# Coordinates
@pytest.fixture
def m_x(): return -100.0
@pytest.fixture    
def m_y(): return -200.0
@pytest.fixture    
def m_z(): return -300.0
@pytest.fixture
def m_x_2(): return -101.0
@pytest.fixture
def m_y_2(): return -199.0
@pytest.fixture
def m_z_2(): return -305.0

# SG peaks dependent on directions
@pytest.fixture
def sg_x(): return -1
@pytest.fixture    
def sg_y(): return -2
@pytest.fixture    
def sg_z(): return -3
@pytest.fixture
def sg_x_2(): return 1
@pytest.fixture
def sg_y_2(): return 2
@pytest.fixture
def sg_z_2(): return 3
@pytest.fixture
def sg_x1(): return -4
@pytest.fixture    
def sg_y1(): return -5
@pytest.fixture
def sg_x1_2(): return 4
@pytest.fixture
def sg_y1_2(): return 5
@pytest.fixture
def sg_x2(): return -6
@pytest.fixture    
def sg_y2(): return -7
@pytest.fixture
def sg_x2_2(): return 6
@pytest.fixture
def sg_y2_2(): return 7

@pytest.fixture
def sc(scope="module"):

    l = localization.Localization()
    machine = Mock()
    screen_manager = Mock()
    settings_manager = Mock()
    job = Mock()
    sc_obj = serial_connection.SerialConnection(machine, screen_manager, settings_manager, l, job)
    sc_obj.s = MagicMock()
    return sc_obj

def test_read_in_position_values(sc):
    status = construct_status()
    sc.process_grbl_push(status)
    assert_positions_equal(sc)

def test_directions_are_zero(sc):
    status = construct_status()
    sc.process_grbl_push(status)
    assert sc.x_dir == 0
    assert sc.y_dir == 0
    assert sc.z_dir == 0

def test_directions(sc, m_x, m_y, m_z, m_x_2, m_y_2, m_z_2):
    status = construct_status(m_x, m_y, m_z)
    sc.process_grbl_push(status)

    # test one way
    status = construct_status(m_x_2, m_y_2, m_z_2)    
    sc.process_grbl_push(status)
    assert sc.x_dir == 1
    assert sc.y_dir == -1
    assert sc.z_dir == -1

    # test opposite way
    status = construct_status(m_x, m_y, m_z)
    sc.process_grbl_push(status)
    assert sc.x_dir == -1
    assert sc.y_dir == 1
    assert sc.z_dir == 1

    # test zero when stationary
    sc.process_grbl_push(status)
    assert sc.x_dir == 0
    assert sc.y_dir == 0
    assert sc.z_dir == 0

def test_peak_sg_values(sc,m_x,m_y,m_z,m_x_2,m_y_2,m_z_2,\
    sg_x,sg_y,sg_z,sg_x_2,sg_y_2,sg_z_2,sg_x1,sg_y1,sg_x1_2,\
    sg_y1_2,sg_x2,sg_y2,sg_x2_2,sg_y2_2):
    
    # This is all testing same code block, just playing with forward and back and dual driver x values
    sc.record_live_sg_peaks_flag = True
    default = -999

    # Drive each axis one way
    status = construct_status_single_x_driver(m_x, m_y, m_z, sg_z, sg_x, sg_y, sg_y1, sg_y2)
    sc.process_grbl_push(status)
    status = construct_status_single_x_driver(m_x_2, m_y_2, m_z_2, sg_z_2, sg_x_2, sg_y_2, sg_y1_2, sg_y2_2)
    sc.process_grbl_push(status)
    assert sc.fw_peak_sg_z_motor_axis == sg_z_2
    assert sc.bw_peak_sg_x_motor_axis == sg_x_2
    assert sc.fw_peak_sg_y_axis == sg_y_2
    assert sc.fw_peak_sg_y1_motor == sg_y1_2
    assert sc.fw_peak_sg_y2_motor == sg_y2_2
    assert sc.bw_peak_sg_z_motor_axis == default
    assert sc.fw_peak_sg_x_motor_axis == default
    assert sc.bw_peak_sg_y_axis == sg_y
    assert sc.bw_peak_sg_y1_motor == sg_y1
    assert sc.bw_peak_sg_y2_motor == sg_y2
    assert sc.fw_peak_sg_x1_motor == default
    assert sc.fw_peak_sg_x2_motor == default
    assert sc.bw_peak_sg_x1_motor == default
    assert sc.bw_peak_sg_x2_motor == default

    # Drive opposite way
    status = construct_status(m_x, m_y, m_z, sg_z, sg_x, sg_y, sg_y1, sg_y2_2, sg_x1, sg_x2)
    sc.process_grbl_push(status)
    assert sc.bw_peak_sg_z_motor_axis == sg_z
    assert sc.fw_peak_sg_x_motor_axis == sg_x
    assert sc.fw_peak_sg_z_motor_axis == sg_z_2
    assert sc.bw_peak_sg_x_motor_axis == sg_x_2
    assert sc.fw_peak_sg_y_axis == sg_y_2
    assert sc.fw_peak_sg_y1_motor == sg_y1_2
    assert sc.fw_peak_sg_y2_motor == sg_y2_2
    assert sc.bw_peak_sg_y_axis == sg_y
    assert sc.bw_peak_sg_y1_motor == sg_y1
    assert sc.bw_peak_sg_y2_motor == sg_y2_2
    assert sc.fw_peak_sg_x1_motor == sg_x1
    assert sc.fw_peak_sg_x2_motor == sg_x2
    assert sc.bw_peak_sg_x1_motor == default
    assert sc.bw_peak_sg_x2_motor == default

    # Stay static, but send a different sg value and confirm no change
    status = construct_status(m_x, m_y, m_z, sg_z_2, sg_x_2, sg_y_2, sg_y1_2, sg_y2_2)
    sc.process_grbl_push(status)
    assert sc.bw_peak_sg_z_motor_axis == sg_z
    assert sc.fw_peak_sg_x_motor_axis == sg_x
    assert sc.fw_peak_sg_z_motor_axis == sg_z_2
    assert sc.bw_peak_sg_x_motor_axis == sg_x_2
    assert sc.fw_peak_sg_y_axis == sg_y_2
    assert sc.fw_peak_sg_y1_motor == sg_y1_2
    assert sc.fw_peak_sg_y2_motor == sg_y2_2
    assert sc.bw_peak_sg_y_axis == sg_y
    assert sc.bw_peak_sg_y1_motor == sg_y1
    assert sc.bw_peak_sg_y2_motor == sg_y2_2
    assert sc.fw_peak_sg_x1_motor == sg_x1
    assert sc.fw_peak_sg_x2_motor == sg_x2
    assert sc.bw_peak_sg_x1_motor == default
    assert sc.bw_peak_sg_x2_motor == default

    # Drive one way, and then the other, and check bw peaks for dual x drivers
    status = construct_status_single_x_driver(m_x_2, m_y_2, m_z_2, sg_z_2, sg_x_2, sg_y_2, sg_y1_2, sg_y2_2)
    sc.process_grbl_push(status)
    status = construct_status(m_x, m_y, m_z, sg_z_2, sg_x_2, sg_y_2, sg_y1_2, sg_y2_2)
    sc.process_grbl_push(status)
    assert sc.bw_peak_sg_x1_motor == 0
    assert sc.bw_peak_sg_x2_motor == 0


def test_min_sg_values(sc,m_x,m_y,m_z,m_x_2,m_y_2,m_z_2,\
    sg_x,sg_y,sg_z,sg_x_2,sg_y_2,sg_z_2,sg_x1,sg_y1,sg_x1_2,\
    sg_y1_2,sg_x2,sg_y2,sg_x2_2,sg_y2_2):
    
    # This is all testing same code block, just playing with forward and back and dual driver x values
    sc.record_live_sg_peaks_flag = True
    default = 1023

    # Drive each axis one way
    status = construct_status_single_x_driver(m_x_2, m_y_2, m_z_2, sg_z_2, sg_x_2, sg_y_2, sg_y1_2, sg_y2_2)
    sc.process_grbl_push(status)
    
    assert sc.fw_min_sg_x_motor_axis == default
    
    status = construct_status_single_x_driver(m_x, m_y, m_z, sg_z, sg_x, sg_y, sg_y1, sg_y2)
    sc.process_grbl_push(status)

    assert sc.bw_min_sg_z_motor_axis == sg_z
    assert sc.fw_min_sg_z_motor_axis == sg_z_2
    assert sc.fw_min_sg_x_motor_axis == sg_x
    assert sc.fw_min_sg_y_axis == default
    assert sc.fw_min_sg_y1_motor == default
    assert sc.fw_min_sg_y2_motor == default
    assert sc.fw_min_sg_x1_motor == default
    assert sc.fw_min_sg_x2_motor == default
    assert sc.fw_min_sg_z_motor_axis == sg_z_2
    assert sc.bw_min_sg_x_motor_axis == sg_x_2
    assert sc.bw_min_sg_y_axis == sg_y
    assert sc.bw_min_sg_y1_motor == sg_y1
    assert sc.bw_min_sg_y2_motor == sg_y2
    assert sc.bw_min_sg_x1_motor == default
    assert sc.bw_min_sg_x2_motor == default

    status = construct_status(m_x_2, m_y_2, m_z_2, sg_z_2, sg_x_2, sg_y_2, sg_y1_2, sg_y2_2)
    sc.process_grbl_push(status)
    
    assert sc.bw_min_sg_x1_motor == 0
    assert sc.bw_min_sg_x2_motor == 0

