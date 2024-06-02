"""
Created on 12 December 2019
Screen to help user calibrate number of steps per distance for X axis 

Distance: step 3

@author: Letty
"""
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from asmcnc.calibration_app import screen_distance_4_x

Builder.load_string(
    """

<DistanceScreen3xClass>:

    title_label:title_label
    value_input:value_input
    set_move_label: set_move_label
    test_instructions_label: test_instructions_label
    user_instructions_text: user_instructions_text
    warning_label:warning_label
    nudge002_button:nudge002_button
    nudge01_button:nudge01_button

    canvas:
        Color:
            rgba: hex('#FFFFFF')
        Rectangle:
            size: self.size
            pos: self.pos

    BoxLayout:
        orientation: 'vertical'
        padding:[dp(0.025)*app.width, dp(0.0416666666667)*app.height]
        spacing: 0
        
        BoxLayout:
            orientation: 'horizontal'
            padding:[0, 0]
            spacing:0.025*app.width
            size_hint_y: 0.2

            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint_y:0.9
                id: getout_button
                size: self.texture_size
                valign: 'top'
                halign: 'center'
                disabled: False
                background_normal: ''
                background_color: hex('#D6EAF8')
                on_press: 
                    root.repeat_section()

                BoxLayout:
                    padding:[dp(0.00625)*app.width, dp(0.0104166666667)*app.height]
                    size: self.parent.size
                    pos: self.parent.pos

                    Label:
                        font_size: str(0.025*app.width) + 'sp'
                        text: '[color=455A64]Go Back[/color]'
                        markup: True

            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint_y:0.9
                id: getout_button
                size: self.texture_size
                valign: 'top'
                halign: 'center'
                disabled: False
                background_normal: ''
                background_color: hex('#D6EAF8')
                on_press: 
                    root.skip_section()

                BoxLayout:
                    padding:[dp(0.00625)*app.width, dp(0.0104166666667)*app.height]
                    size: self.parent.size
                    pos: self.parent.pos

                    Label:
                        #size_hint_y: 1
                        font_size: str(0.025*app.width) + 'sp'
                        text: '[color=455A64]Skip section[/color]'
                        markup: True

            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint_y:0.9
                id: getout_button
                size: self.texture_size
                valign: 'top'
                halign: 'center'
                disabled: False
                background_normal: ''
                background_color: hex('#FFCDD2')
                on_press: 
                    root.quit_calibration()

                BoxLayout:
                    padding:[dp(0.00625)*app.width, dp(0.0104166666667)*app.height]
                    size: self.parent.size
                    pos: self.parent.pos

                    Label:
                        font_size: str(0.025*app.width) + 'sp'
                        text: '[color=455A64]Quit calibration[/color]'
                        markup: True

        BoxLayout:
            orientation: 'horizontal'
            spacing:0.0416666666667*app.height
            padding:[dp(0.0125)*app.width, dp(0.0208333333333)*app.height]

            BoxLayout:
                orientation: 'vertical'
                spacing: 0
                size_hint_x: 1.3
                 
                Label:
                    id: title_label
                    size_hint_y: 0.3
                    font_size: str(0.04375*app.width) + 'sp'
                    text_size: self.size
                    halign: 'left'
                    valign: 'middle'
                    markup: True

                ScrollView:
                    size_hint: 1, 1
                    pos_hint: {'center_x': .5, 'center_y': .5}
                    do_scroll_x: True
                    do_scroll_y: True
                    scroll_type: ['content']
                    
                    RstDocument:
                        id: user_instructions_text
                        background_color: hex('#FFFFFF')
                        base_font_size: str(31.0/800.0*app.width) + 'sp'
                        
                BoxLayout: 
                    orientation: 'horizontal' 
                    padding:[dp(0.0375)*app.width, dp(0.0625)*app.height]
                    spacing:0.0125*app.width
                    
                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        size_hint_y:0.9
                        id: nudge01_button
                        size: self.texture_size
                        valign: 'top'
                        halign: 'center'
                        disabled: False
                        background_normal: ''
                        background_color: hex('#B3E5FC')
                        on_press: 
                            root.nudge_01()
                            
                        BoxLayout:
                            padding:[dp(0.00625)*app.width, dp(0.0104166666667)*app.height]
                            size: self.parent.size
                            pos: self.parent.pos
                            
                            Label:
                                font_size: str(0.025*app.width) + 'sp'
                                text: '[color=455A64]Nudge 0.1 mm[/color]'
                                markup: True

                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        size_hint_y:0.9
                        id: nudge002_button
                        size: self.texture_size
                        valign: 'top'
                        halign: 'center'
                        disabled: False
                        background_normal: ''
                        background_color: hex('#B3E5FC')
                        on_press: 
                            root.nudge_002()
                            
                        BoxLayout:
                            padding:[dp(0.00625)*app.width, dp(0.0104166666667)*app.height]
                            size: self.parent.size
                            pos: self.parent.pos
                            
                            Label:
                                font_size: str(0.025*app.width) + 'sp'
                                text: '[color=455A64]Nudge 0.02 mm[/color]'
                                markup: True

            BoxLayout:
                orientation: 'vertical'
                size_hint_x: 0.6
                
                Label:
                    id: warning_label
                    size_hint_y: 0.4
                    size_hint_x: 1
                    size: self.texture_size
                    text_size: self.size
                    font_size: str(0.0225*app.width) + 'sp'
                    halign: 'center'
                    valign: 'middle'
                    markup: True
                    text: '[color=ff0000]PLEASE ENTER A VALUE![/color]'
                    opacity: 0
                
                BoxLayout: 
                    orientation: 'horizontal'
                    size_hint_y: 0.4
                    TextInput: 
                        id: value_input
                        valign: 'middle'
                        halign: 'center'
                        text_size: self.size
                        font_size: str(0.025*app.width) + 'sp'
                        markup: True
                        input_filter: 'float'
                        multiline: False
                        text: ''
                        on_text_validate: root.save_measured_value()
                        
                    Label: 
                        text_size: self.size
                        text: '[color=000000]  mm[/color]'
                        font_size: str(0.0225*app.width) + 'sp'
                        halign: 'left'
                        valign: 'bottom'
                        markup: True

                Label:
                    id: test_instructions_label
                    text_size: self.size
                    font_size: str(0.0225*app.width) + 'sp'
                    halign: 'center'
                    valign: 'middle'
                    markup: True
                    
                BoxLayout:
                    orientation: 'horizontal'
                    padding:[dp(0.0125)*app.width, dp(0.0208333333333)*app.height]
                    size_hint_y: 0.7

                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        size: self.texture_size
                        valign: 'top'
                        halign: 'center'
                        disabled: False
                        background_normal: ''
                        background_color: hex('#C5E1A5')
                        on_press: 
                            root.next_instruction()

                        BoxLayout:
                            padding:[dp(0.00625)*app.width, dp(0.0104166666667)*app.height]
                            size: self.parent.size
                            pos: self.parent.pos

                            Label:
                                id: set_move_label
                                font_size: str(0.025*app.width) + 'sp'
                                text: '[color=455A64]Set and check[/color]'
                                markup: True
"""
)


