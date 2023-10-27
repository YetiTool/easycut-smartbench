import sys, os

sys.path.append('./src')

from asmcnc.apps.drywall_cutter_app.config.config_loader import DWTConfig

try:
    import unittest
    import pytest
    from mock import Mock, MagicMock

except Exception as e:
    print(e)
    print("Can't import mocking packages, are you on a dev machine?")


def test_load_config():
    dwt_config = DWTConfig()

    os.chdir('./src')
    dwt_config.load_config('test_config.json')

    assert dwt_config.active_config.shape_type == 'rectangle'


def test_save_config():
    dwt_config = DWTConfig()

    dwt_config.load_config('test_config.json')

    dwt_config.save_config('test_config_saved.json')

    assert os.path.exists('asmcnc/apps/drywall_cutter_app/config/configurations/test_config_saved.json')


def test_load_cutter():
    dwt_config = DWTConfig()

    dwt_config.load_cutter('test_cutter.json')

    assert dwt_config.active_cutter.cutter_description == 'unique_label'