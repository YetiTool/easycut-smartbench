'''
Created on 12 December 2019
Screen to help user measure backlash in calibration


2*3 variants of this screen: X and Y versions of: 

Step 1: Test
Setp 2: Repeat measurement
Step 3: Inform

@author: Letty
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.widget import Widget
from kivy.clock import Clock
from asmcnc.calibration_app import screen_distance_1_x
from asmcnc.calibration_app import screen_distance_1_y

Builder.load_string("""

<BacklashScreenClass>:

    test_ok_label: test_ok_label
    test_instructions_label: test_instructions_label
    user_instructions_text: user_instructions_text
    nudge002_button:nudge002_button
    nudge01_button:nudge01_button
    title_label: title_label
    action_button: action_button

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
                background_normal: ''
                background_color: hex('#D6EAF8')
                on_release: 
                    root.repeat_section()
                    
                BoxLayout:
                    padding: 5
                    size: self.parent.size
                    pos: self.parent.pos
                    
                    Label:
                        #size_hint_y: 1
                        font_size: '20sp'
                        text: '[color=455A64]Repeat section[/color]'
                        markup: True

            Button:
                size_hint_y:0.9
                id: getout_button
                size: self.texture_size
                valign: 'top'
                halign: 'center'
                disabled: False
                background_normal: ''
                background_color: hex('#EBF5FB')
                on_release: 
                    root.skip_section()
                    
                BoxLayout:
                    padding: 5
                    size: self.parent.size
                    pos: self.parent.pos
                    
                    Label:
                        #size_hint_y: 1
                        font_size: '20sp'
                        text: '[color=455A64]Skip section[/color]'
                        markup: True
                        
            Button:
                size_hint_y:0.9
                id: getout_button
                size: self.texture_size
                valign: 'top'
                halign: 'center'
                disabled: False
                background_normal: ''
                background_color: hex('#FFCDD2')
                on_release: 
                    root.skip_to_lobby()
                    
                BoxLayout:
                    padding: 5
                    size: self.parent.size
                    pos: self.parent.pos
                    
                    Label:
                        #size_hint_y: 1
                        font_size: '20sp'
                        text: '[color=455A64]Quit calibration[/color]'
                        markup: True

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
                        background_normal: ''
                        background_color: hex('#BBDEFB')
                        on_release: 
                            root.nudge_01()
                            
                        BoxLayout:
                            padding: 5
                            size: self.parent.size
                            pos: self.parent.pos
                            
                            Label:
                                #size_hint_y: 1
                                font_size: '20sp'
                                text: '[color=455A64]Nudge 0.1 mm[/color]'
                                markup: True

                    Button:
                        size_hint_y:0.9
                        id: nudge002_button
                        size: self.texture_size
                        valign: 'top'
                        halign: 'center'
                        disabled: False
                        background_normal: ''
                        background_color: hex('#BBDEFB')
                        on_release: 
                            root.nudge_002()
                            
                        BoxLayout:
                            padding: 5
                            size: self.parent.size
                            pos: self.parent.pos
                            
                            Label:
                                #size_hint_y: 1
                                font_size: '20sp'
                                text: '[color=455A64]Nudge 0.02 mm[/color]'
                                markup: True


            BoxLayout:
                orientation: 'vertical'
                # spacing: 10
                # padding: 10
                size_hint_x: 0.6

                Label:
                    id: test_instructions_label
                    text_size: self.size
                    font_size: '18sp'
                    halign: 'center'
                    valign: 'middle'
                    markup: True
                    
                BoxLayout:
                    orientation: 'horizontal'
                    padding: 20
                    size_hint_y: 0.6
                    
                    Button:
                        id: action_button
                        size: self.texture_size
                        valign: 'top'
                        halign: 'center'
                        disabled: False
                        background_normal: ''
                        background_color: hex('#C5E1A5')
                        on_release: 
                            root.next_instruction()
                            
                        BoxLayout:
                            padding: 5
                            size: self.parent.size
                            pos: self.parent.pos
                            
                            Label:
                                id: test_ok_label
                                #size_hint_y: 1
                                font_size: '20sp'
                                text:'[color=455A64]Test[/color]'
                                markup: True
                        
            
""")

class BacklashScreenClass(Screen):

    title_label = ObjectProperty()
    test_ok_label = ObjectProperty()
    test_instructions_label = ObjectProperty()
    user_instructions_text = ObjectProperty()
    nudge01_button = ObjectProperty()
    nudge002_button = ObjectProperty()
    action_button = ObjectProperty()

    backlash_move_distance = 50
    nudge_counter = 0
    
    sub_screen_count = 0
    
    axis = StringProperty()
    
    def __init__(self, **kwargs):
        super(BacklashScreenClass, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']

    def on_pre_enter(self):
        self.title_label.text = '[color=000000] ' + self.axis + ' backlash:[/color]'
#         if self.axis == 'X':
#             self.screen_x_1() # these don't work if returning from wait screen
#         elif self.axis == 'Y':
#             self.screen_y_1()

    def update_instruction(self, dt):
        if not self.m.state() == 'Jog':
            self.user_instructions_text.text = 'Push the tape measure up against the guard post,' \
                            ' and take a measurement against the end plate. \n\n' \
                            'Do not allow the tape measure to bend. \n\n\n' \
                            'Use the nudge buttons so that the measurement is precisely up to a millimeter line.'
            self.test_instructions_label.text = '[color=000000]When the the measurement is precisely up to a millimeter line press [b]Test[/b].\n' \
                            '\n The axis will be moved backwards and then forwards, attempting to return to the same point.[/color]' 
            self.enable_buttons()        
            Clock.unschedule(self.poll_for_jog_finish)

    def screen_x_1(self):
        self.m.jog_absolute_single_axis('X',-1184,9999)
        self.sub_screen_count = 0
        self.nudge002_button.opacity = 1
        self.nudge002_button.disabled = False
        self.nudge01_button.opacity = 1
        self.nudge01_button.disabled = False
        self.disable_buttons()
        self.user_instructions_text.text = 'Please wait while the machine moves to the next measurement point...'
        self.poll_for_jog_finish = Clock.schedule_interval(self.update_instruction, 0.5)                       
        self.test_instructions_label.text = ''
        self.test_ok_label.text = '[color=455A64]Test[/color]'

    def screen_x_2(self):
        self.test_ok_label.text = '[color=455A64]Ok[/color]'
        self.user_instructions_text.text = 'Repeat the measurement.\n\n' \
                'Use the nudge buttons to return to the exact position, if required.\n\n' \
                'The amount nudged will be added to give the backlash value. If you overshoot, repeat the section.'
        self.test_instructions_label.text = ' '
        self.nudge_counter = 0
    
    def screen_x_3(self):
        self.user_instructions_text.text = 'The backlash is value is ' + str(self.nudge_counter) + ' mm.\n\n' \
                'If this value is higher than 0.3 mm, it is worth inspecting the axis wheels' \
                'and motor pinions to ensure a better engagement.\n\n'
        self.nudge_counter = 0
        self.test_ok_label.text = '[color=455A64]Next section[/color]'
        self.nudge002_button.opacity = 0
        self.nudge002_button.disabled = True
        self.nudge01_button.opacity = 0
        self.nudge01_button.disabled = True

    def screen_y_1(self):
        self.m.jog_absolute_single_axis('X',-660, 9999)
        self.m.jog_absolute_single_axis('Y', -2320, 9999)
        self.sub_screen_count = 0
        self.nudge002_button.opacity = 1
        self.nudge002_button.disabled = False
        self.nudge01_button.opacity = 1
        self.nudge01_button.disabled = False
        self.disable_buttons()
        self.user_instructions_text.text = 'Please wait while the machine moves to the next measurement point...'
        self.poll_for_jog_finish = Clock.schedule_interval(self.update_instruction, 0.5)                       
        self.test_instructions_label.text = ''
        self.test_ok_label.text = '[color=455A64]Test[/color]'
    
    def screen_y_2(self):
        self.test_ok_label.text = '[color=455A64]Ok[/color]'
        self.user_instructions_text.text = 'Repeat the measurement.\n\n' \
                'Use the nudge buttons to return to the exact position, if required.\n\n' \
                'The amount nudged will be added to give the backlash value. If you overshoot, repeat the section.'
        self.test_instructions_label.text = ' '
        self.nudge_counter = 0
    
    def screen_y_3(self):
        self.user_instructions_text.text = 'The backlash is value is ' + str(self.nudge_counter) + ' mm.\n\n' \
                'If this value is higher than 0.3 mm, it is worth inspecting the axis wheels' \
                'and motor pinions to ensure a better engagement.\n\n'
        self.nudge_counter = 0
        self.test_ok_label.text = '[color=455A64]Next section[/color]'
        self.nudge002_button.opacity = 0
        self.nudge002_button.disabled = True
        self.nudge01_button.opacity = 0
        self.nudge01_button.disabled = True

    def skip_to_lobby(self):
        self.sm.current = 'lobby'
    
    def test(self):    
        
        jog_relative_to_stream = ['$J=G91 ' + self.axis + str(self.backlash_move_distance) + ' F9999',
                                  '$J=G91 ' + self.axis + str(-1*self.backlash_move_distance) + ' F9999'
                                  ]
        self.m.s.start_sequential_stream(jog_relative_to_stream)
        
        # want the wait screen called here
        self.sm.get_screen('wait').return_to_screen = 'backlash'
        self.sm.current = 'wait'


    def nudge_01(self):
        self.m.jog_relative(self.axis,0.1,9999)
        self.nudge_counter += 0.1
        
    def nudge_002(self):
        self.m.jog_relative(self.axis,0.02,9999)
        self.nudge_counter += 0.02
        
    def disable_buttons(self):
        self.nudge01_button.disabled = True
        self.nudge002_button.disabled = True
        self.action_button.disabled = True
        
    def enable_buttons(self):
        self.nudge01_button.disabled = False
        self.nudge002_button.disabled = False
        self.action_button.disabled = False
    
    def next_instruction(self):
        
        if self.axis == 'X':
            if self.sub_screen_count == 0:
                self.sub_screen_count = 1
                self.screen_x_2()
                self.test()
    
            elif self.sub_screen_count == 1:
                self.sub_screen_count = 2
                self.screen_x_3()
                
            elif self.sub_screen_count == 2:
                self.sub_screen_count = 0
                self.next_screen()
        elif self.axis == 'Y':
            if self.sub_screen_count == 0:
                self.test()
                self.sub_screen_count = 1
                self.screen_y_2()
    
            elif self.sub_screen_count == 1:
                self.sub_screen_count = 2
                self.screen_y_3()
                
            elif self.sub_screen_count == 2:
                self.sub_screen_count = 0
                self.next_screen()

    def repeat_section(self):
        if self.sub_screen_count == 0:
            self.sm.get_screen('measurement').axis = self.axis
            self.sm.current = 'measurement'
        else:
            if self.axis == 'X':
                self.screen_x_1()
            elif self.axis == 'Y':
                self.screen_y_1()

    def skip_section(self):
        self.next_screen()
        
    def next_screen(self):    
        if self.axis == 'X':       
            if not self.sm.has_screen('distance1x'):
                distance_screen1x = screen_distance_1_x.DistanceScreen1xClass(name = 'distance1x', screen_manager = self.sm, machine = self.m)
                self.sm.add_widget(distance_screen1x)
            self.sm.current = 'distance1x'
        elif self.axis == 'Y':
            if not self.sm.has_screen('distance1y'):
                distance_screen1y = screen_distance_1_y.DistanceScreen1yClass(name = 'distance1y', screen_manager = self.sm, machine = self.m)
                self.sm.add_widget(distance_screen1y)
            self.sm.current = 'distance1y'            
