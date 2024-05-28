import logging
import sys
from asmcnc.comms.logging_system.logging_system import Logger
sys.path.append('./src')
from asmcnc.apps.systemTools_app import screen_manager_systemtools
from asmcnc.comms.localization import Localization
from src.asmcnc.apps.systemTools_app.screen_manager_systemtools import ScreenManagerSystemTools
from src.asmcnc.apps.systemTools_app.screens.screen_support_menu import SupportMenuScreen
try:
    import unittest
    import pytest
    from mock import patch, Mock, create_autospec, call
except Exception as e:
    Logger.info(e)
    Logger.info("Can't import mocking packages, are you on a dev machine?")
"""
RUN WITH 
python -m pytest -p python tests/automated_unit_tests/apps/systemTools/test_system_tools_support.py
FROM EASYCUT-SMARTBENCH DIR
"""


@patch('asmcnc.apps.systemTools_app.screen_manager_systemtools.Clock')
@patch('asmcnc.apps.systemTools_app.screen_manager_systemtools.os')
def test_download_to_usb(mock_os, mock_Clock):
    loc = Localization()
    sm_st = screen_manager_systemtools.ScreenManagerSystemTools(None, None,
        None, None, loc, None)
    sm_st.download_settings_to_usb(Mock())
    copy_to_usb = mock_Clock.method_calls[0][1][0]
    mock_Clock.schedule_once.assert_called()
    sm_st.usb_stick.is_usb_mounted_flag = True
    copy_to_usb(1)
    calls = [call.system(
        'mkdir -p /home/pi/easycut-smartbench/transfer_tmp/easycut-smartbench/src'
        ), call.system(
        'cp -r /home/pi/easycut-smartbench/src/sb_values /home/pi/easycut-smartbench/transfer_tmp/easycut-smartbench/src/'
        ), call.system(
        'rm /home/pi/easycut-smartbench/transfer_tmp/easycut-smartbench/src/sb_values/saved_grbl_settings_params.txt'
        ), call.system(
        'cp -r /home/pi/easycut-smartbench/src/jobCache /home/pi/easycut-smartbench/transfer_tmp/easycut-smartbench/src/'
        ), call.system(
        'cp /home/pi/smartbench* /home/pi/easycut-smartbench/transfer_tmp/'
        ), call.system(
        'cp /home/pi/multiply.txt /home/pi/easycut-smartbench/transfer_tmp/'
        ), call.system(
        'cp /home/pi/plus.txt /home/pi/easycut-smartbench/transfer_tmp/'),
        call.system(
        'sudo tar czf /media/usb/transfer.tar.gz -C /home/pi/easycut-smartbench/transfer_tmp .'
        ), call.system('rm -r /home/pi/easycut-smartbench/transfer_tmp'),
        call.path.isfile('/media/usb/transfer.tar.gz')]
    mock_os.assert_has_calls(calls)


@patch('asmcnc.apps.systemTools_app.screen_manager_systemtools.Clock')
@patch('asmcnc.apps.systemTools_app.screen_manager_systemtools.os')
def test_upload_from_usb(mock_os, mock_Clock):
    loc = Localization()
    sm_st = screen_manager_systemtools.ScreenManagerSystemTools(None, None,
        None, None, loc, None)
    sm_st.upload_settings_from_usb(Mock())
    restore_settings_from_usb = mock_Clock.method_calls[0][1][0]
    mock_Clock.schedule_once.assert_called()
    sm_st.usb_stick.is_usb_mounted_flag = True
    restore_settings_from_usb(1)
    calls = []
    calls.append(call.path.isfile('/media/usb/transfer.tar.gz'))
    calls.append(call.path.isfile().__nonzero__())
    calls.append(call.system(
        'sudo tar xf /media/usb/transfer.tar.gz -C /home/pi/'))
    calls.append(call.system('sudo rm /media/usb/transfer.tar.gz'))
    mock_os.assert_has_calls(calls)
