import logging
"""
Created on 22 Feb 2023
@author: Letty
"""
import sys
from asmcnc.comms.logging_system.logging_system import Logger
sys.path.append('./src')
try:
    import unittest
    import pytest
    from mock import Mock, MagicMock
except:
    Logger.info("Can't import mocking packages, are you on a dev machine?")
from asmcnc.comms import localization
from asmcnc.job.yetipilot import yetipilot
"""
######################################
RUN FROM easycut-smartbench FOLDER WITH: 
python -m pytest tests/automated_unit_tests/job/yetipilot/test_yetipilot_units.py
######################################
"""


@pytest.fixture
def yp():
    m = Mock()
    sm = Mock()
    jd = Mock()
    l = localization.Localization()
    yp = yetipilot.YetiPilot(machine=m, screen_manager=sm, job_data=jd,
        localization=l, test=True)
    return yp


def test_yp_init(yp):
    assert yp.m
    assert yp.sm
    assert yp.jd


def test_start(yp):
    yp.enable()
    assert yp.use_yp


def test_stop(yp):
    yp.disable()
    assert not yp.use_yp


def test_load_parameters_from_json(yp):
    yp.load_parameters()


def test_feed_override_wrapper(yp):
    test_func = Mock()
    yp.use_yp = True
    yp.m.state = Mock(return_value='Idle')
    yp.m.s.is_job_streaming = True
    yp.m.is_machine_paused = False
    yp.feed_override_wrapper(test_func)
    test_func.assert_called()


def test_get_feed_adjustment_percentage(yp):
    yp.get_all_profiles()
    yp.use_profile(yp.available_profiles[0])
    feed_up_args = True, 1, False
    no_feed_up_args = False, 0, True
    assert yp.get_feed_adjustment_percentage(950, *no_feed_up_args,
        feed_multiplier=-45) == -40
    assert yp.get_feed_adjustment_percentage(950, *no_feed_up_args,
        feed_multiplier=45) == 0
    assert yp.get_feed_adjustment_percentage(950, *no_feed_up_args,
        feed_multiplier=17) == 0
    assert yp.get_feed_adjustment_percentage(950, *feed_up_args,
        feed_multiplier=45) == 20
    assert yp.get_feed_adjustment_percentage(950, *feed_up_args,
        feed_multiplier=17) == 17


def test_get_multiplier(yp):
    yp.get_all_profiles()
    yp.use_profile(yp.available_profiles[0])
    yp.set_free_load(400)
    assert yp.get_multiplier(yp.get_total_target_power()) == 0
