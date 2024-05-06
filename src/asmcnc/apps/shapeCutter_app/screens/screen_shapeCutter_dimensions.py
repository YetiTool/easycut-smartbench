"""
Created on 4 March 2020
Dimensions Entry Screen for the Shape Cutter App

@author: Letty
"""
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.uix.textinput import TextInput
from kivy.uix.switch import Switch
from asmcnc.apps.shapeCutter_app.screens import popup_input_error
from asmcnc.core_UI import scaling_utils as utils
from asmcnc.core_UI.popups import WarningPopup

Builder.load_string(
    """

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
    
    on_touch_down: root.on_touch()

    BoxLayout:
        height: dp(1.66666666667*app.height)
        width: dp(0.6*app.width)
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
                height: dp(0.1875*app.height)
                width: dp(1.0*app.width)
                text: "Shape Cutter"
                font_size: 0.0375*app.width
                halign: "center"
                valign: "bottom"
                markup: True

            BoxLayout:
                size_hint: (None,None)
                width: dp(1.0*app.width)
                height: dp(0.114583333333*app.height)
                padding:[dp(0.1875)*app.width, 0, dp(0.1875)*app.width, 0]
                spacing: 0
                orientation: 'horizontal'
                pos: self.parent.pos

                Label:
                    color: color_provider.get_rgba("black")
                    font_size: 0.03*app.width
                    markup: True
                    halign: "center"
                    valign: "bottom"
                    text_size: self.size
                    size: self.parent.size
                    pos: self.parent.pos
                    text: "Please enter dimensions"

            BoxLayout: 
                size_hint: (None,None)
                width: dp(1.0*app.width)
                height: dp(0.6875*app.height)
                orientation: "horizontal"
                spacing: 0
                padding: 0

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(0.84375*app.width)
                    height: dp(0.697916666667*app.height)             
                    spacing: 0
                    padding: 0
                        
                    # Body
                    BoxLayout:
                        size_hint: (None,None)
                        width: dp(0.84375*app.width)
                        height: dp(0.6875*app.height)
                        padding:[dp(0.0075)*app.width, 0, dp(0.00875)*app.width, 0]
                        spacing: 0
                        orientation: 'horizontal'
                        pos: self.parent.pos
                        
                        # Text entry
                        BoxLayout:
                            id: text_entry_box
                            orientation: 'vertical'
                            size_hint: (None,None)
                            width: dp(0.245*app.width)
                            height: dp(0.6875*app.height)
                            padding:[0, 0, 0, dp(0.0625)*app.height]
                            spacing:0.0416666666667*app.height
                            pos: self.parent.pos
                            
                            # BL horizontal
                                # Toggle button
                            BoxLayout:
                                size_hint: (None,None)
                                height: dp(0.0666666666667*app.height)
                                width: dp(0.245*app.width)
                                padding:[dp(0.07)*app.width, 0, dp(0.0125)*app.width, 0]
                                orientation: "horizontal"
        
                                                              
                                BoxLayout: 
                                    size_hint: (None,None)
                                    height: dp(0.0666666666667*app.height)
                                    width: dp(0.15*app.width)
                                    padding:[dp(0.04625)*app.width, 0, 0, 0]
                               
                                    Switch:
                                        id: unit_toggle
                                        size_hint: (None,None)
                                        height: dp(0.0666666666667*app.height)
                                        width: dp(0.10375*app.width)
                                        background_color: color_provider.get_rgba("invisible")
                                        center: self.parent.center
                                        pos: self.parent.pos
                                        on_active: root.toggle_units()
                                        active_norm_pos: max(0., min(1., (int(self.active) + self.touch_distance / sp(0.05125*app.width))))
                                        canvas.after:
                                            Color:
                                                rgb: 1,1,1
                                            Rectangle:
                                                source: './asmcnc/apps/shapeCutter_app/img/slider_bg_mm.png' if unit_toggle.active else './asmcnc/apps/shapeCutter_app/img/slider_bg_inch.png' 
                                                # make or download your background jpg
                                                size: sp(0.10375*app.width), sp(0.0666666666667*app.height)
                                                pos: int(self.center_x - sp(0.05125*app.width)), int(self.center_y - sp(0.0333333333333*app.height))                        
                                         
                                            Rectangle:
                                                #id: switch_rectangle
                                                source: './asmcnc/apps/shapeCutter_app/img/slider_fg_inch.png' if unit_toggle.active else './asmcnc/apps/shapeCutter_app/img/slider_fg_mm.png'
                                                # make or download your slider jpg
                                                size: sp(0.05375*app.width), sp(0.0666666666667*app.height)
                                                pos: int(self.center_x - sp(0.05125*app.width) + self.active_norm_pos * sp(0.05125*app.width)), int(self.center_y - sp(0.0333333333333*app.height))
                                                       
                            # BL horizontal
                                # label + text entry
                            BoxLayout: #dimension 1
                                id: dimension_1
                                size_hint: (None,None)
                                height: dp(0.0833333333333*app.height)
                                width: dp(0.245*app.width)
                                padding:[dp(0.0375)*app.width, 0, dp(0.025)*app.width, 0]
                                orientation: "horizontal"
                                
                                Label: 
                                    text: root.dim_1
                                    color: color_provider.get_rgba("black")
                                    font_size: 0.03*app.width
                                    markup: True
                                    halign: "left"
                                    valign: "middle"
                                    text_size: self.size
                                    size: self.parent.size
                                    pos: self.parent.pos
                                                              
                                BoxLayout:
                                    id: dimesion_1_input_box
                                    size_hint: (None,None)
                                    height: dp(0.0833333333333*app.height)
                                    width: dp(0.15*app.width)
                                    padding:[dp(0.025)*app.width, 0, 0, 0]
                                                
                                    TextInput: 
                                        id: input_dim1
                                        valign: 'middle'
                                        halign: 'center'
                                        text_size: self.size
                                        font_size: str(0.025*app.width) + 'sp'
                                        markup: True
                                        input_filter: 'float'
                                        multiline: False
                                        text: ''

                            BoxLayout: #dimension 2
                                size_hint: (None,None)
                                height: dp(0.0833333333333*app.height)
                                width: dp(0.245*app.width)
                                padding:[dp(0.0375)*app.width, 0, dp(0.025)*app.width, 0]
                                orientation: "horizontal"
                                
                                Label: 
                                    text: root.dim_2
                                    color: color_provider.get_rgba("black")
                                    font_size: 0.03*app.width
                                    markup: True
                                    halign: "left"
                                    valign: "middle"
                                    text_size: self.size
                                    size: self.parent.size
                                    pos: self.parent.pos
                                                              
                                BoxLayout: 
                                    size_hint: (None,None)
                                    height: dp(0.0833333333333*app.height)
                                    width: dp(0.15*app.width)
                                    padding:[dp(0.025)*app.width, 0, 0, 0]
                                                
                                    TextInput: 
                                        id: input_dim2
                                        valign: 'middle'
                                        halign: 'center'
                                        text_size: self.size
                                        font_size: str(0.025*app.width) + 'sp'
                                        markup: True
                                        input_type: 'number'
                                        input_filter: 'float'
                                        multiline: False
                                        text: ''

                            BoxLayout: #dimension 3
                                size_hint: (None,None)
                                height: dp(0.0833333333333*app.height)
                                width: dp(0.245*app.width)
                                padding:[dp(0.0375)*app.width, 0, dp(0.025)*app.width, 0]
                                orientation: "horizontal"
                                
                                Label: 
                                    text: root.dim_3
                                    color: color_provider.get_rgba("black")
                                    font_size: 0.03*app.width
                                    markup: True
                                    halign: "left"
                                    valign: "middle"
                                    text_size: self.size
                                    size: self.parent.size
                                    pos: self.parent.pos
                                                              
                                BoxLayout: 
                                    size_hint: (None,None)
                                    height: dp(0.0833333333333*app.height)
                                    width: dp(0.15*app.width)
                                    padding:[dp(0.025)*app.width, 0, 0, 0]
                                                
                                    TextInput: 
                                        id: input_dim3
                                        valign: 'middle'
                                        halign: 'center'
                                        text_size: self.size
                                        font_size: str(0.025*app.width) + 'sp'
                                        markup: True
                                        input_filter: 'float'
                                        multiline: False
                                        text: ''
                                                                        
                            BoxLayout: #dimension 4
                                size_hint: (None,None)
                                height: dp(0.0833333333333*app.height)
                                width: dp(0.245*app.width)
                                padding:[dp(0.0375)*app.width, 0, dp(0.025)*app.width, 0]
                                orientation: "horizontal"
                                
                                Label: 
                                    text: root.dim_4
                                    color: color_provider.get_rgba("black")
                                    font_size: 0.03*app.width
                                    markup: True
                                    halign: "left"
                                    valign: "middle"
                                    text_size: self.size
                                    size: self.parent.size
                                    pos: self.parent.pos
                                                              
                                BoxLayout: 
                                    size_hint: (None,None)
                                    height: dp(0.0833333333333*app.height)
                                    width: dp(0.15*app.width)
                                    padding:[dp(0.025)*app.width, 0, 0, 0]
                                                
                                    TextInput: 
                                        id: input_dim4
                                        valign: 'top'
                                        halign: 'center'
                                        text_size: self.size
                                        font_size: str(0.025*app.width) + 'sp'
                                        markup: True
                                        input_filter: 'float'
                                        multiline: False
                                        text: ''

                        # Image
                        BoxLayout:
                            size_hint: (None,None)
                            width: dp(0.58*app.width)
                            height: dp(0.6875*app.height)
                            padding:[0, 0, 0, dp(0.0458333333333)*app.height]
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
                        width: dp(0.84375*app.width)
                        height: dp(0.00625*app.height)
                        padding: 0
                        spacing: 0
                        orientation: 'horizontal'
                        pos: self.parent.pos
                    
                BoxLayout: #action box
                    size_hint: (None,None)
                    height: dp(0.6875*app.height)
                    width: dp(0.15625*app.width)
                    padding:[0, dp(0.0416666666667)*app.height, dp(0.04625)*app.width, dp(0.0708333333333)*app.height]
                    spacing:0.0708333333333*app.height
                    orientation: "vertical"
                    
                    BoxLayout: 
                        size_hint: (None,None)
                        height: dp(0.139583333333*app.height)
                        width: dp(0.11*app.width)
                        padding:[dp(0.03)*app.width, 0, dp(0.03)*app.width, dp(0.0708333333333)*app.height]
                        Button:
                            font_size: str(0.01875 * app.width) + 'sp'
                            id: info_button
                            size_hint: (None,None)
                            height: dp(0.0833333333333*app.height)
                            width: dp(0.05*app.width)
                            background_color: color_provider.get_rgba("invisible")
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
                        font_size: str(0.01875 * app.width) + 'sp'
                        id: back_button
                        size_hint: (None,None)
                        height: dp(0.139583333333*app.height)
                        width: dp(0.11*app.width)
                        background_color: color_provider.get_rgba("invisible")
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
                        font_size: str(0.01875 * app.width) + 'sp'
                        size_hint: (None,None)
                        height: dp(0.139583333333*app.height)
                        width: dp(0.11*app.width)
                        background_color: color_provider.get_rgba("invisible")
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
    
                
                
"""
)


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
        self.shapecutter_sm = kwargs["shapecutter"]
        self.m = kwargs["machine"]
        self.j = kwargs["job_parameters"]
        self.kb = kwargs["keyboard"]
        # Add the IDs of ALL the TextInputs on this screen
        self.text_inputs = [
            self.input_dim1,
            self.input_dim2,
            self.input_dim3,
            self.input_dim4,
        ]

    def on_touch(self):
        for text_input in self.text_inputs:
            text_input.focus = False

    def on_pre_enter(self):
        self.info_button.opacity = 0
        if self.j.shape_dict["units"] == "mm":
            self.unit_toggle.active = False
        elif self.j.shape_dict["units"] == "inches":
            self.unit_toggle.active = True
        if self.j.shape_dict["shape"] == "circle":
            self.dimension_1.height = "0"
            self.dimesion_1_input_box.height = "0"
            self.text_entry_box.padding = 0, 0, 0, utils.get_scaled_width(70)
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
            if self.j.shape_dict["cut_type"] == "island":
                self.image_dims.source = (
                    "./asmcnc/apps/shapeCutter_app/img/dims_is_circ.png"
                )
            elif self.j.shape_dict["cut_type"] == "aperture":
                self.image_dims.source = (
                    "./asmcnc/apps/shapeCutter_app/img/dims_apt_circ.png"
                )
        elif self.j.shape_dict["shape"] == "rectangle":
            self.dimension_1.height = utils.get_scaled_width(40)
            self.dimesion_1_input_box.height = utils.get_scaled_width(40)
            self.text_entry_box.padding = 0, 0, 0, utils.get_scaled_width(30)
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
            if self.j.shape_dict["cut_type"] == "island":
                self.image_dims.source = (
                    "./asmcnc/apps/shapeCutter_app/img/dims_is_rect.png"
                )
            elif self.j.shape_dict["cut_type"] == "aperture":
                self.image_dims.source = (
                    "./asmcnc/apps/shapeCutter_app/img/dims_apt_rect.png"
                )

    def on_enter(self):
        self.kb.setup_text_inputs(self.text_inputs)

    def get_info(self):
        pass

    def go_back(self):
        self.shapecutter_sm.previous_screen()

    def next_screen(self):
        self.shapecutter_sm.next_screen()

    def toggle_units(self):
        if self.unit_toggle.active == True:
            self.j.shape_dict["units"] = "inches"
            if not self.input_dim1.text == "":
                self.input_dim1.text = "{:.2f}".format(
                    float(self.input_dim1.text) / 25.4
                )
            if not self.input_dim2.text == "":
                self.input_dim2.text = "{:.2f}".format(
                    float(self.input_dim2.text) / 25.4
                )
            if not self.input_dim3.text == "":
                self.input_dim3.text = "{:.2f}".format(
                    float(self.input_dim3.text) / 25.4
                )
            if not self.input_dim4.text == "":
                self.input_dim4.text = "{:.2f}".format(
                    float(self.input_dim4.text) / 25.4
                )
        elif self.unit_toggle.active == False:
            self.j.shape_dict["units"] = "mm"
            if not self.input_dim1.text == "":
                self.input_dim1.text = "{:.2f}".format(
                    float(self.input_dim1.text) * 25.4
                )
            if not self.input_dim2.text == "":
                self.input_dim2.text = "{:.2f}".format(
                    float(self.input_dim2.text) * 25.4
                )
            if not self.input_dim3.text == "":
                self.input_dim3.text = "{:.2f}".format(
                    float(self.input_dim3.text) * 25.4
                )
            if not self.input_dim4.text == "":
                self.input_dim4.text = "{:.2f}".format(
                    float(self.input_dim4.text) * 25.4
                )

    def check_dimensions(self):
        if self.unit_toggle.active == True:
            self.j.shape_dict["units"] = "inches"
        elif self.unit_toggle.active == False:
            self.j.shape_dict["units"] = "mm"
        units = self.j.shape_dict["units"]
        if self.j.shape_dict["shape"] == "rectangle":
            # if all fields are full
            if (
                not self.input_dim1.text == ""
                and not self.input_dim2.text == ""
                and not self.input_dim3.text == ""
                and not self.input_dim4.text == ""
            ):
                # save the dimensions
                input_dim_list = [
                    ("X", float(self.input_dim1.text)),
                    ("Y", float(self.input_dim2.text)),
                    ("Z", float(self.input_dim3.text)),
                    ("R", float(self.input_dim4.text)),
                ]
                for dim, input in input_dim_list:
                    setting = self.j.validate_shape_dimensions(dim, input)
                    if not setting == True:
                        description = (
                            dim
                            + " dimension isn't valid. \n\n"
                            + dim
                            + " value should be between 0 and "
                            + "{:.2f}".format(setting)
                            + " "
                            + units
                            + ".\n\n"
                            + "Please re-enter your dimensions."
                        )
                        WarningPopup(sm=self.shapecutter_sm, m=self.m, l=self.m.l,
                                    main_string=description,
                                    popup_width=400,
                                    popup_height=380,
                                    main_label_size_delta=40,
                                    button_layout_padding=[50,25,50,0],
                                    main_label_h_align='left',
                                    main_layout_padding=[50,20,50,20],
                                    main_label_padding=[20,20]).open()
                        return False
                self.next_screen()
            else:
                pass
        if self.j.shape_dict["shape"] == "circle":
            if not self.input_dim2.text == "" and not self.input_dim3.text == "":
                # save the dimensions
                input_dim_list = [
                    ("D", float(self.input_dim2.text)),
                    ("Z", float(self.input_dim3.text)),
                ]
                for dim, input in input_dim_list:
                    setting = self.j.validate_shape_dimensions(dim, input)
                    if not setting == True:
                        description = (
                            dim
                            + " dimension isn't valid. \n\n"
                            + dim
                            + " value should be between 0 and "
                            + "{:.2f}".format(setting)
                            + " "
                            + units
                            + ".\n\n"
                            + "Please re-enter your dimensions."
                        )
                        WarningPopup(sm=self.shapecutter_sm, m=self.m, l=self.m.l,
                                    main_string=description,
                                    popup_width=400,
                                    popup_height=380,
                                    main_label_size_delta=40,
                                    button_layout_padding=[50,25,50,0],
                                    main_label_h_align='left',
                                    main_layout_padding=[50,20,50,20],
                                    main_label_padding=[20,20]).open()
                        return False
                self.next_screen()
            else:
                pass