class DistanceScreen3xClass(Screen):
    title_label = ObjectProperty()
    set_move_label = ObjectProperty()
    test_instructions_label = ObjectProperty()
    user_instructions_text = ObjectProperty()
    nudge01_button = ObjectProperty()
    nudge002_button = ObjectProperty()
    value_input = ObjectProperty()
    warning_label = ObjectProperty()
    sub_screen_count = 0
    nudge_counter = 0
    axis = StringProperty()
    initial_x_cal_move = 1000
    x_cal_measure_1 = NumericProperty()
    x_cal_measure_2 = NumericProperty()

    def __init__(self, **kwargs):
        super(DistanceScreen3xClass, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.m = kwargs["machine"]

    def on_pre_enter(self):
        self.nudge_counter = 0
        self.value_input.text = ""
        self.title_label.text = "[color=000000]X Distance:[/color]"
        # set this screen up for when user returns to Step 3 :)
        self.user_instructions_text.text = """Using the nudges move the carriage to achieve a measurement at the next perfect millimeter increment.

Nudging will move the Z head away from X-home."""
        self.test_instructions_label.text = (
            "[color=000000]Enter the value recorded by your tape measure. [/color]"
        )
        self.warning_label.opacity = 0

    def nudge_01(self):
        self.m.jog_relative("X", 0.1, 9999)
        self.nudge_counter += 0.1

    def nudge_002(self):
        self.m.jog_relative("X", 0.02, 9999)
        self.nudge_counter += 0.02

    def save_measured_value(self):
        self.x_cal_measure_2 = float(self.value_input.text)

    def set_and_check(self):
        self.final_x_cal_move = self.initial_x_cal_move + self.nudge_total # (machine thinks)
        self.measured_x_cal_move = self.x_cal_measure_2 - self.x_cal_measure_1
        # get dollar settings
        self.m.get_grbl_settings()
        # get setting 100 from serial screen
        self.existing_x_steps_per_mm = self.m.s.setting_100
        # calculate new steps per mm
        self.new_x_steps_per_mm = self.existing_x_steps_per_mm * (
            self.final_x_cal_move / self.measured_x_cal_move
        )
        self.next_screen()

    def next_instruction(self):
        # When the button under the text input is pressed, it triggers the button command and sets up
        # for the next version of this screen:
        if self.value_input.text == "":
            self.warning_label.opacity = 1
            return
        if self.x_cal_measure_1 == float(self.value_input.text):
            self.test_instructions_label.text = "[color=ff0000]INVALID MEASUREMENT: Please nudge to the next mm increment and record the new value[/color]"
            return
        self.save_measured_value()              # get text input
        self.nudge_total = self.nudge_counter   # keep the nudges this time, we need them!
        self.nudge_counter = 0                  # clear nudge counter
        # Do the actual button command,
        self.set_and_check()

    def quit_calibration(self):
        self.sm.get_screen(
            "tape_measure_alert"
        ).return_to_screen = "calibration_complete"
        self.sm.get_screen("calibration_complete").calibration_cancelled = True
        self.sm.current = "tape_measure_alert"

    def repeat_section(self):
        from asmcnc.calibration_app import screen_distance_1_x # this has to be here

        distance_screen1x = screen_distance_1_x.DistanceScreen1xClass(
            name="distance1x", screen_manager=self.sm, machine=self.m
        )
        self.sm.add_widget(distance_screen1x)
        self.sm.current = "distance1x"

    def skip_section(self):
        self.sm.get_screen("measurement").axis = "Y"
        self.sm.current = "measurement"

    def next_screen(self):
        if not self.sm.has_screen("distance4x"): # only create the new screen if it doesn't exist already
            distance4x_screen = screen_distance_4_x.DistanceScreen4xClass(
                name="distance4x", screen_manager=self.sm, machine=self.m
            )
            self.sm.add_widget(distance4x_screen)
        self.sm.get_screen("distance4x").old_x_steps = self.existing_x_steps_per_mm
        self.sm.get_screen("distance4x").new_x_steps = self.new_x_steps_per_mm
        self.sm.current = "distance4x"

    def on_leave(self):
        if self.sm.current != "alarmScreen" and self.sm.current != "errorScreen":
            self.sm.remove_widget(self.sm.get_screen("distance3x"))
