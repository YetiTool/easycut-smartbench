"""
Created on 4 March 2020
Feedback Screen for the Shape Cutter App

@author: Letty
"""
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from asmcnc.apps.shapeCutter_app.screens import popup_input_error
from asmcnc.core_UI.popups import WarningPopup

Builder.load_string(
    """

<ShapeCutterSaveJobScreenClass>:
    
    save_image: save_image
    file_name: file_name
    
    on_touch_down: root.on_touch()
    
    BoxLayout:
        height: dp(app.get_scaled_height(800))
        width: dp(app.get_scaled_width(480))
        canvas:
            Rectangle: 
                pos: self.pos
                size: self.size
                source: "./asmcnc/apps/shapeCutter_app/img/landing_background.png"

        BoxLayout:
            padding: 0
            spacing: 0
            orientation: "vertical"       
                
            Label:
                color: 1,1,1,1
                size_hint: (None,None)
                height: dp(app.get_scaled_height(90))
                width: dp(app.get_scaled_width(800))
                text: "Would you like to save this as a new profile?"
                font_size: 0.0375*app.width
                halign: "center"
                valign: "bottom"
                markup: True

            BoxLayout: #Body
                size_hint: (None,None)
                height: dp(app.get_scaled_height(390))
                width: dp(app.get_scaled_width(800))
                padding:[0, app.get_scaled_height(20), 0, 0]
                orientation: "horizontal"
                
                BoxLayout: #text box
                    size_hint: (None,None)
                    height: dp(app.get_scaled_height(390))
                    width: dp(app.get_scaled_width(675))
                    padding:[app.get_scaled_width(10), 0, app.get_scaled_width(10), app.get_scaled_height(10)]
                    orientation: "horizontal"
                    BoxLayout: # file save
                        size_hint: (None,None)
                        height: dp(app.get_scaled_height(380))
                        width: dp(app.get_scaled_width(300))
                        padding:[0, app.get_scaled_height(50), 0, 0]
                        orientation: "vertical"
                        spacing:0.0416666666667*app.height
                        BoxLayout: 
                            size_hint: (None,None)
                            height: dp(app.get_scaled_height(100))
                            width: dp(app.get_scaled_width(300))
                            padding:[0, 0, 0, 0]
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
                                pos: self.parent.pos
                                
                            BoxLayout: 
                                size_hint: (None,None)
                                height: dp(app.get_scaled_height(40))
                                width: dp(app.get_scaled_width(300))
                                padding:[app.get_scaled_width(10), 0, app.get_scaled_width(10), 0]
                                            
                                TextInput: 
                                    id: file_name
                                    valign: 'middle'
                                    halign: 'center'
                                    text_size: self.size
                                    font_size: str(get_scaled_width(20)) + 'sp'
                                    markup: True
                                    multiline: False
                                    text: ''
                          
                        BoxLayout: 
                            size_hint: (None,None)
                            height: dp(app.get_scaled_height(168))
                            width: dp(app.get_scaled_width(300))
                            padding:[app.get_scaled_width(66), 0, app.get_scaled_width(66), 0]
                            Button:
                                font_size: str(get_scaled_width(15)) + 'sp'
                                size_hint: (None,None)
                                height: dp(app.get_scaled_height(168))
                                width: dp(app.get_scaled_width(168))
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
                            height: dp(app.get_scaled_height(40))
                            width: dp(app.get_scaled_width(300))
                            padding:[0, 0, 0, 0]
                                        
                    BoxLayout: # document viewer
                        size_hint: (None,None)
                        height: dp(app.get_scaled_height(300))
                        width: dp(app.get_scaled_width(350))
                        padding:[0, 0, 0, 0]
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
                                base_font_size: str(get_scaled_width(24800)) + 'sp'
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
                            opacity: 0
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
                        opacity: 0
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


class ShapeCutterSaveJobScreenClass(Screen):
    info_button = ObjectProperty()
    user_instructions = ObjectProperty()
    display_profile = StringProperty()

    def __init__(self, **kwargs):
        super(ShapeCutterSaveJobScreenClass, self).__init__(**kwargs)
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
        self.display_profile = self.j.parameters_to_string()
        self.file_name.text = str(self.j.profile_filename)
        self.save_image.source = "./asmcnc/apps/shapeCutter_app/img/save_file.png"

    def on_enter(self):
        self.kb.setup_text_inputs(self.text_inputs)

    def next_screen(self):
        self.shapecutter_sm.next_screen()

    def save_file(self):
        if not self.file_name.text == "":
            self.j.save_parameters(self.file_name.text)
            self.j.save_gCode()
            self.save_image.source = "./asmcnc/apps/shapeCutter_app/img/thumbs_up.png"
        else:
            description = """Filename input is empty.

Please enter a name for your parameter profile."""
            WarningPopup(sm=self.shapecutter_sm, m=self.m, l=self.m.l,
                            main_string=description,
                            popup_width=400,
                            popup_height=380,
                            main_label_size_delta=40,
                            button_layout_padding=[50,25,50,0],
                            main_label_h_align='left',
                            main_layout_padding=[50,20,50,20],
                            main_label_padding=[20,20]).open()
