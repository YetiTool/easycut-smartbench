import logging
import sys
from asmcnc.comms.logging_system.logging_system import Logger
from tests import test_utils
sys.path.append('./src')
try:
    import unittest
    import pytest
    from mock import Mock, MagicMock
except:
    Logger.info("Can't import mocking packages, are you on a dev machine?")
from asmcnc.comms import router_machine
from asmcnc.comms import localization
"""
######################################
RUN FROM easycut-smartbench FOLDER WITH: 
python -m pytest tests/automated_unit_tests/comms/test_smartbench_model_detection.py

THIS TEST STILL FAILS
E       AssertionError: assert 'DRYWALLTEC SmartCNC' == 'SmartBench V1.2 Standard CNC Router'
E         - DRYWALLTEC SmartCNC
E         + SmartBench V1.2 Standard CNC Router


######################################
"""
test_utils.create_app()


@pytest.fixture
def m():
    l = localization.Localization()
    screen_manager = Mock()
    settings_manager = Mock()
    job = Mock()
    m = router_machine.RouterMachine('COM', screen_manager,
        settings_manager, l, job)
    m.s.next_poll_time = 0
    m.s.write_direct = Mock()
    m.s.s = MagicMock()
    return m


def test_initial_failure(m):
    m.bench_is_dwt = Mock(return_value=False)
    assert m.smartbench_model() == 'SmartBench model detection failed'


def test_drywalltec_smartcnc(m):
    m.bench_is_dwt = Mock(return_value=False)
    m.grbl_y_max_travel = 2500
    m.s.setting_50 = 0.04
    assert m.smartbench_model() == 'DRYWALLTEC SmartCNC'


def test_precision_pro_x(m):
    m.bench_is_dwt = Mock(return_value=False)
    m.grbl_y_max_travel = 2500
    m.s.setting_50 = 0.05
    assert m.smartbench_model() == 'SmartBench V1.3 PrecisionPro X'


def test_precision_pro_plus(m):
    m.bench_is_dwt = Mock(return_value=False)
    m.grbl_y_max_travel = 2500
    m.s.setting_50 = 0.04
    assert m.smartbench_model() == 'SmartBench V1.3 PrecisionPro Plus'


def test_mini_v1_3_precision_pro(m):
    m.bench_is_dwt = Mock(return_value=False)
    m.grbl_y_max_travel = 1500
    m.s.hw_version = 32
    assert m.smartbench_model() == 'SmartBench Mini V1.3 PrecisionPro'


def test_v1_3_precision_pro(m):
    m.bench_is_dwt = Mock(return_value=False)
    m.grbl_y_max_travel = 2500
    m.s.hw_version = 32
    m.s.fw_version = '2.3.5.4'
    assert m.smartbench_model() == 'SmartBench V1.3 PrecisionPro CNC Router'


def test_v1_2_precision_pro(m):
    m.bench_is_dwt = Mock(return_value=False)
    m.grbl_y_max_travel = 2500
    m.s.hw_version = 19
    m.s.fw_version = '1.4.0'
    assert m.smartbench_model() == 'SmartBench V1.2 PrecisionPro CNC Router'


def test_v1_2_precision_pro_replacement_board(m):
    m.bench_is_dwt = Mock(return_value=False)
    m.grbl_y_max_travel = 2500
    m.s.hw_version = 36
    m.s.fw_version = '1.4.0'
    assert m.smartbench_model() == 'SmartBench V1.2 PrecisionPro CNC Router'


def test_v1_2_precision(m):
    m.bench_is_dwt = Mock(return_value=False)
    m.grbl_y_max_travel = 2500
    m.s.hw_version = 19
    m.s.fw_version = '1.1.2'
    m.s.setting_50 = 0.03
    assert m.smartbench_model() == 'SmartBench V1.2 Precision CNC Router'


def test_v1_2_standard(m):
    m.bench_is_dwt = Mock(return_value=False)
    m.grbl_y_max_travel = 2500
    m.s.hw_version = 19
    m.s.fw_version = '1.1.2'
    m.s.setting_50 = 0.02
    assert m.smartbench_model() == 'SmartBench V1.2 Standard CNC Router'


def test_v1_1(m):
    m.bench_is_dwt = Mock(return_value=False)
    m.grbl_y_max_travel = 2500
    m.s.hw_version = 5
    m.s.fw_version = '1.1.2'
    m.s.setting_50 = 0.01
    assert m.smartbench_model() == 'SmartBench V1.1 CNC Router'


def test_v1_0(m):
    m.bench_is_dwt = Mock(return_value=False)
    m.grbl_y_max_travel = 2500
    m.s.hw_version = 4
    m.s.fw_version = '1.1.2'
    m.s.setting_50 = 0.01
    assert m.smartbench_model() == 'SmartBench V1.0 CNC Router'


def test_drywalltec_machine(m):
    m.bench_is_dwt = Mock(return_value=True)
    assert m.smartbench_model() == 'DRYWALLTEC SmartCNC'
