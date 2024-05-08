"""
Created on 12 December 2019
Screen to help user calibrate distances 

This class covers 2x2 instances of the same screen type:

X and Y 

Distance: step 1



@author: Letty
"""
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from asmcnc.calibration_app import screen_distance_2_x
from _ast import Or

Builder.load_string(
    """

<DistanceScreen1xClass>:

    title_label:title_label
    value_input:value_input
    set_move_label: set_move_label
    test_instructions_label: test_instructions_label
    user_instructions_text: user_instructions_text
    warning_label:warning_label
    nudge002_button:nudge002_button
    nudge01_button:nudge01_button
    set_move_button:set_move_button

    canvas:
        Color: 
            rgba: hex('#FFFFFF')
        Rectangle: 
            size: self.size
            pos: self.pos
             
    BoxLayout:
        orientation: 'vertical'
        padding: app.get_scaled_tuple([20.0, 20.0])
        spacing: 0

        BoxLayout:
            orientation: 'horizontal'
            padding: app.get_scaled_tuple([0.0, 0.0])
            spacing: app.get_scaled_width(20.0)
            size_hint_y: 0.2
        
            Button:
                font_size: app.get_scaled_sp('15.0sp')
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
                    padding: app.get_scaled_tuple([5.0, 5.0])
                    size: self.parent.size
                    pos: self.parent.pos
                    
                    Label:
                        #size_hint_y: 1
                        font_size: app.get_scaled_sp('20.0sp')
                        text: '[color=455A64]Go Back[/color]'
                        markup: True

            Button:
                font_size: app.get_scaled_sp('15.0sp')
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
                    padding: app.get_scaled_tuple([5.0, 5.0])
                    size: self.parent.size
                    pos: self.parent.pos
                    
                    Label:
                        font_size: app.get_scaled_sp('20.0sp')
                        text: '[color=455A64]Skip section[/color]'
                        markup: True
                        
            Button:
                font_size: app.get_scaled_sp('15.0sp')
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
                    padding: app.get_scaled_tuple([5.0, 5.0])
                    size: self.parent.size
                    pos: self.parent.pos
                    
                    Label:
                        font_size: app.get_scaled_sp('20.0sp')
                        text: '[color=455A64]Quit calibration[/color]'
                        markup: True

        BoxLayout:
            orientation: 'horizontal'
            spacing: app.get_scaled_width(20.0)
            padding: app.get_scaled_tuple([10.0, 10.0])

            BoxLayout:
                orientation: 'vertical'
                spacing: 0
                size_hint_x: 1.3
                 
                Label:
                    id: title_label
                    size_hint_y: 0.3
                    font_size: app.get_scaled_sp('35.0sp')
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
                        base_font_size: app.get_scaled_sp('31.0sp')
                        
                BoxLayout: 
                    orientation: 'horizontal' 
                    padding: app.get_scaled_tuple([30.0, 30.0])
                    spacing: app.get_scaled_width(10.0)
                    
                    Button:
                        font_size: app.get_scaled_sp('15.0sp')
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
                            padding: app.get_scaled_tuple([5.0, 5.0])
                            size: self.parent.size
                            pos: self.parent.pos
                            
                            Label:
                                font_size: app.get_scaled_sp('20.0sp')
                                text: '[color=455A64]Nudge 0.1 mm[/color]'
                                markup: True

                    Button:
                        font_size: app.get_scaled_sp('15.0sp')
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
                            padding: app.get_scaled_tuple([5.0, 5.0])
                            size: self.parent.size
                            pos: self.parent.pos
                            
                            Label:
                                font_size: app.get_scaled_sp('20.0sp')
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
                    font_size: app.get_scaled_sp('18.0sp')
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
#                         size_hint_y: 0.4
                        valign: 'middle'
                        halign: 'center'
                        text_size: self.size
                        font_size: app.get_scaled_sp('20.0sp')
                        markup: True
                        input_filter: 'float'
                        multiline: False
                        text: ''
                        on_text_validate: root.save_measured_value()
                        
                    Label: 
                        text_size: self.size
                        text: '[color=000000]  mm[/color]'
                        font_size: app.get_scaled_sp('18.0sp')
                        halign: 'left'
                        valign: 'bottom'
                        markup: True

                Label:
                    id: test_instructions_label
                    text_size: self.size
                    font_size: app.get_scaled_sp('18.0sp')
                    halign: 'center'
                    valign: 'middle'
                    markup: True
                    
                BoxLayout:
                    orientation: 'horizontal'
                    padding: app.get_scaled_tuple([10.0, 10.0])
                    size_hint_y: 0.7
                    
                    Button:
                        font_size: app.get_scaled_sp('15.0sp')
                        id: set_move_button
                        size: self.texture_size
                        valign: 'top'
                        halign: 'center'
                        disabled: False
                        background_normal: ''
                        background_color: hex('#C5E1A5')
                        on_press: 
                            root.next_instruction()
                            
                        BoxLayout:
                            padding: app.get_scaled_tuple([5.0, 5.0])
                            size: self.parent.size
                            pos: self.parent.pos
                            
                            Label:
                                id: set_move_label
                                font_size: app.get_scaled_sp('20.0sp')
                                text: '[color=455A64]Set and move[/color]'
                                markup: True
                        
            
"""
)


