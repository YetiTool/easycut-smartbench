try: 
    import unittest
    from mock import Mock

except:
    print("Can't import mocking packages, are you on a dev machine?")

import sys
sys.path.append('./src')

from datetime import datetime
from asmcnc.apps.systemTools_app.screens.calibration import screen_stall_jig
from asmcnc.comms import localization
from asmcnc.comms import router_machine
from settings import settings_manager

from kivy.clock import Clock

########################################################
# IMPORTANT!!
# Run from easycut-smartbench folder, with 
# python -m test.screen_tests.stall_jig_unit_tests


class StallJigUnitTests(unittest.TestCase):
    """Testing stall jig functions"""


    def setUp(self):
        # If the set_up method raises an exception while the test is running, 
        # the framework will consider the test to have suffered an error, 
        # and the runTest (or test_X_Name) method will not be executed.

        systemtools_sm = Mock()
        systemtools_sm.sm = Mock()
        sm = Mock()

        Cmport = Mock()

        l = localization.Localization()
        sett = settings_manager.Settings(sm)

        # Initialise 'j'ob 'd'ata object
        jd = Mock()
        jd.job_name = ""
        jd.gcode_summary_string = ""

        self.m = router_machine.RouterMachine(Cmport, sm, sett, l, jd)
        self.stall_jig_screen = screen_stall_jig.StallJigScreen(name='stall_jig', systemtools = systemtools_sm, machine = self.m, job = jd, settings = sett, localization = l)

    # GENERAL TESTS

    def test_is_100_greater_than_0(self):
        assert self.screen_stall_jig.StallJigScreen.if_less_than_expected_pos(100), "Not working :("

    def test_is_minus_100_less_than_0(self):
        assert self.stall_jig_screen.if_more_than_expected_pos(-100), "Not working :("

    def test_is_100_greater_than_0_using_function_dict(self):
        assert self.stall_jig_screen.detection_too_late[self.stall_jig_screen.current_axis()](-100), "Not working :("

    def test_determine_test_result_true(self):
        self.stall_jig_screen.threshold_reached = True
        self.assertTrue(self.stall_jig_screen.determine_test_result(100)), "Determine test result func failed"

    def test_determine_test_result_false(self):
        self.stall_jig_screen.threshold_reached = True
        self.assertFalse(self.stall_jig_screen.determine_test_result(-100)), "Determine test result func failed"

    def test_unschedule_all_events(self):
        self.stall_jig_screen.poll_for_homing_completion_loop = Clock.schedule_once(lambda dt: str("ahh"), 100)
        self.stall_jig_screen.unschedule_all_events()

    def test_record_stall_event(self):
        self.m.s.setting_100 = 5
        self.m.s.last_stall_motor_step_size = 5
        self.stall_jig_screen.record_stall_event()
        self.stall_jig_screen.record_stall_event()
        print(self.stall_jig_screen.stall_test_events)

if __name__ == "__main__":
    unittest.main()