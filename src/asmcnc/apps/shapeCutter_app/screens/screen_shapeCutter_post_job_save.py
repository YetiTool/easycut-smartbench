"""
Created on 4 March 2020
Feedback Screen for the Shape Cutter App

@author: Letty
"""
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from asmcnc.apps.shapeCutter_app.screens import popup_input_error
Builder.load_string(
    """

<ShapeCutterSaveJobScreenClass>:
    
    save_image: save_image
    file_name: file_name
    
    on_touch_down: root.on_touch()
    
    BoxLayout:
        height: dp(1.66666666667*app.height)
        width: dp(0.6*app.width)
        canvas:
            Rectangle: 
                pos:self.pos
                size: self.size
                source: "./asmcnc/apps/shapeCutter_app/img/landing_background.png"

        BoxLayout:
            padding: 0
            spacing: 0
            orientation: "vertical"       
                
            Label:
                color: 1,1,1,1
                size_hint: (None,None)
                height: dp(0.1875*app.height)
                width: dp(1.0*app.width)
                text: "Would you like to save this as a new profile?"
                font_size: 0.0375*app.width
                halign: "center"
                valign: "bottom"
                markup: True

            BoxLayout: #Body
                size_hint: (None,None)
                height: dp(0.8125*app.height)
                width: dp(1.0*app.width)
                padding:0,0.0416666666667*app.height,0,0
                orientation: "horizontal"
                
                BoxLayout: #text box
                    size_hint: (None,None)
                    height: dp(0.8125*app.height)
                    width: dp(0.84375*app.width)
                    padding:0.0125*app.width,0,0.03125*app.width,0.0208333333333*app.height
                    orientation: "horizontal"
                    BoxLayout: # file save
                        size_hint: (None,None)
                        height: dp(0.791666666667*app.height)
                        width: dp(0.375*app.width)
                        padding:(0,0.104166666667*app.height,0,0)
                        orientation: "vertical"
                        spacing: 0.0416666666667*app.height 
                        BoxLayout: 
                            size_hint: (None,None)
                            height: dp(0.208333333333*app.height)
                            width: dp(0.375*app.width)
                            padding:(0,0,0,0)
                            orientation: "vertical"
                            spacing:0.0416666666667*app.height

                            Label: 
                                text: ''
                                color: 0,0,0,1
                                font_size: 0.025*app.width
                                markup: True
                                halign: "center"
                                valign: "top"
                                text_size: self.size
                                size: self.parent.size
                                pos:self.parent.pos
                                
                            BoxLayout: 
                                size_hint: (None,None)
                                height: dp(0.0833333333333*app.height)
                                width: dp(0.375*app.width)
                                padding:(0.0125*app.width,0,0.0125*app.width,0)
                                            
                                TextInput: 
                                    id: file_name
                                    valign: 'middle'
                                    halign: 'center'
                                    text_size: self.size
                                    font_size: str(0.025*app.width) + 'sp'
                                    markup: True
                                    multiline: False
                                    text: ''
                          
                        BoxLayout: 
                            size_hint: (None,None)
                            height: dp(0.35*app.height)
                            width: dp(0.375*app.width)
                            padding:(0.0825*app.width,0,0.0825*app.width,0)
                            Button:
                                font_size: str(0.01875 * app.width) + 'sp'
                                size_hint: (None,None)
                                height: dp(0.35*app.height)
                                width: dp(0.21*app.width)
                                on_press: root.save_file()
                                background_color: hex('#F4433600')
                                BoxLayout:
                                    padding: 0
                                    size: self.parent.size
                                    pos:self.parent.pos
                                    Image:
                                        id: save_image
                                        source: "./asmcnc/apps/shapeCutter_app/img/save_file.png"
                                        size: self.parent.size
                                        stretch: True
                        BoxLayout: 
                            size_hint: (None,None)
                            height: dp(0.0833333333333*app.height)
                            width: dp(0.375*app.width)
                            padding:(0,0,0,0)
                                        
                    BoxLayout: # document viewer
                        size_hint: (None,None)
                        height: dp(0.625*app.height)
                        width: dp(0.4375*app.width)
                        padding:(0,0,0,0)
                        ScrollView:
                            size_hint: (None, None)
                            size: self.parent.size
                            pos:self.parent.pos
                            do_scroll_x: True
                            do_scroll_y: True
                            scroll_type: ['content']
                            RstDocument:
                                text: root.display_profile
                                background_color: hex('#FFFFFF')                 
                BoxLayout: #action box
                    size_hint: (None,None)
                    height: dp(0.645833333333*app.height)
                    width: dp(0.15625*app.width)
                    padding:0,0,0,0.0708333333333*app.height
                    spacing: 0.0708333333333*app.height
                    orientation: "vertical"
                    
                    BoxLayout: 
                        size_hint: (None,None)
                        height: dp(0.139583333333*app.height)
                        width: dp(0.11*app.width)
                        padding:(0.03*app.width,0,0.03*app.width,0.0708333333333*app.height)
                        Button:
                            font_size: str(0.01875 * app.width) + 'sp'
                            id: info_button
                            size_hint: (None,None)
                            height: dp(0.0833333333333*app.height)
                            width: dp(0.05*app.width)
                            background_color: hex('#F4433600')
                            opacity: 0
                            on_press: root.get_info()
                            BoxLayout:
                                padding: 0
                                size: self.parent.size
                                pos:self.parent.pos
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
                        background_color: hex('#F4433600')
                        opacity: 0
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos:self.parent.pos
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
                        background_color: hex('#F4433600')
                        on_press: root.next_screen()
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos:self.parent.pos
                            Image:
                                source: "./asmcnc/apps/shapeCutter_app/img/arrow_next.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True               
                    
"""
    )


class ShapeCutterSaveJobScreenClass(Screen):
    info_button = ObjectProperty()
    user_instructions = ObjectProperty()
    display_profile = StringProperty()

    def __init__(self, **kwargs):
        super(ShapeCutterSaveJobScreenClass, self).__init__(**kwargs)
        self.shapecutter_sm = kwargs['shapecutter']
        self.m = kwargs['machine']
        self.j = kwargs['job_parameters']
        self.kb = kwargs['keyboard']
        self.text_inputs = [self.file_name]

    def on_touch(self):
        for text_input in self.text_inputs:
            text_input.focus = False

    def on_pre_enter(self):
        self.display_profile = self.j.parameters_to_string()
        self.file_name.text = str(self.j.profile_filename)
        self.save_image.source = (
            './asmcnc/apps/shapeCutter_app/img/save_file.png')

    def on_enter(self):
        self.kb.setup_text_inputs(self.text_inputs)

    def next_screen(self):
        self.shapecutter_sm.next_screen()

    def save_file(self):
        if not self.file_name.text == '':
            self.j.save_parameters(self.file_name.text)
            self.j.save_gCode()
            self.save_image.source = (
                './asmcnc/apps/shapeCutter_app/img/thumbs_up.png')
        else:
            description = """Filename input is empty.

Please enter a name for your parameter profile."""
            popup_input_error.PopupInputError(self.shapecutter_sm, description)
