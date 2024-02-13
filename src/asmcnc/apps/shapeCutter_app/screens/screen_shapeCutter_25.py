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
from asmcnc.core_UI.popups import WarningPopup

Builder.load_string(
    """

<ShapeCutter25ScreenClass>

    info_button: info_button
    file_name: file_name
    save_image: save_image
    
    on_touch_down: root.on_touch()

    BoxLayout:
        size_hint: (None,None)
        width: dp(app.get_scaled_width(800))
        height: dp(app.get_scaled_height(480))
        padding:dp(0)
        spacing: 0
        orientation: "vertical"

        BoxLayout:
            size_hint: (None,None)
            width: dp(app.get_scaled_width(800))
            height: dp(app.get_scaled_height(90))
            padding:dp(0)
            spacing: 0
            orientation: "horizontal"

            Button:
                font_size: str(get_scaled_width(15)) + 'sp'
                size_hint: (None,None)
                height: dp(app.get_scaled_height(90))
                width: dp(app.get_scaled_width(142))
                on_press: root.prepare()
                BoxLayout:
                    padding:dp(0)
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
                    padding:dp(0)
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/apps/shapeCutter_app/img/load_tab_blue.png"
                        size: self.parent.size
                        allow_stretch: True
            Button:
                font_size: str(get_scaled_width(15)) + 'sp'
                size_hint: (None,None)
                height: dp(app.get_scaled_height(90))
                width: dp(app.get_scaled_width(142))
                on_press: root.define()
                BoxLayout:
                    padding:dp(0)
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/apps/shapeCutter_app/img/define_job_tab_grey.png"
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
                    padding:dp(0)
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
                    padding:dp(0)
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
                    padding:dp(0)
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
            padding:dp(0)
            height: dp(app.get_scaled_height(390))
            width: dp(app.get_scaled_width(800))
            canvas:
                Rectangle: 
                    pos: self.pos
                    size: self.size
                    source: "./asmcnc/apps/shapeCutter_app/img/background.png"
            
            BoxLayout:
                orientation: "vertical"
                padding:dp(0)
                spacing: 0
                    
                BoxLayout: #Header
                    size_hint: (None,None)
                    height: dp(app.get_scaled_height(60))
                    width: dp(app.get_scaled_width(800))
                    padding:(dp(app.get_scaled_width(20)),dp(0),dp(0),dp(0))
                    orientation: "horizontal"
                    
                    BoxLayout: #Screen number
                        size_hint: (None,None)
                        padding:dp(0)
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
                            font_size:dp(0.0325*app.width)
                            markup: True
                                
                                
                        
                    BoxLayout: #Title
                        size_hint: (None,None)
                        height: dp(app.get_scaled_height(60))
                        width: dp(app.get_scaled_width(740))
                        padding:(dp(app.get_scaled_width(20)),dp(app.get_scaled_height(20)),dp(0),dp(0))
                        
                        Label:
                            text: root.title_label
                            color: 0,0,0,1
                            font_size:dp(0.035*app.width)
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
                    padding:(dp(0),dp(app.get_scaled_height(20)),dp(0),dp(0))
                    orientation: "horizontal"
                    
                    BoxLayout: #text box
                        size_hint: (None,None)
                        height: dp(app.get_scaled_height(310))
                        width: dp(app.get_scaled_width(675))
                        padding:(dp(app.get_scaled_width(10)),dp(0),dp(app.get_scaled_width(10)),dp(app.get_scaled_height(10)))
                        orientation: "horizontal"
                        BoxLayout: # file save
                            size_hint: (None,None)
                            height: dp(app.get_scaled_height(300))
                            width: dp(app.get_scaled_width(300))
                            padding:(dp(0),dp(0),dp(0),dp(0))
                            orientation: "vertical"       
                            BoxLayout: 
                                size_hint: (None,None)
                                height: dp(app.get_scaled_height(70))
                                width: dp(app.get_scaled_width(300))
                                padding:(dp(0),dp(0),dp(0),dp(app.get_scaled_height(5)))
                                orientation: "vertical"

#                                 Label: 
#                                     text: ""
#                                     color: 0,0,0,1
#                                     font_size:dp(20)
#                                     markup: True
#                                     halign: "center"
#                                     valign: "top"
#                                     text_size: self.size
#                                     size: self.parent.size
#                                     pos: self.parent.pos
                                    
                                BoxLayout: 
                                    size_hint: (None,None)
                                    height: dp(app.get_scaled_height(40))
                                    width: dp(app.get_scaled_width(300))
                                    padding:(dp(app.get_scaled_width(10)),dp(0),dp(app.get_scaled_width(10)),dp(0))
                                                
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
                                padding:(dp(app.get_scaled_width(66)),dp(0),dp(app.get_scaled_width(66)),dp(0))
                                Button:
                                    font_size: str(get_scaled_width(15)) + 'sp'
                                    size_hint: (None,None)
                                    height: dp(app.get_scaled_height(168))
                                    width: dp(app.get_scaled_width(168))
                                    on_press: root.save_file()
                                    background_color: hex('#F4433600')
                                    BoxLayout:
                                        padding:dp(0)
                                        size: self.parent.size
                                        pos: self.parent.pos
                                        Image:
                                            id: save_image
                                            source: "./asmcnc/apps/shapeCutter_app/img/save_file.png"
                                            size: self.parent.size
                                            allow_stretch: True
                            BoxLayout: 
                                size_hint: (None,None)
                                height: dp(app.get_scaled_height(62))
                                width: dp(app.get_scaled_width(300))
                                padding:(dp(0),dp(0),dp(0),dp(0))
                                Label: 
                                    text: "You can save this profile later after the job too. "
                                    color: 0,0,0,1
                                    font_size:dp(0.025*app.width)
                                    markup: True
                                    halign: "center"
                                    valign: "middle"
                                    text_size: self.size
                                    size: self.parent.size
                                    pos: self.parent.pos                                            
                                            
                        BoxLayout: # document viewer
                            size_hint: (None,None)
                            height: dp(app.get_scaled_height(300))
                            width: dp(app.get_scaled_width(350))
                            padding:(dp(0),dp(0),dp(0),dp(0))
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
                        padding:(dp(0),dp(0),dp(0),dp(app.get_scaled_height(34)))
                        spacing:0.0708333333333*app.height
                        orientation: "vertical"
                        
                        BoxLayout: 
                            size_hint: (None,None)
                            height: dp(app.get_scaled_height(67))
                            width: dp(app.get_scaled_width(88))
                            padding:(dp(app.get_scaled_width(24)),dp(0),dp(app.get_scaled_width(24)),dp(app.get_scaled_height(34)))
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
                                    padding:dp(0)
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
                                padding:dp(0)
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
                                padding:dp(0)
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
