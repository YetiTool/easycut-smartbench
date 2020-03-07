'''
Created on 4 March 2020
Screen 36 for the Shape Cutter App

@author: Letty
'''
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import MetricsBase
from kivy.properties import StringProperty, ObjectProperty
from kivy.clock import Clock

from asmcnc.shapeCutter_app import screen_shapeCutter_feedback
from asmcnc.shapeCutter_app import screen_shapeCutter_repeat
from asmcnc.shapeCutter_app import screen_shapeCutter_post_job_save
from asmcnc.shapeCutter_app import screen_shapeCutter_exit

Builder.load_string("""

<ShapeCutter36ScreenClass>

    info_button: info_button

    BoxLayout:
        size_hint: (None,None)
        width: dp(800)
        height: dp(480)
        padding: 0
        spacing: 0
        orientation: "vertical"

        BoxLayout:
            size_hint: (None,None)
            width: dp(800)
            height: dp(90)
            padding: 0
            spacing: 0
            orientation: "horizontal"

            Button:
                size_hint: (None,None)
                height: dp(90)
                width: dp(142)
                on_press: root.prepare()
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/shapeCutter_app/img/prepare_tab_blue.png"
                        size: self.parent.size
                        stretch: True
            Button:
                size_hint: (None,None)
                height: dp(90)
                width: dp(142)
                on_press: root.load()
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/shapeCutter_app/img/load_tab_blue.png"
                        size: self.parent.size
                        stretch: True
            Button:
                size_hint: (None,None)
                height: dp(90)
                width: dp(142)
                on_press: root.define()
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/shapeCutter_app/img/define_job_tab_blue.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
            Button:
                size_hint: (None,None)
                height: dp(90)
                width: dp(142)
                on_press: root.position()
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/shapeCutter_app/img/position_tab_blue.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
            Button:
                size_hint: (None,None)
                height: dp(90)
                width: dp(142)
                on_press: root.check()
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/shapeCutter_app/img/check_tab_grey.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
            Button:
                size_hint: (None,None)
                height: dp(90)
                width: dp(90)
                on_press: root.exit()
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/shapeCutter_app/img/exit_cross.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True                    
                    
        BoxLayout:
            size_hint: (None,None)
            padding: 0
            height: dp(390)
            width: dp(800)
            canvas:
                Rectangle: 
                    pos: self.pos
                    size: self.size
                    source: "./asmcnc/shapeCutter_app/img/background.png"
            
            BoxLayout:
                orientation: "vertical"
                padding: 0
                spacing: 0
                    
                BoxLayout: #Header
                    size_hint: (None,None)
                    height: dp(60)
                    width: dp(800)
                    padding: (20,0,0,0)
                    orientation: "horizontal"
                    
                    BoxLayout: #Screen number
                        size_hint: (None,None)
                        padding: 0
                        height: dp(40)
                        width: dp(40)
                        canvas:
                            Rectangle: 
                                pos: self.pos
                                size: self.size
                                source: "./asmcnc/shapeCutter_app/img/number_box.png"
                        Label:
                            text: root.screen_number
                            valign: "middle"
                            halign: "center"
                            font_size: 26
                            markup: True
                                
                                
                        
                    BoxLayout: #Title
                        size_hint: (None,None)
                        height: dp(60)
                        width: dp(740)
                        padding: (20,20,0,0)
                        
                        Label:
                            text: root.title_label
                            color: 0,0,0,1
                            font_size: 28
                            markup: True
                            halign: "left"
                            valign: "bottom"
                            text_size: self.size
                            size: self.parent.size
                            pos: self.parent.pos
                        
                    
                BoxLayout: #Body
                    size_hint: (None,None)
                    height: dp(330)
                    width: dp(800)
                    padding: 0,20,0,0
                    orientation: "horizontal"
                 
                    BoxLayout: #text box
                        size_hint: (None,None)
                        height: dp(310)
                        width: dp(675)
                        padding: 80,0,0,5
                        orientation: "vertical"
                        Button:
                            id: spindle_toggle
                            on_release: root.start_job()
                            background_color: 1, 1, 1, 0 
                            BoxLayout:
                                padding: 10
                                size: self.parent.size
                                pos: self.parent.pos      
                                Image:
                                    id: go_image
                                    source: "./asmcnc/skavaUI/img/go.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True  
                        Label:
                            text: root.user_instructions
                            color: 0,0,0,1
                            font_size: 18
                            markup: True
                            halign: "center"
                            valign: "top"
                            text_size: self.size
                            size: self.parent.size
                            pos: self.parent.pos

                    BoxLayout: #action box
                        size_hint: (None,None)
                        height: dp(310)
                        width: dp(125)
                        padding: 0,0,0,34
                        spacing: 34
                        orientation: "vertical"
                        
                        BoxLayout: 
                            size_hint: (None,None)
                            height: dp(67)
                            width: dp(88)
                            padding: (24,0,24,34)
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

                        Button: 
                            size_hint: (None,None)
                            height: dp(67)
                            width: dp(88)
                            background_color: hex('#F4433600')
                            on_press: root.go_back()
                            BoxLayout:
                                padding: 0
                                size: self.parent.size
                                pos: self.parent.pos
                                Image:
                                    source: "./asmcnc/shapeCutter_app/img/arrow_back.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True
                        Button: 
                            size_hint: (None,None)
                            height: dp(67)
                            width: dp(88)
                            background_color: hex('#F4433600')
                            #on_press: root.next_screen()
                            opacity: 0
                            BoxLayout:
                                padding: 0
                                size: self.parent.size
                                pos: self.parent.pos
                                Image:
                                    source: "./asmcnc/shapeCutter_app/img/arrow_next.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True               

""")

