# -*- coding: utf-8 -*- 

'''
Created on 16 Nov 2017
@author: Ed
YetiTool's UI for SmartBench
www.yetitool.com
'''

#config
#import os
#os.environ['KIVY_GL_BACKEND'] = 'sdl2'

# try:
# 	from hanging_threads import start_monitoring
# 	monitoring_thread = start_monitoring(seconds_frozen=3, test_interval=100)
# except:
# 	print("Could not import hanging_threads")

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
#dfghj

import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window


# COMMS IMPORTS
from asmcnc.comms import router_machine  # @UnresolvedImport
from asmcnc.comms import server_connection
from asmcnc.comms import smartbench_flurry_database_connection

# NB: router_machine imports serial_connection
from asmcnc.apps import app_manager # @UnresolvedImport
from settings import settings_manager # @UnresolvedImport
from asmcnc.comms import localization

# JOB DATA IMPORT
from asmcnc.job import job_data
from asmcnc.job.yetipilot.yetipilot import YetiPilot

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
from asmcnc.skavaUI import screen_mstate_warning # @UnresolvedImport
from asmcnc.skavaUI import screen_boundary_warning # @UnresolvedImport
from asmcnc.skavaUI import screen_rebooting # @UnresolvedImport
from asmcnc.skavaUI import screen_job_feedback # @UnresolvedImport
from asmcnc.skavaUI import screen_job_incomplete # @UnresolvedImport
from asmcnc.skavaUI import screen_powercycle_alert # @UnresolvedImport
from asmcnc.skavaUI import screen_door # @UnresolvedImport
from asmcnc.skavaUI import screen_squaring_manual_vs_square # @UnresolvedImport
from asmcnc.skavaUI import screen_homing_prepare # @UnresolvedImport
from asmcnc.skavaUI import screen_homing_active # @UnresolvedImport
from asmcnc.skavaUI import screen_squaring_active # @UnresolvedImport
from asmcnc.skavaUI import screen_spindle_shutdown # @UnresolvedImport
from asmcnc.skavaUI import screen_spindle_cooldown
from asmcnc.skavaUI import screen_stop_or_resume_decision # @UnresolvedImport
from asmcnc.skavaUI import screen_lift_z_on_pause_decision # @UnresolvedImport
from asmcnc.skavaUI import screen_tool_selection # @UnresolvedImport
from asmcnc.skavaUI import screen_restart_smartbench # @UnresolvedImport
from asmcnc.skavaUI import screen_job_recovery # @UnresolvedImport
from asmcnc.skavaUI import screen_nudge # @UnresolvedImport
from asmcnc.skavaUI import screen_recovery_decision # @UnresolvedImport
from asmcnc.skavaUI import screen_homing_decision # @UnresolvedImport

# developer testing
Cmport = 'COM3'

# Current version active/working on
initial_version = 'v2.6.1'

config_flag = False
        
def check_and_update_config():

    if sys.platform != 'win32' and sys.platform != 'darwin':
    
        global config_flag
        config_flag = check_config_flag()

        if config_flag:
            ver0_configuration()
            check_ansible_status()

def check_config_flag():
    
    if (os.popen('grep "check_config=True" /home/pi/easycut-smartbench/src/config.txt').read()).startswith('check_config=True'): 
        return True
    else:
        return False

def ver0_configuration():

    if (os.popen('grep "version=0" /home/pi/easycut-smartbench/src/config.txt').read()).startswith('version=0'):
        os.system('cd /home/pi/easycut-smartbench/ && git update-index --skip-worktree /home/pi/easycut-smartbench/src/config.txt')
        os.system('sudo sed -i "s/config_skipped_by_git=False/config_skipped_by_git=True/" /home/pi/easycut-smartbench/src/config.txt') 
        os.system('sudo sed -i "s/version=0/version=' + initial_version + '/" /home/pi/easycut-smartbench/src/config.txt')

def check_ansible_status():

    ansible_from_easycut = (os.popen('grep "ansible_from_easycut=True" /home/pi/easycut-smartbench/src/config.txt').read())
    # if this comes out empty, run ansible and reboot
    if not ansible_from_easycut:
        # when the playbook fails, it stops the other commands from running as well
        os.system("/home/pi/easycut-smartbench/ansible/templates/ansible-start.sh && sudo systemctl restart ansible.service && sudo reboot")

    
