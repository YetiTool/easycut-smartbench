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

<ShapeCutter22ScreenClass>

    info_button: info_button
    tab_toggle: tab_toggle
    # tab_YN: tab_YN
    unit_toggle: unit_toggle
    # unit_label: unit_label
    main_image: main_image
    td_dimension:td_dimension
    th_dimension:th_dimension
    tw_dimension:tw_dimension
    
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
                        padding: app.get_scaled_tuple([0.0, 0.0, 0.0, 0.0])
                        orientation: "vertical"
                    
                        BoxLayout: #text box
                            size_hint: (None,None)
                            height: app.get_scaled_height(55.0)
                            width: app.get_scaled_width(675.0)
                            padding: app.get_scaled_tuple([80.0, 0.0, 300.0, 0.0])
                            orientation: "vertical"                       
                            BoxLayout: #image box
                                size_hint: (None,None)
                                height: app.get_scaled_height(55.0)
                                width: app.get_scaled_width(295.0)
                                orientation: "horizontal"
                                Label:
                                    text: root.user_instructions
                                    color: 0,0,0,1
                                    font_size: app.get_scaled_width(20.0)
                                    markup: True
                                    halign: "left"
                                    valign: "top"
                                    text_size: self.size
                                    size: self.parent.size
                                    pos: self.parent.pos

                                BoxLayout: 
                                    size_hint: (None,None)
                                    height: app.get_scaled_height(55.0)
                                    width: app.get_scaled_width(85.0)
                                    padding: app.get_scaled_tuple([2.0, 0.0, 0.0, 23.0])

                                    Switch:
                                        id: tab_toggle
                                        size_hint: (None,None)
                                        height: app.get_scaled_height(32.0)
                                        width: app.get_scaled_width(83.0)
                                        background_color: hex('#F4433600')
                                        center: self.parent.center
                                        pos: self.parent.pos
                                        on_active: root.toggle_tabs()
                                        active_norm_pos: max(0., min(1., (int(self.active) + self.touch_distance / sp(0.05125*app.width))))
                                        canvas.after:
                                            Color:
                                                rgb: 1,1,1
                                            Rectangle:
                                                source: './asmcnc/apps/shapeCutter_app/img/slider_bg_no.png' if tab_toggle.active else './asmcnc/apps/shapeCutter_app/img/slider_bg_yes.png' 
                                                # make or download your background jpg
                                                size: sp(0.10375*app.width), sp(0.0666666666667*app.height)
                                                pos: int(self.center_x - sp(0.05125*app.width)), int(self.center_y - sp(0.0333333333333*app.height))
                                         
                                            Rectangle:
                                                #id: switch_rectangle
                                                source: './asmcnc/apps/shapeCutter_app/img/slider_fg_yes.png' if tab_toggle.active else './asmcnc/apps/shapeCutter_app/img/slider_fg_no.png'
                                                # make or download your slider jpg
                                                size: sp(0.05375*app.width), sp(0.0666666666667*app.height)
                                                pos: int(self.center_x - sp(0.05125*app.width) + self.active_norm_pos * sp(0.05125*app.width)), int(self.center_y - sp(0.0333333333333*app.height))

                        BoxLayout: #image & text entry box
                            size_hint: (None,None)
                            height: app.get_scaled_height(255.0)
                            width: app.get_scaled_width(675.0)
                            padding: app.get_scaled_tuple([10.0, 0.0, 0.0, 21.0])
                            orientation: "horizontal"
                            
                            BoxLayout: #image box
                                size_hint: (None,None)
                                height: app.get_scaled_height(255.0)
                                width: app.get_scaled_width(420.0)
                                padding: app.get_scaled_tuple([20.0, 0.0, 0.0, 11.0])
                                Image:
                                    id: main_image
                                    source: "./asmcnc/apps/shapeCutter_app/img/tabs_rect.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True
                                    
                            BoxLayout:
                                orientation: 'vertical'
                                size_hint: (None,None)
                                width: app.get_scaled_width(210.0)
                                height: app.get_scaled_height(330.0)
                                padding: app.get_scaled_tuple([0.0, 0.0, 0.0, 90.0])
                                spacing: app.get_scaled_width(20.0)
                                pos: self.parent.pos
                                
                                # Unit toggle
                                BoxLayout:
                                    size_hint: (None,None)
                                    height: app.get_scaled_height(32.0)
                                    width: app.get_scaled_width(210.0)
                                    padding: app.get_scaled_tuple([70.0, 0.0, 10.0, 0.0])
                                    orientation: "horizontal"
                               
                                    BoxLayout: 
                                        size_hint: (None,None)
                                        height: app.get_scaled_height(32.0)
                                        width: app.get_scaled_width(120.0)
                                        padding: app.get_scaled_tuple([37.0, 0.0, 0.0, 0.0])
                                                                         
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
                                    width: app.get_scaled_width(210.0)
                                    padding: app.get_scaled_tuple([20.0, 0.0, 20.0, 0.0])
                                    orientation: "horizontal"
                                    
                                    Label: 
                                        text: "TD"
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
                                        width: app.get_scaled_width(120.0)
                                        padding: app.get_scaled_tuple([20.0, 0.0, 0.0, 0.0])
                                                    
                                        TextInput: 
                                            id: td_dimension
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
                                    width: app.get_scaled_width(210.0)
                                    padding: app.get_scaled_tuple([20.0, 0.0, 20.0, 0.0])
                                    orientation: "horizontal"
                                    
                                    Label: 
                                        text: "TH"
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
                                        width: app.get_scaled_width(120.0)
                                        padding: app.get_scaled_tuple([20.0, 0.0, 0.0, 0.0])
                                                    
                                        TextInput: 
                                            id: th_dimension
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
                                    width: app.get_scaled_width(210.0)
                                    padding: app.get_scaled_tuple([20.0, 0.0, 20.0, 0.0])
                                    orientation: "horizontal"
                                    
                                    Label: 
                                        text: "TW"
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
                                        width: app.get_scaled_width(120.0)
                                        padding: app.get_scaled_tuple([20.0, 0.0, 0.0, 0.0])
                                                    
                                        TextInput: 
                                            id: tw_dimension
                                            valign: 'top'
                                            halign: 'center'
                                            text_size: self.size
                                            font_size: app.get_scaled_sp('20.0sp')
                                            markup: True
                                            input_filter: 'float'
                                            multiline: False
                                            text: ''
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


