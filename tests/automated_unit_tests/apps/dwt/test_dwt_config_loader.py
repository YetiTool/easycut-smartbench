import sys, os
from asmcnc.apps.drywall_cutter_app.config.config_loader import DWTConfig

sys.path.append('./src')

try:
    import unittest
    import pytest
    from mock import Mock, MagicMock

except Exception as e:
    print(e)
    print("Can't import mocking packages, are you on a dev machine?")


def test_load_config():
    dwt_config = DWTConfig()

    dwt_config.load_config('test_config.json')

    assert dwt_config.active_config.shape_type == 'rectangle'
