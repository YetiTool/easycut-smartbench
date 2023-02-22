'''
Created on 22 Feb 2023
@author: Letty
'''

import sys, os
sys.path.append('./src')

try: 
    import unittest
    import pytest
    from mock import Mock, MagicMock

except: 
    print("Can't import mocking packages, are you on a dev machine?")

from asmcnc.job import job_data
from asmcnc.comms import localization
from datetime import datetime

from kivy.clock import Clock

'''
######################################
RUN FROM easycut-smartbench FOLDER WITH: 
python -m pytest --show-capture=no --disable-pytest-warnings tests/automated_unit_tests/job/test_job_data_units.py
######################################
'''


# FIXTURES
@pytest.fixture
def jd():
    l = localization.Localization()
    settings_manager = Mock()
    jd = job_data.JobData(localization = l, settings_manager = settings_manager)
    return jd

def test_get_jd(jd):
    jd.reset_values()


def test_scrape_last_feed_command(jd):
    index = 6
    job_gcode_object = [
        "G91X0F1000",
        "G1X0F8000",
        "X6.776Y6.776Z-0.720F769.25",
        "CUY",
        "X2.259Y2.259Z-0.240F796.74",
        "X2.259Y2.259Z-0.240F824.88"
    ]
    assert jd.scrape_last_feed_command(job_gcode_object, index) == 824