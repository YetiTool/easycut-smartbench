'''
Created on 4 March 2020
Feedback Screen for the Shape Cutter App

@author: Letty
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty

from asmcnc.apps.shapeCutter_app.screens import popup_input_error

Builder.load_string("""

<ShapeCutterSaveJobScreenClass>:
    
    save_image: save_image
    file_name: file_name
    cut_time_text: cut_time_text
    
    BoxLayout:
        height: dp(800)
        width: dp(480)
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
                height: dp(90)
                width: dp(800)
                text: "Would you like to save this as a new profile?"
                font_size: 30
                halign: "center"
                valign: "bottom"
                markup: True

            BoxLayout: #Body
                size_hint: (None,None)
                height: dp(390)
                width: dp(800)
                padding: 0,20,0,0
                orientation: "horizontal"
                
                BoxLayout: #text box
                    size_hint: (None,None)
                    height: dp(390)
                    width: dp(675)
                    padding: 10,0,25,10
                    orientation: "horizontal"
                    BoxLayout: # file save
                        size_hint: (None,None)
                        height: dp(380)
                        width: dp(300)
                        padding: (0,50,0,0) 
                        orientation: "vertical"
                        spacing: 20 
                        BoxLayout: 
                            size_hint: (None,None)
                            height: dp(100)
                            width: dp(300)
                            padding: (0,0,0,0)
                            orientation: "vertical"
                            spacing:20

                            Label: 
                                id: cut_time_text
                                text: ''
                                color: 0,0,0,1
                                font_size: 20
                                markup: True
                                halign: "center"
                                valign: "top"
                                text_size: self.size
                                size: self.parent.size
                                pos: self.parent.pos
                                
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
                                        stretch: True
                        BoxLayout: 
                            size_hint: (None,None)
                            height: dp(40)
                            width: dp(300)
                            padding: (0,0,0,0)                                           
                                        
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
                        size_hint: (None,None)
                        height: dp(67)
                        width: dp(88)
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
                    
""")

class ShapeCutterSaveJobScreenClass(Screen):

    info_button = ObjectProperty()   
    user_instructions = ObjectProperty()
    display_profile = StringProperty()
    
    def __init__(self, **kwargs):
        super(ShapeCutterSaveJobScreenClass, self).__init__(**kwargs)
        self.shapecutter_sm = kwargs['shapecutter']
        self.m=kwargs['machine']
        self.j=kwargs['job_parameters']
        
    def on_pre_enter(self):
        self.display_profile = self.j.parameters_to_string()
        self.file_name.text = ''
        self.save_image.source = './asmcnc/apps/shapeCutter_app/img/save_file.png'

    def on_enter(self):
        self.cut_time_text = self.shapecutter_sm.sm.get_screen('jobdone').jobdone_text

    def next_screen(self):
        self.shapecutter_sm.next_screen()

    def save_file(self):
        if not self.file_name.text == '':
            self.j.save_parameters(self.file_name.text)
            self.j.save_gCode()            
            self.save_image.source = './asmcnc/apps/shapeCutter_app/img/thumbs_up.png'

        else: 
            
            description = "Filename input is empty.\n\nPlease enter a name for your parameter profile."
            popup_input_error.PopupInputError(self.shapecutter_sm, description)