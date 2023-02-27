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