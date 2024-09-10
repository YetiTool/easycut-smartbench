import os
import sys

from core.logging.logging_system import Logger
from core.managers.user_settings_manager import UserSettingsManager

sys.path.append('./src')

try:
    import unittest
    import pytest
    from mock import Mock, MagicMock

except:
    Logger.info("Can't import mocking packages, are you on a dev machine?")

'''
######################################
RUN FROM easycut-smartbench FOLDER WITH: 
python -m pytest tests/automated_unit_tests/comms/test_user_settings_manager.py
######################################
'''


class UserSettingsManagerTests(unittest.TestCase):
    def test_code_coverage(self):
        #  make sure the file does not exist:
        try:
            os.remove(UserSettingsManager.SETTINGS_FILE_PATH)
        except WindowsError:
            # file seems to be gone already...
            pass
        # file should not exist anymore:
        assert not os.path.exists(UserSettingsManager.SETTINGS_FILE_PATH)
        usm = UserSettingsManager()  # make new instance with default values
        usm.save_settings_to_file()
        # file should exist again:
        assert os.path.exists(usm.SETTINGS_FILE_PATH)

        # getters:
        value = usm.get_value('dust_shoe_detection')
        assert value
        title = usm.get_title('dust_shoe_detection')
        assert title == 'Dust shoe plug detection'
        type = usm.get_type('dust_shoe_detection')
        assert type == bool
        description = usm.get_description('dust_shoe_detection')
        assert (description == 'When activated, the dust shoe needs to be inserted '
                               'when starting the spindle or running jobs.')

        # set_value + callback:
        test = {'is_called': False}

        def callback(i, v):
            test['is_called'] = True

        usm.bind(dust_shoe_detection=callback)
        usm.set_value('dust_shoe_detection', False)
        assert test['is_called']
        value = usm.get_value('dust_shoe_detection')
        assert not value

        # bad cases that should raise an exception:
        self.assertRaises(KeyError, usm.get_value, 'setting_does_not_exist')
        self.assertRaises(KeyError, usm.get_title, 'setting_does_not_exist')
        self.assertRaises(KeyError, usm.get_type, 'setting_does_not_exist')
        self.assertRaises(KeyError, usm.get_description, 'setting_does_not_exist')
        self.assertRaises(KeyError, usm.set_value, 'setting_does_not_exist', True)
        self.assertRaises(ValueError, usm.set_value, 'dust_shoe_detection', 'wrong type')



