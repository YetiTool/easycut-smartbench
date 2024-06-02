# -*- coding: utf-8 -*-
'''
@author: Letty
'''

import sys

from asmcnc.comms.logging_system.logging_system import Logger
from tests import test_utils

sys.path.append('./src')


try: 
    import unittest
    import pytest
    from mock import Mock

except:
    Logger.info("Can't import mocking packages, are you on a dev machine?")

from asmcnc.comms import localization
from asmcnc.apps.systemTools_app.screens.calibration import screen_stall_jig
from asmcnc.comms import router_machine
from easycut.core.settings import settings_manager

from kivy.clock import Clock


'''
########################################################
IMPORTANT!!
Run from easycut-smartbench folder, with 
python -m pytest tests/automated_unit_tests/screens/test_stall_jig_units.py
'''

test_utils.create_app()

@pytest.fixture(scope="module")
def sm():
    return Mock()

@pytest.fixture(scope="module")
def jd():
    jd = Mock()
    jd.job_name = ""
    jd.gcode_summary_string = ""
    return jd

@pytest.fixture(scope="module")
def l():
    return localization.Localization()

@pytest.fixture(scope="module")
def sett(sm):
    return settings_manager.Settings(sm)

@pytest.fixture(scope="module")
def m(sm, sett, l, jd):
    Cmport = Mock()
    return router_machine.RouterMachine(Cmport, sm, sett, l, jd)

@pytest.fixture(scope="module", autouse=True)
def stall_jig_screen(sm, m, jd, sett, l):
        systemtools_sm = Mock()
        systemtools_sm.sm = Mock()
        db = Mock()

        stall_jig_screen = screen_stall_jig.StallJigScreen(name='stall_jig', systemtools = systemtools_sm, machine = m, job = jd, settings = sett, localization = l, calibration_db = db)
        return stall_jig_screen

def test_is_100_greater_than_0(stall_jig_screen):
    assert stall_jig_screen.if_less_than_expected_pos(100)

def test_is_minus_100_less_than_0(stall_jig_screen):
    assert stall_jig_screen.if_more_than_expected_pos(-100)

def test_is_100_greater_than_0_using_function_dict(stall_jig_screen):
    assert stall_jig_screen.detection_too_late[stall_jig_screen.current_axis()](-100)

def test_determine_test_result_true(stall_jig_screen):
    stall_jig_screen.threshold_reached = True
    assert stall_jig_screen.determine_test_result(100)

def test_determine_test_result_false(stall_jig_screen):
    stall_jig_screen.threshold_reached = True
    assert not stall_jig_screen.determine_test_result(-100)

def test_unschedule_all_events(stall_jig_screen):
    stall_jig_screen.poll_for_homing_completion_loop = Clock.schedule_once(lambda dt: str("ahh"), 100)
    stall_jig_screen.unschedule_all_events()

def test_record_stall_event(stall_jig_screen, m):
    m.s.setting_100 = 5
    m.s.last_stall_motor_step_size = 5
    stall_jig_screen.record_stall_event()
    stall_jig_screen.record_stall_event()
    Logger.info(stall_jig_screen.stall_test_events)

