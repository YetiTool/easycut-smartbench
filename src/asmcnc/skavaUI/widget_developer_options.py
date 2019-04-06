'''
Created on 1 Feb 2018
@author: Ed
'''

import sys, os

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
        Button:
            text: 'Bake GRBL settings'
            on_release: root.bake_grbl_settings()
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
        self.sm.get_screen('homing').is_squaring_XY_needed_after_homing = True
        self.m.home_all()

    def return_to_lobby(self):
        #self.sm.transition = SlideTransition()
        #self.sm.transition.direction = 'up'
        self.sm.current = 'lobby'

    def refresh_sw_branch_label(self):
        data = os.popen("git symbolic-ref --short HEAD").read()
        self.sw_branch_label.text = data

    def refresh_sw_version_label(self):
        data = os.popen("git describe --always").read()
        self.sw_version_label.text = data

    def get_sw_update(self):
        os.system("cd /home/pi/easycut-smartbench/ && git pull")
        self.reboot()

    def bake_grbl_settings(self):
        grbl_settings = [
                    '$0=10',    #Step pulse, microseconds
                    '$1=255',    #Step idle delay, milliseconds
                    '$2=4',           #Step port invert, mask
                    '$3=1',           #Direction port invert, mask
                    '$4=0',           #Step enable invert, boolean
                    '$5=1',           #Limit pins invert, boolean
                    '$6=0',           #Probe pin invert, boolean
                    '$10=3',          #Status report, mask <----------------------
                    '$11=0.010',      #Junction deviation, mm
                    '$12=0.002',      #Arc tolerance, mm
                    '$13=0',          #Report inches, boolean
                    '$20=1',          #Soft limits, boolean <-------------------
                    '$21=1',          #Hard limits, boolean <------------------
                    '$22=1',          #Homing cycle, boolean <------------------------
                    '$23=3',          #Homing dir invert, mask
                    '$24=600.0',     #Homing feed, mm/min
                    '$25=3000.0',    #Homing seek, mm/min
                    '$26=250',        #Homing debounce, milliseconds
                    '$27=15.000',      #Homing pull-off, mm
                    '$30=25000.0',      #Max spindle speed, RPM
                    '$31=0.0',         #Min spindle speed, RPM
                    '$32=0',           #Laser mode, boolean
                    '$100=56.649',   #X steps/mm
                    '$101=56.623',   #Y steps/mm
                    '$102=1066.667',   #Z steps/mm
                    '$110=6000.0',   #X Max rate, mm/min
                    '$111=6000.0',   #Y Max rate, mm/min
                    '$112=750.0',   #Z Max rate, mm/min
                    '$120=500.0',    #X Acceleration, mm/sec^2
                    '$121=200.0',    #Y Acceleration, mm/sec^2
                    '$122=200.0',    #Z Acceleration, mm/sec^2
                    '$130=1237.0',   #X Max travel, mm TODO: Link to a settings object
                    '$131=2470.0',   #Y Max travel, mm
                    '$132=143.0',   #Z Max travel, mm
                    '$$', # Echo grbl settings, which will be read by sw, and internal parameters sync'd
                    '$#' # Echo grbl parameter info, which will be read by sw, and internal parameters sync'd
            ]

        self.m.s.start_sequential_stream(grbl_settings, reset_grbl_after_stream=True)   # Send any grbl specific parameters