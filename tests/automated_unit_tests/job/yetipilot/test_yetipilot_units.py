'''
Created on 22 Feb 2023
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



from asmcnc.job.yetipilot import yetipilot

'''
######################################
RUN FROM easycut-smartbench FOLDER WITH: 
python -m pytest --show-capture=no --disable-pytest-warnings tests/automated_unit_tests/job/yetipilot/test_yetipilot_units.py
######################################
'''

# FIXTURES
@pytest.fixture
def yp():

    m = Mock()
    sm = Mock()
    jd = Mock()
    yp = yetipilot.YetiPilot(machine=m, screen_manager=sm, job_data=jd)
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
    yp.load_parameters_from_json()

def test_add_to_stack(yp):
    yp.add_to_stack()

def test_feed_override_wrapper(yp):
    test_func = Mock()
    yp.use_yp = True
    yp.m.state = Mock(return_value="Idle")
    yp.m.s.is_job_streaming = True
    yp.m.is_machine_paused = False
    yp.feed_override_wrapper(test_func)
    test_func.assert_called()

def test_dummy_override(yp):
    yp.dummy_override()

def test_get_adjustment():
    adjustment = yetipilot.get_adjustment(12)
    adjustment_negative = yetipilot.get_adjustment(-12)
    assert adjustment == [10, 1, 1]
    assert adjustment_negative == [-10, -1, -1]

def test_cap_multiplier(yp):
    capped_multiplier = yp.cap_multiplier(25)
    capped_multiplier_negative = yp.cap_multiplier(-45)

    assert capped_multiplier == 20
    assert capped_multiplier_negative == -40