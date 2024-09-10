import os
import sys

from core.logging.logging_system import Logger

sys.path.append('./src')
from apps.drywall_cutter_app.config import config_loader

from apps.drywall_cutter_app.screen_drywall_cutter import DrywallCutterScreen
from core.serial import router_machine

try:
    import unittest
    import pytest
    from mock import Mock, MagicMock

except Exception as e:
    Logger.info(e)
    Logger.info("Can't import mocking packages, are you on a dev machine?")

"""
RUN WITH 
python -m pytest -p python tests/automated_unit_tests/apps/dwt/test_dwt_config.py
FROM EASYCUT-SMARTBENCH DIR
"""


@pytest.fixture
def m():
    l = None
    screen_manager = Mock()
    settings_manager = Mock()
    job = Mock()
    m = router_machine.RouterMachine("COM", screen_manager, settings_manager, l, job)
    m.s.s = MagicMock()
    return m


@pytest.fixture(scope="module")
def l():
    return Mock()


@pytest.fixture(scope="module")
def sm():
    return Mock()


def test_load_config():
    dwt_config = config_loader.DWTConfig()

    dwt_config.load_config('test_config')

    assert dwt_config.active_config.shape_type == 'rectangle'


def test_save_config():
    dwt_config = config_loader.DWTConfig()

    dwt_config.load_config('test_config')

    dwt_config.save_config('test_config_saved')

    assert os.path.exists('src/asmcnc/apps/drywall_cutter_app/config/configurations/test_config_saved')


def test_load_cutter():
    dwt_config = config_loader.DWTConfig()

    dwt_config.load_cutter('tool_6mm.json')

    assert dwt_config.active_cutter.description == '6mm drywall cutter'


def test_save_temp_config():
    dwt_config = config_loader.DWTConfig()

    dwt_config.save_temp_config()

    assert os.path.exists(os.path.join('src', config_loader.TEMP_CONFIG_PATH))


def test_on_parameter_change():
    dwt_screen = DrywallCutterScreen(machine=m, screen_manager=sm, localization=l)

    dwt_screen.dwt_config.on_parameter_change('shape_type', 'circle')
    dwt_screen.dwt_config.on_parameter_change('cutting_depths.material_thickness', 0.5)

    assert dwt_screen.dwt_config.active_config.shape_type == 'circle'
    assert dwt_screen.dwt_config.active_config.cutting_depths.material_thickness == 0.5


def test_get_available_cutter_names():
    dwt_config = config_loader.DWTConfig()

    assert dwt_config.get_available_cutter_names() == {
        'unique_label': 'tool_6mm.json',
        'cutter 2': 'test_cutter2.json'
    }