class DistanceScreen1xClass(Screen):
    title_label = ObjectProperty()
    set_move_label = ObjectProperty()
    test_instructions_label = ObjectProperty()
    user_instructions_text = ObjectProperty()
    nudge01_button = ObjectProperty()
    nudge002_button = ObjectProperty()
    value_input = ObjectProperty()
    warning_label = ObjectProperty()
    set_move_button = ObjectProperty()
    nudge_counter = 0
    axis = StringProperty()
    expected_user_entry = 100
    initial_x_cal_move = 1000
    x_cal_measure_1 = NumericProperty()

    def __init__(self, **kwargs):
        super(DistanceScreen1xClass, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.m = kwargs["machine"]

    def on_pre_enter(self):
        self.title_label.text = "[color=000000]X Distance:[/color]"
        self.user_instructions_text.text = """

Please wait while the machine moves to the next measurement point..."""
        self.disable_buttons()
        self.test_instructions_label.text = (
            "[color=000000]Enter the value recorded by your tape measure. [/color]"
        )
        self.warning_label.opacity = 0
        self.nudge_counter = 0

    def on_enter(self):
        self.initial_move_x()
        self.poll_for_jog_finish = Clock.schedule_interval(self.update_instruction, 0.5)

    def initial_move_x(self):
        self.m.jog_absolute_single_axis("X", -1184, 9999)    # machine moves on screen enter
        self.m.jog_relative("X", -10, 9999)
        self.m.jog_relative("X", 10, 9999)

    def nudge_01(self):
        self.m.jog_relative("X", 0.1, 9999)
        self.nudge_counter += 0.1

    def nudge_002(self):
        self.m.jog_relative("X", 0.02, 9999)
        self.nudge_counter += 0.02

    def save_measured_value(self):
        self.x_cal_measure_1 = float(self.value_input.text)

    def update_instruction(self, dt):
        if not self.m.state() == "Jog":
            self.user_instructions_text.text = """

Push the tape measure up against the guard post, and take an exact measurement against the end plate. 

Do not allow the tape measure to bend. 

Use the nudge buttons so that the measurement is precisely up to a millimeter line,before entering the value on the right.

Nudging will move the Z head away from X-home."""
            self.enable_buttons()
            Clock.unschedule(self.poll_for_jog_finish)

    def set_and_move(self):
        self.m.jog_relative("X", self.initial_x_cal_move, 9999)
        self.next_screen()

    def disable_buttons(self):
        self.nudge01_button.disabled = True
        self.nudge002_button.disabled = True
        self.set_move_button.disabled = True

    def enable_buttons(self):
        self.nudge01_button.disabled = False
        self.nudge002_button.disabled = False
        self.set_move_button.disabled = False

    def next_instruction(self):
        if self.value_input.text == "":
            self.warning_label.text = "[color=ff0000]PLEASE ENTER A VALUE![/color]"
            self.warning_label.opacity = 1
            return
        if float(self.value_input.text) < float(self.expected_user_entry - 20):
            self.warning_label.text = "[color=ff0000]VALUE IS TOO LOW![/color]"
            self.warning_label.opacity = 1
            return
        if float(self.value_input.text) > float(self.expected_user_entry + 20):
            self.warning_label.text = "[color=ff0000]VALUE IS TOO HIGH![/color]"
            self.warning_label.opacity = 1
            return
        self.save_measured_value()  # get text input
        self.nudge_counter = 0      # clear nudge counter
        # Do the actual button command, this will also take us to relevant next screens
        self.set_and_move()

    def quit_calibration(self):
        self.sm.get_screen(
            "tape_measure_alert"
        ).return_to_screen = "calibration_complete"
        self.sm.get_screen("calibration_complete").calibration_cancelled = True
        self.sm.current = "tape_measure_alert"

    def repeat_section(self):
        self.sm.get_screen("backlash").axis = "X"
        self.sm.get_screen("backlash").screen_x_1()
        self.sm.current = "backlash"

    def skip_section(self):
        self.sm.get_screen("measurement").axis = "Y"
        self.sm.current = "measurement"

    def next_screen(self):
        if not self.sm.has_screen("distance2x"): # only create the new screen if it doesn't exist already
            distance2x_screen = screen_distance_2_x.DistanceScreen2xClass(
                name="distance2x", screen_manager=self.sm, machine=self.m
            )
            self.sm.add_widget(distance2x_screen)
        self.sm.get_screen("distance2x").initial_x_cal_move = self.initial_x_cal_move
        self.sm.get_screen("distance2x").x_cal_measure_1 = self.x_cal_measure_1
        self.sm.get_screen("wait").return_to_screen = "distance2x"
        self.sm.current = "wait"

    def on_leave(self):
        if self.sm.current != "alarmScreen" and self.sm.current != "errorScreen":
            self.sm.remove_widget(self.sm.get_screen("distance1x"))