class ShapeCutter36ScreenClass(Screen):
    
    info_button = ObjectProperty()
    vacuum_toggle = ObjectProperty()
    
    screen_number = StringProperty("[b]36[/b]")
    title_label = StringProperty("[b]You\'re all set![/b]")
    user_instructions = StringProperty()
   
    def __init__(self, **kwargs):
        super(ShapeCutter36ScreenClass, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        self.j=kwargs['job_parameters']

    def on_pre_enter(self):
        self.info_button.opacity = 0

        # get job info
        self.user_instructions = ("[b]Your cut time is 13 minutes.[/b]\n\n" \
                                           "(That\'s also the world record time to beat for fastest mile" \
                                           " hula-hooped while balancing a milk bottle on the head. "\
                                           "So what are you waiting for?)")

        if not self.sm.has_screen('sCsavejob'): 
            sCsavejob_screen = screen_shapeCutter_post_job_save.ShapeCutterSaveJobScreenClass(name = 'sCsavejob', screen_manager = self.sm, machine = self.m, job_parameters = self.j)
            self.sm.add_widget(sCsavejob_screen)
            sCfeedback_screen = screen_shapeCutter_feedback.ShapeCutterFeedbackScreenClass(name = 'sCfeedback', screen_manager = self.sm, machine = self.m)
            self.sm.add_widget(sCfeedback_screen)
            sCrepeat_screen = screen_shapeCutter_repeat.ShapeCutterRepeatScreenClass(name = 'sCrepeat', screen_manager = self.sm, machine = self.m)
            self.sm.add_widget(sCrepeat_screen)
            sCexit_screen = screen_shapeCutter_exit.ShapeCutterExitScreenClass(name = 'sCexit', screen_manager = self.sm, machine = self.m)
            self.sm.add_widget(sCexit_screen)
 
# Action buttons       
    def get_info(self):
        pass
    
    def go_back(self):
        self.sm.current = 'sC35'
    
    def next_screen(self):
        self.sm.get_screen('go').job_gcode = self.j.generate_gCode()
        self.sm.get_screen('go').job_filename  = self.j.generate_gCode_filename()
        self.sm.current = 'go'
        self.sm.get_screen('go').return_to_screen = 'sCsavejob'
        self.sm.get_screen('go').cancel_to_screen = 'sC36' 
    
# Tab functions

    def prepare(self):
        self.sm.current = 'sC1'
    
    def load(self):
        self.sm.current = 'sC11'
    
    def define(self):
        self.sm.current = 'sC17'
    
    def position(self):
        self.sm.current = 'sC26'
    
    def check(self):
        self.sm.current = 'sC33'
    
    def exit(self):
        self.sm.current = 'sCexit'
    
# Screen specific
    def start_job(self):
        self.next_screen()