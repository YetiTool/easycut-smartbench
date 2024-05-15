"""
Created on 4 March 2020
Screen 34 for the Shape Cutter App

@author: Letty
"""
from asmcnc.comms.logging_system.logging_system import Logger
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import MetricsBase
from kivy.properties import StringProperty, ObjectProperty
from kivy.clock import Clock

Builder.load_string("""
#:import LabelBase asmcnc.core_UI.components.labels.base_label

<ShapeCutter34ScreenClass>

    info_button: info_button
    vacuum_toggle: vacuum_toggle
    vacuum_image: vacuum_image
    next_button: next_button
    back_button: back_button

    BoxLayout:
        size_hint: (None,None)
        width: app.get_scaled_width(800.0)
        height: app.get_scaled_height(480.0)
        padding: 0
        spacing: 0
        orientation: "vertical"

        BoxLayout:
            size_hint: (None,None)
            width: app.get_scaled_width(800.0)
            height: app.get_scaled_height(90.0)
            padding: 0
            spacing: 0
            orientation: "horizontal"

            Button:
                font_size: app.get_scaled_sp('15.0sp')
                size_hint: (None,None)
                height: app.get_scaled_height(90.0)
                width: app.get_scaled_width(142.0)
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
                font_size: app.get_scaled_sp('15.0sp')
                size_hint: (None,None)
                height: app.get_scaled_height(90.0)
                width: app.get_scaled_width(142.0)
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
                font_size: app.get_scaled_sp('15.0sp')
                size_hint: (None,None)
                height: app.get_scaled_height(90.0)
                width: app.get_scaled_width(142.0)
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
                font_size: app.get_scaled_sp('15.0sp')
                size_hint: (None,None)
                height: app.get_scaled_height(90.0)
                width: app.get_scaled_width(142.0)
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
                font_size: app.get_scaled_sp('15.0sp')
                size_hint: (None,None)
                height: app.get_scaled_height(90.0)
                width: app.get_scaled_width(142.0)
                on_press: root.check()
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/apps/shapeCutter_app/img/check_tab_grey.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
            Button:
                font_size: app.get_scaled_sp('15.0sp')
                size_hint: (None,None)
                height: app.get_scaled_height(90.0)
                width: app.get_scaled_width(90.0)
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
            height: app.get_scaled_height(390.0)
            width: app.get_scaled_width(800.0)
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
                    height: app.get_scaled_height(60.0)
                    width: app.get_scaled_width(800.0)
                    padding: app.get_scaled_tuple([20.0, 0, 0, 0])
                    orientation: "horizontal"
                    
                    BoxLayout: #Screen number
                        size_hint: (None,None)
                        padding: 0
                        height: app.get_scaled_height(40.0)
                        width: app.get_scaled_width(40.0)
                        canvas:
                            Rectangle: 
                                pos: self.pos
                                size: self.size
                                source: "./asmcnc/apps/shapeCutter_app/img/number_box.png"
                        LabelBase:
                            text: root.screen_number
                            valign: "middle"
                            halign: "center"
                            font_size: app.get_scaled_width(26.0)
                            markup: True
                                
                                
                        
                    BoxLayout: #Title
                        size_hint: (None,None)
                        height: app.get_scaled_height(60.0)
                        width: app.get_scaled_width(740.0)
                        padding: app.get_scaled_tuple([20.0, 20.0, 0, 0])
                        
                        LabelBase:
                            text: root.title_label
                            color: 0,0,0,1
                            font_size: app.get_scaled_width(28.0)
                            markup: True
                            halign: "left"
                            valign: "bottom"
                            text_size: self.size
                            size: self.parent.size
                            pos: self.parent.pos
                        
                    
                BoxLayout: #Body
                    size_hint: (None,None)
                    height: app.get_scaled_height(330.0)
                    width: app.get_scaled_width(800.0)
                    padding: app.get_scaled_tuple([0, 20.0, 0, 0])
                    orientation: "horizontal"
                 
                    BoxLayout: #text box
                        size_hint: (None,None)
                        height: app.get_scaled_height(310.0)
                        width: app.get_scaled_width(675.0)
                        padding: app.get_scaled_tuple([80.0, 0, 0, 5.0])
                        orientation: "vertical"
                        ToggleButton:
                            font_size: app.get_scaled_sp('15.0sp')
                            id: vacuum_toggle
                            on_press: root.set_vacuum()
                            background_color: 1, 1, 1, 0 
                            BoxLayout:
                                padding: app.get_scaled_tuple([10.0, 10.0])
                                size: self.parent.size
                                pos: self.parent.pos      
                                Image:
                                    id: vacuum_image
                                    source: "./asmcnc/skavaUI/img/vac_off.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True
                        LabelBase:
                            text: root.user_instructions
                            color: 0,0,0,1
                            font_size: app.get_scaled_width(18.0)
                            markup: True
                            halign: "left"
                            valign: "top"
                            text_size: self.size
                            size: self.parent.size
                            pos: self.parent.pos

                    BoxLayout: #action box
                        size_hint: (None,None)
                        height: app.get_scaled_height(310.0)
                        width: app.get_scaled_width(125.0)
                        padding: app.get_scaled_tuple([0, 0, 0, 34.0])
                        spacing: app.get_scaled_width(34.0)
                        orientation: "vertical"
                        
                        BoxLayout: 
                            size_hint: (None,None)
                            height: app.get_scaled_height(67.0)
                            width: app.get_scaled_width(88.0)
                            padding: app.get_scaled_tuple([24.0, 0, 24.0, 34.0])
                            Button:
                                font_size: app.get_scaled_sp('15.0sp')
                                id: info_button
                                size_hint: (None,None)
                                height: app.get_scaled_height(40.0)
                                width: app.get_scaled_width(40.0)
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
                            font_size: app.get_scaled_sp('15.0sp')
                            id: back_button
                            size_hint: (None,None)
                            height: app.get_scaled_height(67.0)
                            width: app.get_scaled_width(88.0)
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
                            font_size: app.get_scaled_sp('15.0sp')
                            id: next_button
                            size_hint: (None,None)
                            height: app.get_scaled_height(67.0)
                            width: app.get_scaled_width(88.0)
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


class ShapeCutter34ScreenClass(Screen):
    info_button = ObjectProperty()
    vacuum_toggle = ObjectProperty()
    screen_number = StringProperty("[b]34[/b]")
    title_label = StringProperty(
        "[b]Check extractor power (if powered by SmartBench)[/b]"
    )
    user_instructions = StringProperty(
        """Press the button. The extractor should come on for 2 seconds.

If not, check that it's connected and switched on, then retry by pressing the button again."""
    )

    def __init__(self, **kwargs):
        super(ShapeCutter34ScreenClass, self).__init__(**kwargs)
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
    
# Screen specific

    def set_vacuum(self):
        if self.vacuum_toggle.state == "normal":
            self.next_button.disabled = False
            self.back_button.disabled = False
            self.vacuum_image.source = "./asmcnc/skavaUI/img/vac_off.png"
            Logger.info("vac off")
            self.m.turn_off_vacuum()
        else:
            Logger.info("vac on")
            self.next_button.disabled = True
            self.back_button.disabled = True
            self.vacuum_image.source = "./asmcnc/skavaUI/img/vac_on.png"
            self.m.turn_on_vacuum()
            Clock.schedule_once(self.reset_vacuum, 2)

    def reset_vacuum(self, dt):
        #self.m.vac_on()
        self.vacuum_toggle.state = "normal"
        self.set_vacuum()
