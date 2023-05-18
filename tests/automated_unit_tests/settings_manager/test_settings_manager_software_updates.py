'''
Created on 18 May 2023
@author: Letty
'''

import sys, os
sys.path.append('./src')
import re

try: 
    import unittest
    import pytest
    from mock import Mock, MagicMock

except: 
    print("Can't import mocking packages, are you on a dev machine?")

from settings.settings_manager import Settings


'''
######################################
RUN FROM easycut-smartbench FOLDER WITH: 
python -m pytest --show-capture=no --disable-pytest-warnings tests/automated_unit_tests/settings_manager/test_settings_manager_software_updates.py
######################################
'''

# FIXTURES
@pytest.fixture
def sett():
    screen_manager = Mock()
    s = Settings(screen_manager)
    return s

@pytest.fixture
def version_pattern():
    pattern = re.compile(r"^v\d+\.\d+\.\d+$")
    return pattern

@pytest.fixture
def beta_pattern():
    pattern = re.compile(r"^v\d+\.\d+\.\d+-beta")
    return pattern

# Check that we've set the settings object up correctly
def test_get_sett(sett):
    assert sett.ping_command == 'ping -c1 one.one.one.one'

def test_refresh_latest_sw_version(sett, version_pattern, beta_pattern):
    sett.refresh_latest_sw_version()
    assert version_pattern.match(sett.latest_sw_version)
    assert beta_pattern.match(sett.latest_sw_beta)

# def test_get_software_tag_version_list(sett, version_pattern):
    # assert sett.get_software_tag_version_list() == []
    # E       AssertionError: assert ['v2.4.2', 'v...'v2.2.0', ...] == []
    # E         Left contains 11 more items, first extra item: 'v2.4.2'
    # E         Full diff:
    # E         + []
    # E         - ['v2.4.2',
    # E         -  'v2.4.1',
    # E         -  'v2.4.0',
    # E         -  'v2.3.0',
    # E         -  'v2.2.1',
    # E         -  'v2.2.0',
    # E         -  'v2.1.0',
    # E         -  'v2.0.6',
    # E         -  'v2.0.5',
    # E         -  'v2.0.4',
    # E         -  '']
    # assert version_pattern.match(sett.get_software_tag_version_list()[-1])

    # for i in sett.get_software_tag_version_list():
    #     assert version_pattern.match(i)

# def test_get_software_tag_beta_list(sett, beta_pattern):
#     for i in sett.get_software_tag_beta_list():
#         assert beta_pattern.match(i)

