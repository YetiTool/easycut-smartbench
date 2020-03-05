'''
Created on 4 March 202
Screen 23 for the Shape Cutter App

@author: Letty
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import MetricsBase
from kivy.properties import StringProperty, ObjectProperty

from asmcnc.shapeCutter_app import screen_shapeCutter_24

Builder.load_string("""

<ShapeCutter23ScreenClass>

    info_button: info_button
    unit_toggle: unit_toggle
    unit_label: unit_label

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
                        source: "./asmcnc/shapeCutter_app/img/define_job_tab_grey.png"
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
                        source: "./asmcnc/shapeCutter_app/img/check_tab_blue.png"
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
                        padding: 80,0,0,0
                        orientation: "vertical"
                    
                        BoxLayout: #text box
                            size_hint: (None,None)
                            height: dp(55)
                            width: dp(675)
                            padding: 0,0,0,0
                            orientation: "vertical"                       

                        BoxLayout: #image & text entry box
                            size_hint: (None,None)
                            height: dp(255)
                            width: dp(595)
                            padding:0,0,0,21
                            orientation: "horizontal"
                                    
                            BoxLayout:
                                orientation: 'vertical'
                                size_hint: (None,None)
                                width: dp(595)
                                height: dp(255)
                                padding: (0,0,0,50)
                                spacing: 20
                                pos: self.parent.pos
                                
                                # BL horizontal
                                    # Toggle button
                                BoxLayout:
                                    size_hint: (None,None)
                                    height: dp(30)
                                    width: dp(595)
                                    padding: (342.5,0,177.5,0)                   
                                    orientation: "horizontal"
                                                    
                                    ToggleButton:
                                        id: unit_toggle
                                        size_hint: (None,None)
                                        height: dp(30)
                                        width: dp(75)
                                        background_color: hex('#F4433600')
                                        center: self.parent.center
                                        pos: self.parent.pos
                                        on_press: root.toggle_units()
        
                                        BoxLayout:
                                            height: dp(30)
                                            width: dp(75)
                                            canvas:
                                                Rectangle: 
                                                    pos: self.parent.pos
                                                    size: self.parent.size
                                                    source: "./asmcnc/shapeCutter_app/img/mm_inches_toggle.png"  
                                        Label:
                                            id: unit_label
                                            text: "mm"
                                            color: 1,1,1,1
                                            font_size: 20
                                            markup: True
                                            halign: "center"
                                            valign: "middle"
                                            text_size: self.size
                                            size: self.parent.size
                                            pos: self.parent.pos                       
                            
                                BoxLayout: #dimension 1
                                    size_hint: (None,None)
                                    height: dp(30)
                                    width: dp(595)
                                    padding: (0,0,20,0)                   
                                    orientation: "horizontal"
                                    
                                    Label: 
                                        text: "XY feed rate"
                                        color: 0,0,0,1
                                        font_size: 20
                                        markup: True
                                        halign: "left"
                                        valign: "top"
                                        text_size: self.size
                                        size: self.parent.size
                                        pos: self.parent.pos
                                                                  
                                    BoxLayout: 
                                        size_hint: (None,None)
                                        height: dp(30)
                                        width: dp(90)
                                        padding: (10,0,10,0)
                                                    
                                        TextInput: 
                                            id: xy_feed
                                            valign: 'top'
                                            halign: 'center'
                                            text_size: self.size
                                            font_size: '20sp'
                                            markup: True
                                            input_filter: 'float'
                                            multiline: False
                                            text: ''
                                            on_text_validate: root.check_dimensions()
                                    BoxLayout: 
                                        size_hint: (None,None)
                                        height: dp(30)
                                        width: dp(150)
                                        padding: (10,0,10,0)
                                        Label: 
                                            text: "units/min"
                                            color: 0,0,0,1
                                            font_size: 20
                                            markup: True
                                            halign: "left"
                                            valign: "top"
                                            text_size: self.size
                                            size: self.parent.size
                                            pos: self.parent.pos                      
                                
                                BoxLayout: #dimension 2
                                    size_hint: (None,None)
                                    height: dp(30)
                                    width: dp(595)
                                    padding: (0,0,20,0)                   
                                    orientation: "horizontal"
                                    
                                    Label: 
                                        text: "Z feed rate"
                                        color: 0,0,0,1
                                        font_size: 20
                                        markup: True
                                        halign: "left"
                                        valign: "top"
                                        text_size: self.size
                                        size: self.parent.size
                                        pos: self.parent.pos
                                                                  
                                    BoxLayout: 
                                        size_hint: (None,None)
                                        height: dp(30)
                                        width: dp(90)
                                        padding: (10,0,10,0)
                                                    
                                        TextInput: 
                                            id: z_feed
                                            valign: 'top'
                                            halign: 'center'
                                            text_size: self.size
                                            font_size: '20sp'
                                            markup: True
                                            input_filter: 'float'
                                            multiline: False
                                            text: ''
                                            on_text_validate: root.check_dimensions()                           
                                    BoxLayout: 
                                        size_hint: (None,None)
                                        height: dp(30)
                                        width: dp(150)
                                        padding: (10,0,10,0)
                                        Label: 
                                            text: "units/min"
                                            color: 0,0,0,1
                                            font_size: 20
                                            markup: True
                                            halign: "left"
                                            valign: "top"
                                            text_size: self.size
                                            size: self.parent.size
                                            pos: self.parent.pos
                                BoxLayout: #dimension 3
                                    size_hint: (None,None)
                                    height: dp(30)
                                    width: dp(595)
                                    padding: (0,0,20,0)                   
                                    orientation: "horizontal"
                                    
                                    Label: 
                                        text: "Spindle speed (precision only)"
                                        color: 0,0,0,1
                                        font_size: 20
                                        markup: True
                                        halign: "left"
                                        valign: "top"
                                        text_size: self.size
                                        size: self.parent.size
                                        pos: self.parent.pos
                                                                  
                                    BoxLayout: 
                                        size_hint: (None,None)
                                        height: dp(30)
                                        width: dp(90)
                                        padding: (10,0,10,0)
                                                    
                                        TextInput: 
                                            id: spindle_speed
                                            valign: 'top'
                                            halign: 'center'
                                            text_size: self.size
                                            font_size: '20sp'
                                            markup: True
                                            input_filter: 'float'
                                            multiline: False
                                            text: ''
                                            on_text_validate: root.check_dimensions()                                                                
                                    BoxLayout: 
                                        size_hint: (None,None)
                                        height: dp(30)
                                        width: dp(150)
                                        padding: (10,0,10,0)
                                        Label: 
                                            text: "RPM"
                                            color: 0,0,0,1
                                            font_size: 20
                                            markup: True
                                            halign: "left"
                                            valign: "top"
                                            text_size: self.size
                                            size: self.parent.size
                                            pos: self.parent.pos

                                BoxLayout: # reminder
                                    size_hint: (None,None)
                                    height: dp(60)
                                    width: dp(595)
                                    padding: (0,10,60,0)                   
                                    orientation: "horizontal"
                                    
                                    Label: 
                                        text: "[b]Reminder: If you have manual speed control don\'t forget to set this on the dial.[/b]"
                                        color: 0,0,0,1
                                        font_size: 20
                                        markup: True
                                        halign: "left"
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
                            on_press: root.next_screen()
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

class ShapeCutter23ScreenClass(Screen):
    
    info_button = ObjectProperty()
    
    screen_number = StringProperty("[b]23[/b]")
    title_label = StringProperty("[b]Enter feeds and speeds[/b]")
    user_instructions = StringProperty("")
    
    def __init__(self, **kwargs):
        super(ShapeCutter23ScreenClass, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        self.j=kwargs['job_parameters']

    def on_pre_enter(self):
        self.info_button.opacity = 1

# Action buttons       
    def get_info(self):
        pass
    
    def go_back(self):
        self.sm.current = 'sC22'
    
    def next_screen(self):
        self.sm.current = 'sC24'
    
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
    def toggle_units(self):
        if self.unit_toggle.state == 'normal':
            self.unit_label.text = "mm"
        elif self.unit_toggle.state == 'down': 
            self.unit_label.text = "inches"

    def check_dimensions(self):
        pass