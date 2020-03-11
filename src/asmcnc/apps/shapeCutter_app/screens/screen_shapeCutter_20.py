'''
Created on 20 February 2020
Screen 22 for the Shape Cutter App

@author: Letty
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import MetricsBase
from kivy.properties import StringProperty, ObjectProperty

Builder.load_string("""

<ShapeCutter20ScreenClass>

    info_button: info_button
    unit_toggle: unit_toggle
    # unit_label: unit_label
    a_dimension: a_dimension
    b_dimension: b_dimension
    c_dimension: c_dimension

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
                        source: "./asmcnc/apps/shapeCutter_app/img/load_tab_blue.png"
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
                        padding: 80,0,0,0
                        orientation: "vertical"
                    
                        BoxLayout: #text box
                            size_hint: (None,None)
                            height: dp(55)
                            width: dp(675)
                            padding: 80,0,0,0
                            orientation: "vertical"                       

                        BoxLayout: #image & text entry box
                            size_hint: (None,None)
                            height: dp(255)
                            width: dp(575)
                            padding:0,0,0,21
                            orientation: "horizontal"
                                    
                            BoxLayout:
                                orientation: 'vertical'
                                size_hint: (None,None)
                                width: dp(325)
                                height: dp(255)
                                padding: (0,0,0,90)
                                spacing: 20
                                pos: self.parent.pos
                                
                                # BL horizontal
                                    # Toggle button
                                BoxLayout:
                                    size_hint: (None,None)
                                    height: dp(32)
                                    width: dp(325)
                                    padding: (223,0,20,0)                   
                                    orientation: "horizontal"
                                                    
#                                     ToggleButton:
#                                         id: unit_toggle
#                                         size_hint: (None,None)
#                                         height: dp(30)
#                                         width: dp(75)
#                                         background_color: hex('#F4433600')
#                                         center: self.parent.center
#                                         pos: self.parent.pos
#                                         on_press: root.toggle_units()
#         
#                                         BoxLayout:
#                                             height: dp(30)
#                                             width: dp(75)
#                                             canvas:
#                                                 Rectangle: 
#                                                     pos: self.parent.pos
#                                                     size: self.parent.size
#                                                     source: "./asmcnc/apps/shapeCutter_app/img/mm_inches_toggle.png"  
#                                         Label:
#                                             id: unit_label
#                                             text: "mm"
#                                             color: 1,1,1,1
#                                             font_size: 20
#                                             markup: True
#                                             halign: "center"
#                                             valign: "middle"
#                                             text_size: self.size
#                                             size: self.parent.size
#                                             pos: self.parent.pos                       
                                    Switch:
                                        id: unit_toggle
                                        size_hint: (None,None)
                                        height: dp(32)
                                        width: dp(83)
                                        # background_color: hex('#F4433600')
                                        center: self.parent.center
                                        pos: self.parent.pos
                                        on_active: root.toggle_units()
                                        active_norm_pos: max(0., min(1., (int(self.active) + self.touch_distance / sp(41))))
                                        canvas.after:
                                            Color:
                                                rgb: 1,1,1
                                            Rectangle:
                                                source: './asmcnc/apps/shapeCutter_app/img/slider_bg_mm.png' if unit_toggle.active else './asmcnc/apps/shapeCutter_app/img/slider_bg_inch.png' 
                                                # make or download your background jpg
                                                size: sp(83), sp(32)
                                                pos: int(self.center_x - sp(41)), int(self.center_y - sp(16))                        
                                         
                                            Rectangle:
                                                #id: switch_rectangle
                                                source: './asmcnc/apps/shapeCutter_app/img/slider_fg_inch.png' if unit_toggle.active else './asmcnc/apps/shapeCutter_app/img/slider_fg_mm.png'
                                                # make or download your slider jpg
                                                size: sp(43), sp(32)
                                                pos: int(self.center_x - sp(41) + self.active_norm_pos * sp(41)), int(self.center_y - sp(16))                           
                                BoxLayout: #dimension 1
                                    size_hint: (None,None)
                                    height: dp(35)
                                    width: dp(325)
                                    padding: (0,0,20,0)                   
                                    orientation: "horizontal"
                                    
                                    Label: 
                                        text: "Diameter (A):"
                                        color: 0,0,0,1
                                        font_size: 24
                                        markup: True
                                        halign: "left"
                                        valign: "middle"
                                        text_size: self.size
                                        size: self.parent.size
                                        pos: self.parent.pos
                                                                  
                                    BoxLayout: 
                                        size_hint: (None,None)
                                        height: dp(35)
                                        width: dp(90)
                                        padding: (10,0,0,0)
                                                    
                                        TextInput: 
                                            id: a_dimension
                                            valign: 'top'
                                            halign: 'center'
                                            text_size: self.size
                                            font_size: '20sp'
                                            markup: True
                                            input_filter: 'float'
                                            multiline: False
                                            text: ''                           
                                
                                BoxLayout: #dimension 2
                                    size_hint: (None,None)
                                    height: dp(35)
                                    width: dp(325)
                                    padding: (0,0,20,0)                   
                                    orientation: "horizontal"
                                    
                                    Label: 
                                        text: "Cutting length (B):"
                                        color: 0,0,0,1
                                        font_size: 24
                                        markup: True
                                        halign: "left"
                                        valign: "middle"
                                        text_size: self.size
                                        size: self.parent.size
                                        pos: self.parent.pos
                                                                  
                                    BoxLayout: 
                                        size_hint: (None,None)
                                        height: dp(35)
                                        width: dp(90)
                                        padding: (10,0,0,0)
                                                    
                                        TextInput: 
                                            id: b_dimension
                                            valign: 'top'
                                            halign: 'center'
                                            text_size: self.size
                                            font_size: '20sp'
                                            markup: True
                                            input_filter: 'float'
                                            multiline: False
                                            text: ''
                           
                                BoxLayout: #dimension 3
                                    size_hint: (None,None)
                                    height: dp(35)
                                    width: dp(325)
                                    padding: (0,0,20,0)                   
                                    orientation: "horizontal"
                                    
                                    Label: 
                                        text: "Shoulder length (C):"
                                        color: 0,0,0,1
                                        font_size: 24
                                        markup: True
                                        halign: "left"
                                        valign: "middle"
                                        text_size: self.size
                                        size: self.parent.size
                                        pos: self.parent.pos
                                                                  
                                    BoxLayout: 
                                        size_hint: (None,None)
                                        height: dp(35)
                                        width: dp(90)
                                        padding: (10,0,0,0)
                                                    
                                        TextInput: 
                                            id: c_dimension
                                            valign: 'top'
                                            halign: 'center'
                                            text_size: self.size
                                            font_size: '20sp'
                                            markup: True
                                            input_filter: 'float'
                                            multiline: False
                                            text: ''                           
                            BoxLayout: #image box
                                size_hint: (None,None)
                                height: dp(271)
                                width: dp(250)
                                padding: 45,0,25,19                          
                                Image:
                                    source: "./asmcnc/apps/shapeCutter_app/img/dims_cutter.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True                           

                                
                        
                                        

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

""")

class ShapeCutter20ScreenClass(Screen):
    
    info_button = ObjectProperty()
    
    screen_number = StringProperty("[b]20[/b]")
    title_label = StringProperty("[b]Check the dimensions of your cutter[/b]")
    user_instructions = StringProperty("")
    
    def __init__(self, **kwargs):
        super(ShapeCutter20ScreenClass, self).__init__(**kwargs)
        self.shapecutter_sm = kwargs['shapecutter']
        self.m=kwargs['machine']
        self.j=kwargs['job_parameters']

    def on_pre_enter(self):
        self.info_button.opacity = 1
        self.a_dimension.text = self.j.parameter_dict["cutter dimensions"]["diameter"]
        self.b_dimension.text = self.j.parameter_dict["cutter dimensions"]["cutting length"]
        self.c_dimension.text = self.j.parameter_dict["cutter dimensions"]["shoulder length"]
        # self.unit_label.text = self.j.parameter_dict["cutter dimensions"]["units"]
        if self.j.parameter_dict["cutter dimensions"]["units"] == "mm":
            self.unit_toggle.active = False
        elif self.j.parameter_dict["cutter dimensions"]["units"] == "inches":
            self.unit_toggle.active = True


# Action buttons       
    def get_info(self):
        pass
    
    def go_back(self):
        self.shapecutter_sm.previous_screen()
    
    def next_screen(self):
        self.check_dimensions()
    
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
#     def toggle_units(self):
#         if self.unit_toggle.state == 'normal':
#             self.unit_label.text = "mm"
#             self.j.parameter_dict["cutter dimensions"]["units"] = self.unit_label.text
#         elif self.unit_toggle.state == 'down': 
#             self.unit_label.text = "inches"
#             self.j.parameter_dict["cutter dimensions"]["units"] = self.unit_label.text

    def toggle_units(self):       
        if self.unit_toggle.active == True:
            print "inches"
            self.j.parameter_dict["cutter dimensions"]["units"] = "inches"

        elif self.unit_toggle.active == False: 
            print "mm"
            self.j.parameter_dict["cutter dimensions"]["units"] = "mm"

    def check_dimensions(self):        
        if not self.a_dimension.text == "" and not self.b_dimension.text == "" \
        and not self.c_dimension.text == "":
            self.j.parameter_dict["cutter dimensions"]["diameter"] = self.a_dimension.text
            self.j.parameter_dict["cutter dimensions"]["cutting length"] = self.b_dimension.text
            self.j.parameter_dict["cutter dimensions"]["shoulder length"] = self.c_dimension.text
            
            if self.unit_toggle.active == True:
                print "inches"
                self.j.parameter_dict["cutter dimensions"]["units"] = "inches"
    
            elif self.unit_toggle.active == False: 
                print "mm"
                self.j.parameter_dict["cutter dimensions"]["units"] = "mm"
            
            self.shapecutter_sm.next_screen()
        else:
            pass
 
        