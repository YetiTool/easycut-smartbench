'''
Created on 18 Aug 2022
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


from asmcnc.comms import router_machine
from asmcnc.comms import localization

'''
######################################
RUN FROM easycut-smartbench FOLDER WITH: 
python -m pytest tests/automated_unit_tests/comms/test_router_machine_tuning_and_calibration.py
######################################
'''

test_utils.create_app()

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

def build_tuning_array(machine, sg_z_motor_axis = None, sg_x_motor_axis = None, sg_y_axis = None, sg_y1_motor = None, sg_y2_motor = None, sg_x1_motor = None, sg_x2_motor = None):
	sg_list = [sg_z_motor_axis, sg_x_motor_axis, sg_y_axis, sg_y1_motor, sg_y2_motor, sg_x1_motor, sg_x2_motor]
	status = construct_status(*sg_list)
	machine.s.record_sg_values_flag = True
	machine.s.process_grbl_push(status)

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


def test_do_tuning_with_no_x1_x2_vals(m):
	m.print_tmc_registers = Mock()
	m.sweep_toff_and_sgt_and_motor_driver_temp = Mock()
	m.sweep_toff_and_sgt_and_motor_driver_temp.return_value = [], 50
	m.get_target_SG_from_current_temperature = Mock(return_value=50)
	m.find_best_combo_per_motor_or_axis = Mock()
	m.find_best_combo_per_motor_or_axis.return_value = 2,10
	m.toff_and_sgt_found = False
	m.do_tuning(True, False, False)
	assert m.toff_and_sgt_found
	assert m.x1_toff_tuned == 2
	assert m.x1_sgt_tuned == 10
	assert m.x2_toff_tuned == 2
	assert m.x2_sgt_tuned == 10

def test_do_tuning_with_x1_x2_vals(m):
	m.print_tmc_registers = Mock()
	m.sweep_toff_and_sgt_and_motor_driver_temp = Mock()
	m.sweep_toff_and_sgt_and_motor_driver_temp.return_value = [], 50
	m.get_target_SG_from_current_temperature = Mock(return_value=50)
	m.find_best_combo_per_motor_or_axis = Mock()
	m.find_best_combo_per_motor_or_axis.return_value = 2,10
	m.toff_and_sgt_found = False
	m.s.sg_x1_motor = 30
	m.s.sg_x2_motor = 32
	m.do_tuning(True, False, False)
	assert m.toff_and_sgt_found
	assert m.x1_toff_tuned == 2
	assert m.x1_sgt_tuned == 10
	assert m.x2_toff_tuned == 2
	assert m.x2_sgt_tuned == 10

def test_get_abs_maximums_from_sg_array(m):
	build_tuning_array(m,3,4,5,6,7,8,9)
	build_tuning_array(m,1,2,3,4,5,6,7)
	build_tuning_array(m,2,3,4,5,6,7,8)
	assert m.get_abs_maximums_from_sg_array(m.temp_sg_array,0) == 3
	assert m.get_abs_maximums_from_sg_array(m.temp_sg_array,1) == 4
	assert m.get_abs_maximums_from_sg_array(m.temp_sg_array,2) == 5
	assert m.get_abs_maximums_from_sg_array(m.temp_sg_array,3) == 6
	assert m.get_abs_maximums_from_sg_array(m.temp_sg_array,4) == 7
	assert m.get_abs_maximums_from_sg_array(m.temp_sg_array,5) == 8
	assert m.get_abs_maximums_from_sg_array(m.temp_sg_array,6) == 9

def test_are_sg_values_in_range_after_calibration_5_drivers(m):
	build_tuning_array(m,1,2,3,4000,5,6,7)
	build_tuning_array(m,3,4,5,6,7,8000,9)
	build_tuning_array(m,2,3,4,5,6,7,8)
	values = m.are_sg_values_in_range_after_calibration(["X", "Y"])
	assert values[0] == 4
	assert values[1] == 5
	assert values[2] == None
	assert not m.checking_calibration_fail_info

def test_are_sg_values_in_range_after_calibration_4_drivers(m):
	build_tuning_array(m,3,4,5,6,7)
	build_tuning_array(m,1,2,3,4000,5)
	build_tuning_array(m,2,3,4,5,6)
	values = m.are_sg_values_in_range_after_calibration(["X", "Y", "Z"])
	assert values[0] == 4
	assert values[1] == 5
	assert values[2] == 3
	assert not m.checking_calibration_fail_info

def test_are_sg_values_in_range_after_calibration_fails_as_expected(m):
	build_tuning_array(m,1,2,3,4,5,1000,7)
	build_tuning_array(m,2000,3,4,5,6,7,8)
	build_tuning_array(m,3,4000,5,6,7,8,9)
	values = m.are_sg_values_in_range_after_calibration(["X", "Y", "Z"])
	assert values[0] == 4000
	assert values[1] == 5
	assert values[2] == 2000
	assert m.checking_calibration_fail_info == ("X SG values out of expected range: 4000| " + \
								"Z SG values out of expected range, max: 2000|")









