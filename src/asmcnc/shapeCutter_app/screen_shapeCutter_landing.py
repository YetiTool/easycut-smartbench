'''
Created on 19 February 2020
Landing Screen for the Shape Cutter App

@author: Letty
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty

from asmcnc.shapeCutter_app import screen_shapeCutter_tutorial
from asmcnc.shapeCutter_app import screen_shapeCutter_aperture_island
from asmcnc.shapeCutter_app import screen_shapeCutter_dimensions

from asmcnc.shapeCutter_app import screen_shapeCutter_1
from asmcnc.shapeCutter_app import screen_shapeCutter_2
from asmcnc.shapeCutter_app import screen_shapeCutter_3
from asmcnc.shapeCutter_app import screen_shapeCutter_4
from asmcnc.shapeCutter_app import screen_shapeCutter_5
from asmcnc.shapeCutter_app import screen_shapeCutter_6
from asmcnc.shapeCutter_app import screen_shapeCutter_7
from asmcnc.shapeCutter_app import screen_shapeCutter_8
from asmcnc.shapeCutter_app import screen_shapeCutter_9
from asmcnc.shapeCutter_app import screen_shapeCutter_10
from asmcnc.shapeCutter_app import screen_shapeCutter_11
from asmcnc.shapeCutter_app import screen_shapeCutter_12
from asmcnc.shapeCutter_app import screen_shapeCutter_13
from asmcnc.shapeCutter_app import screen_shapeCutter_14
from asmcnc.shapeCutter_app import screen_shapeCutter_15
from asmcnc.shapeCutter_app import screen_shapeCutter_16
from asmcnc.shapeCutter_app import screen_shapeCutter_17
from asmcnc.shapeCutter_app import screen_shapeCutter_18
from asmcnc.shapeCutter_app import screen_shapeCutter_19
from asmcnc.shapeCutter_app import screen_shapeCutter_20
from asmcnc.shapeCutter_app import screen_shapeCutter_21
from asmcnc.shapeCutter_app import screen_shapeCutter_22
from asmcnc.shapeCutter_app import screen_shapeCutter_23
from asmcnc.shapeCutter_app import screen_shapeCutter_24
from asmcnc.shapeCutter_app import screen_shapeCutter_25
from asmcnc.shapeCutter_app import screen_shapeCutter_26
from asmcnc.shapeCutter_app import screen_shapeCutter_27
from asmcnc.shapeCutter_app import screen_shapeCutter_28
from asmcnc.shapeCutter_app import screen_shapeCutter_29
from asmcnc.shapeCutter_app import screen_shapeCutter_30
from asmcnc.shapeCutter_app import screen_shapeCutter_31
from asmcnc.shapeCutter_app import screen_shapeCutter_32
from asmcnc.shapeCutter_app import screen_shapeCutter_33
from asmcnc.shapeCutter_app import screen_shapeCutter_34
from asmcnc.shapeCutter_app import screen_shapeCutter_35
from asmcnc.shapeCutter_app import screen_shapeCutter_36

from asmcnc.shapeCutter_app import screen_shapeCutter_feedback
from asmcnc.shapeCutter_app import screen_shapeCutter_repeat
from asmcnc.shapeCutter_app import screen_shapeCutter_post_job_save
from asmcnc.shapeCutter_app import screen_shapeCutter_exit

from asmcnc.shapeCutter_app.cut_parameters import sC_job_parameters

Builder.load_string("""

<ShapeCutterLandingScreenClass>:
    
    BoxLayout:
        height: dp(800)
        width: dp(480)
        canvas:
            Rectangle: 
                pos: self.pos
                size: self.size
                source: "./asmcnc/shapeCutter_app/img/landing_background.png"

        BoxLayout:
            padding: 0
            spacing: 0
            orientation: "vertical"       
                
            Label:
                size_hint: (None,None)
                height: dp(90)
                width: dp(800)
                text: "Welcome to Shape Cutter"
                font_size: 30
                halign: "center"
                valign: "bottom"
                markup: True
                   
                    
            BoxLayout:
                size_hint: (None,None)
                width: dp(800)
                height: dp(140)
                padding: 0
                spacing: 0
                Label:
                    size_hint: (None,None)
                    height: dp(170)
                    width: dp(800)
                    halign: "center"
                    valign: "middle"
                    text: "Select a shape to cut..."
                    color: 0,0,0,1
                    font_size: 26
                    markup: True

            BoxLayout:
                size_hint: (None,None)
                width: dp(800)
                height: dp(170)
                padding: (180,0,180,30)
                spacing: 0
                orientation: 'horizontal'
                pos: self.parent.pos                
                
                BoxLayout:
                    size_hint: (None,None)
                    width: dp(220)
                    height: dp(170)
                    padding: (25,0,27,0)
                    pos: self.parent.pos
                    
                    # Circle button
                    Button:
                        size_hint: (None,None)
                        height: dp(168)
                        width: dp(168)
                        background_color: hex('#F4433600')
                        center: self.parent.center
                        pos: self.parent.pos
                        on_press: root.cut_circle()
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                source: "./asmcnc/shapeCutter_app/img/cut_circle.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True
                BoxLayout:
                    size_hint: (None,None)
                    width: dp(220)
                    height: dp(170)
                    padding: (27,0,25,0)
                    pos: self.parent.pos
                    
                    # rectangle button
                    Button:
                        size_hint: (None,None)
                        height: dp(168)
                        width: dp(168)
                        background_color: hex('#F4433600')
                        center: self.parent.center
                        pos: self.parent.pos
                        on_press: root.cut_rectangle()
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                source: "./asmcnc/shapeCutter_app/img/cut_rectangle.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True  
            # Info button
            BoxLayout:
                size_hint: (None,None)
                width: dp(800)
                height: dp(80)
                padding: (740,0,0,20)
                spacing: 0
                orientation: 'horizontal'
                pos: self.parent.pos
                Button:
                    id: info_button
                    size_hint: (None,None)
                    height: dp(40)
                    width: dp(40)
                    background_color: hex('#F4433600')
                    opacity: 1
                    on_press: root.get_info()
                    BoxLayout:
                        padding: 0
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            source: "./asmcnc/shapeCutter_app/img/info_icon.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True
""")

class ShapeCutterLandingScreenClass(Screen):

    info_button = ObjectProperty()   
#     user_instruction = ObjectProperty()
    
    def __init__(self, **kwargs):
        super(ShapeCutterLandingScreenClass, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        
        # initialise job parameters
        self.j = sC_job_parameters.ShapeCutterJobParameters()

    def on_pre_enter(self):
        if not self.sm.has_screen('sC1'):
            self.load_screens()
        
    def load_screens(self):
        sCtutorial_screen = screen_shapeCutter_tutorial.ShapeCutterTutorialScreenClass(name = 'sCtutorial', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(sCtutorial_screen)
        sCApIs_screen = screen_shapeCutter_aperture_island.ShapeCutterApIsScreenClass(name = 'sCApIs', screen_manager = self.sm, machine = self.m, job_parameters = self.j)
        self.sm.add_widget(sCApIs_screen)
        sCdimensions_screen = screen_shapeCutter_dimensions.ShapeCutterDimensionsScreenClass(name = 'sCdimensions', screen_manager = self.sm, machine = self.m, job_parameters = self.j)
        self.sm.add_widget(sCdimensions_screen)
        
        sC1_screen = screen_shapeCutter_1.ShapeCutter1ScreenClass(name = 'sC1', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(sC1_screen)
        sC2_screen = screen_shapeCutter_2.ShapeCutter2ScreenClass(name = 'sC2', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(sC2_screen)
        sC3_screen = screen_shapeCutter_3.ShapeCutter3ScreenClass(name = 'sC3', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(sC3_screen)
        sC4_screen = screen_shapeCutter_4.ShapeCutter4ScreenClass(name = 'sC4', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(sC4_screen)
        sC5_screen = screen_shapeCutter_5.ShapeCutter5ScreenClass(name = 'sC5', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(sC5_screen)
        sC6_screen = screen_shapeCutter_6.ShapeCutter6ScreenClass(name = 'sC6', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(sC6_screen)
        sC7_screen = screen_shapeCutter_7.ShapeCutter7ScreenClass(name = 'sC7', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(sC7_screen)
        sC8_screen = screen_shapeCutter_8.ShapeCutter8ScreenClass(name = 'sC8', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(sC8_screen)
        sC9_screen = screen_shapeCutter_9.ShapeCutter9ScreenClass(name = 'sC9', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(sC9_screen)
        sC10_screen = screen_shapeCutter_10.ShapeCutter10ScreenClass(name = 'sC10', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(sC10_screen)
        sC11_screen = screen_shapeCutter_11.ShapeCutter11ScreenClass(name = 'sC11', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(sC11_screen)
        sC12_screen = screen_shapeCutter_12.ShapeCutter12ScreenClass(name = 'sC12', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(sC12_screen)
        sC13_screen = screen_shapeCutter_13.ShapeCutter13ScreenClass(name = 'sC13', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(sC13_screen)
        sC14_screen = screen_shapeCutter_14.ShapeCutter14ScreenClass(name = 'sC14', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(sC14_screen)
        sC15_screen = screen_shapeCutter_15.ShapeCutter15ScreenClass(name = 'sC15', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(sC15_screen)
        sC16_screen = screen_shapeCutter_16.ShapeCutter16ScreenClass(name = 'sC16', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(sC16_screen)
        sC17_screen = screen_shapeCutter_17.ShapeCutter17ScreenClass(name = 'sC17', screen_manager = self.sm, machine = self.m, job_parameters = self.j)
        self.sm.add_widget(sC17_screen)
        sC18_screen = screen_shapeCutter_18.ShapeCutter18ScreenClass(name = 'sC18', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(sC18_screen)
        sC19_screen = screen_shapeCutter_19.ShapeCutter19ScreenClass(name = 'sC19', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(sC19_screen)
        sC20_screen = screen_shapeCutter_20.ShapeCutter20ScreenClass(name = 'sC20', screen_manager = self.sm, machine = self.m, job_parameters = self.j)
        self.sm.add_widget(sC20_screen)
        sC21_screen = screen_shapeCutter_21.ShapeCutter21ScreenClass(name = 'sC21', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(sC21_screen)
        sC22_screen = screen_shapeCutter_22.ShapeCutter22ScreenClass(name = 'sC22', screen_manager = self.sm, machine = self.m, job_parameters = self.j)
        self.sm.add_widget(sC22_screen)
        sC23_screen = screen_shapeCutter_23.ShapeCutter23ScreenClass(name = 'sC23', screen_manager = self.sm, machine = self.m, job_parameters = self.j)
        self.sm.add_widget(sC23_screen)
        sC24_screen = screen_shapeCutter_24.ShapeCutter24ScreenClass(name = 'sC24', screen_manager = self.sm, machine = self.m, job_parameters = self.j)
        self.sm.add_widget(sC24_screen)
        sC25_screen = screen_shapeCutter_25.ShapeCutter25ScreenClass(name = 'sC25', screen_manager = self.sm, machine = self.m, job_parameters = self.j)
        self.sm.add_widget(sC25_screen)
        sC26_screen = screen_shapeCutter_26.ShapeCutter26ScreenClass(name = 'sC26', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(sC26_screen)
        sC27_screen = screen_shapeCutter_27.ShapeCutter27ScreenClass(name = 'sC27', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(sC27_screen)
        sC28_screen = screen_shapeCutter_28.ShapeCutter28ScreenClass(name = 'sC28', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(sC28_screen)
        sC29_screen = screen_shapeCutter_29.ShapeCutter29ScreenClass(name = 'sC29', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(sC29_screen)
        sC30_screen = screen_shapeCutter_30.ShapeCutter30ScreenClass(name = 'sC30', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(sC30_screen)
        sC31_screen = screen_shapeCutter_31.ShapeCutter31ScreenClass(name = 'sC31', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(sC31_screen)
        sC32_screen = screen_shapeCutter_32.ShapeCutter32ScreenClass(name = 'sC32', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(sC32_screen)
        sC33_screen = screen_shapeCutter_33.ShapeCutter33ScreenClass(name = 'sC33', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(sC33_screen)
        sC34_screen = screen_shapeCutter_34.ShapeCutter34ScreenClass(name = 'sC34', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(sC34_screen)
        sC35_screen = screen_shapeCutter_35.ShapeCutter35ScreenClass(name = 'sC35', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(sC35_screen)
        sC36_screen = screen_shapeCutter_36.ShapeCutter36ScreenClass(name = 'sC36', screen_manager = self.sm, machine = self.m, job_parameters = self.j)
        self.sm.add_widget(sC36_screen)

        sCsavejob_screen = screen_shapeCutter_post_job_save.ShapeCutterSaveJobScreenClass(name = 'sCsavejob', screen_manager = self.sm, machine = self.m, job_parameters = self.j)
        self.sm.add_widget(sCsavejob_screen)
        sCfeedback_screen = screen_shapeCutter_feedback.ShapeCutterFeedbackScreenClass(name = 'sCfeedback', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(sCfeedback_screen)
        sCrepeat_screen = screen_shapeCutter_repeat.ShapeCutterRepeatScreenClass(name = 'sCrepeat', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(sCrepeat_screen)
        sCexit_screen = screen_shapeCutter_exit.ShapeCutterExitScreenClass(name = 'sCexit', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(sCexit_screen)
        
    def get_info(self):
        self.sm.current = 'sCtutorial'
      
    def cut_rectangle(self):
        self.j.shape_dict["shape"] = "rectangle"
        self.next_screen()
    
    def cut_circle(self):
        self.j.shape_dict["shape"] = "circle"
        self.next_screen()
    
    def next_screen(self):
        self.sm.current = 'sCApIs'

