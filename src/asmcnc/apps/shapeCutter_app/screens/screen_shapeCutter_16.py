"""
Created on 2 March 2020
Screen 16 for the Shape Cutter App

@author: Letty
"""
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import MetricsBase
from kivy.properties import StringProperty, ObjectProperty

Builder.load_string(
    """

<ShapeCutter16ScreenClass>

    info_button: info_button

    BoxLayout:
        size_hint: (None,None)
        width: dp(app.get_scaled_width(800))
        height: dp(app.get_scaled_height(480))
        padding: 0
        spacing: 0
        orientation: "vertical"

        BoxLayout:
            size_hint: (None,None)
            width: dp(app.get_scaled_width(800))
            height: dp(app.get_scaled_height(90))
            padding: 0
            spacing: 0
            orientation: "horizontal"

            Button:
                font_size: str(get_scaled_width(15)) + 'sp'
                size_hint: (None,None)
                height: dp(app.get_scaled_height(90))
                width: dp(app.get_scaled_width(142))
                on_press: root.prepare()
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/apps/shapeCutter_app/img/prepare_tab_blue.png"
                        size: self.parent.size
                        allow_stretch: True
            Button:
                font_size: str(get_scaled_width(15)) + 'sp'
                size_hint: (None,None)
                height: dp(app.get_scaled_height(90))
                width: dp(app.get_scaled_width(142))
                on_press: root.load()
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/apps/shapeCutter_app/img/load_tab_grey.png"
                        size: self.parent.size
                        allow_stretch: True
            Button:
                font_size: str(get_scaled_width(15)) + 'sp'
                size_hint: (None,None)
                height: dp(app.get_scaled_height(90))
                width: dp(app.get_scaled_width(142))
                on_press: root.define()
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/apps/shapeCutter_app/img/define_job_tab_blue.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
            Button:
                font_size: str(get_scaled_width(15)) + 'sp'
                size_hint: (None,None)
                height: dp(app.get_scaled_height(90))
                width: dp(app.get_scaled_width(142))
                on_press: root.position()
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/apps/shapeCutter_app/img/position_tab_blue.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
            Button:
                font_size: str(get_scaled_width(15)) + 'sp'
                size_hint: (None,None)
                height: dp(app.get_scaled_height(90))
                width: dp(app.get_scaled_width(142))
                on_press: root.check()
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/apps/shapeCutter_app/img/check_tab_blue.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
            Button:
                font_size: str(get_scaled_width(15)) + 'sp'
                size_hint: (None,None)
                height: dp(app.get_scaled_height(90))
                width: dp(app.get_scaled_width(90))
                on_press: root.exit()
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/apps/shapeCutter_app/img/exit_cross.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True                    
                    
        BoxLayout:
            size_hint: (None,None)
            padding: 0
            height: dp(app.get_scaled_height(390))
            width: dp(app.get_scaled_width(800))
            canvas:
                Rectangle: 
                    pos: self.pos
                    size: self.size
                    source: "./asmcnc/apps/shapeCutter_app/img/background.png"
            
            BoxLayout:
                orientation: "vertical"
                padding: 0
                spacing: 0
                    
                BoxLayout: #Header
                    size_hint: (None,None)
                    height: dp(app.get_scaled_height(60))
                    width: dp(app.get_scaled_width(800))
                    padding:[app.get_scaled_width(20), 0, 0, 0]
                    orientation: "horizontal"
                    
                    BoxLayout: #Screen number
                        size_hint: (None,None)
                        padding: 0
                        height: dp(app.get_scaled_height(40))
                        width: dp(app.get_scaled_width(40))
                        canvas:
                            Rectangle: 
                                pos: self.pos
                                size: self.size
                                source: "./asmcnc/apps/shapeCutter_app/img/number_box.png"
                        Label:
                            text: root.screen_number
                            valign: "middle"
                            halign: "center"
                            font_size: 0.0325*app.width
                            markup: True
                                
                                
                        
                    BoxLayout: #Title
                        size_hint: (None,None)
                        height: dp(app.get_scaled_height(60))
                        width: dp(app.get_scaled_width(740))
                        padding:[app.get_scaled_width(20), app.get_scaled_height(20), 0, 0]
                        
                        Label:
                            text: root.title_label
                            color: 0,0,0,1
                            font_size: 0.035*app.width
                            markup: True
                            halign: "left"
                            valign: "bottom"
                            text_size: self.size
                            size: self.parent.size
                            pos: self.parent.pos
                        
                    
                BoxLayout: #Body
                    size_hint: (None,None)
                    height: dp(app.get_scaled_height(330))
                    width: dp(app.get_scaled_width(800))
                    padding:[0, app.get_scaled_height(20), 0, 0]
                    orientation: "horizontal"
                    
                    BoxLayout: #text box
                        size_hint: (None,None)
                        height: dp(app.get_scaled_height(310))
                        width: dp(app.get_scaled_width(675))
                        padding:[app.get_scaled_width(80), 0, 0, app.get_scaled_height(122)]
                        spacing:0.0208333333333*app.height
                        orientation: "vertical"
                        
                        Label:
                            text: root.user_instructions
                            color: 0,0,0,1
                            font_size: 0.025*app.width
                            markup: True
                            halign: "left"
                            valign: "top"
                            text_size: self.size
                            size: self.parent.size
                            pos: self.parent.pos
                            
                        BoxLayout: #checklist 1
                            size_hint: (None,None)
                            height: dp(app.get_scaled_height(22))
                            width: dp(app.get_scaled_width(595))
                            padding:[app.get_scaled_width(20), 0, app.get_scaled_width(20), 0]
                            orientation: "horizontal"
                            
                            BoxLayout: 
                                size_hint: (None,None)
                                height: dp(app.get_scaled_height(22))
                                width: dp(app.get_scaled_width(30))
                                padding:[0, 0, app.get_scaled_width(8), 0]
                                Image: 
                                    source: "./asmcnc/apps/shapeCutter_app/img/box_checked.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True
                                
                            Label: 
                                text: "Home SmartBench"
                                color: 0,0,0,1
                                font_size: 0.025*app.width
                                markup: True
                                halign: "left"
                                valign: "top"
                                text_size: self.size
                                size: self.parent.size
                                pos: self.parent.pos

                        BoxLayout: #checklist 2
                            size_hint: (None,None)
                            height: dp(app.get_scaled_height(22))
                            width: dp(app.get_scaled_width(595))
                            padding:[app.get_scaled_width(20), 0, app.get_scaled_width(20), 0]
                            orientation: "horizontal"

                            BoxLayout: 
                                size_hint: (None,None)
                                height: dp(app.get_scaled_height(22))
                                width: dp(app.get_scaled_width(30))
                                padding:[0, 0, app.get_scaled_width(8), 0]
                                Image: 
                                    source: "./asmcnc/apps/shapeCutter_app/img/box_checked.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True
                                
                            Label: 
                                text: "Secure spoilboard if required"
                                color: 0,0,0,1
                                font_size: 0.025*app.width
                                markup: True
                                halign: "left"
                                valign: "top"
                                text_size: self.size
                                size: self.parent.size
                                pos: self.parent.pos
                                
                        BoxLayout: #checklist 3
                            size_hint: (None,None)
                            height: dp(app.get_scaled_height(22))
                            width: dp(app.get_scaled_width(595))
                            padding:[app.get_scaled_width(20), 0, app.get_scaled_width(20), 0]
                            orientation: "horizontal"
                            
                            BoxLayout: 
                                size_hint: (None,None)
                                height: dp(app.get_scaled_height(22))
                                width: dp(app.get_scaled_width(30))
                                padding:[0, 0, app.get_scaled_width(8), 0]
                                Image: 
                                    source: "./asmcnc/apps/shapeCutter_app/img/box_checked.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True
                                
                            Label: 
                                text: "Secure stock material"
                                color: 0,0,0,1
                                font_size: 0.025*app.width
                                markup: True
                                halign: "left"
                                valign: "top"
                                text_size: self.size
                                size: self.parent.size
                                pos: self.parent.pos

                        BoxLayout: #checklist 4
                            size_hint: (None,None)
                            height: dp(app.get_scaled_height(22))
                            width: dp(app.get_scaled_width(595))
                            padding:[app.get_scaled_width(20), 0, app.get_scaled_width(20), 0]
                            orientation: "horizontal"

                            BoxLayout: 
                                size_hint: (None,None)
                                height: dp(app.get_scaled_height(22))
                                width: dp(app.get_scaled_width(30))
                                padding:[0, 0, app.get_scaled_width(8), 0]
                                Image: 
                                    source: "./asmcnc/apps/shapeCutter_app/img/box_checked.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True
                                
                            Label: 
                                text: "Clamp X beam"
                                color: 0,0,0,1
                                font_size: 0.025*app.width
                                markup: True
                                halign: "left"
                                valign: "top"
                                text_size: self.size
                                size: self.parent.size
                                pos: self.parent.pos
                                                        
                        BoxLayout: #checklist 5
                            size_hint: (None,None)
                            height: dp(app.get_scaled_height(22))
                            width: dp(app.get_scaled_width(595))
                            padding:[app.get_scaled_width(20), 0, app.get_scaled_width(20), 0]
                            orientation: "horizontal"
#                             
#                             BoxLayout: 
#                                 size_hint: (None,None)
#                                 height: dp(22)
#                                 width: dp(30)
#                                 padding: (0,0,8,0)                        
#                                 Image: 
#                                     source: "./asmcnc/apps/shapeCutter_app/img/box_checked.png"
#                                     center_x: self.parent.center_x
#                                     y: self.parent.y
#                                     size: self.parent.width, self.parent.height
#                                     allow_stretch: True
#                                 
#                             Label: 
#                                 text: "Fit cutter"
#                                 color: 0,0,0,1
#                                 font_size: 20
#                                 markup: True
#                                 halign: "left"
#                                 valign: "top"
#                                 text_size: self.size
#                                 size: self.parent.size
#                                 pos: self.parent.pos

                    BoxLayout: #action box
                        size_hint: (None,None)
                        height: dp(app.get_scaled_height(310))
                        width: dp(app.get_scaled_width(125))
                        padding:[0, 0, 0, app.get_scaled_height(34)]
                        spacing:0.0708333333333*app.height
                        orientation: "vertical"
                        
                        BoxLayout: 
                            size_hint: (None,None)
                            height: dp(app.get_scaled_height(67))
                            width: dp(app.get_scaled_width(88))
                            padding:[app.get_scaled_width(24), 0, app.get_scaled_width(24), app.get_scaled_height(34)]
                            Button:
                                font_size: str(get_scaled_width(15)) + 'sp'
                                id: info_button
                                size_hint: (None,None)
                                height: dp(app.get_scaled_height(40))
                                width: dp(app.get_scaled_width(40))
                                background_color: hex('#F4433600')
                                opacity: 1
                                on_press: root.get_info()
                                BoxLayout:
                                    padding: 0
                                    size: self.parent.size
                                    pos: self.parent.pos
                                    Image:
                                        source: "./asmcnc/apps/shapeCutter_app/img/info_icon.png"
                                        center_x: self.parent.center_x
                                        y: self.parent.y
                                        size: self.parent.width, self.parent.height
                                        allow_stretch: True

                        Button: 
                            font_size: str(get_scaled_width(15)) + 'sp'
                            size_hint: (None,None)
                            height: dp(app.get_scaled_height(67))
                            width: dp(app.get_scaled_width(88))
                            background_color: hex('#F4433600')
                            on_press: root.go_back()
                            BoxLayout:
                                padding: 0
                                size: self.parent.size
                                pos: self.parent.pos
                                Image:
                                    source: "./asmcnc/apps/shapeCutter_app/img/arrow_back.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True
                        Button: 
                            font_size: str(get_scaled_width(15)) + 'sp'
                            size_hint: (None,None)
                            height: dp(app.get_scaled_height(67))
                            width: dp(app.get_scaled_width(88))
                            background_color: hex('#F4433600')
                            on_press: root.next_screen()
                            BoxLayout:
                                padding: 0
                                size: self.parent.size
                                pos: self.parent.pos
                                Image:
                                    source: "./asmcnc/apps/shapeCutter_app/img/arrow_next.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True               

"""
)


class ShapeCutter16ScreenClass(Screen):
    info_button = ObjectProperty()
    screen_number = StringProperty("[b]16[/b]")
    title_label = StringProperty("[b]Loaded![/b]")
    user_instructions = StringProperty()

    def __init__(self, **kwargs):
        super(ShapeCutter16ScreenClass, self).__init__(**kwargs)
        self.shapecutter_sm = kwargs["shapecutter"]
        self.m = kwargs["machine"]

    def on_pre_enter(self):
        self.info_button.opacity = 0

# Action buttons       
    def get_info(self):
        pass

    def go_back(self):
        self.shapecutter_sm.previous_screen()

    def next_screen(self):
        self.shapecutter_sm.define_tab()

# Tab functions

    def prepare(self):
        self.shapecutter_sm.prepare_tab()

    def load(self):
        self.shapecutter_sm.load_tab()

    def define(self):
        self.shapecutter_sm.define_tab()

    def position(self):
        self.shapecutter_sm.position_tab()

    def check(self):
        self.shapecutter_sm.check_tab()

    def exit(self):
        self.shapecutter_sm.exit_shapecutter()
