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

def construct_status(x_pos=0.0, y_pos=0.0, z_pos=0.0):

	status = "<Idle|MPos:" + \
		str(x_pos) + ","+ \
		str(y_pos) + ","+ \
		str(z_pos) + ","+ \
		"|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822|Sp:1,2,3,4,5,6,7>"

	return status

def assert_positions_equal(sc_obj, x_pos=0.0, y_pos=0.0, z_pos=0.0):
	assert sc_obj.m_x == str(x_pos)
	assert sc_obj.m_y == str(y_pos)
	assert sc_obj.m_z == str(z_pos)


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
