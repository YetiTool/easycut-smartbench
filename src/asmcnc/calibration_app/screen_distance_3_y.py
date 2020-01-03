'''
Created on 12 December 2019
Screen to help user calibrate distances for Y axis

Step 3 

Allows user to input next measurement

@author: Letty
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from asmcnc.calibration_app import screen_distance_4_y

Builder.load_string("""

<DistanceScreen3Class>:

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
        padding: 20
        spacing: 0

        BoxLayout:
            orientation: 'horizontal'
            padding: 0, 0
            spacing: 20
            size_hint_y: 0.2
        
            Button:
                size_hint_y:0.9
                id: getout_button
                size: self.texture_size
                valign: 'top'
                halign: 'center'
                disabled: False
                # background_color: hex('#a80000FF')
                on_release: 
                    root.repeat_section()
                    
                BoxLayout:
                    padding: 5
                    size: self.parent.size
                    pos: self.parent.pos
                    
                    Label:
                        #size_hint_y: 1
                        font_size: '20sp'
                        text: 'Repeat section'

            Button:
                size_hint_y:0.9
                id: getout_button
                size: self.texture_size
                valign: 'top'
                halign: 'center'
                disabled: False
                # background_color: hex('#a80000FF')
                on_release: 
                    root.skip_section()
                    
                BoxLayout:
                    padding: 5
                    size: self.parent.size
                    pos: self.parent.pos
                    
                    Label:
                        #size_hint_y: 1
                        font_size: '20sp'
                        text: 'Skip section'
                        
            Button:
                size_hint_y:0.9
                id: getout_button
                size: self.texture_size
                valign: 'top'
                halign: 'center'
                disabled: False
                # background_color: hex('#a80000FF')
                on_release: 
                    root.skip_to_lobby()
                    
                BoxLayout:
                    padding: 5
                    size: self.parent.size
                    pos: self.parent.pos
                    
                    Label:
                        #size_hint_y: 1
                        font_size: '20sp'
                        text: 'Quit calibration'

        BoxLayout:
            orientation: 'horizontal'
            spacing: 20
            padding: 10

            BoxLayout:
                orientation: 'vertical'
                spacing: 0
                size_hint_x: 1.3
                 
                Label:
                    id: title_label
                    size_hint_y: 0.3
                    font_size: '35sp'
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
                        
                BoxLayout: 
                    orientation: 'horizontal' 
                    padding: 30
                    spacing: 10
                    
                    Button:
                        size_hint_y:0.9
                        id: nudge01_button
                        size: self.texture_size
                        valign: 'top'
                        halign: 'center'
                        disabled: False
                        # background_color: hex('#a80000FF')
                        on_release: 
                            root.nudge_01()
                            
                        BoxLayout:
                            padding: 5
                            size: self.parent.size
                            pos: self.parent.pos
                            
                            Label:
                                #size_hint_y: 1
                                font_size: '20sp'
                                text: 'Nudge 0.1 mm'

                    Button:
                        size_hint_y:0.9
                        id: nudge002_button
                        size: self.texture_size
                        valign: 'top'
                        halign: 'center'
                        disabled: False
                        # background_color: hex('#a80000FF')
                        on_release: 
                            root.nudge_002()
                            
                        BoxLayout:
                            padding: 5
                            size: self.parent.size
                            pos: self.parent.pos
                            
                            Label:
                                #size_hint_y: 1
                                font_size: '20sp'
                                text: 'Nudge 0.02 mm'


            BoxLayout:
                orientation: 'vertical'
                size_hint_x: 0.6
                
                Label:
                    id: warning_label
                    size_hint_y: 0.4
                    size_hint_x: 1
                    size: self.texture_size
                    text_size: self.size
                    font_size: '18sp'
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
                        font_size: '20sp'
                        markup: True
                        input_filter: 'float'
                        multiline: False
                        text: ''
                        on_text_validate: root.save_measured_value()
                        
                    Label: 
                        text_size: self.size
                        text: '[color=000000]  mm[/color]'
                        font_size: '18sp'
                        halign: 'left'
                        valign: 'bottom'
                        markup: True

                Label:
                    id: test_instructions_label
#                    size_hint_y: 0.5
                    text_size: self.size
                    font_size: '18sp'
                    halign: 'center'
                    valign: 'middle'
                    markup: True
                    
                BoxLayout:
                    orientation: 'horizontal'
                    padding: 10
                    size_hint_y: 0.7
                    
                    Button:
                        size: self.texture_size
                        valign: 'top'
                        halign: 'center'
                        disabled: False
                        on_release: 
                            root.next_instruction()
                            
                        BoxLayout:
                            padding: 5
                            size: self.parent.size
                            pos: self.parent.pos
                            
                            Label:
                                id: set_move_label
                                #size_hint_y: 1
                                font_size: '20sp'
                                text: 'Set and move'
                        
            
""")

class DistanceScreen3Class(Screen):

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

    
    initial_y_cal_move = 2000
    y_cal_measure_1 = NumericProperty()
    y_cal_measure_2 = NumericProperty()
    
      
    def __init__(self, **kwargs):
        super(DistanceScreen3Class, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']

    def on_pre_enter(self):
        self.nudge_counter = 0
        self.value_input.text = ''
        self.warning_label.opacity = 0

        self.title_label.text = '[color=000000]Y Distance:[/color]'
        # set this screen up for when user returns to Step 3 :)       
        self.user_instructions_text.text = 'Using the nudges move the carriage to achieve' \
                                            ' a measurement at the next perfect millimeter increment.'
        self.test_instructions_label.text = '[color=000000]Enter the value recorded by your tape measure. [/color]'  
        self.set_move_label.text = 'Set and check'

    def nudge_01(self):
        self.m.jog_relative('Y',0.1,9999)
        self.nudge_counter += 0.1
        
    def nudge_002(self):
        self.m.jog_relative('Y',0.02,9999)
        self.nudge_counter += 0.02

    def save_measured_value(self):
        self.y_cal_measure_2 = float(self.value_input.text)
    
    # Step 3 / sub-screen 2
    def set_and_check(self):
 
        self.final_y_cal_move = self.initial_y_cal_move + self.nudge_total # (machine thinks) 
        self.measured_y_cal_move =  self.y_cal_measure_2 - self.y_cal_measure_1
        
        # get dollar settings
        self.m.get_grbl_settings()
        
        # get setting 100 from serial screen
        self.existing_y_steps_per_mm = self.m.s.setting_101
        
        #calculate new steps per mm
        self.new_y_steps_per_mm = self.existing_y_steps_per_mm * ( self.final_y_cal_move / self.measured_y_cal_move )          
    
        # Ask user to check this in the next screen: 
        self.next_screen()


    def next_instruction(self):
        
        # When the button under the text input is pressed, it triggers the button command and sets up
        # for the next version of this screen:         
        if self.value_input.text == '':
            self.warning_label.opacity = 1
            return
            
        if self.y_cal_measure_1 == float(self.value_input.text):
            self.test_instructions_label.text = '[color=ff0000]INVALID MEASUREMENT: Please nudge to the next mm increment' \
                                                'and record the new value[/color]'
            return

        self.save_measured_value()              # get text input
        self.nudge_total = self.nudge_counter   # keep the nudges this time, we need them! 
        self.nudge_counter = 0                  # clear nudge counter
        
        # Do the actual button command,
        self.set_and_check()

    def skip_to_lobby(self):
        self.sm.current = 'lobby'

    def repeat_section(self):
        from asmcnc.calibration_app import screen_distance_1_y # this has to be here
        distance_screen1y = screen_distance_1_y.DistanceScreen1Class(name = 'distance1y', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(distance_screen1y)
        self.sm.current = 'distance1y'

    def skip_section(self):
        self.skip_to_lobby()
        
    def next_screen(self):       
        if not self.sm.has_screen('distance4y'): # only create the new screen if it doesn't exist already
            distance4y_screen = screen_distance_4_y.DistanceScreen4Class(name = 'distance4y', screen_manager = self.sm, machine = self.m)
            self.sm.add_widget(distance4y_screen)
            
        self.sm.get_screen('distance4y').old_y_steps = self.existing_y_steps_per_mm
        self.sm.get_screen('distance4y').new_y_steps = self.new_y_steps_per_mm

        self.sm.current = 'distance4y'

    def on_leave(self):
        self.sm.remove_widget(self.sm.get_screen('distance3y'))
