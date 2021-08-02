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
from datetime import datetime
import os.path
from os import path

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


# COMMS IMPORTS
from asmcnc.comms import router_machine  # @UnresolvedImport
from asmcnc.comms import database_storage # @UnresolvedImport
from asmcnc.comms import server_connection
from asmcnc.comms import archie_db

# NB: router_machine imports serial_connection
from asmcnc.apps import app_manager # @UnresolvedImport
from settings import settings_manager # @UnresolvedImport

# SKAVAUI IMPORTS (LEGACY)
from asmcnc.skavaUI import screen_home # @UnresolvedImport
from asmcnc.skavaUI import screen_local_filechooser # @UnresolvedImport
from asmcnc.skavaUI import screen_usb_filechooser # @UnresolvedImport
from asmcnc.skavaUI import screen_go # @UnresolvedImport
from asmcnc.skavaUI import screen_jobstart_warning
from asmcnc.skavaUI import screen_lobby # @UnresolvedImport
from asmcnc.skavaUI import screen_file_loading # @UnresolvedImport
from asmcnc.skavaUI import screen_check_job # @UnresolvedImport
from asmcnc.skavaUI import screen_error # @UnresolvedImport
from asmcnc.skavaUI import screen_serial_failure # @UnresolvedImport
from asmcnc.skavaUI import screen_homing # @UnresolvedImport
from asmcnc.skavaUI import screen_safety_warning # @UnresolvedImport
from asmcnc.skavaUI import screen_mstate_warning # @UnresolvedImport
from asmcnc.skavaUI import screen_boundary_warning # @UnresolvedImport
from asmcnc.skavaUI import screen_rebooting # @UnresolvedImport
from asmcnc.skavaUI import screen_job_done # @UnresolvedImport
from asmcnc.skavaUI import screen_powercycle_alert # @UnresolvedImport
from asmcnc.skavaUI import screen_door # @UnresolvedImport
from asmcnc.skavaUI import screen_squaring_manual_vs_square # @UnresolvedImport
from asmcnc.skavaUI import screen_homing_prepare # @UnresolvedImport
from asmcnc.skavaUI import screen_homing_active # @UnresolvedImport
from asmcnc.skavaUI import screen_squaring_active # @UnresolvedImport
from asmcnc.skavaUI import screen_welcome # @UnresolvedImport
from asmcnc.skavaUI import screen_spindle_shutdown # @UnresolvedImport
from asmcnc.skavaUI import screen_spindle_cooldown
from asmcnc.skavaUI import screen_stop_or_resume_decision # @UnresolvedImport
from asmcnc.skavaUI import screen_lift_z_on_pause_decision # @UnresolvedImport
from asmcnc.skavaUI import screen_tool_selection # @UnresolvedImport



# developer testing
Cmport = 'COM3'

# Current version active/working on
initial_version = 'v1.7.2'

# default starting screen
start_screen = 'welcome'

# Config management
def check_and_update_gpu_mem():
    # System config (this should eventually be moved into platform management)
    # Update GPU memory to handle more app
    case = (os.popen('grep -Fx "gpu_mem=128" /boot/config.txt').read())
    if case.startswith('gpu_mem=128'):
        os.system('sudo sed -i "s/gpu_mem=128/gpu_mem=256/" /boot/config.txt')     
        os.system('sudo reboot')
        
def check_and_update_config():
    
    def ver0_configuration():
        if (os.popen('grep "version=0" /home/pi/easycut-smartbench/src/config.txt').read()).startswith('version=0'):
            os.system('cd /home/pi/easycut-smartbench/ && git update-index --skip-worktree /home/pi/easycut-smartbench/src/config.txt')
            os.system('sudo sed -i "s/config_skipped_by_git=False/config_skipped_by_git=True/" /home/pi/easycut-smartbench/src/config.txt') 
            os.system('sudo sed -i "s/version=0/version=' + initial_version + '/" /home/pi/easycut-smartbench/src/config.txt')   
    
    if (os.popen('grep "check_config=True" /home/pi/easycut-smartbench/src/config.txt').read()).startswith('check_config=True'):
        ver0_configuration()
        os.system('sudo sed -i "s/check_config=True/check_config=False/" /home/pi/easycut-smartbench/src/config.txt')
        check_and_update_gpu_mem()

        # if software update has happened, launch the power cycle screen instead
        check_and_launch_powercycle_screen()        

def check_and_launch_powercycle_screen():
    # Check whether machine needs to be power cycled (currently only after a software update)
    pc_alert = (os.popen('grep "power_cycle_alert=True" /home/pi/easycut-smartbench/src/config.txt').read())
    if pc_alert.startswith('power_cycle_alert=True'):
        os.system('sudo sed -i "s/power_cycle_alert=True/power_cycle_alert=False/" /home/pi/easycut-smartbench/src/config.txt') 
        global start_screen
        start_screen = 'pc_alert'


if sys.platform != 'win32' and sys.platform != 'darwin':
    
    ## Easycut config
    check_and_update_config()

def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + message)


