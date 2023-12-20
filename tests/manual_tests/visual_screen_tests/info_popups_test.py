"""
From the easycut folder: python -m tests.manual_tests.visual_screen_tests.info_popups_test
"""
import os
import sys
import textwrap
from functools import partial

from kivy.clock import Clock
from mock.mock import MagicMock


path_to_EC = os.getcwd()
sys.path.append('./src')
os.chdir('./src')

from kivy.app import App

from asmcnc.core_UI.popup_manager import PopupManager
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from asmcnc.skavaUI import popup_info
from asmcnc.comms import localization

from kivy.config import Config

Config.set('kivy', 'keyboard_mode', 'systemanddock')

if sys.platform.startswith("linux"):
    # get screen resolution as "1280x800" or "800x480"
    resolution = os.popen(""" fbset | grep -oP 'mode "\K[^"]+' """).read().strip()
    width, height = resolution.split("x")
    Config.set('graphics', 'width', width)
    Config.set('graphics', 'height', height)
else:
    Config.set('graphics', 'width', '800')
    Config.set('graphics', 'height', '480')

Config.set('graphics', 'maxfps', '60')
Config.set('kivy', 'KIVY_CLOCK', 'interrupt')

# path_to_EC = os.getcwd()
# sys.path.append('./src')
# os.chdir('./src')

Builder.load_string("""
<MenuScreen>:
    BoxLayout:
        Button:
            text: 'Popup'
            on_press: root.test()
""")


# Declare both screens
class MenuScreen(Screen):
    test_no = 0
    popup_no = 0

    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.l = kwargs['l']

        self.wait_popups = None
        self.popup_9_text = 'None'
        self.popup_8_text = 'None'
        self.popup_7_text = 'None'
        self.popup_6_text = 'None'
        self.popup_5_text = 'None'
        self.popup_4_text = 'None'
        self.popup_3_text = 'None'
        self.popup_2_text = 'None'
        self.popup_1_text = 'None'

        print(kwargs)
        self.sm = kwargs['sm']
        self.l = kwargs['l']
        self.set_strings()

    def set_strings(self):
        self.update_strings()
        self.wait_popups = [
            (self.popup_0_text),
            (self.popup_1_text),
            (self.popup_2_text),
            (self.popup_3_text),
            (self.popup_4_text),
            (self.popup_5_text)]
            # (self.popup_6_text),
            # (self.popup_7_text),
            # (self.popup_8_text),
            # (self.popup_9_text)]

    def test(self):
        self.next_lang()
        self.set_strings()

        for i in range(len(self.wait_popups)):
            Clock.schedule_once(lambda dt, i=i: self.cycle(i), i * 3)

    def cycle(self, i):
        Clock.schedule_once(lambda dt: self.open_popup(i), 0.5)

    def open_popup(self, i):
        self.sm.pm.show_wait_popup(self.wait_popups[i])
        Clock.schedule_once(lambda dt: self.sm.pm.close_wait_popup(), 2)
        

    def format_command(self, cmd):
        wrapped_cmd = textwrap.fill(cmd, width=50, break_long_words=False)
        return wrapped_cmd

    def next_lang(self):
        # LOCALIZATION TESTING -----------------------------------------------------------
        if self.test_no < len(self.l.approved_languages):
            lang = self.l.approved_languages[self.test_no]
            self.l.load_in_new_language(lang)
            print("New lang: " + str(lang))
            self.test_no = self.test_no + 1
        else:
            self.test_no = 0

    def update_strings(self):
        self.popup_0_text = self.l.get_str('Downloading logs, please wait') + '...'
        self.popup_1_text = self.l.get_str('Please wait') + '...'
        self.popup_2_text = self.l.get_str('Downloading grbl settings, please wait') + '...'
        self.popup_3_text = self.l.get_str('Restoring grbl settings, please wait') + '...'
        self.popup_4_text = self.l.get_str('Ensuring USB is unmounted, please wait...')
        self.popup_5_text = self.l.get_str("Please wait")
        # self.popup_6_text = 
        # self.popup_7_text =
        # self.popup_8_text =
        # self.popup_9_text =


class TestApp(App):

    def build(self):
        l = localization.Localization()

        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu', sm=sm, l=l))

        m = MagicMock()

        popup_manager = PopupManager(sm, m, l)
        sm.pm = popup_manager

        return sm


if __name__ == '__main__':
    TestApp().run()
