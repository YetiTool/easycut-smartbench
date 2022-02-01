'''
Created on 1 Feb 2022
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
    from asmcnc.comms import serial_connection
    from asmcnc.comms import localization

except: 
    pass

########################################################
# IMPORTANT!!
# Run from easycut-smartbench folder, with 
# python -m test.comms_serial_connection_tests.SGtest

class SGTest(unittest.TestCase):

    status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822>"

    param = None

    case_107_140 = 1
    case_228_NOW = 2

    t_z_motor_axis = -21
    t_x_motor_axis = -20
    t_y_axis = 15
    t_y1_motor = 46
    t_y2_motor = -2


    def give_me_a_PCB(outerSelf):

        class YETIPCB(MockSerial):

            @serial_query("?")
            def do_something(self):
                return outerSelf.status

        return YETIPCB


    def status_and_PCB_constructor(self, case=None, 
                        z_motor_axis = 0,
                        x_motor_axis = 0,
                        y_axis = 0,
                        y1_motor = 0,
                        y2_motor = 0):

        # Use this to construct the test status passed out by mock serial object

        if case == 1 or case==None:

            self.status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822>"


        elif case == 2:

            # <Run|MPos:-692.704,-2142.446,-39.392|Bf:0,121|FS:6060,0|Pn:G|SG:-12,-20,15,46,-2>

            self.status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Ld:0|SG:" + \
                str(z_motor_axis) + "," + \
                str(x_motor_axis) + "," + \
                str(y_axis) + "," + \
                str(y1_motor) + "," + \
                str(y2_motor) + ">"


        # Need to construct mock PCB after the status, otherwise it'll run something else:
        self.serial_module.s = DummySerial(self.give_me_a_PCB())
        self.serial_module.s.fd = 1 # this is needed to force it to run
        self.serial_module.start_services(1)
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

        self.serial_module = serial_connection.SerialConnection(self.m, self.sm, self.sett, self.l, self.jd)
        # self.serial_module.VERBOSE_ALL_RESPONSE = True


    def tearDown(self):
      self.serial_module.__del__()


    def test_does_serial_think_its_connected(self):
        """Test that serial module thinks it is connected"""
        self.status_and_PCB_constructor()
        assert self.serial_module.is_connected(), 'not connected'

    def test_the_mock_interface(self):
        """Test that we're getting statuses back"""
        self.status_and_PCB_constructor(1)
        assert self.serial_module.m_state == "Idle", 'not idle'


    ## CASE 1 TESTS:
    def test_z_motor_SG_case_107_140(self):
        """ 
        Test that Z motor SG is None, but that serial continues to work
        This is relevant to FW between v107 and v140
        """
        self.status_and_PCB_constructor(self.case_107_140)
        self.assertEqual(self.serial_module.z_motor_axis, None), 'z motor SG error, case 1'
        assert self.serial_module.is_connected(), 'not connected'

    def test_x_motor_SG_case_107_140(self):
        """ 
        Test that X motor SG is None, but that serial continues to work
        This is relevant to FW between v107 and v140
        """
        self.status_and_PCB_constructor(self.case_107_140)
        self.assertEqual(self.serial_module.x_motor_axis, None), 'x motor SG error, case 1'
        assert self.serial_module.is_connected(), 'not connected'

    def test_y_axis_SG_case_107_140(self):
        """ 
        Test that Y axis SG is None, but that serial continues to work
        This is relevant to FW between v107 and v140
        """
        self.status_and_PCB_constructor(self.case_107_140)
        self.assertEqual(self.serial_module.y_axis, None), 'y axis SG error, case 1'
        assert self.serial_module.is_connected(), 'not connected'

    def test_y1_motor_SG_case_107_140(self):
        """ 
        Test that Y1 motor SG is None, but that serial continues to work
        This is relevant to FW between v107 and v140
        """
        self.status_and_PCB_constructor(self.case_107_140)
        self.assertEqual(self.serial_module.y1_motor, None), 'y1 motor SG error, case 1'
        assert self.serial_module.is_connected(), 'not connected'

    def test_y2_motor_SG_case_107_140(self):
        """ 
        Test that Y2 motor SG is None, but that serial continues to work
        This is relevant to FW between v107 and v140
        """
        self.status_and_PCB_constructor(self.case_107_140)
        self.assertEqual(self.serial_module.y2_motor, None), 'y2 motor SG error, case 1'
        assert self.serial_module.is_connected(), 'not connected'


    ## CASE 2 TESTS:
    def test_z_motor_SG_case_228_NOW(self):
        """ 
        Test that Z motor SG is expected value, and that serial continues to work
        This is relevant to FW between v228 onwards
        """
        self.status_and_PCB_constructor(self.case_228_NOW, z_motor_axis = self.t_z_motor_axis)
        self.assertEqual(self.serial_module.z_motor_axis, self.t_z_motor_axis), 'z motor SG error, case 1'
        assert self.serial_module.is_connected(), 'not connected'

    def test_x_motor_SG_case_228_NOW(self):
        """ 
        Test that X motor SG is expected value, and that serial continues to work
        This is relevant to FW between v228 onwards
        """
        self.status_and_PCB_constructor(self.case_228_NOW, x_motor_axis = self.t_x_motor_axis)
        self.assertEqual(self.serial_module.x_motor_axis, self.t_x_motor_axis), 'x motor SG error, case 1'
        assert self.serial_module.is_connected(), 'not connected'

    def test_y_axis_SG_case_228_NOW(self):
        """ 
        Test that Y axis SG is expected value, and that serial continues to work
        This is relevant to FW between v228 onwards
        """
        self.status_and_PCB_constructor(self.case_228_NOW, y_axis = self.t_y_axis)
        self.assertEqual(self.serial_module.y_axis, self.t_y_axis), 'y axis SG error, case 1'
        assert self.serial_module.is_connected(), 'not connected'

    def test_y1_motor_SG_case_228_NOW(self):
        """ 
        Test that Y1 motor SG is expected value, and that serial continues to work
        This is relevant to FW between v228 onwards
        """
        self.status_and_PCB_constructor(self.case_228_NOW, y1_motor = self.t_y1_motor)
        self.assertEqual(self.serial_module.y1_motor, self.t_y1_motor), 'y1 motor SG error, case 1'
        assert self.serial_module.is_connected(), 'not connected'

    def test_y2_motor_SG_case_228_NOW(self):
        """ 
        Test that Y2 motor SG is expected value, and that serial continues to work
        This is relevant to FW between v228 onwards
        """
        self.status_and_PCB_constructor(self.case_228_NOW, y2_motor = self.t_y2_motor)
        self.assertEqual(self.serial_module.y2_motor, self.t_y2_motor), 'y2 motor SG error, case 1'
        assert self.serial_module.is_connected(), 'not connected'


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()