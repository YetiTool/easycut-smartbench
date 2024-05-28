import logging
"""
Created on 22 Feb 2023
@author: Letty
"""
import sys, os
from asmcnc.comms.logging_system.logging_system import Logger
sys.path.append('./src')
try:
    import unittest
    import pytest
    from mock import Mock, MagicMock
except:
    Logger.info("Can't import mocking packages, are you on a dev machine?")
from asmcnc.job import job_data
from asmcnc.comms import localization
from datetime import datetime
from kivy.clock import Clock
"""
######################################
RUN FROM easycut-smartbench FOLDER WITH: 
python -m pytest tests/automated_unit_tests/job/test_job_data_units.py
######################################
"""


@pytest.fixture
def jd():
    l = localization.Localization()
    settings_manager = Mock()
    jd = job_data.JobData(localization=l, settings_manager=settings_manager)
    return jd


def test_get_jd(jd):
    jd.reset_values()


def test_scrape_last_feed_command_float(jd):
    index = 5
    job_gcode_object = ['G91X0F1000', 'G1X0F8000',
        'X6.776Y6.776Z-0.720F769.25', 'CUY', 'X2.259Y2.259Z-0.240F796.74',
        'X2.259Y2.259Z-0.240F824.88']
    assert jd.scrape_last_feed_command(job_gcode_object, index) == 824.88


def test_scrape_last_feed_command_int_mid_job(jd):
    index = 1
    job_gcode_object = ['G91X0F1000', 'G1X0F8000',
        'X6.776Y6.776Z-0.720F769.25', 'X2.259Y2.259Z-0.240F796.74',
        'X2.259Y2.259Z-0.240F824.88']
    assert jd.scrape_last_feed_command(job_gcode_object, index) == 8000


def test_scrape_last_end_of_job(jd):
    job_gcode_object = ['G91X0F1000', 'G1X0F8000',
        'X6.776Y6.776Z-0.720F769.25', 'CUY', 'X2.259Y2.259Z-0.240F796.74',
        'X2.259Y2.259Z-0.240F824.88']
    index = len(job_gcode_object)
    assert jd.scrape_last_feed_command(job_gcode_object, index) == 824.88


def test_scrape_last_feed_command_start_of_job(jd):
    index = 0
    job_gcode_object = ['G91X0F1000', 'G1X0F8000']
    assert jd.scrape_last_feed_command(job_gcode_object, index) == 1000


def test_scrape_last_feed_command_no_feeds(jd):
    index = 3
    job_gcode_object = ['G91', 'G1', 'G90', 'G0']
    assert jd.scrape_last_feed_command(job_gcode_object, index) == 0


def test_scrape_last_feed_command_no_obj(jd):
    index = 3
    job_gcode_object = []
    assert jd.scrape_last_feed_command(job_gcode_object, index) == 0


def test_scrape_last_feed_command_no_F(jd):
    index = 2
    job_gcode_object = ['G91X0F1000', 'G1X0F8000', 'X6.776Y6.776Z-0.720F']
    assert jd.scrape_last_feed_command(job_gcode_object, index) == 0


def test_scrape_last_feed_command_feed_start_of_line(jd):
    index = 2
    job_gcode_object = ['G91X0F1000', 'G1X0F8000', 'F6000X6.776Y6.776Z-0.720']
    assert jd.scrape_last_feed_command(job_gcode_object, index) == 6000


def test_scrape_last_feed_command_feed_mid_line(jd):
    index = 0
    job_gcode_object = ['G91F1000X0']
    assert jd.scrape_last_feed_command(job_gcode_object, index) == 1000


def test_remove_line_numbers(jd):
    assert jd.remove_line_number('N14G1X90') == 'G1X90'


def test_remove_line_numbers_mid(jd):
    assert jd.remove_line_number('G1N4X90') == 'G1X90'


def test_remove_line_numbers_on_evil_file(jd):
    file = ['N999 (VECTRIC POST REVISION)',
        'N0 (FC16A22438222CB0A5088D1738135480)', 'N1 T1', 'N2 G17',
        'N3 G21', 'N4 G90', 'G0Z20.320', 'N6 G0X0.000Y0.000', 'N7 S16000M3',
        'N8 G0X-0.218Y0.000Z5.080', 'N9 G0Z2.500',
        'N9999999 G1Z-8.000F381.0', 'N99999999 G1X1099.782F4000.0',
        'N12 G1Y20.000', 'N13 G1X-0.218']
    file_numberless = [' (VECTRIC POST REVISION)',
        ' (FC16A22438222CB0A5088D1738135480)', ' T1', ' G17', ' G21',
        ' G90', 'G0Z20.320', ' G0X0.000Y0.000', ' S16000M3',
        ' G0X-0.218Y0.000Z5.080', ' G0Z2.500', ' G1Z-8.000F381.0',
        ' G1X1099.782F4000.0', ' G1Y20.000', ' G1X-0.218']
    for idx, fileline in enumerate(file):
        assert jd.remove_line_number(fileline) == file_numberless[idx]
