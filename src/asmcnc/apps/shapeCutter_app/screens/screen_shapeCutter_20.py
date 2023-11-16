"""
Created on 20 February 2020
Screen 22 for the Shape Cutter App

@author: Letty
"""
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import MetricsBase
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.switch import Switch
from asmcnc.apps.shapeCutter_app.screens import popup_info
from asmcnc.apps.shapeCutter_app.screens import popup_input_error

Builder.load_string(
    """

<ShapeCutter20ScreenClass>

    info_button: info_button
    unit_toggle: unit_toggle
    # unit_label: unit_label
    a_dimension: a_dimension
    b_dimension: b_dimension
    c_dimension: c_dimension
    
    on_touch_down: root.on_touch()

    BoxLayout:
        size_hint: (None,None)
        width: dp(1.0*app.width)
        height: dp(1.0*app.height)
        padding: 0
        spacing: 0
        orientation: "vertical"

        BoxLayout:
            size_hint: (None,None)
            width: dp(1.0*app.width)
            height: dp(0.1875*app.height)
            padding: 0
            spacing: 0
            orientation: "horizontal"

            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint: (None,None)
                height: dp(0.1875*app.height)
                width: dp(0.1775*app.width)
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
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint: (None,None)
                height: dp(0.1875*app.height)
                width: dp(0.1775*app.width)
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
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint: (None,None)
                height: dp(0.1875*app.height)
                width: dp(0.1775*app.width)
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
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint: (None,None)
                height: dp(0.1875*app.height)
                width: dp(0.1775*app.width)
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
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint: (None,None)
                height: dp(0.1875*app.height)
                width: dp(0.1775*app.width)
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
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint: (None,None)
                height: dp(0.1875*app.height)
                width: dp(0.1125*app.width)
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
            height: dp(0.8125*app.height)
            width: dp(1.0*app.width)
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
                    height: dp(0.125*app.height)
                    width: dp(1.0*app.width)
                    padding:[dp(0.025)*app.width, 0, 0, 0]
                    orientation: "horizontal"
                    
                    BoxLayout: #Screen number
                        size_hint: (None,None)
                        padding: 0
                        height: dp(0.0833333333333*app.height)
                        width: dp(0.05*app.width)
                        canvas:
                            Rectangle: 
                                pos: self.pos
                                size: self.size
                                source: "./asmcnc/apps/shapeCutter_app/img/number_box.png"
                        Label:
                            text: root.screen_number
                            valign: "middle"
                            halign: "center"
                            font_size: 0.0325*app.width
                            markup: True
                                
                                
                        
                    BoxLayout: #Title
                        size_hint: (None,None)
                        height: dp(0.125*app.height)
                        width: dp(0.925*app.width)
                        padding:[dp(0.025)*app.width, dp(0.0416666666667)*app.height, 0, 0]
                        
                        Label:
                            text: root.title_label
                            color: 0,0,0,1
                            font_size: 0.035*app.width
                            markup: True
                            halign: "left"
                            valign: "bottom"
                            text_size: self.size
                            size: self.parent.size
                            pos: self.parent.pos
                        
                    
                BoxLayout: #Body
                    size_hint: (None,None)
                    height: dp(0.6875*app.height)
                    width: dp(1.0*app.width)
                    padding:[0, dp(0.0416666666667)*app.height, 0, 0]
                    orientation: "horizontal"
                    
                    BoxLayout: #text box
                        size_hint: (None,None)
                        height: dp(0.645833333333*app.height)
                        width: dp(0.84375*app.width)
                        padding:[dp(0.1)*app.width, 0, 0, 0]
                        orientation: "vertical"
                    
                        BoxLayout: #text box
                            size_hint: (None,None)
                            height: dp(0.114583333333*app.height)
                            width: dp(0.84375*app.width)
                            padding:[dp(0.1)*app.width, 0, 0, 0]
                            orientation: "vertical"                       

                        BoxLayout: #image & text entry box
                            size_hint: (None,None)
                            height: dp(0.53125*app.height)
                            width: dp(0.71875*app.width)
                            padding:[0, 0, 0, dp(0.04375)*app.height]
                            orientation: "horizontal"
                                    
                            BoxLayout:
                                orientation: 'vertical'
                                size_hint: (None,None)
                                width: dp(0.40625*app.width)
                                height: dp(0.53125*app.height)
                                padding:[0, 0, 0, dp(0.1875)*app.height]
                                spacing:0.0416666666667*app.height
                                pos: self.parent.pos
                                
                                # BL horizontal
                                    # Toggle button
                                BoxLayout:
                                    size_hint: (None,None)
                                    height: dp(0.0666666666667*app.height)
                                    width: dp(0.40625*app.width)
                                    padding:[dp(0.27875)*app.width, 0, dp(0.025)*app.width, 0]
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
                                        height: dp(0.0666666666667*app.height)
                                        width: dp(0.10375*app.width)
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
                                BoxLayout: #dimension 1
                                    size_hint: (None,None)
                                    height: dp(0.0729166666667*app.height)
                                    width: dp(0.40625*app.width)
                                    padding:[0, 0, dp(0.025)*app.width, 0]
                                    orientation: "horizontal"
                                    
                                    Label: 
                                        text: "Diameter (A):"
                                        color: 0,0,0,1
                                        font_size: 0.03*app.width
                                        markup: True
                                        halign: "left"
                                        valign: "middle"
                                        text_size: self.size
                                        size: self.parent.size
                                        pos: self.parent.pos
                                                                  
                                    BoxLayout: 
                                        size_hint: (None,None)
                                        height: dp(0.0729166666667*app.height)
                                        width: dp(0.1125*app.width)
                                        padding:[dp(0.0125)*app.width, 0, 0, 0]
                                                    
                                        TextInput: 
                                            id: a_dimension
                                            valign: 'top'
                                            halign: 'center'
                                            text_size: self.size
                                            font_size: str(0.025*app.width) + 'sp'
                                            markup: True
                                            input_filter: 'float'
                                            multiline: False
                                            text: ''                           
                                
                                BoxLayout: #dimension 2
                                    size_hint: (None,None)
                                    height: dp(0.0729166666667*app.height)
                                    width: dp(0.40625*app.width)
                                    padding:[0, 0, dp(0.025)*app.width, 0]
                                    orientation: "horizontal"
                                    
                                    Label: 
                                        text: "Cutting length (B):"
                                        color: 0,0,0,1
                                        font_size: 0.03*app.width
                                        markup: True
                                        halign: "left"
                                        valign: "middle"
                                        text_size: self.size
                                        size: self.parent.size
                                        pos: self.parent.pos
                                                                  
                                    BoxLayout: 
                                        size_hint: (None,None)
                                        height: dp(0.0729166666667*app.height)
                                        width: dp(0.1125*app.width)
                                        padding:[dp(0.0125)*app.width, 0, 0, 0]
                                                    
                                        TextInput: 
                                            id: b_dimension
                                            valign: 'top'
                                            halign: 'center'
                                            text_size: self.size
                                            font_size: str(0.025*app.width) + 'sp'
                                            markup: True
                                            input_filter: 'float'
                                            multiline: False
                                            text: ''
                           
                                BoxLayout: #dimension 3
                                    size_hint: (None,None)
                                    height: dp(0.0729166666667*app.height)
                                    width: dp(0.40625*app.width)
                                    padding:[0, 0, dp(0.025)*app.width, 0]
                                    orientation: "horizontal"
                                    
                                    Label: 
                                        text: "Shoulder length (C):"
                                        color: 0,0,0,1
                                        font_size: 0.03*app.width
                                        markup: True
                                        halign: "left"
                                        valign: "middle"
                                        text_size: self.size
                                        size: self.parent.size
                                        pos: self.parent.pos
                                                                  
                                    BoxLayout: 
                                        size_hint: (None,None)
                                        height: dp(0.0729166666667*app.height)
                                        width: dp(0.1125*app.width)
                                        padding:[dp(0.0125)*app.width, 0, 0, 0]
                                                    
                                        TextInput: 
                                            id: c_dimension
                                            valign: 'top'
                                            halign: 'center'
                                            text_size: self.size
                                            font_size: str(0.025*app.width) + 'sp'
                                            markup: True
                                            input_filter: 'float'
                                            multiline: False
                                            text: ''                           
                            BoxLayout: #image box
                                size_hint: (None,None)
                                height: dp(0.564583333333*app.height)
                                width: dp(0.3125*app.width)
                                padding:[dp(0.05625)*app.width, 0, dp(0.03125)*app.width, dp(0.0395833333333)*app.height]
                                Image:
                                    source: "./asmcnc/apps/shapeCutter_app/img/dims_cutter.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True                           

                                
                        
                                        

                    BoxLayout: #action box
                        size_hint: (None,None)
                        height: dp(0.645833333333*app.height)
                        width: dp(0.15625*app.width)
                        padding:[0, 0, 0, dp(0.0708333333333)*app.height]
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
                            font_size: str(0.01875 * app.width) + 'sp'
                            size_hint: (None,None)
                            height: dp(0.139583333333*app.height)
                            width: dp(0.11*app.width)
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
                            font_size: str(0.01875 * app.width) + 'sp'
                            size_hint: (None,None)
                            height: dp(0.139583333333*app.height)
                            width: dp(0.11*app.width)
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


class ShapeCutter20ScreenClass(Screen):
    info_button = ObjectProperty()
    screen_number = StringProperty("[b]20[/b]")
    title_label = StringProperty("[b]Check the dimensions of your cutter[/b]")
    user_instructions = StringProperty("")

    def __init__(self, **kwargs):
        super(ShapeCutter20ScreenClass, self).__init__(**kwargs)
        self.shapecutter_sm = kwargs["shapecutter"]
        self.m = kwargs["machine"]
        self.j = kwargs["job_parameters"]
        self.kb = kwargs["keyboard"]
        self.text_inputs = [self.a_dimension, self.b_dimension, self.c_dimension]

    def on_touch(self):
        for text_input in self.text_inputs:
            text_input.focus = False

    def on_pre_enter(self):
        self.info_button.opacity = 1
        self.a_dimension.text = "{:.2f}".format(
            float(self.j.parameter_dict["cutter dimensions"]["diameter"])
        )
        self.b_dimension.text = "{:.2f}".format(
            float(self.j.parameter_dict["cutter dimensions"]["cutting length"])
        )
        self.c_dimension.text = "{:.2f}".format(
            float(self.j.parameter_dict["cutter dimensions"]["shoulder length"])
        )
        if self.j.parameter_dict["cutter dimensions"]["units"] == "mm":
            self.unit_toggle.active = False
        elif self.j.parameter_dict["cutter dimensions"]["units"] == "inches":
            self.unit_toggle.active = True

    def on_enter(self):
        self.kb.setup_text_inputs(self.text_inputs)

    def get_info(self):
        info = """To maintain accuracy, it is important that you measure the dimensions of your cutter.

 The shoulder length must be equal or larger than the cutting length."""
        popup_info.PopupInfo(self.shapecutter_sm, info)

    def go_back(self):
        self.shapecutter_sm.previous_screen()

    def next_screen(self):
        self.check_dimensions()

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

    def toggle_units(self):
        if self.unit_toggle.active == True:
            self.j.parameter_dict["cutter dimensions"]["units"] = "inches"
            if not self.a_dimension.text == "":
                self.a_dimension.text = "{:.2f}".format(
                    float(self.a_dimension.text) / 25.4
                )
            if not self.b_dimension.text == "":
                self.b_dimension.text = "{:.2f}".format(
                    float(self.b_dimension.text) / 25.4
                )
            if not self.c_dimension.text == "":
                self.c_dimension.text = "{:.2f}".format(
                    float(self.c_dimension.text) / 25.4
                )
        elif self.unit_toggle.active == False:
            self.j.parameter_dict["cutter dimensions"]["units"] = "mm"
            if not self.a_dimension.text == "":
                self.a_dimension.text = "{:.2f}".format(
                    float(self.a_dimension.text) * 25.4
                )
            if not self.b_dimension.text == "":
                self.b_dimension.text = "{:.2f}".format(
                    float(self.b_dimension.text) * 25.4
                )
            if not self.c_dimension.text == "":
                self.c_dimension.text = "{:.2f}".format(
                    float(self.c_dimension.text) * 25.4
                )

    def check_dimensions(self):
        if (
            not self.a_dimension.text == ""
            and not self.b_dimension.text == ""
            and not self.c_dimension.text == ""
        ):
            if self.unit_toggle.active == True:
                self.j.parameter_dict["cutter dimensions"]["units"] = "inches"
            elif self.unit_toggle.active == False:
                self.j.parameter_dict["cutter dimensions"]["units"] = "mm"
            units = self.j.parameter_dict["cutter dimensions"]["units"]
            input_dim_list = [
                ("diameter", float(self.a_dimension.text)),
                ("cutting length", float(self.b_dimension.text)),
                ("shoulder length", float(self.c_dimension.text)),
            ]
            for dim, input in input_dim_list:
                setting = self.j.validate_cutter_dimensions(dim, input)
                if not setting == True:
                    if dim == "shoulder length":
                        description = (
                            "The "
                            + dim
                            + " input isn't valid.\n\n"
                            + "The shoulder length should be greater"
                            + """ than the cutting length, and the Z dimension.

"""
                            + "Please re-enter your parameters."
                        )
                    elif dim == "cutting length":
                        description = (
                            "The "
                            + dim
                            + " input isn't valid.\n\nThe "
                            + dim
                            + " value should be greater than "
                            + "{:.2f}".format(setting)
                            + " "
                            + units
                            + ".\n\n"
                            + "Please re-enter your parameters."
                        )
                    elif dim == "diameter":
                        description = (
                            "The "
                            + dim
                            + " input isn't valid.\n\nThe "
                            + dim
                            + " value should be greater than 0 "
                            + "and less than "
                            + "{:.2f}".format(setting)
                            + " "
                            + units
                            + ".\n\n"
                            + "Please re-enter your parameters."
                        )
                    popup_input_error.PopupInputError(self.shapecutter_sm, description)
                    return False
            self.shapecutter_sm.next_screen()
        else:
            pass
