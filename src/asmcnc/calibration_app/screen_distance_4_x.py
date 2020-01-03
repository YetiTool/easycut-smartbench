'''
Created on 12 December 2019
Screen 2 to help user calibrate distances

Screen needs to do the following: 

Step 2: Inform user of measurement after machine has moved, and ask user if they want to adjust steps per mm 

@author: Letty
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
# from asmcnc.calibration_app import screen_measurement

Builder.load_string("""

<DistanceScreen4Class>:

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
                        size: self.texture_size
                        valign: 'top'
                        halign: 'center'
                        disabled: False
                        # background_color: hex('#a80000FF')
                        on_release: 
                            root.left_button()
                            
                        BoxLayout:
                            padding: 5
                            size: self.parent.size
                            pos: self.parent.pos
                            
                            Label:
                                id: improve_button_label
                                #size_hint_y: 1
                                font_size: '20sp'
                                text: 'I want to try to improve the result'

                    Button:
                        size_hint_y:0.9

                        valign: 'top'
                        halign: 'center'
                        disabled: False
                        # background_color: hex('#a80000FF')
                        on_release: 
                            root.right_button()
                            
                        BoxLayout:
                            padding: 5
                            size: self.parent.size
                            pos: self.parent.pos
                            
                            Label:
                                id: continue_button_label
                                text_size: self.size
                                text: 'Ok, it measures as expected. Move to the next section.'
                                valign: 'middle'
                                halign: 'center'
                                #markup: True


                        
            
""")

class DistanceScreen4Class(Screen):

    title_label = ObjectProperty()
    improve_button_label = ObjectProperty()
    continue_button_label = ObjectProperty()
    user_instructions_text = ObjectProperty()
    
    old_x_steps = NumericProperty()
    new_x_steps = NumericProperty()
   
    def __init__(self, **kwargs):
        super(DistanceScreen4Class, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']

    def on_pre_enter(self):
        old_steps = str(self.old_x_steps)
        new_steps = str(self.new_x_steps)        
        self.title_label.text = '[color=000000]X Distance:[/color]'
        self.user_instructions_text.text = 'The old number of steps per mm was : [b]' + old_steps + '[/b] \n\n' \
                            'The new number of steps per mm is: [b]' + new_steps + '[/b] \n\n' \
                            'You will need to home the machine, and then repeat steps 1 and 2 to verify your results. \n\n' \
                            ' \n [color=ff0000][b]WARNING: SETTING THE NEW NUMBER OF STEPS WILL CHANGE HOW THE MACHINE MOVES.[/b][/color] \n\n' \
                            '[color=000000]Would you like to set the new number of steps?[/color]'
                            
                            
        self.improve_button_label.text = 'NO - RESTART THIS SECTION'
        self.continue_button_label.text = 'YES - HOME AND VERIFY'
    
    def left_button(self):
        self.repeat_section()

    def right_button(self):
        # set new steps per mm
        set_new_steps_sequence = ['$100 =' + str(self.new_x_steps),
                                  '$$'
                                  ]
        self.m.s.start_sequential_stream(set_new_steps_sequence) 
        # this makes sure we stay on this screen until steps have been set before triggering homing sequence     
        self.poll_for_success = Clock.schedule_interval(self.check_for_successful_completion,1)

    def check_for_successful_completion(self, dt):
        # if sequential_stream completes successfully
        if self.m.s.is_sequential_streaming == False:
            print ("New steps have been set: $100 = " + str(self.new_x_steps))
            Clock.unschedule(self.poll_for_success)
            self.next_screen()


    def repeat_section(self):
        from asmcnc.calibration_app import screen_distance_1_x # this has to be here
        distance_screen1x = screen_distance_1_x.DistanceScreenClass(name = 'distance1x', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(distance_screen1x)
        self.sm.current = 'distance1x'

    def skip_section(self):
        # Y STUFF
        self.sm.get_screen('measurement').axis = 'Y'
        self.sm.current = 'measurement'
    
    def next_screen(self):
        # set up distance screen 1-x to return to after homing
        from asmcnc.calibration_app import screen_distance_1_x # this has to be here
        distance_screen1x = screen_distance_1_x.DistanceScreen1Class(name = 'distance1x', screen_manager = self.sm, machine = self.m)     
        self.sm.add_widget(distance_screen1x)
        self.sm.get_screen('homing').return_to_screen = 'distance1x'        
        # get homing screen
        # FLAG: HOMING SCREEN DIDN'T STAY UP THE WHOLE TIME MACHINE WAS HOMING... why the hell not??
        self.sm.current = 'homing'
    
    def skip_to_lobby(self):
        self.sm.current = 'lobby'
       
    def on_leave(self):
        self.sm.remove_widget(self.sm.get_screen('distance4x'))