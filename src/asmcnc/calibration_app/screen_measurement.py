'''
Created on 12 December 2019
Landing Screen for the Calibration App

@author: Letty
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.widget import Widget

from asmcnc.calibration_app import screen_backlash

Builder.load_string("""

<MeasurementScreenClass>:
    image_select:image_select

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
                    root.next_screen()
                    
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

            BoxLayout:
                orientation: 'vertical'
                # spacing: 10
                size_hint_x: 1.3
                 
                Label:
                    size_hint_y: 0.5
                    font_size: '35sp'
                    text: '[color=000000]X Measurement[/color]'
                    markup: True

                Image:
                    id: image_select
                    source: "./asmcnc/skavaUI/img/x_measurement_1.PNG"
                    center_x: self.parent.center_x
                    center_y: self.parent.center_y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

            BoxLayout:
                orientation: 'vertical'
                # spacing: 10
                # padding: 10
                size_hint_x: 0.6

                Label:
                    id: instruction
                    text_size: self.size
                    font_size: '18sp'
                    halign: 'left'
                    valign: 'middle'
                    text: root.instruction
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
                                #size_hint_y: 1
                                font_size: '20sp'
                                text: 'Next'
                        
            
""")

class MeasurementScreenClass(Screen):
    
    instruction = StringProperty()
    image_select = ObjectProperty()
    go_to_next_screen = False
    
    def __init__(self, **kwargs):
        super(MeasurementScreenClass, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']

        self.instruction = '[color=000000]Use the guard post on the Z head as a reference point for the end of the tape measure.[/color]'
        
    def skip_to_lobby(self):
        self.sm.current = 'lobby'
        
    def repeat_section(self):
        if self.go_to_next_screen == True:
            self.go_to_next_screen = False
            self.instruction = '[color=000000]Use the guard post on the Z head as a reference point for the end of the tape measure.[/color]'
            self.image_select.source = "./asmcnc/skavaUI/img/x_measurement_1.PNG"
        else: 
            self.sm.current = 'prep'
          
    def next_instruction(self):
        if self.go_to_next_screen == False:
            self.instruction = '[color=000000]Use the home end end plate as an edge to measure against.[/color]'
            self.image_select.source = "./asmcnc/skavaUI/img/x_measurement_2.PNG"
            self.go_to_next_screen = True
        else: 
            self.next_screen()
        
    def next_screen(self):
        if not self.sm.has_screen('backlash'):
            backlash_screen = screen_backlash.BacklashScreenClass(name = 'backlash', screen_manager = self.sm, machine = self.m)
            self.sm.add_widget(backlash_screen)
        self.sm.current = 'backlash'