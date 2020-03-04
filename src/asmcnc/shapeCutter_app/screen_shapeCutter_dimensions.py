'''
Created on 4 March 2020
Dimensions Entry Screen for the Shape Cutter App

@author: Letty
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.uix.textinput import TextInput


Builder.load_string("""

<ShapeCutterDimensionsScreenClass>:

    image_dims: image_dims
    unit_toggle: unit_toggle
    unit_label: unit_label
    x_dimension: x_dimension
    y_dimension: y_dimension
    z_dimension: z_dimension
    r_dimension: r_dimension

    BoxLayout:
        height: dp(800)
        width: dp(480)
        canvas:
            Rectangle: 
                pos: self.pos
                size: self.size
                source: "./asmcnc/shapeCutter_app/img/landing_background.png"

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
                   
#                     
#             BoxLayout:
#                 size_hint: (None,None)
#                 width: dp(800)
#                 height: dp(50)
#                 padding: 0
#                 spacing: 0
#                 Label:
#                     size_hint: (None,None)
#                     height: dp(100)
#                     width: dp(800)
#                     halign: "center"
#                     valign: "middle"
#                     text: "Enter dimensions"
#                     color: 0,0,0,1
#                     font_size: 26
#                     markup: True

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
                    padding: (0,0,0,50)
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
                                            source: "./asmcnc/shapeCutter_app/img/mm_inches_toggle.png"  
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
                        height: dp(30)
                        width: dp(220)
                        padding: (30,0,20,0)                   
                        orientation: "horizontal"
                        
                        Label: 
                            text: "X"
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
                            height: dp(30)
                            width: dp(120)
                            padding: (20,0,0,0)
                                        
                            TextInput: 
                                id: x_dimension
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
                        height: dp(30)
                        width: dp(220)
                        padding: (30,0,20,0)                     
                        orientation: "horizontal"
                        
                        Label: 
                            text: "Y"
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
                            height: dp(30)
                            width: dp(120)
                            padding: (20,0,0,0)
                                        
                            TextInput: 
                                id: y_dimension
                                valign: 'middle'
                                halign: 'center'
                                text_size: self.size
                                font_size: '20sp'
                                markup: True
                                input_filter: 'float'
                                multiline: False
                                text: ''
                                on_text_validate: root.check_dimensions()
                    BoxLayout: #dimension 3
                        size_hint: (None,None)
                        height: dp(30)
                        width: dp(220)
                        padding: (30,0,20,0)                     
                        orientation: "horizontal"
                        
                        Label: 
                            text: "Z"
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
                            height: dp(30)
                            width: dp(120)
                            padding: (20,0,0,0)
                                        
                            TextInput: 
                                id: z_dimension
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
                        height: dp(30)
                        width: dp(220)
                        padding: (30,0,20,0)                  
                        orientation: "horizontal"
                        
                        Label: 
                            text: "r"
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
                            height: dp(30)
                            width: dp(120)
                            padding: (20,0,0,0)
                                        
                            TextInput: 
                                id: r_dimension
                                valign: 'middle'
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
                            source: "./asmcnc/shapeCutter_app/img/is_rect.png"
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
    #X_dimension = ObjectProperty()
    units = StringProperty("mm")
    shape = 'rectangle'
    cut_type = 'island'
    
    def __init__(self, **kwargs):
        super(ShapeCutterDimensionsScreenClass, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        
    def on_pre_enter(self):
        if self.shape == 'circle' and self.cut_type == 'island':
            self.image_dims.source = ("./asmcnc/shapeCutter_app/img/dims_is_circ.png")
            
            # pick dimensions for each shape (only some are relevant)
        
        elif self.shape == 'rectangle' and self.cut_type == 'island':
            self.image_dims.source = ("./asmcnc/shapeCutter_app/img/dims_is_rect.png")
            
        elif self.shape == 'circle' and self.cut_type == 'aperture':
            self.image_dims.source = ("./asmcnc/shapeCutter_app/img/dims_apt_circ.png")
        
        elif self.shape == 'rectangle' and self.cut_type == 'aperture':
            self.image_dims.source = ("./asmcnc/shapeCutter_app/img/dims_apt_rect.png")

      
    def toggle_units(self):
        if self.unit_toggle.state == 'normal':
            self.unit_label.text = "mm"
        elif self.unit_toggle.state == 'down': 
            self.unit_label.text = "inches"
    
    def check_dimensions(self):
        
        if not (self.x_dimension.text == "") and not (self.y_dimension.text == "") \
        and not (self.z_dimension.text == "") and not (self.r_dimension.text == ""):
            # save the dimensions
            self.next_screen()     
        else:
            pass        
        
        
            
    def next_screen(self):
        self.sm.current = 'sC1'