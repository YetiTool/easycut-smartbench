'''
Created on 4 March 2020
Dimensions Entry Screen for the Shape Cutter App

@author: Letty
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.uix.textinput import TextInput
from kivy.uix.behaviors import FocusBehavior

Builder.load_string("""

<ShapeCutterDimensionsScreenClass>:

    image_dims: image_dims
    unit_toggle: unit_toggle
    unit_label: unit_label
    input_dim1: input_dim1
    input_dim2: input_dim2
    input_dim3: input_dim3
    input_dim4: input_dim4

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
            
            # Header
            Label:
                size_hint: (None,None)
                height: dp(90)
                width: dp(800)
                text: "Shape Cutter"
                font_size: 30
                halign: "center"
                valign: "bottom"
                markup: True

            # Body
            BoxLayout:
                size_hint: (None,None)
                width: dp(800)
                height: dp(330)
                padding: (80,0,34,0)
                spacing: 0
                orientation: 'horizontal'
                pos: self.parent.pos                
                
                # Text entry
                BoxLayout:
                    orientation: 'vertical'
                    size_hint: (None,None)
                    width: dp(220)
                    height: dp(330)
                    padding: (0,0,0,30)
                    spacing: 20
                    pos: self.parent.pos
                    
                    # BL horizontal
                        # Toggle button
                    BoxLayout:
                        size_hint: (None,None)
                        height: dp(30)
                        width: dp(220)
                        padding: (80,0,10,0)                   
                        orientation: "horizontal"

                                                      
                        BoxLayout: 
                            size_hint: (None,None)
                            height: dp(30)
                            width: dp(120)
                            padding: (45,0,0,0)
                                        
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
                                            source: "./asmcnc/apps/shapeCutter_app/img/mm_inches_toggle.png"  
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
                                               
                    # BL horizontal
                        # label + text entry
                    BoxLayout: #dimension 1
                        size_hint: (None,None)
                        height: dp(40)
                        width: dp(220)
                        padding: (30,0,20,0)                   
                        orientation: "horizontal"
                        
                        Label: 
                            text: root.dim_1
                            color: 0,0,0,1
                            font_size: 24
                            markup: True
                            halign: "left"
                            valign: "top"
                            text_size: self.size
                            size: self.parent.size
                            pos: self.parent.pos
                                                      
                        BoxLayout: 
                            size_hint: (None,None)
                            height: dp(40)
                            width: dp(120)
                            padding: (20,0,0,0)
                                        
                            TextInput: 
                                id: input_dim1
                                valign: 'middle'
                                halign: 'center'
                                text_size: self.size
                                font_size: '20sp'
                                markup: True
                                input_filter: 'float'
                                multiline: False
                                text: ''
                                on_text_validate: root.check_dimensions()
                    BoxLayout: #dimension 2
                        size_hint: (None,None)
                        height: dp(40)
                        width: dp(220)
                        padding: (30,0,20,0)                     
                        orientation: "horizontal"
                        
                        Label: 
                            text: root.dim_2
                            color: 0,0,0,1
                            font_size: 24
                            markup: True
                            halign: "left"
                            valign: "top"
                            text_size: self.size
                            size: self.parent.size
                            pos: self.parent.pos
                                                      
                        BoxLayout: 
                            size_hint: (None,None)
                            height: dp(40)
                            width: dp(120)
                            padding: (20,0,0,0)
                                        
                            TextInput: 
                                id: input_dim2
                                valign: 'middle'
                                halign: 'center'
                                text_size: self.size
                                font_size: '20sp'
                                markup: True
                                input_type: 'number'
                                input_filter: 'float'
                                multiline: False
                                text: ''
                                on_text_validate: root.check_dimensions()
                    BoxLayout: #dimension 3
                        size_hint: (None,None)
                        height: dp(40)
                        width: dp(220)
                        padding: (30,0,20,0)                     
                        orientation: "horizontal"
                        
                        Label: 
                            text: root.dim_3
                            color: 0,0,0,1
                            font_size: 24
                            markup: True
                            halign: "left"
                            valign: "top"
                            text_size: self.size
                            size: self.parent.size
                            pos: self.parent.pos
                                                      
                        BoxLayout: 
                            size_hint: (None,None)
                            height: dp(40)
                            width: dp(120)
                            padding: (20,0,0,0)
                                        
                            TextInput: 
                                id: input_dim3
                                valign: 'middle'
                                halign: 'center'
                                text_size: self.size
                                font_size: '20sp'
                                markup: True
                                input_filter: 'float'
                                multiline: False
                                text: ''
                                on_text_validate: root.check_dimensions()
                                                                
                    BoxLayout: #dimension 4
                        size_hint: (None,None)
                        height: dp(40)
                        width: dp(220)
                        padding: (30,0,20,0)                  
                        orientation: "horizontal"
                        
                        Label: 
                            text: root.dim_4
                            color: 0,0,0,1
                            font_size: 24
                            markup: True
                            halign: "left"
                            valign: "top"
                            text_size: self.size
                            size: self.parent.size
                            pos: self.parent.pos
                                                      
                        BoxLayout: 
                            size_hint: (None,None)
                            height: dp(40)
                            width: dp(120)
                            padding: (20,0,0,0)
                                        
                            TextInput: 
                                id: input_dim4
                                valign: 'top'
                                halign: 'center'
                                text_size: self.size
                                font_size: '20sp'
                                markup: True
                                input_filter: 'float'
                                multiline: False
                                text: ''
                                on_text_validate: root.check_dimensions()          
                # Image
                BoxLayout:
                    size_hint: (None,None)
                    width: dp(464)
                    height: dp(310)
                    padding: (0,0,0,0)
                    pos: self.parent.pos
                    
                    # image box
                    BoxLayout:
                        padding: 0
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            id: image_dims
                            source: "./asmcnc/apps/shapeCutter_app/img/is_rect.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True  
            BoxLayout:
                size_hint: (None,None)
                width: dp(800)
                height: dp(60)
                padding: (150,0,150,20)
                spacing: 0
                orientation: 'horizontal'
                pos: self.parent.pos
""")

class ShapeCutterDimensionsScreenClass(Screen):

    info_button = ObjectProperty()
    units = StringProperty("mm")
    dim_1 = StringProperty()
    dim_2 = StringProperty()
    dim_3 = StringProperty()
    dim_4 = StringProperty()

    
    def __init__(self, **kwargs):
        super(ShapeCutterDimensionsScreenClass, self).__init__(**kwargs)
        self.shapecutter_sm = kwargs['shapecutter']
        self.m=kwargs['machine']
        self.j=kwargs['job_parameters']
        
        
        
    def on_pre_enter(self):
        if self.j.shape_dict["shape"] == 'circle':            
            self.input_dim1.opacity = 0
            self.input_dim2.opacity = 1
            self.input_dim3.opacity = 1
            self.input_dim4.opacity = 0
            self.input_dim1.disabled = True
            self.input_dim2.disabled = False
            self.input_dim3.disabled = False
            self.input_dim4.disabled = True
            self.dim_1 = ""
            self.dim_2 = "D"
            self.dim_3 = "Z"
            self.dim_4 = ""
            
            self.j.shape_dict["dimensions"] = self.j.circle_dimensions
            
            if self.j.shape_dict["cut_type"] == 'island':
                self.image_dims.source = ("./asmcnc/apps/shapeCutter_app/img/dims_is_circ.png")
            
            elif self.j.shape_dict["cut_type"] == 'aperture':
                self.image_dims.source = ("./asmcnc/apps/shapeCutter_app/img/dims_apt_circ.png")
              
        elif self.j.shape_dict["shape"] == 'rectangle':
            self.input_dim1.opacity = 1
            self.input_dim2.opacity = 1
            self.input_dim3.opacity = 1
            self.input_dim4.opacity = 1
            self.input_dim1.disabled = False
            self.input_dim2.disabled = False
            self.input_dim3.disabled = False
            self.input_dim4.disabled = False
            self.dim_1 = "X"
            self.dim_2 = "Y"
            self.dim_3 = "R"
            self.dim_4 = "Z"

            self.j.shape_dict["dimensions"] = self.j.rectangle_dimensions 
            
            if self.j.shape_dict["cut_type"] == 'island':
                self.image_dims.source = ("./asmcnc/apps/shapeCutter_app/img/dims_is_rect.png")

            elif self.j.shape_dict["cut_type"] == 'aperture':
                self.image_dims.source = ("./asmcnc/apps/shapeCutter_app/img/dims_apt_rect.png")

      
    def toggle_units(self):
        if self.unit_toggle.state == 'normal':
            self.unit_label.text = "mm"
        elif self.unit_toggle.state == 'down': 
            self.unit_label.text = "inches"
    
    def check_dimensions(self):
        
        if self.j.shape_dict["shape"] == 'rectangle':
            
            # if all fields are full
            if not (self.input_dim1.text == "") and not (self.input_dim2.text == "") \
            and not (self.input_dim3.text == "") and not (self.input_dim4.text == ""):
            
                # save the dimensions
                self.j.shape_dict["dimensions"]["X"] = self.input_dim1.text
                self.j.shape_dict["dimensions"]["Y"] = self.input_dim2.text
                self.j.shape_dict["dimensions"]["Z"] = self.input_dim3.text
                self.j.shape_dict["dimensions"]["R"] = self.input_dim4.text
                
                self.next_screen()
            else:
                pass
            
        if self.j.shape_dict["shape"] == 'circle':
            if not (self.input_dim2.text == "") and not (self.input_dim3.text == ""):            # save the dimensions
                # save the dimensions
                self.j.shape_dict["dimensions"]["D"] = self.input_dim2.text
                self.j.shape_dict["dimensions"]["Z"] = self.input_dim3.text
                
                self.next_screen()
            else:
                pass

    def next_screen(self):
        self.shapecutter_sm.prepare_tab()