## Easycut config
check_and_update_config()

def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + message)


class SkavaUI(App):

    test_no = 0

    def build(self):

        log("Starting App:")

        # Establish screens
        sm = ScreenManager(transition=NoTransition())

        # Localization/language object
        l = localization.Localization()

        # Initialise settings object
        sett = settings_manager.Settings(sm)

        # Initialise 'j'ob 'd'ata object
        jd = job_data.JobData(localization = l, settings_manager = sett)

        # Initialise 'm'achine object
        m = router_machine.RouterMachine(Cmport, sm, sett, l, jd)

        # Initialise yetipilot
        yp = YetiPilot(screen_manager=sm, machine=m, job_data=jd, localization=l)

        # Create database object to talk to
        db = smartbench_flurry_database_connection.DatabaseEventManager(sm, m, sett)

        # App manager object
        am = app_manager.AppManagerClass(sm, m, sett, l, jd, db, config_flag, initial_version)

        # Alarm screens are set up in serial comms, need access to the db object
        m.s.alarm.db = db

        # Serial comms needs to access YP
        m.s.yp = yp

        # Server connection object
        sc = server_connection.ServerConnection(sett)
        
        # initialise the screens (legacy)
        lobby_screen = screen_lobby.LobbyScreen(name='lobby', screen_manager = sm, machine = m, app_manager = am, localization = l)
        home_screen = screen_home.HomeScreen(name='home', screen_manager = sm, machine = m, job = jd, settings = sett, localization = l)
        local_filechooser = screen_local_filechooser.LocalFileChooser(name='local_filechooser', screen_manager = sm, job = jd, localization = l)
        usb_filechooser = screen_usb_filechooser.USBFileChooser(name='usb_filechooser', screen_manager = sm, job = jd, localization = l)
        go_screen = screen_go.GoScreen(name='go', screen_manager = sm, machine = m, job = jd, app_manager = am, database=db, localization = l, yetipilot=yp)
        jobstart_warning_screen= screen_jobstart_warning.JobstartWarningScreen(name='jobstart_warning', screen_manager = sm, machine = m, localization = l)
        loading_screen = screen_file_loading.LoadingScreen(name = 'loading', screen_manager = sm, machine =m, job = jd, localization = l)
        checking_screen = screen_check_job.CheckingScreen(name = 'check_job', screen_manager = sm, machine =m, job = jd, localization = l)
        error_screen = screen_error.ErrorScreenClass(name='errorScreen', screen_manager = sm, machine = m, job = jd, database = db, localization = l)
        serial_screen = screen_serial_failure.SerialFailureClass(name='serialScreen', screen_manager = sm, machine = m, win_port = Cmport, localization = l) 
        mstate_screen = screen_mstate_warning.WarningMState(name = 'mstate', screen_manager = sm, machine =m, localization = l)
        boundary_warning_screen = screen_boundary_warning.BoundaryWarningScreen(name='boundary',screen_manager = sm, machine = m, localization = l)
        rebooting_screen = screen_rebooting.RebootingScreen(name = 'rebooting', screen_manager = sm, localization = l)
        job_feedback_screen = screen_job_feedback.JobFeedbackScreen(name = 'job_feedback', screen_manager = sm, machine =m, database = db, job = jd, localization = l)
        job_incomplete_screen = screen_job_incomplete.JobIncompleteScreen(name = 'job_incomplete', screen_manager = sm, machine =m, database = db, job = jd, localization = l)
        door_screen = screen_door.DoorScreen(name = 'door', screen_manager = sm, machine =m, job = jd, database = db, localization = l)
        squaring_decision_screen = screen_squaring_manual_vs_square.SquaringScreenDecisionManualVsSquare(name = 'squaring_decision', screen_manager = sm, machine =m, localization = l)
        prepare_to_home_screen = screen_homing_prepare.HomingScreenPrepare(name = 'prepare_to_home', screen_manager = sm, machine =m, localization = l)
        homing_active_screen = screen_homing_active.HomingScreenActive(name = 'homing_active', screen_manager = sm, machine =m, localization = l)
        squaring_active_screen = screen_squaring_active.SquaringScreenActive(name = 'squaring_active', screen_manager = sm, machine =m, localization = l)
        spindle_shutdown_screen = screen_spindle_shutdown.SpindleShutdownScreen(name = 'spindle_shutdown', screen_manager = sm, machine =m, job = jd, database = db, localization = l)
        spindle_cooldown_screen = screen_spindle_cooldown.SpindleCooldownScreen(name = 'spindle_cooldown', screen_manager = sm, machine =m, localization = l)
        stop_or_resume_decision_screen = screen_stop_or_resume_decision.StopOrResumeDecisionScreen(name = 'stop_or_resume_job_decision', screen_manager = sm, machine =m, job = jd, database = db, localization = l)
        lift_z_on_pause_decision_screen = screen_lift_z_on_pause_decision.LiftZOnPauseDecisionScreen(name = 'lift_z_on_pause_or_not', screen_manager = sm, machine =m, localization = l)
        tool_selection_screen = screen_tool_selection.ToolSelectionScreen(name = 'tool_selection', screen_manager = sm, machine =m, localization = l)
        job_recovery_screen = screen_job_recovery.JobRecoveryScreen(name = 'job_recovery', screen_manager = sm, machine = m, job = jd, localization = l)
        nudge_screen = screen_nudge.NudgeScreen(name = 'nudge', screen_manager = sm, machine = m, job = jd, localization = l)
        recovery_decision_screen = screen_recovery_decision.RecoveryDecisionScreen(name = 'recovery_decision', screen_manager = sm, machine = m, job = jd, localization = l)
        homing_decision_screen = screen_homing_decision.HomingDecisionScreen(name = 'homing_decision', screen_manager = sm, machine = m, localization = l)

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
        sm.add_widget(mstate_screen)
        sm.add_widget(boundary_warning_screen)
        sm.add_widget(rebooting_screen)
        sm.add_widget(job_feedback_screen)
        sm.add_widget(job_incomplete_screen)        
        sm.add_widget(door_screen)
        sm.add_widget(squaring_decision_screen)
        sm.add_widget(prepare_to_home_screen)
        sm.add_widget(homing_active_screen)
        sm.add_widget(squaring_active_screen)
        sm.add_widget(spindle_shutdown_screen)
        sm.add_widget(spindle_cooldown_screen)
        sm.add_widget(stop_or_resume_decision_screen)
        sm.add_widget(lift_z_on_pause_decision_screen)
        sm.add_widget(tool_selection_screen)
        sm.add_widget(job_recovery_screen)
        sm.add_widget(nudge_screen)
        sm.add_widget(recovery_decision_screen)
        sm.add_widget(homing_decision_screen)

        # Setting the first screen:        
        # sm.current is set at the end of start_services in serial_connection 
        # This ensures kivy has fully loaded and initial kivy schedule calls are safely made before screen is presented

        log('Screen manager activated: ' + str(sm.current))


        ## LOCALIZATION TESTING -----------------------------------------------------------

        # test_languages = ["English (GB)", "Deutsch (DE)",  "Français (FR)", "Italiano (IT)", "Suomalainen (FI)", "Polski (PL)", "Dansk (DK)"]

        # def test_cycle(dt):
        #     if self.test_no < len(test_languages):
        #         lang = test_languages[self.test_no]
        #         l.load_in_new_language(lang)
        #         print("New lang: " + str(lang))
        #         try:
        #             sm.get_screen(str(sm.current)).update_strings()
        #         except: 
        #             print(str(sm.current) + " has no update strings function")

        #         self.test_no = self.test_no + 1
        #     else: 
        #         self.test_no = 0

        # Clock.schedule_interval(test_cycle, 5)



        # def test_run_through_sequence(dt):

        # 	if sm.current != 'warranty_3' and sm.current != 'consent_3' and sm.current != 'starting_smartbench':
        # 		sm.get_screen(str(sm.current)).next_screen()

        # 	elif sm.current == 'warranty_3':
        # 		sm.get_screen('warranty_3').activation_code.text = "42230169"

        # 	elif sm.current == 'consent_3':
        # 		sm.get_screen('consent_3').terms_checkbox.active = True
        # 		sm.get_screen('consent_3').accept_terms()


        # def start_loop(dt):
        # 	Clock.schedule_interval(test_run_through_sequence, 3)

        # Clock.schedule_once(start_loop, 10)

        ## -----------------------------------------------------------------------------------
        return sm

if __name__ == '__main__':

    SkavaUI().run()
    
