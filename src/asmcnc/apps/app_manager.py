'''
Created 5 March 2020
@author: Letty
Module to manage apps and screens
'''

from asmcnc.apps.warranty_app import screen_warranty_registration_1, \
screen_warranty_registration_2, screen_warranty_registration_3, \
screen_warranty_registration_4, screen_warranty_registration_5

from asmcnc.apps.shapeCutter_app import screen_manager_shapecutter
from asmcnc.apps.wifi_app import screen_wifi
from asmcnc.apps.SWupdater_app import screen_update_SW
from asmcnc.calibration_app import screen_landing
from asmcnc.calibration_app import screen_finished
from asmcnc.apps.maintenance_app import screen_maintenance
from asmcnc.apps.systemTools_app import screen_manager_systemtools


# import shape cutter managing object

class AppManagerClass(object):
    
    current_app = ''
    
    def __init__(self, screen_manager, machine, settings):

        self.sm = screen_manager
        self.m = machine
        self.set = settings
        
        # initialise app screen_manager classes     
        self.shapecutter_sm = screen_manager_shapecutter.ScreenManagerShapeCutter(self, self.sm, self.m)
        self.systemtools_sm = screen_manager_systemtools.ScreenManagerSystemTools(self, self.sm, self.m, self.set)
        
        wifi_screen = screen_wifi.WifiScreen(name = 'wifi', screen_manager = self.sm)
        self.sm.add_widget(wifi_screen)
        

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
       
    def start_shapecutter_app(self):
        self.current_app = 'shapecutter'
        self.shapecutter_sm.open_shapecutter()
    
    def start_pro_app(self):
        self.current_app = 'pro'
    
    def start_wifi_app(self):
        self.current_app = 'wifi'
        self.sm.current = 'wifi'
        
    def start_update_app(self):
        update_screen = screen_update_SW.SWUpdateScreen(name = 'update', screen_manager = self.sm, settings = self.set)
        self.sm.add_widget(update_screen)
        
        self.current_app = 'update'
        self.sm.current = 'update'

    def start_maintenance_app(self, landing_tab):
        if not self.sm.has_screen('maintenance'):
            maintenance_screen = screen_maintenance.MaintenanceScreenClass(name = 'maintenance', screen_manager = self.sm, machine = self.m)
            self.sm.add_widget(maintenance_screen)

        self.sm.get_screen('maintenance').landing_tab = landing_tab
        self.sm.current = 'maintenance'


    def start_systemtools_app(self):
        self.current_app = 'system_tools'
        self.systemtools_sm.open_system_tools()

    def start_warranty_app(self):
        if not self.sm.has_screen('warranty_1'):
            warranty_registration_1_screen = screen_warranty_registration_1.WarrantyScreen1(name = 'warranty_1', screen_manager = self.sm, machine = self.m)
            sm.add_widget(warranty_registration_1_screen)
        if not self.sm.has_screen('warranty_2'):
            warranty_registration_2_screen = screen_warranty_registration_2.WarrantyScreen2(name = 'warranty_2', screen_manager = self.sm, machine = self.m)
            sm.add_widget(warranty_registration_2_screen)
        if not self.sm.has_screen('warranty_3'):
            warranty_registration_3_screen = screen_warranty_registration_3.WarrantyScreen3(name = 'warranty_3', screen_manager = self.sm, machine = self.m)
            sm.add_widget(warranty_registration_3_screen)
        if not self.sm.has_screen('warranty_4'):
            warranty_registration_4_screen = screen_warranty_registration_4.WarrantyScreen4(name = 'warranty_4', screen_manager = self.sm, machine = self.m)
            sm.add_widget(warranty_registration_4_screen)
        if not self.sm.has_screen('warranty_5'):
            warranty_registration_5_screen = screen_warranty_registration_5.WarrantyScreen5(name = 'warranty_5', screen_manager = self.sm, machine = self.m)
            sm.add_widget(warranty_registration_5_screen)

        self.current_app = 'warranty'
        self.sm.current = 'warranty_1'


















