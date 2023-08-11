import sys, os

sys.path.append("./src")
try:
    import unittest
    import pytest
    from mock import Mock, MagicMock
except:
    print("Can't import mocking packages, are you on a dev machine?")
from asmcnc.comms import router_machine
from asmcnc.comms import localization
from datetime import datetime

"""
######################################
RUN FROM easycut-smartbench FOLDER WITH: 
python -m pytest --show-capture=no --disable-pytest-warnings tests/automated_unit_tests/comms/test_smartbench_model_detection.py
######################################
"""


@pytest.fixture
def m():
    l = localization.Localization()
    screen_manager = Mock()
    settings_manager = Mock()
    job = Mock()
    m = router_machine.RouterMachine("COM", screen_manager, settings_manager, l, job)
    m.s.next_poll_time = 0
    m.s.write_direct = Mock()
    m.s.s = MagicMock()
    return m


def test_initial_failure(m):
    assert m.smartbench_model() == "SmartBench model detection failed"


def test_mini_v1_3_precision_pro(m):
    m.grbl_y_max_travel = 1500
    m.s.versions.hardware = 32
    assert m.smartbench_model() == "SmartBench Mini V1.3 PrecisionPro"


def test_v1_3_precision_pro(m):
    m.grbl_y_max_travel = 2500
    m.s.versions.hardware = 32
    m.s.versions.firmware = "2.3.5.4"
    assert m.smartbench_model() == "SmartBench V1.3 PrecisionPro CNC Router"


def test_v1_2_precision_pro(m):
    m.grbl_y_max_travel = 2500
    m.s.versions.hardware = 19
    m.s.versions.firmware = "1.4.0"
    assert m.smartbench_model() == "SmartBench V1.2 PrecisionPro CNC Router"


def test_v1_2_precision_pro_replacement_board(m):
    m.grbl_y_max_travel = 2500
    m.s.versions.hardware = 36
    m.s.versions.firmware = "1.4.0"
    assert m.smartbench_model() == "SmartBench V1.2 PrecisionPro CNC Router"


def test_v1_2_precision(m):
    m.grbl_y_max_travel = 2500
    m.s.versions.hardware = 19
    m.s.versions.firmware = "1.1.2"
    m.s.settings.s50 = 0.03
    assert m.smartbench_model() == "SmartBench V1.2 Precision CNC Router"


def test_v1_2_standard(m):
    m.grbl_y_max_travel = 2500
    m.s.versions.hardware = 19
    m.s.versions.firmware = "1.1.2"
    m.s.settings.s50 = 0.02
    assert m.smartbench_model() == "SmartBench V1.2 Standard CNC Router"


def test_v1_1(m):
    m.grbl_y_max_travel = 2500
    m.s.versions.hardware = 5
    m.s.versions.firmware = "1.1.2"
    m.s.settings.s50 = 0.01
    assert m.smartbench_model() == "SmartBench V1.1 CNC Router"


def test_v1_0(m):
    m.grbl_y_max_travel = 2500
    m.s.versions.hardware = 4
    m.s.versions.firmware = "1.1.2"
    m.s.settings.s50 = 0.01
    assert m.smartbench_model() == "SmartBench V1.0 CNC Router"
