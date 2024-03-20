'''
Created on 15 Feb 2022
@author: Letty
'''
from asmcnc.comms.logging_system.logging_system import Logger

try: 
    import unittest
    from mock import Mock, MagicMock
    from serial_mock.mock import MockSerial, DummySerial
    from serial_mock.decorators import serial_query
    from random import randint

except: 
    Logger.info("Can't import mocking packages, are you on a dev machine?")

from time import sleep

import sys
sys.path.append('./src')

try:
    from asmcnc.comms import router_machine
    from asmcnc.comms import localization

except:
    pass

from asmcnc.comms.yeti_grbl_protocol.c_defines import *


########################################################
# IMPORTANT!!
# Run from easycut-smartbench folder, with 
# python -m test.protocol_tests.calibration_tuning_tests

Cmport = 'COM3'

class MotorCommandsTest(unittest.TestCase):

    sg_values = [-12,-20,15,46,-2]
    # sg_values = [500,500,500,500,500]

    normalized_SGs = "<Run|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822|SG:-12,-20,15,-999,-2>"
    raw_SGs = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822|SG:500,500,500,500,500>"

    temp_to_test_against = 45

    tuning_array_to_test = None

    status = normalized_SGs


    def give_status(self):

        if randint(0,1) == 0: 
            status = "<Run|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822|SG:-999,-20,15,-20,-2>"

        else:
            status = "<Run|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822|SG:-999,-16,-15,-20,-2>"

        return status

    test_arr = [[[832, 1023, -999, 1023, 1023], [838, 1023, -999, 1023, 1023], [841, 1023, -999, 1023, 1023], [847, 1023, -999, 1023, 1023], [846, 1023, -999, 1023, 1023], [843, 1023, -999, 1023, 1023], [829, 1023, -999, 1023, 1023], [830, 1023, -999, 1023, 1023]]*(11)]*(21)

    def give_me_a_PCB(outerSelf):

        class YETIPCB(MockSerial):
            simple_queries = {
                "?": outerSelf.give_status(),
                "\x18": ""
            }

        return YETIPCB

    def setUp(self):
        # If the set_up method raises an exception while the test is running, 
        # the framework will consider the test to have suffered an error, 
        # and the runTest (or test_X_Name) method will not be executed.

        self.sm = Mock()
        self.sett = Mock()
        self.sett.ip_address = ''
        self.l = localization.Localization()
        self.jd = Mock()

        self.m = router_machine.RouterMachine(Cmport, self.sm, self.sett, self.l, self.jd)
        self.m.s.s = DummySerial(self.give_me_a_PCB())
        self.m.s.s.fd = 1 # this is needed to force it to run
        self.m.s.start_services(1)
        self.m.s.motor_driver_temp = self.temp_to_test_against

        # self.tuning_array_to_test, temp_temp = self.m.sweep_toff_and_sgt_and_motor_driver_temp()

        sleep(0.01)

    def tearDown(self):
      self.m.s.__del__()

    # def test_does_serial_think_its_connected(self):
    #     """Test that serial module thinks it is connected"""
    #     assert self.m.s.is_connected(), 'not connected'

    # def test_the_mock_interface(self):
    #     """Test that we're getting statuses back"""
    #     assert self.m.s.m_state == "Run", 'not idle'

    def test_are_sg_values_in_range_after_calibration(self):
        self.m.temp_sg_array = []
        self.m.s.record_sg_values_flag = True
        sleep(3)
        self.m.s.record_sg_values_flag = False
        self.m.are_sg_values_in_range_after_calibration(['X', 'Y', 'Z'])
        Logger.info(self.m.checking_calibration_fail_info)
        assert(self.m.checking_calibration_fail_info.startswith("All values -999 for idx: 0"))


    # def test_get_abs_maximums_from_sg_array_x(self):
    #     self.m.temp_sg_array = []
    #     self.m.s.record_sg_values_flag = True
    #     sleep(3)
    #     self.m.s.record_sg_values_flag = False
    #     val = self.m.get_abs_maximums_from_sg_array(self.m.temp_sg_array, 1)
    #     self.assertEqual(val, -20)


    # def test_get_abs_maximums_from_sg_array_y(self):
    #     self.m.temp_sg_array = []
    #     self.m.s.record_sg_values_flag = True
    #     sleep(3)
    #     self.m.s.record_sg_values_flag = False
    #     val = self.m.get_abs_maximums_from_sg_array(self.m.temp_sg_array, 2)
    #     self.assertEqual(val, 15)

    # TEST THAT self.m.sweep_toff_and_sgt() DOES ROUGHLY WHAT'S EXPECTED

    # def test_sweep_toff_and_sgt(self):
    #     tuning_array, temp = self.m.sweep_toff_and_sgt_and_motor_driver_temp()

    #     for toff in range(2,self.m.toff_max + 1):

    #         for sgt in range(0,self.m.sgt_max + 1):

    #             self.assertEqual(len(tuning_array[toff][sgt]), 8)
    #             for sg in range(0,8):



    #                 self.assertEqual(len(tuning_array[toff][sgt][sg]), 5)
    #                 self.assertEqual(tuning_array[toff][sgt][sg], self.sg_values)

    #     self.assertEqual(temp, self.temp_to_test_against)

    #     self.tuning_array_to_test = tuning_array

    # def test_start_tuning(self):
    #     self.m.start_tuning(False, False, False)

    # def test_tuning_array(self):
    #     assert(self.tuning_array_to_test != None)

    # def test_point_averaging(self):
    #     avg = self.m.average_points_in_sub_array(self.tuning_array_to_test[10][20], 3)
    #     self.assertEqual(avg, self.sg_values[3])

    # def test_combo_finding(self):
    #     '''find_best_combo_per_motor_or_axis(self, tuning_array, target_SG, idx)'''
    #     toff, sgt = self.m.find_best_combo_per_motor_or_axis(self.tuning_array_to_test, 500, 3)
    #     self.assertEqual(toff, 2)
    #     self.assertEqual(sgt, 0)

    # def test_get_target(self):
    #     '''get_target_SG_from_current_temperature'''
    #     target = self.m.get_target_SG_from_current_temperature('Y', -100)
    #     # self.assertEqual(target, 500)
    #     Logger.info("SG TARG: " + str(target))

    # def test_get_another_target(self):
    #     '''get_target_SG_from_current_temperature'''
    #     target = self.m.get_target_SG_from_current_temperature('Y', 100)
    #     # self.assertEqual(target, 500)
    #     Logger.info("SG TARG: " + str(target))

    # def test_find_combo(self):

    #     out = self.m.find_best_combo_per_motor_or_axis(self.test_arr, 800, 0)

    #     print out



    # temps_in = [
    #                 30,
    #                 31,
    #                 32,
    #                 33,
    #                 34,
    #                 35,
    #                 36,
    #                 37,
    #                 38,
    #                 39,
    #                 40,
    #                 41,
    #                 42,
    #                 43,
    #                 44,
    #                 45,
    #                 46,
    #                 47,
    #                 48,
    #                 49,
    #                 50,
    #                 51,
    #                 52,
    #                 53,
    #                 54,
    #                 55,
    #                 56,
    #                 57,
    #                 58,
    #                 59
    # ]

    # targets_out = [
    #                 713,
    #                 699,
    #                 685,
    #                 670,
    #                 656,
    #                 642,
    #                 628,
    #                 613,
    #                 599,
    #                 585,
    #                 571,
    #                 556,
    #                 542,
    #                 528,
    #                 514,
    #                 500,
    #                 486,
    #                 472,
    #                 458,
    #                 444,
    #                 429,
    #                 415,
    #                 401,
    #                 387,
    #                 372,
    #                 358,
    #                 344,
    #                 330,
    #                 315,
    #                 301

    # ]



    # def test_get_target(self):

    #     for idx, val in enumerate(self.temps_in):

    #         '''get_target_SG_from_current_temperature'''
    #         target = self.m.get_target_SG_from_current_temperature('X', val)
    #         self.assertEqual(target, self.targets_out[idx])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()



















