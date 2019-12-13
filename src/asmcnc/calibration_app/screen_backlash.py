'''
Created on 12 December 2019
Screen to inform user of essential preparation before they continue calibrating

@author: Letty
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.widget import Widget

# from asmcnc.calibration_app import screen_measurement

Builder.load_string("""

<BacklashScreenClass>:

    test_ok_label: test_ok_label
    test_instructions_label: test_instructions_label
    user_instructions_text: user_instructions_text
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
                    size_hint_y: 0.3
                    font_size: '35sp'
                    text_size: self.size
                    halign: 'left'
                    valign: 'middle'
                    text: '[color=000000]  X backlash:[/color]'
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
                                id: test_ok_label
                                #size_hint_y: 1
                                font_size: '20sp'
                                text: 'Test'
                        
            
""")

class BacklashScreenClass(Screen):

    test_ok_label = ObjectProperty()
    test_instructions_label = ObjectProperty()
    user_instructions_text = ObjectProperty()
    nudge01_button = ObjectProperty()
    nudge002_button = ObjectProperty()

    backlash_move_distance = 50
    nudge_counter = 0
    
    sub_screen_count = 0
    
    def __init__(self, **kwargs):
        super(BacklashScreenClass, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']

    def on_enter(self):
        self.m.jog_absolute_single_axis('X',-1184,9999)
        self.nudge002_button.opacity = 1
        self.nudge002_button.disabled = False
        self.nudge01_button.opacity = 1
        self.nudge01_button.disabled = False
        
        self.user_instructions_text.text = 'Push the tape measure up against the guard post,' \
                        ' and take a measurement against the end plate. \n\n' \
                        'Do not allow the tape measure to bend. \n\n\n' \
                        'Use the nudge buttons so that the measurement is precisely up to a millimeter line.'
                        
        self.test_instructions_label.text = '[color=000000]When the the measurement is precisely up to a millimeter line press [b]Test[/b].\n' \
                        '\n The axis will be moved backwards and then forwards, attempting to return to the same point.[/color]'

        self.test_ok_label.text = 'Test'


    def skip_to_lobby(self):
        self.sm.current = 'lobby'
    
    def test(self):
        self.m.jog_relative('X', self.backlash_move_distance, 9999)
        self.m.jog_relative('X', -1*self.backlash_move_distance, 9999)
            
    def nudge_01(self):
        self.m.jog_relative('X',0.1,9999)
        self.nudge_counter += 0.1
        
    def nudge_002(self):
        self.m.jog_relative('X',0.02,9999)
        self.nudge_counter += 0.02
    
    def next_instruction(self):
        if self.sub_screen_count == 0:
            self.test()
            self.nudge_counter = 0
            self.sub_screen_count = 1
            self.test_ok_label.text = 'Ok'
            self.user_instructions_text.text = 'Repeat the measurement.\n\n' \
                    'Use the nudge buttons to return to the exact position, if required.\n\n' \
                    'The amount nudged will be added to give the backlash value. If you overshoot, repeat the section.'
            self.test_instructions_label.text = ' '
        elif self.sub_screen_count == 1:
            self.sub_screen_count = 2
            self.user_instructions_text.text = 'The backlash is value is ' + str(self.nudge_counter) + ' mm.\n\n' \
                    'If this value is higher than 0.3 mm, it is worth inspecting the axis wheels' \
                    'and motor pinions to ensure a better engagement.\n\n'
            self.nudge_counter = 0
            self.test_ok_label.text = 'Next section'
            self.nudge002_button.opacity = 0
            self.nudge002_button.disabled = True
            self.nudge01_button.opacity = 0
            self.nudge01_button.disabled = True
            
        elif self.sub_screen_count == 2:
            self.sub_screen_count = 0
            self.next_screen()

    def repeat_section(self):
        self.sm.current = 'measurement'

    def skip_section(self):
        self.next_screen()
        
    def next_screen(self):
#         measurement_screen = screen_measurement.MeasurementScreenClass(name = 'measurement', screen_manager = self.sm, machine = self.m)
#         self.sm.add_widget(measurement_screen)
#         self.sm.current = 'measurement'
        pass