class ShapeCutter22ScreenClass(Screen):
    info_button = ObjectProperty()
    screen_number = StringProperty("[b]22[/b]")
    title_label = StringProperty("[b]Set tabs[/b]")
    user_instructions = StringProperty("Are you using tabs?")

    def __init__(self, **kwargs):
        super(ShapeCutter22ScreenClass, self).__init__(**kwargs)
        self.shapecutter_sm = kwargs["shapecutter"]
        self.m = kwargs["machine"]
        self.j = kwargs["job_parameters"]
        self.kb = kwargs["keyboard"]
        # Add the IDs of ALL the TextInputs on this screen
        self.text_inputs = [self.td_dimension, self.th_dimension, self.tw_dimension]

    def on_touch(self):
        for text_input in self.text_inputs:
            text_input.focus = False

    def on_pre_enter(self):
        self.info_button.opacity = 1
        if self.j.shape_dict["shape"] == "circle":
            self.main_image.source = "./asmcnc/apps/shapeCutter_app/img/tabs_circ.png"
        elif self.j.shape_dict["shape"] == "rectangle":
            self.main_image.source = "./asmcnc/apps/shapeCutter_app/img/tabs_rect.png"
        if self.j.parameter_dict["tabs"]["tabs?"] == "True":
            self.tab_toggle.active = True
            self.td_dimension.disabled = False
            self.th_dimension.disabled = False
            self.tw_dimension.disabled = False
            self.td_dimension.text = "{:.2f}".format(
                float(self.j.parameter_dict["tabs"]["spacing"])
            )
            self.th_dimension.text = "{:.2f}".format(
                float(self.j.parameter_dict["tabs"]["height"])
            )
            self.tw_dimension.text = "{:.2f}".format(
                float(self.j.parameter_dict["tabs"]["width"])
            )
        else:
            self.tab_toggle.active = False
            self.td_dimension.text = ""
            self.td_dimension.disabled = True
            self.th_dimension.text = ""
            self.th_dimension.disabled = True
            self.tw_dimension.text = ""
            self.tw_dimension.disabled = True
            if self.j.parameter_dict["tabs"]["units"] == "mm":
                self.unit_toggle.active = False
            else:
                self.unit_toggle.active = True
        if self.j.parameter_dict["tabs"]["units"] == "inches":
            self.unit_toggle.active = True
        else:
            self.unit_toggle.active = False

    def on_enter(self):
        self.kb.setup_text_inputs(self.text_inputs)
            
