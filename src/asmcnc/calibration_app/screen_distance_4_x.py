"""
Created on 12 December 2019
Screen 2 to help user calibrate distances

Screen needs to do the following: 

Step 2: Inform user of measurement after machine has moved, and ask user if they want to adjust steps per mm 

@author: Letty
"""
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.screenmanager import Screen

Builder.load_string(
    """

<DistanceScreen4xClass>:

    title_label:title_label
    user_instructions_text: user_instructions_text
    improve_button_label:improve_button_label
    continue_button_label:continue_button_label
    right_button_id: right_button_id

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
                        
                BoxLayout: 
                    orientation: 'horizontal' 
                    padding:[dp(0.0375)*app.width, dp(0.0625)*app.height]
                    spacing:0.0125*app.width
                    
                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        size_hint_y:0.9
                        size: self.texture_size
                        valign: 'top'
                        halign: 'center'
                        disabled: False
                        background_normal: ''
                        background_color: hex('#FFCDD2')
                        on_press: 
                            root.left_button()
                            
                        BoxLayout:
                            padding:[dp(0.00625)*app.width, dp(0.0104166666667)*app.height]
                            size: self.parent.size
                            pos: self.parent.pos
                            
                            Label:
                                id: improve_button_label
                                font_size: str(0.025*app.width) + 'sp'
                                text: '[color=455A64]NO - RESTART THIS SECTION[/color]'
                                markup: True

                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        id: right_button_id
                        size_hint_y:0.9
                        valign: 'top'
                        halign: 'center'
                        disabled: False
                        background_normal: ''
                        background_color: hex('#C5E1A5')
                        on_press: 
                            root.right_button()
                            
                        BoxLayout:
                            padding:[dp(0.00625)*app.width, dp(0.0104166666667)*app.height]
                            size: self.parent.size
                            pos: self.parent.pos
                            
                            Label:
                                id: continue_button_label
                                text_size: self.size
                                text: '[color=455A64]YES - SET, HOME, AND VERIFY[/color]'
                                font_size: str(0.025*app.width) + 'sp'
                                valign: 'middle'
                                halign: 'center'
                                markup: True


                        
            
"""
)


class DistanceScreen4xClass(Screen):
    title_label = ObjectProperty()
    improve_button_label = ObjectProperty()
    continue_button_label = ObjectProperty()
    user_instructions_text = ObjectProperty()
    right_button_id = ObjectProperty()
    old_x_steps = NumericProperty()
    new_x_steps = NumericProperty()
    expected_steps = 56.7

    def __init__(self, **kwargs):
        super(DistanceScreen4xClass, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']

    def on_pre_enter(self):
        old_steps = str(self.old_x_steps)
        new_steps = str(self.new_x_steps)
        self.title_label.text = '[color=000000]X Distance:[/color]'
        if self.new_x_steps < self.expected_steps - 2:
            self.user_instructions_text.text = 'The old number of steps per mm was : [b]' + old_steps + """[/b] 

The new number of steps per mm is: [b]""" + new_steps + """[/b] 

[color=ff0000][b]This is outside of the expected range, please repeat the section.[/b][/color] 

If you get this result again, please contact customer support for help."""
            self.right_button_id.disabled = True
        elif self.new_x_steps > self.expected_steps + 2:
            self.user_instructions_text.text = 'The old number of steps per mm was : [b]' + old_steps + """[/b] 

The new number of steps per mm is: [b]""" + new_steps + """[/b] 

[color=ff0000][b]This is outside of the expected range, please repeat the section.[/b][/color] 

If you get this result again, please contact customer support for help."""
            self.right_button_id.disabled = True
        else:
            self.user_instructions_text.text = 'The old number of steps per mm was : [b]' + old_steps + """[/b] 

The new number of steps per mm is: [b]""" + new_steps + """[/b] 

You will need to home the machine, and then repeat steps 1 and 2 to verify your results. 

 
 [color=ff0000][b]WARNING: SETTING THE NEW NUMBER OF STEPS WILL CHANGE HOW THE MACHINE MOVES.[/b][/color] 

[color=000000]Would you like to set the new number of steps?[/color]"""
            self.right_button_id.disabled = False

    def left_button(self):
        self.repeat_section()

    def right_button(self):
        set_new_steps_sequence = ['$100 =' + str(self.new_x_steps), '$$']
        self.m.s.start_sequential_stream(set_new_steps_sequence)
        self.poll_for_success = Clock.schedule_interval(self.
                                                        check_for_successful_completion, 1)

    def check_for_successful_completion(self, dt):
        if self.m.s.is_sequential_streaming == False:
            print 'New steps have been set: $100 = ' + str(self.new_x_steps)
            Clock.unschedule(self.poll_for_success)
            self.next_screen()

    def repeat_section(self):
        from asmcnc.calibration_app import screen_distance_1_x
        distance_screen1x = screen_distance_1_x.DistanceScreen1xClass(name=
                                                                      'distance1x', screen_manager=self.sm,
                                                                      machine=self.m)
        self.sm.add_widget(distance_screen1x)
        self.sm.current = 'distance1x'

    def skip_section(self):
        self.sm.get_screen('measurement').axis = 'Y'
        self.sm.current = 'measurement'

    def next_screen(self):
        from asmcnc.calibration_app import screen_distance_1_x
        distance_screen1x = screen_distance_1_x.DistanceScreen1xClass(name=
                                                                      'distance1x', screen_manager=self.sm,
                                                                      machine=self.m)
        self.sm.add_widget(distance_screen1x)
        self.m.request_homing_procedure('distance1x', 'calibration_complete')

    def quit_calibration(self):
        self.sm.get_screen('tape_measure_alert'
                           ).return_to_screen = 'calibration_complete'
        self.sm.get_screen('calibration_complete').calibration_cancelled = True
        self.sm.current = 'tape_measure_alert'

    def on_leave(self):
        if (self.sm.current != 'alarmScreen' and self.sm.current !=
                'errorScreen'):
            self.sm.remove_widget(self.sm.get_screen('distance4x'))
