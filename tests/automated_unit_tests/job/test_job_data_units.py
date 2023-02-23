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
        "G1X0F8000",
        "X6.776Y6.776Z-0.720F769.25",
        "CUY",
        "X2.259Y2.259Z-0.240F796.74",
        "X2.259Y2.259Z-0.240F824.88"
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

# LINE COUNTING

def test_setup_running_job_gcode(jd):

    # Set this up for future :)

    jd.job_gcode_running = []

    job_gcode_object = [
        "G91X0F1000",
        "G1X0F8000",
        "AE",
        "X6.776Y6.776Z-0.720F769.25",
        "X2.259Y2.259Z-0.240F796.74",
        "X2.259Y2.259Z-0.240F824.88"
    ]

    jd.setup_running_job_gcode(job_gcode_object)
    assert jd.job_gcode_running == job_gcode_object

def test_setup_running_job_gcode_empty(jd):
    jd.job_gcode_running = ["ahh"]
    job_gcode_object = []
    expected_gcode_with_line_numbers = []
    jd.setup_running_job_gcode(job_gcode_object)
    assert jd.job_gcode_running == expected_gcode_with_line_numbers


import timeit
import functools

def test_add_line_numbers_to_gcode(jd):
    job_gcode_object = [
        "G91X0F1000",
        "G1X0F8000",
        "X6.776Y6.776Z-0.720F769.25",
        "X2.259Y2.259Z-0.240F796.74",
        "X2.259Y2.259Z-0.240F824.88"
    ]

    expected_gcode_with_line_numbers = [
        "N0G91X0F1000",
        "N1G1X0F8000",
        "N2X6.776Y6.776Z-0.720F769.25",
        "N3X2.259Y2.259Z-0.240F796.74",
        "N4X2.259Y2.259Z-0.240F824.88"
    ]

    assert jd.add_line_numbers_to_gcode(job_gcode_object) == expected_gcode_with_line_numbers


def test_gcode_line_is_excluded(jd):

    uncountable_gcodes = [
        '(',
        ')',
        '$',
        'AE',
        'AF'
    ]
    number_gcodes = 1
    for line in uncountable_gcodes:
        assert jd.gcode_line_is_excluded(line)
    assert jd.gcode_line_is_excluded("(AHHH)")

def test_gcode_line_is_not_excluded(jd):
    assert not jd.gcode_line_is_excluded("G90")
    assert not jd.gcode_line_is_excluded("GX1Y4F600")
    assert not jd.gcode_line_is_excluded("GX1Y4F600")

def test_add_line_number_to_gcode_line(jd):
    assert jd.add_line_number_to_gcode_line("G1", 4) == "N4G1"
    assert jd.add_line_number_to_gcode_line("AE", 2) == "AE"















