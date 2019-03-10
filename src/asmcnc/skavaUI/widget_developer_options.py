'''
Created on 1 Feb 2018
@author: Ed
'''

import sys, os, subprocess

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty # @UnresolvedImport
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.base import runTouchApp
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty, NumericProperty, StringProperty # @UnresolvedImport


Builder.load_string("""

<DevOptions>:

    sw_version_label:sw_version_label
    sw_branch_label:sw_branch_label

    GridLayout:
        size: self.parent.size
        pos: self.parent.pos
        cols: 2
#         rows: 2

        Button:
            text: 'Reboot'
            on_release: root.reboot()
        Button:
            text: 'Quit to Console'
            on_release: root.quit_to_console()
        Button:
            text: 'Square axes'
            on_release: root.square_axes()
        Button:
            text: 'Return to lobby'
            on_release: root.return_to_lobby()
        BoxLayout:
            orientation: 'vertical'
            Switch:
                active: False
            Label:
                text: 'GRBL gcode check'
                font_size: 18
                color: 0,0,0,1
        ToggleButton:
            state: root.buffer_log_mode
            text: 'Buffer Log'
            on_state:
                root.buffer_log_mode = self.state
                print root.buffer_log_mode
        ToggleButton:
            state: root.virtual_hw_mode
            text: 'Virtual HW'
            on_state:
                root.virtual_hw_mode = self.state
                root.virtual_hw_toggled()
        Button:
            text: 'Get SW update'
            on_release: root.get_sw_update()
        Label:
            test: 'Repository Branch'
            font_size: 18
            color: 0,0,0,1
            id: sw_branch_label
        Label:
            text: 'SW VER'
            font_size: 18
            color: 0,0,0,1
            id: sw_branch_label
            id: sw_version_label
""")


class DevOptions(Widget):

    buffer_log_mode = StringProperty('normal') # toggles between 'normal' or 'down'(/looks like it's been pressed)
    virtual_hw_mode = StringProperty('normal') # toggles between 'normal' or 'down'(/looks like it's been pressed)

    def __init__(self, **kwargs):

        super(DevOptions, self).__init__(**kwargs)
        self.m=kwargs['machine']
        self.sm=kwargs['screen_manager']
        self.refresh_sw_branch_label()
        self.refresh_sw_version_label()

    def virtual_hw_toggled(self):
        if self.virtual_hw_mode == 'normal': # virtual hw mode OFF
            #turn soft limits, hard limts and homing cycle ON
            print 'Virtual HW mode OFF: switching soft limits, hard limts and homing cycle on'
            settings = ['$22=1','$21=1','$20=1']
            self.m.s.start_sequential_stream(settings)
        if self.virtual_hw_mode == 'down': # virtual hw mode ON
            #turn soft limits, hard limts and homing cycle OFF
            print 'Virtual HW mode ON: switching soft limits, hard limts and homing cycle off'
            settings = ['$22=0','$20=0','$21=0']
            self.m.s.start_sequential_stream(settings)

    def reboot(self):

        if sys.platform != "win32":
            sudoPassword = 'posys'
            command = 'sudo reboot'
            p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))

    def quit_to_console(self):
        print 'Bye!'
        sys.exit()

    def square_axes(self):
        self.m.is_squaring_XY_needed_after_homing = True
        self.m.home_all()

    def return_to_lobby(self):
        #self.sm.transition = SlideTransition()
        #self.sm.transition.direction = 'up'
        self.sm.current = 'lobby'

    def refresh_sw_branch_label(self):
        data = subprocess.check_output(["git", "symbolic-ref", "--short", "HEAD"]).strip()
        self.sw_branch_label.text = data

    def refresh_sw_version_label(self):
        data = subprocess.check_output(["git", "describe", "--always"]).strip()
        self.sw_version_label.text = data

    def get_sw_update(self):
        os.system("cd /home/pi/easycut-smartbench/ && git pull")
