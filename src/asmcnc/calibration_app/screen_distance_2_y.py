"""
Created on 12 December 2019
Screen 2 to help user calibrate distances for Y axis

Step 2: Inform user of measurement after machine has moved, and ask user if they want to adjust steps per mm 

@author: Letty
"""
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from asmcnc.calibration_app import screen_distance_3_y

Builder.load_string(
    """

<DistanceScreen2yClass>:

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
                background_color: hex('#D6EAF8')
                on_press: 
                    root.repeat_section()
                    
                BoxLayout:
                    padding: 5
                    size: self.parent.size
                    pos: self.parent.pos
                    
                    Label:
                        font_size: '20sp'
                        text: '[color=455A64]Go Back[/color]'
                        markup: True

            Button:
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
                on_press: 
                    root.quit_calibration()
                    
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
                        background_color: hex('#FFF59D')
                        on_press: 
                            root.left_button()
                            
                        BoxLayout:
                            padding: 5
                            size: self.parent.size
                            pos: self.parent.pos
                            
                            Label:
                                id: improve_button_label
                                #size_hint_y: 1
                                font_size: '20sp'
                                text: '[color=455A64]I want to try to improve the result[/color]'
                                markup: True

                    Button:
                        size_hint_y:0.9

                        valign: 'top'
                        halign: 'center'
                        disabled: False
                        background_normal: ''
                        background_color: hex('#C5E1A5')
                        on_press: 
                            root.right_button()
                            
                        BoxLayout:
                            padding: 5
                            size: self.parent.size
                            pos: self.parent.pos
                            
                            Label:
                                id: continue_button_label
                                text_size: self.size
                                text: '[color=455A64]Ok, it measures as expected. Move to the next section.[/color]'
                                font_size: '18sp'
                                valign: 'middle'
                                halign: 'center'
                                markup: True   
"""
)


class DistanceScreen2yClass(Screen):
    title_label = ObjectProperty()
    improve_button_label = ObjectProperty()
    continue_button_label = ObjectProperty()
    user_instructions_text = ObjectProperty()
    initial_y_cal_move = NumericProperty()
    y_cal_measure_1 = NumericProperty()

    def __init__(self, **kwargs):
        self.sm = kwargs.pop("screen_manager")
        self.m = kwargs.pop("machine")
        super(DistanceScreen2yClass, self).__init__(**kwargs)

    def on_pre_enter(self):
        measure_string = str(self.initial_y_cal_move + self.y_cal_measure_1)
        self.title_label.text = "[color=000000]Y Distance:[/color]"
        self.user_instructions_text.text = (
            """Re-measure distance between the beam and the home end. 

[b]The distance should measure """
            + measure_string
            + "[/b]"
        )
        self.continue_button_label.text = """[color=455A64]Ok, it measures as expected.
 Finish calibration.[/color]"""

    def left_button(self):
        self.next_screen()

    def right_button(self):
        self.skip_section()

    def repeat_section(self):
        from asmcnc.calibration_app import screen_distance_1_y

        distance_screen1y = screen_distance_1_y.DistanceScreen1yClass(
            name="distance1y", screen_manager=self.sm, machine=self.m
        )
        self.sm.add_widget(distance_screen1y)
        self.sm.current = "distance1y"

    def skip_section(self):
        self.sm.get_screen("calibration_complete").calibration_cancelled = False
        self.sm.get_screen(
            "tape_measure_alert"
        ).return_to_screen = "calibration_complete"
        self.sm.current = "tape_measure_alert"

    def quit_calibration(self):
        self.sm.get_screen(
            "tape_measure_alert"
        ).return_to_screen = "calibration_complete"
        self.sm.get_screen("calibration_complete").calibration_cancelled = True
        self.sm.current = "tape_measure_alert"

    def next_screen(self):
        if not self.sm.has_screen("distance3y"):
            distance3y_screen = screen_distance_3_y.DistanceScreen3yClass(
                name="distance3y", screen_manager=self.sm, machine=self.m
            )
            self.sm.add_widget(distance3y_screen)
        self.sm.get_screen("distance3y").y_cal_measure_1 = self.y_cal_measure_1
        self.sm.current = "distance3y"

    def on_leave(self):
        if self.sm.current != "alarmScreen" and self.sm.current != "errorScreen":
            self.sm.remove_widget(self.sm.get_screen("distance2y"))
