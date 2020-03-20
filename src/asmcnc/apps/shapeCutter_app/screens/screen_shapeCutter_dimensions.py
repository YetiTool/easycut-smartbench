'''
Created on 4 March 2020
Dimensions Entry Screen for the Shape Cutter App

@author: Letty
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.uix.textinput import TextInput
from kivy.uix.switch import Switch

from asmcnc.apps.shapeCutter_app.screens import popup_input_error

Builder.load_string("""

<ShapeCutterDimensionsScreenClass>:

    image_dims: image_dims
    unit_toggle: unit_toggle
    #unit_label: unit_label
    
    dimension_1: dimension_1
    dimesion_1_input_box: dimesion_1_input_box
    text_entry_box: text_entry_box
    
    input_dim1: input_dim1
    input_dim2: input_dim2
    input_dim3: input_dim3
    input_dim4: input_dim4
    
    back_button:back_button
    info_button:info_button
    #switch_rectangle:switch_rectangle

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

            BoxLayout:
                size_hint: (None,None)
                width: dp(800)
                height: dp(55)
                padding: (150,0,150,0)
                spacing: 0
                orientation: 'horizontal'
                pos: self.parent.pos

                Label:
                    color: 0,0,0,1
                    font_size: 24
                    markup: True
                    halign: "center"
                    valign: "bottom"
                    text_size: self.size
                    size: self.parent.size
                    pos: self.parent.pos
                    text: "Please enter dimensions"

            BoxLayout: 
                size_hint: (None,None)
                width: dp(800)
                height: dp(330)
                orientation: "horizontal"
                spacing: 0
                padding: 0

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(675)
                    height: dp(335)             
                    spacing: 0
                    padding: 0
                        
                    # Body
                    BoxLayout:
                        size_hint: (None,None)
                        width: dp(675)
                        height: dp(330)
                        padding: (6,0,7,0)
                        spacing: 0
                        orientation: 'horizontal'
                        pos: self.parent.pos
                        
                        # Text entry
                        BoxLayout:
                            id: text_entry_box
                            orientation: 'vertical'
                            size_hint: (None,None)
                            width: dp(196)
                            height: dp(330)
                            padding: (0,0,0,30)
                            spacing: 20
                            pos: self.parent.pos
                            
                            # BL horizontal
                                # Toggle button
                            BoxLayout:
                                size_hint: (None,None)
                                height: dp(32)
                                width: dp(196)
                                padding: (56,0,10,0)                   
                                orientation: "horizontal"
        
                                                              
                                BoxLayout: 
                                    size_hint: (None,None)
                                    height: dp(32)
                                    width: dp(120)
                                    padding: (37,0,0,0)
                               
                                    Switch:
                                        id: unit_toggle
                                        size_hint: (None,None)
                                        height: dp(32)
                                        width: dp(83)
                                        background_color: hex('#F4433600')
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
                                                       
                            # BL horizontal
                                # label + text entry
                            BoxLayout: #dimension 1
                                id: dimension_1
                                size_hint: (None,None)
                                height: dp(40)
                                width: dp(196)
                                padding: (30,0,20,0)                   
                                orientation: "horizontal"
                                
                                Label: 
                                    text: root.dim_1
                                    color: 0,0,0,1
                                    font_size: 24
                                    markup: True
                                    halign: "left"
                                    valign: "middle"
                                    text_size: self.size
                                    size: self.parent.size
                                    pos: self.parent.pos
                                                              
                                BoxLayout:
                                    id: dimesion_1_input_box
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

                            BoxLayout: #dimension 2
                                size_hint: (None,None)
                                height: dp(40)
                                width: dp(196)
                                padding: (30,0,20,0)                     
                                orientation: "horizontal"
                                
                                Label: 
                                    text: root.dim_2
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

                            BoxLayout: #dimension 3
                                size_hint: (None,None)
                                height: dp(40)
                                width: dp(196)
                                padding: (30,0,20,0)                     
                                orientation: "horizontal"
                                
                                Label: 
                                    text: root.dim_3
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
                                                                        
                            BoxLayout: #dimension 4
                                size_hint: (None,None)
                                height: dp(40)
                                width: dp(196)
                                padding: (30,0,20,0)                  
                                orientation: "horizontal"
                                
                                Label: 
                                    text: root.dim_4
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

                        # Image
                        BoxLayout:
                            size_hint: (None,None)
                            width: dp(464)
                            height: dp(330)
                            padding: (0,0,0,22)
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
                        width: dp(675)
                        height: dp(3)
                        padding: 0
                        spacing: 0
                        orientation: 'horizontal'
                        pos: self.parent.pos
                    
                BoxLayout: #action box
                    size_hint: (None,None)
                    height: dp(330)
                    width: dp(125)
                    padding: 0,20,37,34
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
                        id: back_button
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
                        on_press: root.check_dimensions()
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

class ShapeCutterDimensionsScreenClass(Screen):

    info_button = ObjectProperty()
    back_button = ObjectProperty()
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
        self.info_button.opacity = 0
        
        if self.j.shape_dict["units"] == 'mm':
            self.unit_toggle.active = False
        elif self.j.shape_dict["units"] == 'inches':
            self.unit_toggle.active = True
       
        if self.j.shape_dict["shape"] == 'circle':
            
            self.dimension_1.height = '0'
            self.dimesion_1_input_box.height = '0'
            self.text_entry_box.padding = (0,0,0,70)
            
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
            
            self.dimension_1.height = '40'
            self.dimesion_1_input_box.height = '40'
            self.text_entry_box.padding = (0,0,0,30)
            
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
            self.dim_3 = "Z"
            self.dim_4 = "R"

            self.j.shape_dict["dimensions"] = self.j.rectangle_dimensions 
            
            if self.j.shape_dict["cut_type"] == 'island':
                self.image_dims.source = ("./asmcnc/apps/shapeCutter_app/img/dims_is_rect.png")

            elif self.j.shape_dict["cut_type"] == 'aperture':
                self.image_dims.source = ("./asmcnc/apps/shapeCutter_app/img/dims_apt_rect.png")

    def get_info(self):
        pass
    
    def go_back(self):
        self.shapecutter_sm.previous_screen()
    
    def next_screen(self):
        self.shapecutter_sm.next_screen()
      
    def toggle_units(self):       
        if self.unit_toggle.active == True:
            self.j.shape_dict["units"] = "inches"
            
            if not (self.input_dim1.text == ""): self.input_dim1.text = "{:.2f}".format(float(self.input_dim1.text) / 25.4)
            if not (self.input_dim2.text == ""): self.input_dim2.text = "{:.2f}".format(float(self.input_dim2.text) / 25.4)
            if not (self.input_dim3.text == ""): self.input_dim3.text = "{:.2f}".format(float(self.input_dim3.text) / 25.4)
            if not (self.input_dim4.text == ""): self.input_dim4.text = "{:.2f}".format(float(self.input_dim4.text) / 25.4)
        elif self.unit_toggle.active == False:
            self.j.shape_dict["units"] = "mm"
            
            if not (self.input_dim1.text == ""): self.input_dim1.text = "{:.2f}".format(float(self.input_dim1.text) * 25.4)
            if not (self.input_dim2.text == ""): self.input_dim2.text = "{:.2f}".format(float(self.input_dim2.text) * 25.4)
            if not (self.input_dim3.text == ""): self.input_dim3.text = "{:.2f}".format(float(self.input_dim3.text) * 25.4)
            if not (self.input_dim4.text == ""): self.input_dim4.text = "{:.2f}".format(float(self.input_dim4.text) * 25.4)

    def check_dimensions(self):    

        if self.unit_toggle.active == True:
            self.j.shape_dict["units"] = "inches"

        elif self.unit_toggle.active == False:
            self.j.shape_dict["units"] = "mm"
        
        units = self.j.shape_dict["units"]
        
        if self.j.shape_dict["shape"] == 'rectangle':
            
            # if all fields are full
            if not (self.input_dim1.text == "") and not (self.input_dim2.text == "") \
            and not (self.input_dim3.text == "") and not (self.input_dim4.text == ""):
            
                # save the dimensions
                input_dim_list = [("X", float(self.input_dim1.text)),
                                  ("Y", float(self.input_dim2.text)),
                                  ("Z", float(self.input_dim3.text)),
                                  ("R", float(self.input_dim4.text))]
                
                for (dim, input) in input_dim_list:
                    setting = self.j.validate_shape_dimensions(dim, input)
                    if not setting == True:
                        description = dim + " dimension isn't valid. \n\n" + \
                                    dim + " value should be between 0 and " + "{:.2f}".format(setting) + " " + units + ".\n\n" \
                                    + "Please re-enter your dimensions."
                        
                        popup_input_error.PopupInputError(self.shapecutter_sm, description)
                        return False
                
                self.next_screen()
            else:
                pass
            
        if self.j.shape_dict["shape"] == 'circle':
            if not (self.input_dim2.text == "") and not (self.input_dim3.text == ""):            # save the dimensions
                                    
                # save the dimensions
                input_dim_list = [("D", float(self.input_dim2.text)),
                                  ("Z", float(self.input_dim3.text))]
                
                for (dim, input) in input_dim_list:
                    setting = self.j.validate_shape_dimensions(dim, input)
                    if not setting == True:
                        description = dim + " dimension isn't valid. \n\n" + \
                                    dim + " value should be between 0 and " + "{:.2f}".format(setting) + " " + units + ".\n\n" \
                                    + "Please re-enter your dimensions."
                        
                        popup_input_error.PopupInputError(self.shapecutter_sm, description)
                        return False
                
                self.next_screen()
            else:
                pass
