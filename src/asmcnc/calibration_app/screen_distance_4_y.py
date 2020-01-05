'''
Created on 12 December 2019
Screen to help user calibrate distances for Y axis

Step 4: Report old no. steps vs. new no. steps, and allow user to home and verfiy. 
        They will then need to go through the homing screen, and back to step 1.

@author: Letty
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

from asmcnc.calibration_app import screen_finished

Builder.load_string("""

<DistanceScreen4yClass>:

    title_label:title_label
    user_instructions_text: user_instructions_text
    improve_button_label:improve_button_label
    continue_button_label:continue_button_label

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
                background_color: hex('#EBF5FB')
                on_release: 
                    root.repeat_section()
                    
                BoxLayout:
                    padding: 5
                    size: self.parent.size
                    pos: self.parent.pos
                    
                    Label:
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
                        size: self.texture_size
                        valign: 'top'
                        halign: 'center'
                        disabled: False
                        background_normal: ''
                        background_color: hex('#FFCDD2')
                        on_release: 
                            root.left_button()
                            
                        BoxLayout:
                            padding: 5
                            size: self.parent.size
                            pos: self.parent.pos
                            
                            Label:
                                id: improve_button_label
                                font_size: '20sp'
                                text: '[color=455A64]NO - RESTART THIS SECTION[/color]'
                                markup: True

                    Button:
                        size_hint_y:0.9

                        valign: 'top'
                        halign: 'center'
                        disabled: False
                        background_normal: ''
                        background_color: hex('#C5E1A5')
                        on_release: 
                            root.right_button()
                            
                        BoxLayout:
                            padding: 5
                            size: self.parent.size
                            pos: self.parent.pos
                            
                            Label:
                                id: continue_button_label
                                text_size: self.size
                                text: '[color=455A64]YES - HOME AND VERIFY[/color]'
                                valign: 'middle'
                                halign: 'center'
                                markup: True


                        
            
""")

class DistanceScreen4yClass(Screen):

    title_label = ObjectProperty()
    improve_button_label = ObjectProperty()
    continue_button_label = ObjectProperty()
    user_instructions_text = ObjectProperty()
    
    old_y_steps = NumericProperty()
    new_y_steps = NumericProperty()
    
    sub_screen_count = 0
    
    axis = StringProperty()
   
    def __init__(self, **kwargs):
        super(DistanceScreen4yClass, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']

    def on_pre_enter(self):
        
        self.title_label.text = '[color=000000]Y Distance:[/color]' 
 
        old_steps = str(self.old_y_steps)
        new_steps = str(self.new_y_steps)

        # Step 4: 
        self.user_instructions_text.text = 'The old number of steps per mm was : [b]' + old_steps + '[/b] \n\n' \
                        'The new number of steps per mm is: [b]' + new_steps + '[/b] \n\n' \
                        'You will need to home the machine, and then repeat steps 1 and 2 to verify your results. \n\n' \
                        ' \n [color=ff0000][b]WARNING: SETTING THE NEW NUMBER OF STEPS WILL CHANGE HOW THE MACHINE MOVES.[/b][/color] \n\n' \
                        '[color=000000]Would you like to set the new number of steps?[/color]'
                        
                        
#         self.improve_button_label.text = '[color=455A64]NO - RESTART THIS SECTION[/color]'
#         self.continue_button_label.text = '[color=455A64]YES - HOME AND VERIFY[/color]'
                        

    def left_button(self):
        self.repeat_section()

    def right_button(self):
        # set new steps per mm
        set_new_steps_sequence = ['$101 =' + str(self.new_y_steps),
                                  '$$'
                                  ]
        self.m.s.start_sequential_stream(set_new_steps_sequence) 
        # this makes sure we stay on this screen until steps have been set before triggering homing sequence     
        self.poll_for_success = Clock.schedule_interval(self.check_for_successful_completion,1)

    def check_for_successful_completion(self, dt):
        # if sequential_stream completes successfully
        if self.m.s.is_sequential_streaming == False:
            print ("New steps have been set: $101 = " + str(self.new_y_steps))
            Clock.unschedule(self.poll_for_success)
            self.next_screen()

    def repeat_section(self):
        from asmcnc.calibration_app import screen_distance_1_y # this has to be here
        distance_screen1y = screen_distance_1_y.DistanceScreen1yClass(name = 'distance1y', screen_manager = self.sm, machine = self.m)     
        self.sm.add_widget(distance_screen1y)
        self.sm.current = 'distance1y'

    def skip_section(self):
        final_screen = screen_finished.FinishedCalScreenClass(name = 'calibration_complete', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(final_screen)
        self.sm.current = 'calibration_complete'
        
    def skip_to_lobby(self):
        self.sm.current = 'lobby'
        
    def next_screen(self):
        # set up distance screen 1-x to return to after homing
        from asmcnc.calibration_app import screen_distance_1_y # this has to be here
        distance_screen1y = screen_distance_1_y.DistanceScreen1yClass(name = 'distance1y', screen_manager = self.sm, machine = self.m)     
        self.sm.add_widget(distance_screen1y)
        self.sm.get_screen('homing').return_to_screen = 'distance1y'        
        # get homing screen
        # FLAG: HOMING SCREEN DIDN'T STAY UP THE WHOLE TIME MACHINE WAS HOMING... why the hell not??
        self.sm.current = 'homing'
