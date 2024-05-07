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
from asmcnc.core_UI.popups import InfoPopup, WarningPopup

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
        width: app.get_scaled_width(800.0)
        height: app.get_scaled_height(480.0)
        padding: 0
        spacing: 0
        orientation: "vertical"

        BoxLayout:
            size_hint: (None,None)
            width: app.get_scaled_width(800.0)
            height: app.get_scaled_height(90.0)
            padding: 0
            spacing: 0
            orientation: "horizontal"

            Button:
                font_size: app.get_scaled_sp('15.0sp')
                size_hint: (None,None)
                height: app.get_scaled_height(90.0)
                width: app.get_scaled_width(142.0)
                on_press: root.prepare()
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/apps/shapeCutter_app/img/prepare_tab_blue.png"
                        size: self.parent.size
                        allow_stretch: True
            Button:
                font_size: app.get_scaled_sp('15.0sp')
                size_hint: (None,None)
                height: app.get_scaled_height(90.0)
                width: app.get_scaled_width(142.0)
                on_press: root.load()
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/apps/shapeCutter_app/img/load_tab_blue.png"
                        size: self.parent.size
                        allow_stretch: True
            Button:
                font_size: app.get_scaled_sp('15.0sp')
                size_hint: (None,None)
                height: app.get_scaled_height(90.0)
                width: app.get_scaled_width(142.0)
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
                font_size: app.get_scaled_sp('15.0sp')
                size_hint: (None,None)
                height: app.get_scaled_height(90.0)
                width: app.get_scaled_width(142.0)
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
                font_size: app.get_scaled_sp('15.0sp')
                size_hint: (None,None)
                height: app.get_scaled_height(90.0)
                width: app.get_scaled_width(142.0)
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
                font_size: app.get_scaled_sp('15.0sp')
                size_hint: (None,None)
                height: app.get_scaled_height(90.0)
                width: app.get_scaled_width(90.0)
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
            height: app.get_scaled_height(390.0)
            width: app.get_scaled_width(800.0)
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
                    height: app.get_scaled_height(60.0)
                    width: app.get_scaled_width(800.0)
                    padding: app.get_scaled_tuple([20.0, 0.0, 0.0, 0.0])
                    orientation: "horizontal"
                    
                    BoxLayout: #Screen number
                        size_hint: (None,None)
                        padding: 0
                        height: app.get_scaled_height(40.0)
                        width: app.get_scaled_width(40.0)
                        canvas:
                            Rectangle: 
                                pos: self.pos
                                size: self.size
                                source: "./asmcnc/apps/shapeCutter_app/img/number_box.png"
                        Label:
                            text: root.screen_number
                            valign: "middle"
                            halign: "center"
                            font_size: app.get_scaled_width(26.0)
                            markup: True
                                
                                
                        
                    BoxLayout: #Title
                        size_hint: (None,None)
                        height: app.get_scaled_height(60.0)
                        width: app.get_scaled_width(740.0)
                        padding: app.get_scaled_tuple([20.0, 20.0, 0.0, 0.0])
                        
                        Label:
                            text: root.title_label
                            color: 0,0,0,1
                            font_size: app.get_scaled_width(28.0)
                            markup: True
                            halign: "left"
                            valign: "bottom"
                            text_size: self.size
                            size: self.parent.size
                            pos: self.parent.pos
                        
                    
                BoxLayout: #Body
                    size_hint: (None,None)
                    height: app.get_scaled_height(330.0)
                    width: app.get_scaled_width(800.0)
                    padding: app.get_scaled_tuple([0.0, 20.0, 0.0, 0.0])
                    orientation: "horizontal"
                    
                    BoxLayout: #text box
                        size_hint: (None,None)
                        height: app.get_scaled_height(310.0)
                        width: app.get_scaled_width(675.0)
                        padding: app.get_scaled_tuple([80.0, 0.0, 0.0, 0.0])
                        orientation: "vertical"
                    
                        BoxLayout: #text box
                            size_hint: (None,None)
                            height: app.get_scaled_height(55.0)
                            width: app.get_scaled_width(675.0)
                            padding: app.get_scaled_tuple([80.0, 0.0, 0.0, 0.0])
                            orientation: "vertical"                       

                        BoxLayout: #image & text entry box
                            size_hint: (None,None)
                            height: app.get_scaled_height(255.0)
                            width: app.get_scaled_width(575.0)
                            padding: app.get_scaled_tuple([0.0, 0.0, 0.0, 21.0])
                            orientation: "horizontal"
                                    
                            BoxLayout:
                                orientation: 'vertical'
                                size_hint: (None,None)
                                width: app.get_scaled_width(325.0)
                                height: app.get_scaled_height(255.0)
                                padding: app.get_scaled_tuple([0.0, 0.0, 0.0, 90.0])
                                spacing: app.get_scaled_width(20.0)
                                pos: self.parent.pos
                                
                                # BL horizontal
                                    # Toggle button
                                BoxLayout:
                                    size_hint: (None,None)
                                    height: app.get_scaled_height(32.0)
                                    width: app.get_scaled_width(325.0)
                                    padding: app.get_scaled_tuple([223.0, 0.0, 20.0, 0.0])
                                    orientation: "horizontal"
                                                    
