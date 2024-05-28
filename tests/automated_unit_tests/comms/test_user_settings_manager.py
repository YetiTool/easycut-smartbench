import logging
import os
import sys
from asmcnc.comms.logging_system.logging_system import Logger
from asmcnc.comms.user_settings_manager import UserSettingsManager
sys.path.append('./src')
try:
    import unittest
    import pytest
    from mock import Mock, MagicMock
except:
    Logger.info("Can't import mocking packages, are you on a dev machine?")
"""
######################################
RUN FROM easycut-smartbench FOLDER WITH: 
python -m pytest tests/automated_unit_tests/comms/test_user_settings_manager.py
######################################
"""


class UserSettingsManagerTests(unittest.TestCase):

    def test_code_coverage(self):
        try:
            os.remove(UserSettingsManager.SETTINGS_FILE_PATH)
        except WindowsError:
            pass
        assert not os.path.exists(UserSettingsManager.SETTINGS_FILE_PATH)
        usm = UserSettingsManager()
        usm.save_settings_to_file()
        assert os.path.exists(usm.SETTINGS_FILE_PATH)
        value = usm.get_value('dust_shoe_detection')
        assert value
        title = usm.get_title('dust_shoe_detection')
        assert title == 'Dust shoe plug detection'
        type = usm.get_type('dust_shoe_detection')
        assert type == bool
        description = usm.get_description('dust_shoe_detection')
        assert description == 'When activated, the dust shoe needs to be inserted when starting the spindle or running jobs.'
        test = {'is_called': False}

        def callback(i, v):
            test['is_called'] = True
        usm.bind(dust_shoe_detection=callback)
        usm.set_value('dust_shoe_detection', False)
        assert test['is_called']
        value = usm.get_value('dust_shoe_detection')
        assert not value
        self.assertRaises(KeyError, usm.get_value, 'setting_does_not_exist')
        self.assertRaises(KeyError, usm.get_title, 'setting_does_not_exist')
        self.assertRaises(KeyError, usm.get_type, 'setting_does_not_exist')
        self.assertRaises(KeyError, usm.get_description,
            'setting_does_not_exist')
        self.assertRaises(KeyError, usm.set_value, 'setting_does_not_exist',
            True)
        self.assertRaises(ValueError, usm.set_value, 'dust_shoe_detection',
            'wrong type')
