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


# FEED RATE SCRAPE

def test_scrape_last_feed_command_float(jd):
    index = 6
    job_gcode_object = [
        "G91X0F1000",
        "G1X0F8000",
        "X6.776Y6.776Z-0.720F769.25",
        "CUY",
        "X2.259Y2.259Z-0.240F796.74",
        "X2.259Y2.259Z-0.240F824.88"
    ]
    assert jd.scrape_last_feed_command(job_gcode_object, index) == 824.88

def test_scrape_last_feed_command_int_mid_job(jd):
    index = 2
    job_gcode_object = [
        "G91X0F1000",
        "G1X0F8000",
        "X6.776Y6.776Z-0.720F769.25",
        "X2.259Y2.259Z-0.240F796.74",
        "X2.259Y2.259Z-0.240F824.88"
    ]
    assert jd.scrape_last_feed_command(job_gcode_object, index) == 8000

def test_scrape_last_end_of_job(jd):
    job_gcode_object = [
        "G91X0F1000",
        "G1X0F8000",
        "X6.776Y6.776Z-0.720F769.25",
        "CUY",
        "X2.259Y2.259Z-0.240F796.74",
        "X2.259Y2.259Z-0.240F824.88"
    ]
    index = len(job_gcode_object)
    assert jd.scrape_last_feed_command(job_gcode_object, index) == 824.88

def test_scrape_last_feed_command_start_of_job(jd):
    index = 0
    job_gcode_object = [
        "G91X0F1000",
        "G1X0F8000"
    ]
    assert jd.scrape_last_feed_command(job_gcode_object, index) == 0

def test_scrape_last_feed_command_no_feeds(jd):
    index = 3
    job_gcode_object = [
        "G91",
        "G1",
        "G90",
        "G0"
    ]
    assert jd.scrape_last_feed_command(job_gcode_object, index) == 0

def test_scrape_last_feed_command_no_obj(jd):
    index = 3
    job_gcode_object = []
    assert jd.scrape_last_feed_command(job_gcode_object, index) == 0

def test_scrape_last_feed_command_no_F(jd):
    index = 3
    job_gcode_object = [
        "G91X0F1000",
        "G1X0F8000",
        "X6.776Y6.776Z-0.720F",
    ]
    assert jd.scrape_last_feed_command(job_gcode_object, index) == 0

def test_scrape_last_feed_command_feed_start_of_line(jd):
    index = 3
    job_gcode_object = [
        "G91X0F1000",
        "G1X0F8000",
        "F6000X6.776Y6.776Z-0.720",
    ]
    assert jd.scrape_last_feed_command(job_gcode_object, index) == 6000

def test_scrape_last_feed_command_feed_mid_line(jd):
    index = 1
    job_gcode_object = [
        "G91F1000X0",
    ]
    assert jd.scrape_last_feed_command(job_gcode_object, index) == 1000

def test_remove_line_numbers(jd):
    assert jd.remove_line_number("N4G1X90") == "G1X90"

def test_remove_line_numbers_mid(jd):
    assert jd.remove_line_number("G1N4X90") == "G1X90"











