"""
Created on 4 March 2020
Screen 25 for the Shape Cutter App

@author: Letty
"""

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import MetricsBase
from kivy.properties import StringProperty, ObjectProperty

from asmcnc.apps.shapeCutter_app.screens import popup_input_error

Builder.load_string(
    """

<ShapeCutter25ScreenClass>

    info_button: info_button
    file_name: file_name
    save_image: save_image
    
    on_touch_down: root.on_touch()

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
                        source: "./asmcnc/apps/shapeCutter_app/img/prepare_tab_blue.png"
                        size: self.parent.size
                        allow_stretch: True
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
                        source: "./asmcnc/apps/shapeCutter_app/img/load_tab_blue.png"
                        size: self.parent.size
                        allow_stretch: True
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
                        source: "./asmcnc/apps/shapeCutter_app/img/define_job_tab_grey.png"
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
                        source: "./asmcnc/apps/shapeCutter_app/img/position_tab_blue.png"
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
                        source: "./asmcnc/apps/shapeCutter_app/img/check_tab_blue.png"
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
                        source: "./asmcnc/apps/shapeCutter_app/img/exit_cross.png"
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
                    source: "./asmcnc/apps/shapeCutter_app/img/background.png"
            
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
                                source: "./asmcnc/apps/shapeCutter_app/img/number_box.png"
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
                        padding: 10,0,25,10
                        orientation: "horizontal"
                        BoxLayout: # file save
                            size_hint: (None,None)
                            height: dp(300)
                            width: dp(300)
                            padding: (0,0,0,0) 
                            orientation: "vertical"       
                            BoxLayout: 
                                size_hint: (None,None)
                                height: dp(70)
                                width: dp(300)
                                padding: (0,0,0,5)
                                orientation: "vertical"

#                                 Label: 
#                                     text: ""
#                                     color: 0,0,0,1
#                                     font_size: 20
#                                     markup: True
#                                     halign: "center"
#                                     valign: "top"
#                                     text_size: self.size
#                                     size: self.parent.size
#                                     pos: self.parent.pos
                                    
                                BoxLayout: 
                                    size_hint: (None,None)
                                    height: dp(40)
                                    width: dp(300)
                                    padding: (10,0,10,0)
                                                
                                    TextInput: 
                                        id: file_name
                                        valign: 'middle'
                                        halign: 'center'
                                        text_size: self.size
                                        font_size: '20sp'
                                        markup: True
                                        multiline: False
                                        text: ''                           
                            BoxLayout: 
                                size_hint: (None,None)
                                height: dp(168)
                                width: dp(300)
                                padding: (66,0,66,0)
                                Button:
                                    size_hint: (None,None)
                                    height: dp(168)
                                    width: dp(168)
                                    on_press: root.save_file()
                                    background_color: hex('#F4433600')
                                    BoxLayout:
                                        padding: 0
                                        size: self.parent.size
                                        pos: self.parent.pos
                                        Image:
                                            id: save_image
                                            source: "./asmcnc/apps/shapeCutter_app/img/save_file.png"
                                            size: self.parent.size
                                            allow_stretch: True
                            BoxLayout: 
                                size_hint: (None,None)
                                height: dp(62)
                                width: dp(300)
                                padding: (0,0,0,0)
                                Label: 
                                    text: "You can save this profile later after the job too. "
                                    color: 0,0,0,1
                                    font_size: 20
                                    markup: True
                                    halign: "center"
                                    valign: "middle"
                                    text_size: self.size
                                    size: self.parent.size
                                    pos: self.parent.pos                                            
                                            
                        BoxLayout: # document viewer
                            size_hint: (None,None)
                            height: dp(300)
                            width: dp(350)
                            padding: (0,0,0,0)
                            ScrollView:
                                size_hint: (None, None)
                                size: self.parent.size
                                pos: self.parent.pos
                                do_scroll_x: True
                                do_scroll_y: True
                                scroll_type: ['content']
                                RstDocument:
                                    text: root.display_profile
                                    background_color: hex('#FFFFFF')

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
                                        source: "./asmcnc/apps/shapeCutter_app/img/info_icon.png"
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
                                    source: "./asmcnc/apps/shapeCutter_app/img/arrow_back.png"
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
                                    source: "./asmcnc/apps/shapeCutter_app/img/arrow_next.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True               

"""
)


class ShapeCutter25ScreenClass(Screen):
    info_button = ObjectProperty()

    screen_number = StringProperty("[b]25[/b]")
    title_label = StringProperty("[b]Would you like to save this as a new profile?[/b]")
    display_profile = StringProperty()

    def __init__(self, **kwargs):
        super(ShapeCutter25ScreenClass, self).__init__(**kwargs)
        self.shapecutter_sm = kwargs["shapecutter"]
        self.m = kwargs["machine"]
        self.j = kwargs["job_parameters"]
        self.kb = kwargs["keyboard"]

        # Add the IDs of ALL the TextInputs on this screen
        self.text_inputs = [self.file_name]

    def on_touch(self):
        for text_input in self.text_inputs:
            text_input.focus = False

    def on_pre_enter(self):
        self.info_button.opacity = 0
        self.display_profile = self.j.parameters_to_string()
        self.file_name.text = ""
        self.save_image.source = "./asmcnc/apps/shapeCutter_app/img/save_file.png"

    def on_enter(self):
        self.kb.setup_text_inputs(self.text_inputs)

    # Action buttons
    def get_info(self):
        pass

    def go_back(self):
        self.shapecutter_sm.previous_screen()

    def next_screen(self):
        self.shapecutter_sm.position_tab()

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

    # Screen commands
    def save_file(self):
        if not self.file_name.text == "":
            self.j.save_parameters(self.file_name.text)
            self.save_image.source = "./asmcnc/apps/shapeCutter_app/img/thumbs_up.png"
        #         self.j.generate_gCode()
        #         self.j.save_gCode()

        else:
            description = "Filename input is empty.\n\nPlease enter a name for your parameter profile."
            popup_input_error.PopupInputError(self.shapecutter_sm, description)
