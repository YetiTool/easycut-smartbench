'''
Created on 1 Feb 2022
@author: Letty
'''
from asmcnc.comms.logging_system.logging_system import Logger

try: 
    import unittest
    from mock import Mock, MagicMock
    from serial_mock.mock import MockSerial, DummySerial
    from serial_mock.decorators import serial_query

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

Cmport = 'COM3'
from asmcnc.comms.yeti_grbl_protocol.c_defines import *

########################################################
# IMPORTANT!!
# Run from easycut-smartbench folder, with 
# python -m test.comms_serial_connection_tests.calibration_coeffs_test

class SGTest(unittest.TestCase):

    status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822>"

    param = None

    case_107_140 = 1
    case_228_NOW = 2


    tcal_id = 0
    test_SG_dataset = [
            405,405,405,405,405,405,405,405,405,410,417,430,434,440,449,451,462,465,472,479,483,484,490,497,503,508,514,517,522,526,533,
            538,541,545,549,555,556,562,560,566,567,575,575,581,581,583,584,583,583,589,579,580,575,577,571,570,571,573,580,588,595,596,597,
            592,589,588,590,591,598,597,595,590,588,589,587,587,591,585,592,586,589,584,583,587,581,583,582,580,577,575,574,570,572,565,567,566,557,
            559,555,555,555,553,550,549,542,538,538,540,541,537,541,541,541,541,541,541,541,541,541,541,541,541,541,541,541,541,541,541
            ]

    test_current_setting = 26
    test_sgt_setting = 9
    test_toff_setting = 8
    test_temp_at_cal = 4500


    def give_me_a_PCB(outerSelf):

        class YETIPCB(MockSerial):

            simple_queries = {
                "?": outerSelf.status,
                "\x18": ""

            }
        return YETIPCB


    def status_and_PCB_constructor( self, case=None, motor_id=0):

        # Use this to construct the test status passed out by mock serial object

        if case == 1 or case==None:

            self.status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822>"


        elif case == 2:

            string_ints = [str(j) for j in self.test_SG_dataset]
            dataset_str = ",".join(string_ints)

            self.status =   "<Idle|TCAL:" + \
                            "M" + str(motor_id) + ":," + dataset_str + "," + \
                            str(self.test_current_setting) + "," + str(self.test_sgt_setting) + "," \
                            + str(self.test_toff_setting) + "," + str(self.test_temp_at_cal) + ">"

            Logger.info(self.status)


        # Need to construct mock PCB after the status, otherwise it'll run something else:
        self.m.s.s = DummySerial(self.give_me_a_PCB())
        self.m.s.s.fd = 1 # this is needed to force it to run
        self.m.s.start_services(1)
        sleep(0.01)

    def setUp(self):
        # If the set_up method raises an exception while the test is running, 
        # the framework will consider the test to have suffered an error, 
        # and the runTest (or test_X_Name) method will not be executed.

        self.m = Mock()
        self.sm = Mock()
        self.sett = Mock()
        self.l = localization.Localization()
        self.jd = Mock()

        self.m = router_machine.RouterMachine(Cmport, self.sm, self.sett, self.l, self.jd)


    def tearDown(self):
      self.m.s.__del__()


    def test_does_serial_think_its_connected(self):
        """Test that serial module thinks it is connected"""
        self.status_and_PCB_constructor()
        assert self.m.s.is_connected(), 'not connected'

    def test_the_mock_interface(self):
        """Test that we're getting statuses back"""
        self.status_and_PCB_constructor(1)
        assert self.m.s.m_state == "Idle", 'not idle'


    def test_motor_x1(self):
        """ 
        Test that motor registers are expected value for x1, and that serial continues to work
        This is relevant to FW between v228 onwards
        """
        self.status_and_PCB_constructor(case=2, motor_id = 0)
        self.assertEqual(self.m.TMC_motor[TMC_X1].calibration_dataset_SG_values, self.test_SG_dataset), 'x1 test_SG_dataset error'
        self.assertEqual(len(self.test_SG_dataset), 128), 'x1 test_SG_dataset length error'
        self.assertEqual(len(self.m.TMC_motor[TMC_X1].calibration_dataset_SG_values), 128), 'x1 test_SG_dataset length error'
        self.assertEqual(self.m.TMC_motor[TMC_X1].calibrated_at_current_setting, self.test_current_setting), 'x1 test_current_setting error'
        self.assertEqual(self.m.TMC_motor[TMC_X1].calibrated_at_sgt_setting, self.test_sgt_setting), 'x1 test_sgt_setting error'
        self.assertEqual(self.m.TMC_motor[TMC_X1].calibrated_at_toff_setting, self.test_toff_setting), 'x1 test_toff_setting error'
        self.assertEqual(self.m.TMC_motor[TMC_X1].calibrated_at_temperature, self.test_temp_at_cal), 'x1 test_temp_at_cal error'
        assert self.m.s.is_connected(), 'not connected'

    def test_motor_x2(self):
        """ 
        Test that motor calibration are expected value for x2, and that serial continues to work
        This is relevant to FW between v228 onwards
        """
        self.status_and_PCB_constructor(case=2, motor_id = 1)
        self.assertEqual(self.m.TMC_motor[TMC_X2].calibration_dataset_SG_values, self.test_SG_dataset), 'x2 test_SG_dataset error'
        self.assertEqual(len(self.m.TMC_motor[TMC_X2].calibration_dataset_SG_values), 128), 'x2 test_SG_dataset length error'
        self.assertEqual(self.m.TMC_motor[TMC_X2].calibrated_at_current_setting, self.test_current_setting), 'x2 test_current_setting error' 
        self.assertEqual(self.m.TMC_motor[TMC_X2].calibrated_at_sgt_setting, self.test_sgt_setting), 'x2 test_sgt_setting error'
        self.assertEqual(self.m.TMC_motor[TMC_X2].calibrated_at_toff_setting, self.test_toff_setting),'x2 test_toff_setting error'
        self.assertEqual(self.m.TMC_motor[TMC_X2].calibrated_at_temperature, self.test_temp_at_cal), 'x2 test_temp_at_cal error'
        assert self.m.s.is_connected(), 'not connected'

    def test_motor_y1(self):
        """ 
        Test that motor id is expected value for y1, and that serial continues to work
        This is relevant to FW between v228 onwards
        """
        self.status_and_PCB_constructor(case=2, motor_id = 2)
        self.assertEqual(self.m.TMC_motor[TMC_Y1].calibration_dataset_SG_values, self.test_SG_dataset), 'y1 test_SG_dataset error'
        self.assertEqual(len(self.m.TMC_motor[TMC_Y1].calibration_dataset_SG_values), 128), 'y1 test_SG_dataset length error'
        self.assertEqual(self.m.TMC_motor[TMC_Y1].calibrated_at_current_setting, self.test_current_setting), 'y1 test_current_setting error' 
        self.assertEqual(self.m.TMC_motor[TMC_Y1].calibrated_at_sgt_setting, self.test_sgt_setting), 'y1 test_sgt_setting error'
        self.assertEqual(self.m.TMC_motor[TMC_Y1].calibrated_at_toff_setting, self.test_toff_setting),'y1 test_toff_setting error'
        self.assertEqual(self.m.TMC_motor[TMC_Y1].calibrated_at_temperature, self.test_temp_at_cal), 'y1 test_temp_at_cal error'
        assert self.m.s.is_connected(), 'not connected'

    def test_motor_y2(self):
        """ 
        Test that motor id is expected value for y2, and that serial continues to work
        This is relevant to FW between v228 onwards
        """
        self.status_and_PCB_constructor(case=2, motor_id = 3)
        self.assertEqual(self.m.TMC_motor[TMC_Y2].calibration_dataset_SG_values, self.test_SG_dataset), 'y2 test_SG_dataset error'
        self.assertEqual(len(self.m.TMC_motor[TMC_Y2].calibration_dataset_SG_values), 128), 'y2 test_SG_dataset length error'
        self.assertEqual(self.m.TMC_motor[TMC_Y2].calibrated_at_current_setting, self.test_current_setting), 'y2 test_current_setting error' 
        self.assertEqual(self.m.TMC_motor[TMC_Y2].calibrated_at_sgt_setting, self.test_sgt_setting), 'y2 test_sgt_setting error'
        self.assertEqual(self.m.TMC_motor[TMC_Y2].calibrated_at_toff_setting, self.test_toff_setting),'y2 test_toff_setting error'
        self.assertEqual(self.m.TMC_motor[TMC_Y2].calibrated_at_temperature, self.test_temp_at_cal), 'y2 test_temp_at_cal error'
        assert self.m.s.is_connected(), 'not connected'

    def test_motor_z(self):
        """ 
        Test that motor id is expected value for z, and that serial continues to work
        This is relevant to FW between v228 onwards
        """
        self.status_and_PCB_constructor(case=2, motor_id = 4)
        self.assertEqual(self.m.TMC_motor[TMC_Z].calibration_dataset_SG_values, self.test_SG_dataset), 'z test_SG_dataset error'
        self.assertEqual(len(self.m.TMC_motor[TMC_Z].calibration_dataset_SG_values), 128), 'z test_SG_dataset length error'
        self.assertEqual(self.m.TMC_motor[TMC_Z].calibrated_at_current_setting, self.test_current_setting), 'z test_current_setting error' 
        self.assertEqual(self.m.TMC_motor[TMC_Z].calibrated_at_sgt_setting, self.test_sgt_setting), 'z test_sgt_setting error'
        self.assertEqual(self.m.TMC_motor[TMC_Z].calibrated_at_toff_setting, self.test_toff_setting),'z test_toff_setting error'
        self.assertEqual(self.m.TMC_motor[TMC_Z].calibrated_at_temperature, self.test_temp_at_cal), 'z test_temp_at_cal error'
        assert self.m.s.is_connected(), 'not connected'

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()