class SkavaUI(App):


    def build(self):

        log("Starting App:")

        # Establish screens
        sm = ScreenManager(transition=NoTransition())

        if start_screen == 'pc_alert': 
            powercycle_screen = screen_powercycle_alert.PowerCycleScreen(name = 'pc_alert', screen_manager = sm)

        else: 

            # Initialise settings object
            sett = settings_manager.Settings(sm)

            # Initialise 'm'achine object
            m = router_machine.RouterMachine(Cmport, sm, sett)
            
            job_gcode = []  # declare g-code object
            
            # App manager object
            am = app_manager.AppManagerClass(sm, m, sett)

            # Create database object to talk to
            # db = database_storage.DatabaseStorage(sm, m)

            db = archie_db.SQLRabbit(sm, m)

            # Server connection object
            sc = server_connection.ServerConnection()

            

            # initialise the screens (legacy)
            lobby_screen = screen_lobby.LobbyScreen(name='lobby', screen_manager = sm, machine = m, app_manager = am)
            home_screen = screen_home.HomeScreen(name='home', screen_manager = sm, machine = m, job = job_gcode, settings = sett)
            local_filechooser = screen_local_filechooser.LocalFileChooser(name='local_filechooser', screen_manager = sm)
            usb_filechooser = screen_usb_filechooser.USBFileChooser(name='usb_filechooser', screen_manager = sm)
            go_screen = screen_go.GoScreen(name='go', screen_manager = sm, machine = m, job = job_gcode, app_manager = am)
            jobstart_warning_screen= screen_jobstart_warning.JobstartWarningScreen(name='jobstart_warning', screen_manager = sm, machine = m)
            loading_screen = screen_file_loading.LoadingScreen(name = 'loading', screen_manager = sm, machine =m, job = job_gcode)
            checking_screen = screen_check_job.CheckingScreen(name = 'check_job', screen_manager = sm, machine =m, job = job_gcode)
            error_screen = screen_error.ErrorScreenClass(name='errorScreen', screen_manager = sm, machine = m)
            serial_screen = screen_serial_failure.SerialFailureClass(name='serialScreen', screen_manager = sm, machine = m, win_port = Cmport)
            homing_screen = screen_homing.HomingScreen(name = 'homing', screen_manager = sm, machine =m)
            safety_screen = screen_safety_warning.SafetyScreen(name = 'safety', screen_manager = sm, machine =m)
            mstate_screen = screen_mstate_warning.WarningMState(name = 'mstate', screen_manager = sm, machine =m)
            boundary_warning_screen = screen_boundary_warning.BoundaryWarningScreen(name='boundary',screen_manager = sm, machine = m)
            rebooting_screen = screen_rebooting.RebootingScreen(name = 'rebooting', screen_manager = sm)
            job_done_screen = screen_job_done.JobDoneScreen(name = 'jobdone', screen_manager = sm, machine =m)
            door_screen = screen_door.DoorScreen(name = 'door', screen_manager = sm, machine =m)
            squaring_decision_screen = screen_squaring_manual_vs_square.SquaringScreenDecisionManualVsSquare(name = 'squaring_decision', screen_manager = sm, machine =m)
            prepare_to_home_screen = screen_homing_prepare.HomingScreenPrepare(name = 'prepare_to_home', screen_manager = sm, machine =m)
            homing_active_screen = screen_homing_active.HomingScreenActive(name = 'homing_active', screen_manager = sm, machine =m)
            squaring_active_screen = screen_squaring_active.SquaringScreenActive(name = 'squaring_active', screen_manager = sm, machine =m)
            welcome_screen = screen_welcome.WelcomeScreenClass(name = 'welcome', screen_manager = sm, machine =m, settings = sett, database = db, app_manager = am)
            spindle_shutdown_screen = screen_spindle_shutdown.SpindleShutdownScreen(name = 'spindle_shutdown', screen_manager = sm, machine =m)
            spindle_cooldown_screen = screen_spindle_cooldown.SpindleCooldownScreen(name = 'spindle_cooldown', screen_manager = sm, machine =m)
            stop_or_resume_decision_screen = screen_stop_or_resume_decision.StopOrResumeDecisionScreen(name = 'stop_or_resume_job_decision', screen_manager = sm, machine =m)
            lift_z_on_pause_decision_screen = screen_lift_z_on_pause_decision.LiftZOnPauseDecisionScreen(name = 'lift_z_on_pause_or_not', screen_manager = sm, machine =m)
            tool_selection_screen = screen_tool_selection.ToolSelectionScreen(name = 'tool_selection', screen_manager = sm, machine =m)


        if start_screen == 'pc_alert': 
            sm.add_widget(powercycle_screen)
        else:
            # add the screens to screen manager
            sm.add_widget(lobby_screen)
            sm.add_widget(home_screen)
            sm.add_widget(local_filechooser)
            sm.add_widget(usb_filechooser)
            sm.add_widget(go_screen)
            sm.add_widget(jobstart_warning_screen)
            sm.add_widget(loading_screen)
            sm.add_widget(checking_screen)
            sm.add_widget(error_screen)
            sm.add_widget(serial_screen)
            sm.add_widget(homing_screen)
            sm.add_widget(safety_screen)
            sm.add_widget(mstate_screen)
            sm.add_widget(boundary_warning_screen)
            sm.add_widget(rebooting_screen)
            sm.add_widget(job_done_screen)
            sm.add_widget(door_screen)
            sm.add_widget(squaring_decision_screen)
            sm.add_widget(prepare_to_home_screen)
            sm.add_widget(homing_active_screen)
            sm.add_widget(squaring_active_screen)
            sm.add_widget(welcome_screen)
            sm.add_widget(spindle_shutdown_screen)
            sm.add_widget(spindle_cooldown_screen)
            sm.add_widget(stop_or_resume_decision_screen)
            sm.add_widget(lift_z_on_pause_decision_screen)
            sm.add_widget(tool_selection_screen)

        # Setting the first screen:        
        # sm.current is set at the end of start_services in serial_connection 
        # This ensures kivy has fully loaded and initial kivy schedule calls are safely made before screen is presented

        sm.current = start_screen

        log('Screen manager activated: ' + str(sm.current))


        
        return sm

if __name__ == '__main__':

    SkavaUI().run()
    
