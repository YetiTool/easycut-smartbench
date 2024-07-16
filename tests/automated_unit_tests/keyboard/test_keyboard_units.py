# -*- coding: utf-8 -*-
'''
Created on 16 Jul 2024
@author: Letty
'''

import sys, os
sys.path.append('./src')

try: 
    import unittest
    import pytest
    from mock import Mock, MagicMock

except: 
    Logger.info("Can't import mocking packages, are you on a dev machine?")

from asmcnc.keyboard.custom_keyboard import Keyboard
from asmcnc.comms import localization
from datetime import datetime

from kivy.clock import Clock

'''
######################################
RUN FROM easycut-smartbench FOLDER WITH: 
python -m pytest tests/automated_unit_tests/keyboard/test_keyboard_units.py
######################################
'''

# FIXTURES
@pytest.fixture
def kb():
    l = localization.Localization()
    kb = Keyboard(localization=l)
    return kb


def test_get_kb(kb):
    assert kb.font_color == [0, 0, 0, 1]

def test_generate_kanji_suggestions(kb):
    kana_string = "まほうしょうじょ"
    kanji_output = ['魔法少女','魔法省所','魔法省女','魔法消除','魔法小所','魔法昇叙','魔法証所','魔法性所','魔法症所']
    assert kb.generate_kanji_suggestions(kana_string) == kanji_output

def test_create_kanji_layout(kb):
    assert kb.build_layout_with_kanji()