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

        m = router_machine.RouterMachine(Cmport, sm, sett, l, jd)

        self.stall_jig_screen = screen_stall_jig.StallJigScreen(name='stall_jig', systemtools = systemtools_sm, machine = m, job = jd, settings = sett, localization = l)

    # GENERAL TESTS

    def test_is_connected(self):
        self.assertIsNotNone(self.stall_jig_screen.if_less_than_coord(100), "Not working :(")

    def test_is_100_greater_than_0(self):
        assert self.stall_jig_screen.if_less_than_coord(100), "Not working :("

if __name__ == "__main__":
    unittest.main()