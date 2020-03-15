'''
Created on 16 Nov 2017
@author: Ed
YetiTool's UI for SmartBench
www.yetitool.com
'''

#config
#import os
#os.environ['KIVY_GL_BACKEND'] = 'sdl2'
import time
import sys, os

from kivy.config import Config
from kivy.clock import Clock
Config.set('kivy', 'keyboard_mode', 'systemanddock')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
Config.set('graphics', 'maxfps', '60')
Config.set('kivy', 'KIVY_CLOCK', 'interrupt')
Config.write()

import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window

from asmcnc.comms import router_machine 
# NB: router_machine imports serial_connection
from asmcnc.apps import app_manager

from asmcnc.skavaUI import screen_initial, screen_help
from asmcnc.skavaUI import screen_home
from asmcnc.skavaUI import screen_local_filechooser
from asmcnc.skavaUI import screen_usb_filechooser
from asmcnc.skavaUI import screen_go
from asmcnc.skavaUI import screen_template
from asmcnc.skavaUI import screen_lobby
from asmcnc.skavaUI import screen_vj_polygon
from asmcnc.skavaUI import screen_file_loading
from asmcnc.skavaUI import screen_check_job
from asmcnc.skavaUI import screen_alarm
from asmcnc.skavaUI import screen_error
from asmcnc.skavaUI import screen_serial_failure
from asmcnc.skavaUI import screen_homing
from asmcnc.skavaUI import screen_safety_warning
from asmcnc.skavaUI import screen_mstate_warning
from asmcnc.skavaUI import screen_homing_warning
from asmcnc.skavaUI import screen_boundary_warning
from asmcnc.skavaUI import screen_rebooting
from asmcnc.skavaUI import screen_job_done
from asmcnc.skavaUI import screen_developer
from asmcnc.skavaUI import screen_diagnostics

Cmport = 'COM3'

if sys.platform != 'win32':
    
    case = (os.popen('grep -Fx "gpu_mem=128" /boot/config.txt').read())
    if case == 0:
        os.system('sudo sed -i "s/gpu_mem=128/gpu_mem=256/" /boot/config.txt')     
        os.system('sudo reboot')   
    elif case == 1:
        print "gpu mem already 256"
    elif case == 2:
        print "an error occured re-assigning gpu memory"
    else:
        print case
        print "popen failed"

class SkavaUI(App):

    def build(self):

        print("Starting " + time.strftime('%H:%M:%S'))
        # Establish screens
        sm = ScreenManager(transition=NoTransition())

        # Initialise 'm'achine object
        m = router_machine.RouterMachine(Cmport, sm)
        
        job_gcode = []  # declare g-code object
        
        am = app_manager.AppManagerClass(sm, m)
        
        # initialise the screens
        lobby_screen = screen_lobby.LobbyScreen(name='lobby', screen_manager = sm, machine = m, app_manager = am)
        home_screen = screen_home.HomeScreen(name='home', screen_manager = sm, machine = m, job = job_gcode)
        local_filechooser = screen_local_filechooser.LocalFileChooser(name='local_filechooser', screen_manager = sm)
        usb_filechooser = screen_usb_filechooser.USBFileChooser(name='usb_filechooser', screen_manager = sm)
        go_screen = screen_go.GoScreen(name='go', screen_manager = sm, machine = m, job = job_gcode)
        template_screen = screen_template.TemplateScreen(name='template', screen_manager = sm)
        vj_polygon_screen = screen_vj_polygon.ScreenVJPolygon(name='vj_polygon', screen_manager = sm)
        loading_screen = screen_file_loading.LoadingScreen(name = 'loading', screen_manager = sm, machine =m, job = job_gcode)
        checking_screen = screen_check_job.CheckingScreen(name = 'check_job', screen_manager = sm, machine =m, job = job_gcode)
        error_screen = screen_error.ErrorScreenClass(name='errorScreen', screen_manager = sm, machine = m)
        alarm_screen = screen_alarm.AlarmScreenClass(name='alarmScreen', screen_manager = sm, machine = m)
        serial_screen = screen_serial_failure.SerialFailureClass(name='serialScreen', screen_manager = sm, machine = m, win_port = Cmport)
        homing_screen = screen_homing.HomingScreen(name = 'homing', screen_manager = sm, machine =m)
        safety_screen = screen_safety_warning.SafetyScreen(name = 'safety', screen_manager = sm)
        mstate_screen = screen_mstate_warning.WarningMState(name = 'mstate', screen_manager = sm, machine =m)
        homing_warning_screen = screen_homing_warning.WarningHoming(name = 'homingWarning', screen_manager = sm, machine =m)
        boundary_warning_screen = screen_boundary_warning.BoundaryWarningScreen(name='boundary',screen_manager = sm, machine = m)
        rebooting_screen = screen_rebooting.RebootingScreen(name = 'rebooting', screen_manager = sm)
        job_done_screen = screen_job_done.JobDoneScreen(name = 'jobdone', screen_manager = sm, machine =m)
        developer_screen = screen_developer.DeveloperScreen(name = 'dev', screen_manager = sm, machine =m)
        diagnostics_screen = screen_diagnostics.DiagnosticsScreen(name = 'diagnostics', screen_manager = sm, machine =m)

        # add the screens to screen manager
        sm.add_widget(lobby_screen)
        sm.add_widget(home_screen)
        sm.add_widget(local_filechooser)
        sm.add_widget(usb_filechooser)
        sm.add_widget(go_screen)
        sm.add_widget(template_screen)
        sm.add_widget(vj_polygon_screen)
        sm.add_widget(loading_screen)
        sm.add_widget(checking_screen)
        sm.add_widget(error_screen)
        sm.add_widget(alarm_screen)
        sm.add_widget(serial_screen)
        sm.add_widget(homing_screen)
        sm.add_widget(safety_screen)
        sm.add_widget(mstate_screen)
        sm.add_widget(homing_warning_screen)
        sm.add_widget(boundary_warning_screen)
        sm.add_widget(rebooting_screen)
        sm.add_widget(job_done_screen)
        sm.add_widget(developer_screen)
        sm.add_widget(diagnostics_screen)

        # set screen to start on
        sm.current = 'lobby'
        return sm


if __name__ == '__main__':

    SkavaUI().run()