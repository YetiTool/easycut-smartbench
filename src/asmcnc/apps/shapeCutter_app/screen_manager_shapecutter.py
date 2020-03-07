'''
Created 5 March 2020
@author: Letty
Module to manage screens within the shape cutter app
'''

from kivy.uix.screenmanager import ScreenManager, Screen

from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_landing
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_tutorial
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_aperture_island
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_dimensions
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_1
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_2
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_3
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_4
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_5
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_6
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_7
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_8
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_9
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_10
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_11
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_12
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_13
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_14
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_15
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_16
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_17
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_18
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_19
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_20
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_21
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_22
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_23
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_24
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_25
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_26
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_27
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_28
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_29
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_30
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_31
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_32
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_33
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_34
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_35
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_36
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_feedback
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_repeat
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_post_job_save
from asmcnc.apps.shapeCutter_app.screens import screen_shapeCutter_exit

from asmcnc.apps.shapeCutter_app.cut_parameters import sC_job_parameters

# import shape cutter managing object

class ScreenManagerShapeCutter(object):
    
    def __init__(self, app_manager, screen_manager, machine):

        self.am = app_manager
        self.sm = screen_manager
        self.m = machine
        self.j = sC_job_parameters.ShapeCutterJobParameters()

    def prepare_tab(self):
        self.load_prepare_screens()
        self.sm.current = 'sC1'
        
    def load_tab(self):
        self.load_load_screens()
        self.sm.current = 'sC10'
        
    def define_tab(self):
        self.load_define_screens()
        self.sm.current = 'sC17'

    def position_tab(self):
        self.load_position_screens()
        self.sm.current = 'sC26'
        
    def check_tab(self):
        self.load_check_screens()
        self.sm.current = 'sC33'

    def next_screen(self):
        if self.sm.current == 'sCtutorial':
            if not self.sm.has_screen('sClanding'): 
                sClanding_screen = screen_shapeCutter_landing.ShapeCutterLandingScreenClass(name = 'sClanding', screen_manager = self.sm, machine = self.m, job_parameters = self.j, shapecutter = self)
                self.sm.add_widget(sClanding_screen)
                self.sm.current = 'sClanding'
        elif self.sm.current == 'sClanding':
            # self.load_entry_screens()
            if not self.sm.has_screen('sCApIs'):
                sCApIs_screen = screen_shapeCutter_aperture_island.ShapeCutterApIsScreenClass(name = 'sCApIs', screen_manager = self.sm, machine = self.m, job_parameters = self.j, shapecutter = self)
                self.sm.add_widget(sCApIs_screen)
                self.sm.current = 'sCApIs'
        elif self.sm.current == 'sCApIs':
            self.sm.current = 'sCdimensions'           
        elif self.sm.current == 'sCdimensions':
            self.prepare_tab()
        elif self.sm.current == 'sC1':
            self.sm.current = 'sC2'
        elif self.sm.current == 'sC2':
            self.sm.current = 'sC3'
        elif self.sm.current == 'sC3':
            self.sm.current = 'sC4'
        elif self.sm.current == 'sC4':
            self.sm.current = 'sC5'
        elif self.sm.current == 'sC5':
            self.sm.current = 'sC6'           
        elif self.sm.current == 'sC6':
            self.sm.current = 'sC7'
        elif self.sm.current == 'sC7':
            self.sm.current = 'sC8'
        elif self.sm.current == 'sC8':
            self.sm.current = 'sC9'
        elif self.sm.current == 'sC9':
            self.load_tab()
        elif self.sm.current == 'sC10':
            self.sm.current = 'sC11'
        elif self.sm.current == 'sC11':
            self.sm.current = 'sC12'  
        elif self.sm.current == 'sC12':
            self.sm.current = 'sC13'
        elif self.sm.current == 'sC13':
            self.sm.current = 'sC14' 
        elif self.sm.current == 'sC14':
            self.sm.current = 'sC15'
        elif self.sm.current == 'sC15':
            self.sm.current = 'sC16'
        elif self.sm.current == 'sC16':
            self.define_tab()
        elif self.sm.current == 'sC17':
            self.sm.current = 'sC18'
        elif self.sm.current == 'sC18':
            self.sm.current = 'sC19'
        elif self.sm.current == 'sC19':
            self.sm.current = 'sC20'
        elif self.sm.current == 'sC20':
            self.sm.current = 'sC21'  
        elif self.sm.current == 'sC21':
            self.sm.current = 'sC22'
        elif self.sm.current == 'sC22':
            self.sm.current = 'sC23' 
        elif self.sm.current == 'sC23':
            self.sm.current = 'sC24'
        elif self.sm.current == 'sC24':
            self.sm.current = 'sC25'
        elif self.sm.current == 'sC25':
            self.position_tab()
        elif self.sm.current == 'sC26':
            self.sm.current = 'sC27'
        elif self.sm.current == 'sC27':
            self.sm.current = 'sC28'
        elif self.sm.current == 'sC28':
            self.sm.current = 'sC29'            
        elif self.sm.current == 'sC29':
            self.sm.current = 'sC30'  
        elif self.sm.current == 'sC30':
            self.sm.current = 'sC31'
        elif self.sm.current == 'sC31':
            self.sm.current = 'sC32' 
        elif self.sm.current == 'sC32':
            self.check_tab()
        elif self.sm.current == 'sC33':
            self.sm.current = 'sC34'
        elif self.sm.current == 'sC34':
            self.sm.current = 'sC35'
        elif self.sm.current == 'sC35':
            self.sm.current = 'sC36'
        elif self.sm.current == 'sC36':
            self.load_final_screens()
            self.sm.current = 'sCsavejob'
        elif self.sm.current == 'sCsavejob':
            self.sm.current = 'sCfeedback'       
        elif self.sm.current == 'sCfeedback':
            self.sm.current = 'sCrepeat'
            
    def previous_screen(self):
        if self.sm.current == 'sCtutorial':
            self.sm.current = 'sClanding'
        elif self.sm.current == 'sC1':
            self.load_entry_screens()
            self.sm.current = 'sClanding'
        elif self.sm.current == 'sC2':
            self.sm.current = 'sC1'
        elif self.sm.current == 'sC3':
            self.sm.current = 'sC2'
        elif self.sm.current == 'sC4':
            self.sm.current = 'sC3'            
        elif self.sm.current == 'sC5':
            self.sm.current = 'sC4'           
        elif self.sm.current == 'sC6':
            self.sm.current = 'sC5'
        elif self.sm.current == 'sC7':
            self.sm.current = 'sC6'
        elif self.sm.current == 'sC8':
            self.sm.current = 'sC7'
        elif self.sm.current == 'sC9':
            self.sm.current = 'sC8'
        elif self.sm.current == 'sC10':
            self.load_prepare_screens()
            self.sm.current = 'sC9'
        elif self.sm.current == 'sC11':
            self.sm.current = 'sC10'  
        elif self.sm.current == 'sC12':
            self.sm.current = 'sC11'
        elif self.sm.current == 'sC13':
            self.sm.current = 'sC12' 
        elif self.sm.current == 'sC14':
            self.sm.current = 'sC13'
        elif self.sm.current == 'sC15':
            self.sm.current = 'sC14'
        elif self.sm.current == 'sC16':
            self.sm.current = 'sC15'
        elif self.sm.current == 'sC17':
            self.load_load_screens()
            self.sm.current = 'sC16'
        elif self.sm.current == 'sC18':
            self.sm.current = 'sC17'
        elif self.sm.current == 'sC19':
            self.sm.current = 'sC18'
        elif self.sm.current == 'sC20':
            self.sm.current = 'sC19'  
        elif self.sm.current == 'sC21':
            self.sm.current = 'sC20'
        elif self.sm.current == 'sC22':
            self.sm.current = 'sC21' 
        elif self.sm.current == 'sC23':
            self.sm.current = 'sC22'
        elif self.sm.current == 'sC24':
            self.sm.current = 'sC23'
        elif self.sm.current == 'sC25':
            self.sm.current = 'sC24'
        elif self.sm.current == 'sC26':
            self.load_define_screens()
            self.sm.current = 'sC25'
        elif self.sm.current == 'sC27':
            self.sm.current = 'sC26'
        elif self.sm.current == 'sC28':
            self.sm.current = 'sC27'            
        elif self.sm.current == 'sC29':
            self.sm.current = 'sC28'  
        elif self.sm.current == 'sC30':
            self.sm.current = 'sC29'
        elif self.sm.current == 'sC31':
            self.sm.current = 'sC30' 
        elif self.sm.current == 'sC32':
            self.sm.current = 'sC31'
        elif self.sm.current == 'sC33':
            self.load_position_screens()
            self.sm.current = 'sC32'
        elif self.sm.current == 'sC34':
            self.sm.current = 'sC33'
        elif self.sm.current == 'sC35':
            self.sm.current = 'sC34'
        elif self.sm.current == 'sC36':
            self.load_check_screens()
            self.sm.current = 'sC35'

    def exit_shapecutter(self):
        self.sm.current = 'sCexit'

    def tutorial(self):
        if not self.sm.has_screen('sCtutorial'):
            sCtutorial_screen = screen_shapeCutter_tutorial.ShapeCutterTutorialScreenClass(name = 'sCtutorial', screen_manager = self.sm, machine = self.m, shapecutter = self)
            self.sm.add_widget(sCtutorial_screen)
        self.sm.current = 'sCtutorial'        

    def go_screen(self, cancel_to_screen, return_to_screen):    
        self.sm.get_screen('go').return_to_screen = return_to_screen
        self.sm.get_screen('go').cancel_to_screen = cancel_to_screen        
        self.sm.get_screen('go').job_gcode = self.j.generate_gCode()
        self.sm.get_screen('go').job_filename  = self.j.generate_gCode_filename()
        self.sm.current = 'go'
    
    def homing_screen(self, cancel_to_screen, return_to_screen):
        self.sm.get_screen('homing').return_to_screen = return_to_screen
        self.sm.get_screen('homing').cancel_to_screen = cancel_to_screen  
        self.sm.current = 'homing'

    def return_to_EC(self):
        if not self.sm.current == 'alarmScreen':
            self.shapecutter_sm.sm.current = 'lobby'
   
    def open_shapecutter(self):
        #self.load_entry_screens()
        if not self.sm.has_screen('sClanding'): 
            sClanding_screen = screen_shapeCutter_landing.ShapeCutterLandingScreenClass(name = 'sClanding', screen_manager = self.sm, machine = self.m, job_parameters = self.j, shapecutter = self)
            self.sm.add_widget(sClanding_screen)
            self.sm.current = 'sClanding'

    def load_all_screens(self):        
        self.load_entry_screens()
        self.load_prepare_screens()
        self.load_load_screens()
        self.load_define_screens()
        self.load_position_screens()
        self.load_check_screens()
      
    def load_entry_screens(self):
        if not self.sm.has_screen('sClanding'): 
            sClanding_screen = screen_shapeCutter_landing.ShapeCutterLandingScreenClass(name = 'sClanding', screen_manager = self.sm, machine = self.m, job_parameters = self.j, shapecutter = self)
            self.sm.add_widget(sClanding_screen)
        if not self.sm.has_screen('sCexit'):
            sCexit_screen = screen_shapeCutter_exit.ShapeCutterExitScreenClass(name = 'sCexit', screen_manager = self.sm, machine = self.m, shapecutter = self)
            self.sm.add_widget(sCexit_screen)
        if not self.sm.has_screen('sCApIs'):
            sCApIs_screen = screen_shapeCutter_aperture_island.ShapeCutterApIsScreenClass(name = 'sCApIs', screen_manager = self.sm, machine = self.m, job_parameters = self.j, shapecutter = self)
            self.sm.add_widget(sCApIs_screen)
        if not self.sm.has_screen('sCdimensions'):
            sCdimensions_screen = screen_shapeCutter_dimensions.ShapeCutterDimensionsScreenClass(name = 'sCdimensions', screen_manager = self.sm, machine = self.m, job_parameters = self.j, shapecutter = self)
            self.sm.add_widget(sCdimensions_screen)
    
    def load_prepare_screens(self):     
        if not self.sm.has_screen('sC1'):
            sC1_screen = screen_shapeCutter_1.ShapeCutter1ScreenClass(name = 'sC1', screen_manager = self.sm, machine = self.m, shapecutter = self)
            self.sm.add_widget(sC1_screen)
        if not self.sm.has_screen('sC2'):
            sC2_screen = screen_shapeCutter_2.ShapeCutter2ScreenClass(name = 'sC2', screen_manager = self.sm, machine = self.m, shapecutter = self)
            self.sm.add_widget(sC2_screen)
        if not self.sm.has_screen('sC3'):
            sC3_screen = screen_shapeCutter_3.ShapeCutter3ScreenClass(name = 'sC3', screen_manager = self.sm, machine = self.m, shapecutter = self)
            self.sm.add_widget(sC3_screen)
        if not self.sm.has_screen('sC4'):
            sC4_screen = screen_shapeCutter_4.ShapeCutter4ScreenClass(name = 'sC4', screen_manager = self.sm, machine = self.m, shapecutter = self)
            self.sm.add_widget(sC4_screen)
        if not self.sm.has_screen('sC5'):
            sC5_screen = screen_shapeCutter_5.ShapeCutter5ScreenClass(name = 'sC5', screen_manager = self.sm, machine = self.m, shapecutter = self)
            self.sm.add_widget(sC5_screen)
        if not self.sm.has_screen('sC6'):
            sC6_screen = screen_shapeCutter_6.ShapeCutter6ScreenClass(name = 'sC6', screen_manager = self.sm, machine = self.m, shapecutter = self)
            self.sm.add_widget(sC6_screen)
        if not self.sm.has_screen('sC7'):
            sC7_screen = screen_shapeCutter_7.ShapeCutter7ScreenClass(name = 'sC7', screen_manager = self.sm, machine = self.m, shapecutter = self)
            self.sm.add_widget(sC7_screen)
        if not self.sm.has_screen('sC8'):
            sC8_screen = screen_shapeCutter_8.ShapeCutter8ScreenClass(name = 'sC8', screen_manager = self.sm, machine = self.m, shapecutter = self)
            self.sm.add_widget(sC8_screen)
        if not self.sm.has_screen('sC9'):
            sC9_screen = screen_shapeCutter_9.ShapeCutter9ScreenClass(name = 'sC9', screen_manager = self.sm, machine = self.m, shapecutter = self)
            self.sm.add_widget(sC9_screen)

    def load_load_screens(self):
        if not self.sm.has_screen('sC10'):
            sC10_screen = screen_shapeCutter_10.ShapeCutter10ScreenClass(name = 'sC10', screen_manager = self.sm, machine = self.m, shapecutter = self)
            self.sm.add_widget(sC10_screen)
        if not self.sm.has_screen('sC11'):
            sC11_screen = screen_shapeCutter_11.ShapeCutter11ScreenClass(name = 'sC11', screen_manager = self.sm, machine = self.m, shapecutter = self)
            self.sm.add_widget(sC11_screen)
        if not self.sm.has_screen('sC12'):
            sC12_screen = screen_shapeCutter_12.ShapeCutter12ScreenClass(name = 'sC12', screen_manager = self.sm, machine = self.m, shapecutter = self)
            self.sm.add_widget(sC12_screen)
        if not self.sm.has_screen('sC13'):
            sC13_screen = screen_shapeCutter_13.ShapeCutter13ScreenClass(name = 'sC13', screen_manager = self.sm, machine = self.m, shapecutter = self)
            self.sm.add_widget(sC13_screen)
        if not self.sm.has_screen('sC14'):
            sC14_screen = screen_shapeCutter_14.ShapeCutter14ScreenClass(name = 'sC14', screen_manager = self.sm, machine = self.m, shapecutter = self)
            self.sm.add_widget(sC14_screen)
        if not self.sm.has_screen('sC15'):
            sC15_screen = screen_shapeCutter_15.ShapeCutter15ScreenClass(name = 'sC15', screen_manager = self.sm, machine = self.m, shapecutter = self)
            self.sm.add_widget(sC15_screen)
        if not self.sm.has_screen('sC16'):
            sC16_screen = screen_shapeCutter_16.ShapeCutter16ScreenClass(name = 'sC16', screen_manager = self.sm, machine = self.m, shapecutter = self)
            self.sm.add_widget(sC16_screen)

    def load_define_screens(self):
        if not self.sm.has_screen('sC17'):
            sC17_screen = screen_shapeCutter_17.ShapeCutter17ScreenClass(name = 'sC17', screen_manager = self.sm, machine = self.m, job_parameters = self.j, shapecutter = self)
            self.sm.add_widget(sC17_screen)
        if not self.sm.has_screen('sC18'):
            sC18_screen = screen_shapeCutter_18.ShapeCutter18ScreenClass(name = 'sC18', screen_manager = self.sm, machine = self.m, shapecutter = self)
            self.sm.add_widget(sC18_screen)
        if not self.sm.has_screen('sC19'):
            sC19_screen = screen_shapeCutter_19.ShapeCutter19ScreenClass(name = 'sC19', screen_manager = self.sm, machine = self.m, shapecutter = self)
            self.sm.add_widget(sC19_screen)
        if not self.sm.has_screen('sC20'):
            sC20_screen = screen_shapeCutter_20.ShapeCutter20ScreenClass(name = 'sC20', screen_manager = self.sm, machine = self.m, job_parameters = self.j, shapecutter = self)
            self.sm.add_widget(sC20_screen)
        if not self.sm.has_screen('sC21'):
            sC21_screen = screen_shapeCutter_21.ShapeCutter21ScreenClass(name = 'sC21', screen_manager = self.sm, machine = self.m, shapecutter = self)
            self.sm.add_widget(sC21_screen)
        if not self.sm.has_screen('sC22'):
            sC22_screen = screen_shapeCutter_22.ShapeCutter22ScreenClass(name = 'sC22', screen_manager = self.sm, machine = self.m, job_parameters = self.j, shapecutter = self)
            self.sm.add_widget(sC22_screen)
        if not self.sm.has_screen('sC23'):
            sC23_screen = screen_shapeCutter_23.ShapeCutter23ScreenClass(name = 'sC23', screen_manager = self.sm, machine = self.m, job_parameters = self.j, shapecutter = self)
            self.sm.add_widget(sC23_screen)
        if not self.sm.has_screen('sC24'):
            sC24_screen = screen_shapeCutter_24.ShapeCutter24ScreenClass(name = 'sC24', screen_manager = self.sm, machine = self.m, job_parameters = self.j, shapecutter = self)
            self.sm.add_widget(sC24_screen)
        if not self.sm.has_screen('sC25'):
            sC25_screen = screen_shapeCutter_25.ShapeCutter25ScreenClass(name = 'sC25', screen_manager = self.sm, machine = self.m, job_parameters = self.j, shapecutter = self)
            self.sm.add_widget(sC25_screen)
    
    def load_position_screens(self):
        if not self.sm.has_screen('sC26'):
            sC26_screen = screen_shapeCutter_26.ShapeCutter26ScreenClass(name = 'sC26', screen_manager = self.sm, machine = self.m, shapecutter = self)
            self.sm.add_widget(sC26_screen)
        if not self.sm.has_screen('sC27'):
            sC27_screen = screen_shapeCutter_27.ShapeCutter27ScreenClass(name = 'sC27', screen_manager = self.sm, machine = self.m, shapecutter = self)
            self.sm.add_widget(sC27_screen)
        if not self.sm.has_screen('sC28'):
            sC28_screen = screen_shapeCutter_28.ShapeCutter28ScreenClass(name = 'sC28', screen_manager = self.sm, machine = self.m, shapecutter = self)
            self.sm.add_widget(sC28_screen)
        if not self.sm.has_screen('sC29'):
            sC29_screen = screen_shapeCutter_29.ShapeCutter29ScreenClass(name = 'sC29', screen_manager = self.sm, machine = self.m, shapecutter = self)
            self.sm.add_widget(sC29_screen)
        if not self.sm.has_screen('sC30'):
            sC30_screen = screen_shapeCutter_30.ShapeCutter30ScreenClass(name = 'sC30', screen_manager = self.sm, machine = self.m, shapecutter = self)
            self.sm.add_widget(sC30_screen)
        if not self.sm.has_screen('sC31'):
            sC31_screen = screen_shapeCutter_31.ShapeCutter31ScreenClass(name = 'sC31', screen_manager = self.sm, machine = self.m, shapecutter = self)
            self.sm.add_widget(sC31_screen)
        if not self.sm.has_screen('sC32'):
            sC32_screen = screen_shapeCutter_32.ShapeCutter32ScreenClass(name = 'sC32', screen_manager = self.sm, machine = self.m, shapecutter = self)
            self.sm.add_widget(sC32_screen)
    
    def load_check_screens(self):
        if not self.sm.has_screen('sC33'):
            sC33_screen = screen_shapeCutter_33.ShapeCutter33ScreenClass(name = 'sC33', screen_manager = self.sm, machine = self.m, shapecutter = self)
            self.sm.add_widget(sC33_screen)
        if not self.sm.has_screen('sC34'):
            sC34_screen = screen_shapeCutter_34.ShapeCutter34ScreenClass(name = 'sC34', screen_manager = self.sm, machine = self.m, shapecutter = self)
            self.sm.add_widget(sC34_screen)
        if not self.sm.has_screen('sC35'):
            sC35_screen = screen_shapeCutter_35.ShapeCutter35ScreenClass(name = 'sC35', screen_manager = self.sm, machine = self.m, shapecutter = self)
            self.sm.add_widget(sC35_screen)
        if not self.sm.has_screen('sC36'):
            sC36_screen = screen_shapeCutter_36.ShapeCutter36ScreenClass(name = 'sC36', screen_manager = self.sm, machine = self.m, job_parameters = self.j, shapecutter = self)
            self.sm.add_widget(sC36_screen)
        
    def load_final_screens(self):
        if not self.sm.has_screen('sCsavejob'): 
            sCsavejob_screen = screen_shapeCutter_post_job_save.ShapeCutterSaveJobScreenClass(name = 'sCsavejob', screen_manager = self.sm, machine = self.m, job_parameters = self.j, shapecutter = self)
            self.sm.add_widget(sCsavejob_screen)
        if not self.sm.has_screen('sCfeedback'):
            sCfeedback_screen = screen_shapeCutter_feedback.ShapeCutterFeedbackScreenClass(name = 'sCfeedback', screen_manager = self.sm, machine = self.m, shapecutter = self)
            self.sm.add_widget(sCfeedback_screen)
        if not self.sm.has_screen('sCrepeat'):
            sCrepeat_screen = screen_shapeCutter_repeat.ShapeCutterRepeatScreenClass(name = 'sCrepeat', screen_manager = self.sm, machine = self.m, shapecutter = self)
            self.sm.add_widget(sCrepeat_screen)
    
    def destroy_screens(self):
        pass
    
    def destroy_entry_screens(self):
        pass
    
    def destroy_prepare_screens(self):
        pass
    
    def destroy_load_screens(self):
        pass
    
    def destroy_define_screens(self):
        pass
    
    def destroy_position_screens(self):
        pass
    
    def destroy_check_screens(self):
        pass
    
    def destroy_final_screens(self):
        pass