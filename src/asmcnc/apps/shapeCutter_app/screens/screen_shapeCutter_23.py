"""
Created on 4 March 202
Screen 23 for the Shape Cutter App

@author: Letty
"""
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import MetricsBase
from kivy.properties import StringProperty, ObjectProperty
from kivy.clock import Clock
from asmcnc.apps.shapeCutter_app.screens import popup_info
from asmcnc.apps.shapeCutter_app.screens import popup_input_error
from asmcnc.core_UI.popups import InfoPopup, WarningPopup

Builder.load_string(
    """

<ShapeCutter23ScreenClass>

    info_button: info_button
    unit_toggle: unit_toggle
    # unit_label: unit_label
    xy_feed_units: xy_feed_units
    z_feed_units: z_feed_units
    xy_feed: xy_feed
    z_feed: z_feed
    spindle_speed: spindle_speed
    
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
                        allow_stretch: True
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
                        allow_stretch: True
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
                            color: color_provider.get_rgba("black")
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
                            padding:[0, 0, 0, 0]
                            orientation: "vertical"                       

                        BoxLayout: #image & text entry box
                            size_hint: (None,None)
                            height: dp(0.53125*app.height)
                            width: dp(0.74375*app.width)
                            padding:[0, 0, 0, dp(0.04375)*app.height]
                            orientation: "horizontal"
                                    
                            BoxLayout:
                                orientation: 'vertical'
                                size_hint: (None,None)
                                width: dp(0.74375*app.width)
                                height: dp(0.53125*app.height)
                                padding:[0, 0, 0, dp(0.104166666667)*app.height]
                                spacing:0.0416666666667*app.height
                                pos: self.parent.pos
                                
                                # BL horizontal
                                    # Toggle button
                                BoxLayout:
                                    size_hint: (None,None)
                                    height: dp(0.0666666666667*app.height)
                                    width: dp(0.74375*app.width)
                                    padding:[dp(0.4775)*app.width, 0, dp(0.1625)*app.width, 0]
                                    orientation: "horizontal"
                                                    
                      
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
                            
                                BoxLayout: #dimension 1
                                    size_hint: (None,None)
                                    height: dp(0.0729166666667*app.height)
                                    width: dp(0.74375*app.width)
                                    padding:[0, 0, dp(0.025)*app.width, 0]
                                    orientation: "horizontal"
                                    
                                    Label: 
                                        text: "XY feed rate"
                                        color: color_provider.get_rgba("black")
                                        font_size: 0.025*app.width
                                        markup: True
                                        halign: "left"
                                        valign: "middle"
                                        text_size: self.size
                                        size: self.parent.size
                                        pos: self.parent.pos
                                                                  
                                    BoxLayout: 
                                        size_hint: (None,None)
                                        height: dp(0.0729166666667*app.height)
                                        width: dp(0.14125*app.width)
                                        padding:[dp(0.0125)*app.width, 0, 0, 0]
                                                    
                                        TextInput: 
                                            id: xy_feed
                                            valign: 'top'
                                            halign: 'center'
                                            text_size: self.size
                                            font_size: str(0.025*app.width) + 'sp'
                                            markup: True
                                            input_filter: 'float'
                                            multiline: False
                                            text: ''
                                    BoxLayout: 
                                        size_hint: (None,None)
                                        height: dp(0.0729166666667*app.height)
                                        width: dp(0.1375*app.width)
                                        padding:[dp(0.0125)*app.width, 0, dp(0.0125)*app.width, 0]
                                        Label: 
                                            id: xy_feed_units
                                            color: color_provider.get_rgba("black")
                                            font_size: 0.025*app.width
                                            markup: True
                                            halign: "left"
                                            valign: "middle"
                                            text_size: self.size
                                            size: self.parent.size
                                            pos: self.parent.pos                      
                                
                                BoxLayout: #dimension 2
                                    size_hint: (None,None)
                                    height: dp(0.0729166666667*app.height)
                                    width: dp(0.74375*app.width)
                                    padding:[0, 0, dp(0.025)*app.width, 0]
                                    orientation: "horizontal"
                                    
                                    Label: 
                                        text: "Plunge rate"
                                        color: color_provider.get_rgba("black")
                                        font_size: 0.025*app.width
                                        markup: True
                                        halign: "left"
                                        valign: "middle"
                                        text_size: self.size
                                        size: self.parent.size
                                        pos: self.parent.pos
                                                                  
                                    BoxLayout: 
                                        size_hint: (None,None)
                                        height: dp(0.0729166666667*app.height)
                                        width: dp(0.14125*app.width)
                                        padding:[dp(0.0125)*app.width, 0, 0, 0]
                                                    
                                        TextInput: 
                                            id: z_feed
                                            valign: 'top'
                                            halign: 'center'
                                            text_size: self.size
                                            font_size: str(0.025*app.width) + 'sp'
                                            markup: True
                                            input_filter: 'float'
                                            multiline: False
                                            text: ''                           
                                    BoxLayout: 
                                        size_hint: (None,None)
                                        height: dp(0.0729166666667*app.height)
                                        width: dp(0.1375*app.width)
                                        padding:[dp(0.0125)*app.width, 0, dp(0.0125)*app.width, 0]
                                        Label: 
                                            id: z_feed_units
                                            color: color_provider.get_rgba("black")
                                            font_size: 0.025*app.width
                                            markup: True
                                            halign: "left"
                                            valign: "middle"
                                            text_size: self.size
                                            size: self.parent.size
                                            pos: self.parent.pos
                                BoxLayout: #dimension 3
                                    size_hint: (None,None)
                                    height: dp(0.0729166666667*app.height)
                                    width: dp(0.74375*app.width)
                                    padding:[0, 0, dp(0.025)*app.width, 0]
                                    orientation: "horizontal"
                                    
                                    Label: 
                                        text: "Spindle speed (precision only)"
                                        color: color_provider.get_rgba("black")
                                        font_size: 0.025*app.width
                                        markup: True
                                        halign: "left"
                                        valign: "middle"
                                        text_size: self.size
                                        size: self.parent.size
                                        pos: self.parent.pos
                                                                  
                                    BoxLayout: 
                                        size_hint: (None,None)
                                        height: dp(0.0729166666667*app.height)
                                        width: dp(0.14125*app.width)
                                        padding:[dp(0.0125)*app.width, 0, 0, 0]
                                                    
                                        TextInput: 
                                            id: spindle_speed
                                            valign: 'top'
                                            halign: 'center'
                                            text_size: self.size
                                            font_size: str(0.025*app.width) + 'sp'
                                            markup: True
                                            input_filter: 'float'
                                            multiline: False
                                            text: ''                                                                
                                    BoxLayout: 
                                        size_hint: (None,None)
                                        height: dp(0.0729166666667*app.height)
                                        width: dp(0.1375*app.width)
                                        padding:[dp(0.0125)*app.width, 0, dp(0.0125)*app.width, 0]
                                        Label: 
                                            text: "RPM"
                                            color: color_provider.get_rgba("black")
                                            font_size: 0.025*app.width
                                            markup: True
                                            halign: "left"
                                            valign: "middle"
                                            text_size: self.size
                                            size: self.parent.size
                                            pos: self.parent.pos

                                BoxLayout: # reminder
                                    size_hint: (None,None)
                                    height: dp(0.125*app.height)
                                    width: dp(0.74375*app.width)
                                    padding:[0, dp(0.0208333333333)*app.height, dp(0.075)*app.width, 0]
                                    orientation: "horizontal"
                                    
                                    Label: 
                                        text: "[b]Reminder: If you have manual speed control don't forget to set this on the dial.[/b]"
                                        color: color_provider.get_rgba("black")
                                        font_size: 0.025*app.width
                                        markup: True
                                        halign: "left"
                                        valign: "top"
                                        text_size: self.size
                                        size: self.parent.size
                                        pos: self.parent.pos

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


class ShapeCutter23ScreenClass(Screen):
    info_button = ObjectProperty()
    screen_number = StringProperty("[b]23[/b]")
    title_label = StringProperty("[b]Enter feeds and speeds[/b]")
    user_instructions = StringProperty("")

    def __init__(self, **kwargs):
        super(ShapeCutter23ScreenClass, self).__init__(**kwargs)
        self.shapecutter_sm = kwargs["shapecutter"]
        self.m = kwargs["machine"]
        self.j = kwargs["job_parameters"]
        self.l = kwargs["localization"]
        self.kb = kwargs["keyboard"]
        # Add the IDs of ALL the TextInputs on this screen
        self.text_inputs = [self.xy_feed, self.z_feed, self.spindle_speed]

    def on_touch(self):
        for text_input in self.text_inputs:
            text_input.focus = False

    def on_pre_enter(self):
        self.info_button.opacity = 1
        self.xy_feed.text = "{:.2f}".format(
            float(self.j.parameter_dict["feed rates"]["xy feed rate"])
        )
        self.z_feed.text = "{:.2f}".format(
            float(self.j.parameter_dict["feed rates"]["z feed rate"])
        )
        self.spindle_speed.text = "{:.0f}".format(
            float(self.j.parameter_dict["feed rates"]["spindle speed"])
        )
        if self.j.parameter_dict["feed rates"]["units"] == "inches":
            self.unit_toggle.active = True
            self.xy_feed_units.text = "inches/min"
            self.z_feed_units.text = "inches/min"
        elif self.j.parameter_dict["feed rates"]["units"] == "mm":
            self.unit_toggle.active = False
            self.xy_feed_units.text = "mm/min"
            self.z_feed_units.text = "mm/min"

    def on_enter(self):
        self.kb.setup_text_inputs(self.text_inputs)

# Action buttons       
    def get_info(self):
        # info = "[b]XY Feed Rate:[/b] Feed used in cutting moves.\n\n" \
        # "[b]Z Feed Rate (Plunge Rate):[/b] Feed when vertically plunging into stock.\n\n" \
        # "[b]Spindle Speed:[/b] Rotational speed of the tool.\n\n" \
        # "For more help please visit: https://www.yetitool.com/support/knowledge-\nbase/hardware-smartbench-feeds-speeds"
        wait_popup = InfoPopup(sm=self.shapecutter_sm, m=self.m, l=self.m.l,
                               main_string="Please wait, loading feeds and speeds look-up table...",
                               popup_width=500,
                               popup_height=400,
                               main_label_size_delta=140,
                               button_layout_padding=[0,0,0,0],
                               main_layout_padding=[40,20,40,20],
                               main_label_padding=[40,20],
                               main_label_size_hint_y=1,
                               main_label_h_align="center")
        wait_popup.open()
        Clock.schedule_once(
            lambda dt: wait_popup.dismiss(),
            2.5,
        )
        Clock.schedule_once(
            lambda dt: popup_info.PopupFeedsAndSpeedsLookupTable(self.shapecutter_sm),
            1.5,
        )

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
            self.j.parameter_dict["feed rates"]["units"] = "inches"
            self.xy_feed_units.text = "inches/min"
            self.z_feed_units.text = "inches/min"
            if not self.xy_feed.text == "":
                self.xy_feed.text = "{:.2f}".format(float(self.xy_feed.text) / 25.4)
            if not self.z_feed.text == "":
                self.z_feed.text = "{:.2f}".format(float(self.z_feed.text) / 25.4)
        elif self.unit_toggle.active == False:
            self.j.parameter_dict["feed rates"]["units"] = "mm"
            self.xy_feed_units.text = "mm/min"
            self.z_feed_units.text = "mm/min"
            if not self.xy_feed.text == "":
                self.xy_feed.text = "{:.2f}".format(float(self.xy_feed.text) * 25.4)
            if not self.z_feed.text == "":
                self.z_feed.text = "{:.2f}".format(float(self.z_feed.text) * 25.4)

    def check_dimensions(self):
        if not self.xy_feed.text == "" and not self.z_feed.text == "":
            if self.unit_toggle.active == True:
                self.j.parameter_dict["feed rates"]["units"] = "inches"
            elif self.unit_toggle.active == False:
                self.j.parameter_dict["feed rates"]["units"] = "mm"
            # save the dimensions
            input_dim_list = [
                ("xy feed rate", float(self.xy_feed.text)),
                ("z feed rate", float(self.z_feed.text)),
                ("spindle speed", float(self.spindle_speed.text)),
            ]
            for dim, input in input_dim_list:
                setting = self.j.validate_feed_rates(dim, input)
                if not setting == True:
                    if dim == "spindle speed":
                        description = (
                            "The "
                            + dim
                            + " input isn't valid.\n\n"
                            + "The "
                            + dim
                            + " should be greater than 6000"
                            + """ and less than 25000 RPM.

"""
                            + "Please re-enter your parameters."
                        )
                    else:
                        description = (
                            "The "
                            + dim
                            + " input isn't valid.\n\n"
                            + dim
                            + """ value should be greater than 0.

"""
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
