'''
Created 5 March 2020
@author: Letty
Module to manage apps and screens
'''

import os

from asmcnc.apps.wifi_app import screen_wifi
from asmcnc.apps.SWupdater_app import screen_update_SW
from asmcnc.calibration_app import screen_landing
from asmcnc.calibration_app import screen_finished
from asmcnc.apps.maintenance_app import screen_maintenance
from asmcnc.apps.systemTools_app import screen_manager_systemtools
from asmcnc.apps.start_up_sequence import start_up_sequence_manager
from asmcnc.apps.upgrade_app import screen_upgrade, screen_upgrade_successful, screen_already_upgraded
from asmcnc.apps.drywall_cutter_app import screen_drywall_cutter
from asmcnc.comms.model_manager import ModelManagerSingleton


# import shape cutter managing object

class AppManagerClass(object):
    
    current_app = ''
    model_manager = ModelManagerSingleton()
    
    def __init__(self, screen_manager, machine, settings, localization, keyboard, job, database, config_check, version, popup_manager):

        self.sm = screen_manager
        self.m = machine
        self.set = settings
        self.jd = job
        self.l = localization
        self.kb = keyboard
        self.db = database
        self.cc = config_check
        self.v = version
        self.pm = popup_manager

        
        # initialise app screen_manager classes
        self.systemtools_sm = screen_manager_systemtools.ScreenManagerSystemTools(self, self.sm, self.m, self.set, self.l, self.kb)
        wifi_screen = screen_wifi.WifiScreen(name = 'wifi', screen_manager = self.sm, settings_manager = self.set, localization = self.l, keyboard = self.kb)
        self.sm.add_widget(wifi_screen)

        # Set up maintenance screen asap, to avoid long load time on app entry
        maintenance_screen = screen_maintenance.MaintenanceScreenClass(name = 'maintenance', screen_manager = self.sm, machine = self.m, localization = self.l, keyboard = self.kb, job = self.jd)
        self.sm.add_widget(maintenance_screen)

        drywall_cutter_screen = screen_drywall_cutter.DrywallCutterScreen(self.sm, self.m, self.kb, self.jd, name="drywall_cutter")
        self.sm.add_widget(drywall_cutter_screen)
        
        # Start start up sequence
        self.start_up = start_up_sequence_manager.StartUpSequence(self, self.sm, self.m, self.set, self.l, self.kb, self.jd, self.db, self.cc, self.v)


    # here are all the functions that might be called in the lobby e.g. 
    
    def start_calibration_app(self, return_to_screen):
        self.current_app = 'calibration_landing'
        if not self.sm.has_screen('calibration_landing'):
            calibration_landing_screen = screen_landing.CalibrationLandingScreenClass(name = 'calibration_landing', screen_manager = self.sm, machine = self.m)
            self.sm.add_widget(calibration_landing_screen)
        if not self.sm.has_screen('calibration_complete'):
            final_screen = screen_finished.FinishedCalScreenClass(name = 'calibration_complete', screen_manager = self.sm, machine = self.m)
            self.sm.add_widget(final_screen)
        self.sm.get_screen('calibration_complete').return_to_screen = return_to_screen
        self.sm.get_screen('calibration_landing').return_to_screen = return_to_screen
        self.sm.current = 'calibration_landing'
    
    def start_pro_app(self):
        self.current_app = 'pro'
    
    def start_wifi_app(self):
        self.current_app = 'wifi'
        self.sm.current = 'wifi'
        
    def start_update_app(self):
        if not self.sm.has_screen('update'):
            update_screen = screen_update_SW.SWUpdateScreen(name = 'update', screen_manager = self.sm, settings = self.set, localization = self.l)
            self.sm.add_widget(update_screen)
        
        self.current_app = 'update'
        self.sm.current = 'update'

    def start_maintenance_app(self, landing_tab):
        self.sm.get_screen('maintenance').landing_tab = landing_tab
        self.sm.current = 'maintenance'

    def start_systemtools_app(self):
        self.current_app = 'system_tools'
        self.systemtools_sm.open_system_tools()

    def start_upgrade_app(self):
        self.current_app = 'upgrade'

        if not self.m.theateam():
            if not self.sm.has_screen('upgrade'):
                upgrade_screen = screen_upgrade.UpgradeScreen(name='upgrade', screen_manager=self.sm, machine=self.m, localization=self.l, keyboard=self.kb)
                self.sm.add_widget(upgrade_screen)

            if not self.sm.has_screen('upgrade_successful'):
                upgrade_successful_screen = screen_upgrade_successful.UpgradeSuccessfulScreen(name='upgrade_successful', screen_manager=self.sm, machine=self.m, localization=self.l)
                self.sm.add_widget(upgrade_successful_screen)

            self.sm.current = 'upgrade'
        else:
            if not self.sm.has_screen('already_upgraded'):
                already_upgraded_screen = screen_already_upgraded.AlreadyUpgradedScreen(name='already_upgraded', screen_manager=self.sm, machine=self.m, localization=self.l)
                self.sm.add_widget(already_upgraded_screen)

            self.sm.current = 'already_upgraded'

    def start_drywall_cutter_app(self):
        self.current_app = 'drywall_cutter'
        self.sm.current = 'drywall_cutter'