#                                     ToggleButton:
#                                         id: unit_toggle
#                                         size_hint: (None,None)
#                                         height: app.get_scaled_height(30.0)
#                                         width: app.get_scaled_width(75.0)
#                                         background_color: hex('#F4433600')
#                                         center: self.parent.center
#                                         pos: self.parent.pos
#                                         on_press: root.toggle_units()
#         
#                                         BoxLayout:
#                                             height: app.get_scaled_height(30.0)
#                                             width: app.get_scaled_width(75.0)
#                                             canvas:
#                                                 Rectangle: 
#                                                     pos: self.parent.pos
#                                                     size: self.parent.size
#                                                     source: "./asmcnc/apps/shapeCutter_app/img/mm_inches_toggle.png"  
#                                         Label:
#                                             id: unit_label
#                                             text: "mm"
#                                             color: 1,1,1,1
#                                             font_size: app.get_scaled_width(20.0)
#                                             markup: True
#                                             halign: "center"
#                                             valign: "middle"
#                                             text_size: self.size
#                                             size: self.parent.size
#                                             pos: self.parent.pos                       
                                    Switch:
                                        id: unit_toggle
                                        size_hint: (None,None)
                                        height: app.get_scaled_height(32.0)
                                        width: app.get_scaled_width(83.0)
                                        background_color: hex('#F4433600')
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
                                BoxLayout: #dimension 1
                                    size_hint: (None,None)
                                    height: app.get_scaled_height(35.0)
                                    width: app.get_scaled_width(325.0)
                                    padding: app.get_scaled_tuple([0.0, 0.0, 20.0, 0.0])
                                    orientation: "horizontal"
                                    
                                    Label: 
                                        text: "Diameter (A):"
                                        color: 0,0,0,1
                                        font_size: app.get_scaled_width(24.0)
                                        markup: True
                                        halign: "left"
                                        valign: "middle"
                                        text_size: self.size
                                        size: self.parent.size
                                        pos: self.parent.pos
                                                                  
                                    BoxLayout: 
                                        size_hint: (None,None)
                                        height: app.get_scaled_height(35.0)
                                        width: app.get_scaled_width(90.0)
                                        padding: app.get_scaled_tuple([10.0, 0.0, 0.0, 0.0])
                                                    
                                        TextInput: 
                                            id: a_dimension
                                            valign: 'top'
                                            halign: 'center'
                                            text_size: self.size
                                            font_size: app.get_scaled_sp('20.0sp')
                                            markup: True
                                            input_filter: 'float'
                                            multiline: False
                                            text: ''                           
                                
                                BoxLayout: #dimension 2
                                    size_hint: (None,None)
                                    height: app.get_scaled_height(35.0)
                                    width: app.get_scaled_width(325.0)
                                    padding: app.get_scaled_tuple([0.0, 0.0, 20.0, 0.0])
                                    orientation: "horizontal"
                                    
                                    Label: 
                                        text: "Cutting length (B):"
                                        color: 0,0,0,1
                                        font_size: app.get_scaled_width(24.0)
                                        markup: True
                                        halign: "left"
                                        valign: "middle"
                                        text_size: self.size
                                        size: self.parent.size
                                        pos: self.parent.pos
                                                                  
                                    BoxLayout: 
                                        size_hint: (None,None)
                                        height: app.get_scaled_height(35.0)
                                        width: app.get_scaled_width(90.0)
                                        padding: app.get_scaled_tuple([10.0, 0.0, 0.0, 0.0])
                                                    
                                        TextInput: 
                                            id: b_dimension
                                            valign: 'top'
                                            halign: 'center'
                                            text_size: self.size
                                            font_size: app.get_scaled_sp('20.0sp')
                                            markup: True
                                            input_filter: 'float'
                                            multiline: False
                                            text: ''
                           
                                BoxLayout: #dimension 3
                                    size_hint: (None,None)
                                    height: app.get_scaled_height(35.0)
                                    width: app.get_scaled_width(325.0)
                                    padding: app.get_scaled_tuple([0.0, 0.0, 20.0, 0.0])
                                    orientation: "horizontal"
                                    
                                    Label: 
                                        text: "Shoulder length (C):"
                                        color: 0,0,0,1
                                        font_size: app.get_scaled_width(24.0)
                                        markup: True
                                        halign: "left"
                                        valign: "middle"
                                        text_size: self.size
                                        size: self.parent.size
                                        pos: self.parent.pos
                                                                  
                                    BoxLayout: 
                                        size_hint: (None,None)
                                        height: app.get_scaled_height(35.0)
                                        width: app.get_scaled_width(90.0)
                                        padding: app.get_scaled_tuple([10.0, 0.0, 0.0, 0.0])
                                                    
                                        TextInput: 
                                            id: c_dimension
                                            valign: 'top'
                                            halign: 'center'
                                            text_size: self.size
                                            font_size: app.get_scaled_sp('20.0sp')
                                            markup: True
                                            input_filter: 'float'
                                            multiline: False
                                            text: ''                           
                            BoxLayout: #image box
                                size_hint: (None,None)
                                height: app.get_scaled_height(271.0)
                                width: app.get_scaled_width(250.0)
                                padding: app.get_scaled_tuple([45.0, 0.0, 25.0, 19.0])
                                Image:
                                    source: "./asmcnc/apps/shapeCutter_app/img/dims_cutter.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True                           

                                
                        
                                        

                    BoxLayout: #action box
                        size_hint: (None,None)
                        height: app.get_scaled_height(310.0)
                        width: app.get_scaled_width(125.0)
                        padding: app.get_scaled_tuple([0.0, 0.0, 0.0, 34.0])
                        spacing: app.get_scaled_width(34.0)
                        orientation: "vertical"
                        
                        BoxLayout: 
                            size_hint: (None,None)
                            height: app.get_scaled_height(67.0)
                            width: app.get_scaled_width(88.0)
                            padding: app.get_scaled_tuple([24.0, 0.0, 24.0, 34.0])
                            Button:
                                font_size: app.get_scaled_sp('15.0sp')
                                id: info_button
                                size_hint: (None,None)
                                height: app.get_scaled_height(40.0)
                                width: app.get_scaled_width(40.0)
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
                            font_size: app.get_scaled_sp('15.0sp')
                            size_hint: (None,None)
                            height: app.get_scaled_height(67.0)
                            width: app.get_scaled_width(88.0)
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
                            font_size: app.get_scaled_sp('15.0sp')
                            size_hint: (None,None)
                            height: app.get_scaled_height(67.0)
                            width: app.get_scaled_width(88.0)
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
        # Add the IDs of ALL the TextInputs on this screen
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
        # self.unit_label.text = self.j.parameter_dict["cutter dimensions"]["units"]
        if self.j.parameter_dict["cutter dimensions"]["units"] == "mm":
            self.unit_toggle.active = False
        elif self.j.parameter_dict["cutter dimensions"]["units"] == "inches":
            self.unit_toggle.active = True

    def on_enter(self):
        self.kb.setup_text_inputs(self.text_inputs)

# Action buttons       
    def get_info(self):
        info = """To maintain accuracy, it is important that you measure the dimensions of your cutter.

 The shoulder length must be equal or larger than the cutting length."""
        InfoPopup(sm=self.shapecutter_sm, m=self.m, l=self.m.l,
                  main_string=info,
                  popup_width=500,
                  popup_height=400,
                  main_label_size_delta=140).open()

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
            # save the dimensions
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
            self.shapecutter_sm.next_screen()
        else:
            pass
