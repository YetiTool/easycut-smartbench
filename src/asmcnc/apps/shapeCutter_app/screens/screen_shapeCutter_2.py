"""
Created on 2 March 2020
Screen 2 for the Shape Cutter App

@author: Letty
"""
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import MetricsBase
from kivy.properties import StringProperty, ObjectProperty

Builder.load_string(
    """

<ShapeCutter2ScreenClass>

    info_button: info_button

    BoxLayout:
        size_hint: (None,None)
        width: dp(1.0*app.width)
        height: dp(1.0*app.height)
        padding: 0
        spacing: 0
        orientation: "vertical"

        BoxLayout:
            size_hint: (None,None)
            width: dp(1.0*app.width)
            height: dp(0.1875*app.height)
            padding: 0
            spacing: 0
            orientation: "horizontal"

            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint: (None,None)
                height: dp(0.1875*app.height)
                width: dp(0.1775*app.width)
                on_press: root.prepare()
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/apps/shapeCutter_app/img/prepare_tab_grey.png"
                        size: self.parent.size
                        allow_stretch: True
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint: (None,None)
                height: dp(0.1875*app.height)
                width: dp(0.1775*app.width)
                on_press: root.load()
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/apps/shapeCutter_app/img/load_tab_blue.png"
                        size: self.parent.size
                        allow_stretch: True
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint: (None,None)
                height: dp(0.1875*app.height)
                width: dp(0.1775*app.width)
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
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint: (None,None)
                height: dp(0.1875*app.height)
                width: dp(0.1775*app.width)
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
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint: (None,None)
                height: dp(0.1875*app.height)
                width: dp(0.1775*app.width)
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
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint: (None,None)
                height: dp(0.1875*app.height)
                width: dp(0.1125*app.width)
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
            height: dp(0.8125*app.height)
            width: dp(1.0*app.width)
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
                    height: dp(0.125*app.height)
                    width: dp(1.0*app.width)
                    padding:[dp(0.025)*app.width, 0, 0, 0]
                    orientation: "horizontal"
                    
                    BoxLayout: #Screen number
                        size_hint: (None,None)
                        padding: 0
                        height: dp(0.0833333333333*app.height)
                        width: dp(0.05*app.width)
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
                        height: dp(0.125*app.height)
                        width: dp(0.925*app.width)
                        padding:[dp(0.025)*app.width, dp(0.0416666666667)*app.height, 0, 0]
                        
                        Label:
                            text: root.title_label
                            color: color_provider.get_rgba("black")
                            font_size: 0.035*app.width
                            markup: True
                            halign: "left"
                            valign: "bottom"
                            text_size: self.size
                            size: self.parent.size
                            pos: self.parent.pos
                        
                    
                BoxLayout: #Body
                    size_hint: (None,None)
                    height: dp(0.6875*app.height)
                    width: dp(1.0*app.width)
                    padding:[0, dp(0.0416666666667)*app.height, 0, 0]
                    orientation: "horizontal"
                    
                    BoxLayout: #text box
                        size_hint: (None,None)
                        height: dp(0.645833333333*app.height)
                        width: dp(0.84375*app.width)
                        padding:[dp(0.1)*app.width, 0, 0, dp(0.145833333333)*app.height]
                        spacing:0.0208333333333*app.height
                        orientation: "vertical"
                        
                        Label:
                            text: root.user_instructions
                            color: color_provider.get_rgba("black")
                            font_size: 0.025*app.width
                            markup: True
                            halign: "left"
                            valign: "top"
                            text_size: self.size
                            size: self.parent.size
                            pos: self.parent.pos
                            
                        BoxLayout: #checklist 1
                            size_hint: (None,None)
                            height: dp(0.0458333333333*app.height)
                            width: dp(0.74375*app.width)
                            padding:[dp(0.025)*app.width, 0, dp(0.025)*app.width, 0]
                            orientation: "horizontal"
                            
                            BoxLayout: 
                                size_hint: (None,None)
                                height: dp(0.0458333333333*app.height)
                                width: dp(0.0375*app.width)
                                padding:[0, 0, dp(0.01)*app.width, 0]
                                Image: 
                                    source: "./asmcnc/apps/shapeCutter_app/img/box_unchecked.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True
                                
                            Label: 
                                text: "Clear SmartBench topside"
                                color: color_provider.get_rgba("black")
                                font_size: 0.025*app.width
                                markup: True
                                halign: "left"
                                valign: "top"
                                text_size: self.size
                                size: self.parent.size
                                pos: self.parent.pos

                        BoxLayout: #checklist 2
                            size_hint: (None,None)
                            height: dp(0.0458333333333*app.height)
                            width: dp(0.74375*app.width)
                            padding:[dp(0.025)*app.width, 0, dp(0.025)*app.width, 0]
                            orientation: "horizontal"

                            BoxLayout: 
                                size_hint: (None,None)
                                height: dp(0.0458333333333*app.height)
                                width: dp(0.0375*app.width)
                                padding:[0, 0, dp(0.01)*app.width, 0]
                                Image: 
                                    source: "./asmcnc/apps/shapeCutter_app/img/box_unchecked.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True
                                
                            Label: 
                                text: "Clean SmartBench axes"
                                color: color_provider.get_rgba("black")
                                font_size: 0.025*app.width
                                markup: True
                                halign: "left"
                                valign: "top"
                                text_size: self.size
                                size: self.parent.size
                                pos: self.parent.pos
                                
                        BoxLayout: #checklist 3
                            size_hint: (None,None)
                            height: dp(0.0458333333333*app.height)
                            width: dp(0.74375*app.width)
                            padding:[dp(0.025)*app.width, 0, dp(0.025)*app.width, 0]
                            orientation: "horizontal"
                            
                            BoxLayout: 
                                size_hint: (None,None)
                                height: dp(0.0458333333333*app.height)
                                width: dp(0.0375*app.width)
                                padding:[0, 0, dp(0.01)*app.width, 0]
                                Image: 
                                    source: "./asmcnc/apps/shapeCutter_app/img/box_unchecked.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True
                                
                            Label: 
                                text: "Empty vacuum bag"
                                color: color_provider.get_rgba("black")
                                font_size: 0.025*app.width
                                markup: True
                                halign: "left"
                                valign: "top"
                                text_size: self.size
                                size: self.parent.size
                                pos: self.parent.pos

                        BoxLayout: #checklist 4
                            size_hint: (None,None)
                            height: dp(0.0458333333333*app.height)
                            width: dp(0.74375*app.width)
                            padding:[dp(0.025)*app.width, 0, dp(0.025)*app.width, 0]
                            orientation: "horizontal"

                            BoxLayout: 
                                size_hint: (None,None)
                                height: dp(0.0458333333333*app.height)
                                width: dp(0.0375*app.width)
                                padding:[0, 0, dp(0.01)*app.width, 0]
                                Image: 
                                    source: "./asmcnc/apps/shapeCutter_app/img/box_unchecked.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True
                                
                            Label: 
                                text: "Fit vacuum hose"
                                color: color_provider.get_rgba("black")
                                font_size: 0.025*app.width
                                markup: True
                                halign: "left"
                                valign: "top"
                                text_size: self.size
                                size: self.parent.size
                                pos: self.parent.pos
                                                        
                        BoxLayout: #checklist 5
                            size_hint: (None,None)
                            height: dp(0.0458333333333*app.height)
                            width: dp(0.74375*app.width)
                            padding:[dp(0.025)*app.width, 0, dp(0.025)*app.width, 0]
                            orientation: "horizontal"
                            
                            BoxLayout: 
                                size_hint: (None,None)
                                height: dp(0.0458333333333*app.height)
                                width: dp(0.0375*app.width)
                                padding:[0, 0, dp(0.01)*app.width, 0]
                                Image: 
                                    source: "./asmcnc/apps/shapeCutter_app/img/box_unchecked.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True
                                
                            Label: 
                                text: "Secure power cords"
                                color: color_provider.get_rgba("black")
                                font_size: 0.025*app.width
                                markup: True
                                halign: "left"
                                valign: "top"
                                text_size: self.size
                                size: self.parent.size
                                pos: self.parent.pos

                        BoxLayout: #checklist 6
                            size_hint: (None,None)
                            height: dp(0.0458333333333*app.height)
                            width: dp(0.74375*app.width)
                            padding:[dp(0.025)*app.width, 0, dp(0.025)*app.width, 0]
                            orientation: "horizontal"

                            BoxLayout: 
                                size_hint: (None,None)
                                height: dp(0.0458333333333*app.height)
                                width: dp(0.0375*app.width)
                                padding:[0, 0, dp(0.01)*app.width, 0]
                                Image: 
                                    source: "./asmcnc/apps/shapeCutter_app/img/box_unchecked.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True
                                
                            Label: 
                                text: "Lock Z head connections"
                                color: color_provider.get_rgba("black")
                                font_size: 0.025*app.width
                                markup: True
                                halign: "left"
                                valign: "top"
                                text_size: self.size
                                size: self.parent.size
                                pos: self.parent.pos

                    BoxLayout: #action box
                        size_hint: (None,None)
                        height: dp(0.645833333333*app.height)
                        width: dp(0.15625*app.width)
                        padding:[0, 0, 0, dp(0.0708333333333)*app.height]
                        spacing:0.0708333333333*app.height
                        orientation: "vertical"
                        
                        BoxLayout: 
                            size_hint: (None,None)
                            height: dp(0.139583333333*app.height)
                            width: dp(0.11*app.width)
                            padding:[dp(0.03)*app.width, 0, dp(0.03)*app.width, dp(0.0708333333333)*app.height]
                            Button:
                                font_size: str(0.01875 * app.width) + 'sp'
                                id: info_button
                                size_hint: (None,None)
                                height: dp(0.0833333333333*app.height)
                                width: dp(0.05*app.width)
                                background_color: color_provider.get_rgba("invisible")
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
                            font_size: str(0.01875 * app.width) + 'sp'
                            size_hint: (None,None)
                            height: dp(0.139583333333*app.height)
                            width: dp(0.11*app.width)
                            background_color: color_provider.get_rgba("invisible")
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
                            font_size: str(0.01875 * app.width) + 'sp'
                            size_hint: (None,None)
                            height: dp(0.139583333333*app.height)
                            width: dp(0.11*app.width)
                            background_color: color_provider.get_rgba("invisible")
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


class ShapeCutter2ScreenClass(Screen):
    info_button = ObjectProperty()
    screen_number = StringProperty("[b]2[/b]")
    title_label = StringProperty("[b]Preparation checklist[/b]")
    user_instructions = StringProperty(
        """Step through this section for illustrations of each check:

"""
    )

    def __init__(self, **kwargs):
        super(ShapeCutter2ScreenClass, self).__init__(**kwargs)
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
        self.shapecutter_sm.next_screen()
    
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
