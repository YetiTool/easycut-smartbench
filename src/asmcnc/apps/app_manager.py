'''
Created 5 March 2020
@author: Letty
Module to manage apps and screens
'''
from asmcnc.apps.shapeCutter_app import screen_manager_shapecutter
from asmcnc.calibration_app import screen_landing

# import shape cutter managing object

class AppManagerClass(object):
    
    def __init__(self, screen_manager, machine):

        self.sm = screen_manager
        self.m = machine
        
        # initialise app screen_manager classes     
        self.shapecutter_sm = screen_manager_shapecutter.ScreenManagerShapeCutter(self, self.sm, self.m)
        
    # here are all the functions that might be called in the lobby e.g. 
    
    def start_calibration_app(self):
        if not self.sm.has_screen('calibration_landing'):
            calibration_landing_screen = screen_landing.CalibrationLandingScreenClass(name = 'calibration_landing', screen_manager = self.sm, machine = self.m)
            self.sm.add_widget(calibration_landing_screen)
        self.sm.current = 'calibration_landing'
    
    
    def start_shapecutter_app(self):
        self.shapecutter_sm.open_shapecutter()
    
    
    
    
    