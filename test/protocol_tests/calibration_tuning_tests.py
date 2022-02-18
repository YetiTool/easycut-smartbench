'''
Created on 15 Feb 2022
@author: Letty
'''

try: 
    import unittest
    from mock import Mock, MagicMock
    from serial_mock.mock import MockSerial, DummySerial
    from serial_mock.decorators import serial_query

except: 
    print("Can't import mocking packages, are you on a dev machine?")

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

    normalized_SGs = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822|SG:-12,-20,15,46,-2>"
    raw_SGs = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822|SG:500,500,500,500,500>"

    temp_to_test_against = 45

    tuning_array_to_test = None

    status = normalized_SGs

    def give_me_a_PCB(outerSelf):

        class YETIPCB(MockSerial):
            simple_queries = {
                "?": outerSelf.status,
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

        self.tuning_array_to_test, temp_temp = self.m.sweep_toff_and_sgt_and_motor_driver_temp()

        sleep(0.01)

    def tearDown(self):
      self.m.s.__del__()

    # def test_does_serial_think_its_connected(self):
    #     """Test that serial module thinks it is connected"""
    #     assert self.m.s.is_connected(), 'not connected'

    # def test_the_mock_interface(self):
    #     """Test that we're getting statuses back"""
    #     assert self.m.s.m_state == "Idle", 'not idle'


    # TEST THAT self.m.sweep_toff_and_sgt() DOES ROUGHLY WHAT'S EXPECTED

    def test_sweep_toff_and_sgt(self):
        tuning_array, temp = self.m.sweep_toff_and_sgt_and_motor_driver_temp()

        for toff in range(2,11):

            for sgt in range(0,21):

                self.assertEqual(len(tuning_array[toff][sgt]), 8)

                for sg in range(0,8):
                    self.assertEqual(len(tuning_array[toff][sgt][sg]), 5)
                    self.assertEqual(tuning_array[toff][sgt][sg], self.sg_values)

        self.assertEqual(temp, self.temp_to_test_against)

        self.tuning_array_to_test = tuning_array

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
    #     target = self.m.get_target_SG_from_current_temperature('X', self.temp_to_test_against)
    #     self.assertEqual(target, 500)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()



