# Action buttons       
    def get_info(self):
        info = """Tabs are used to hold your piece in place when cutting from a sheet.

For more help please visit: https://www.yetitool.com/support/knowledge-
base/hardware-smartbench-workholding"""
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
    def toggle_units(self):
        if self.unit_toggle.active == True:
            self.j.parameter_dict["tabs"]["units"] = "inches"
            if not self.td_dimension.text == "":
                self.td_dimension.text = "{:.2f}".format(
                    float(self.td_dimension.text) / 25.4
                )
            if not self.th_dimension.text == "":
                self.th_dimension.text = "{:.2f}".format(
                    float(self.th_dimension.text) / 25.4
                )
            if not self.tw_dimension.text == "":
                self.tw_dimension.text = "{:.2f}".format(
                    float(self.tw_dimension.text) / 25.4
                )
        elif self.unit_toggle.active == False:
            self.j.parameter_dict["tabs"]["units"] = "mm"
            if not self.td_dimension.text == "":
                self.td_dimension.text = "{:.2f}".format(
                    float(self.td_dimension.text) * 25.4
                )
            if not self.th_dimension.text == "":
                self.th_dimension.text = "{:.2f}".format(
                    float(self.th_dimension.text) * 25.4
                )
            if not self.tw_dimension.text == "":
                self.tw_dimension.text = "{:.2f}".format(
                    float(self.tw_dimension.text) * 25.4
                )

    def toggle_tabs(self):
        if self.tab_toggle.active == True:
            self.j.parameter_dict["tabs"]["tabs?"] = True
            self.td_dimension.disabled = False
            self.th_dimension.disabled = False
            self.tw_dimension.disabled = False
        elif self.tab_toggle.active == False:
            self.j.parameter_dict["tabs"]["tabs?"] = False
            self.td_dimension.text = ""
            self.td_dimension.disabled = True
            self.th_dimension.text = ""
            self.th_dimension.disabled = True
            self.tw_dimension.text = ""
            self.tw_dimension.disabled = True

    def check_dimensions(self):
        if self.tab_toggle.active == True:
            self.j.parameter_dict["tabs"]["tabs?"] = True
            if (
                not self.td_dimension.text == ""
                and not self.th_dimension.text == ""
                and not self.tw_dimension.text == ""
            ):
                if self.unit_toggle.active == True:
                    self.j.parameter_dict["tabs"]["units"] = "inches"
                elif self.unit_toggle.active == False:
                    self.j.parameter_dict["tabs"]["units"] = "mm"
                units = self.j.parameter_dict["tabs"]["units"]
                # save the dimensions
                input_dim_list = [
                    ("width", float(self.tw_dimension.text)),
                    ("height", float(self.th_dimension.text)),
                    ("spacing", float(self.td_dimension.text)),
                ]
                for dim, input in input_dim_list:
                    setting = self.j.validate_tabs(dim, input)
                    if not setting == True:
                        if dim == "width" or dim == "height":
                            description = (
                                "The tab "
                                + dim
                                + """ dimension isn't valid.

"""
                                + "The tab "
                                + dim
                                + " should be greater than 0 and less"
                                + " than "
                                + "{:.2f}".format(setting)
                                + " "
                                + units
                                + ".\n\n"
                                + "Please re-enter your dimensions."
                            )
                        else:
                            description = (
                                "The tab "
                                + dim
                                + " dimension isn't valid.\n\n"
                                + "The tab "
                                + dim
                                + " value should be greater than "
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
                self.shapecutter_sm.next_screen()
            else:
                pass
        elif self.tab_toggle.active == False:
            self.j.parameter_dict["tabs"]["tabs?"] = False
            self.shapecutter_sm.next_screen()
