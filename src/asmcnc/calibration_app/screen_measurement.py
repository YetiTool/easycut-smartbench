'''
Created on 12 December 2019
Screen to inform user about how to conduct measurements during calibration. 

X-measurement: 
 Has 3 sub screens: just pictures and text
 
Y measurement: 
 Has 2 sub screens: just pictures and text

@author: Letty
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.widget import Widget

from asmcnc.calibration_app import screen_backlash
from asmcnc.calibration_app import screen_distance_1_x

Builder.load_string("""

<MeasurementScreenClass>:
    image_select:image_select
    action_button:action_button
    instruction_top:instruction_top
    instruction_left:instruction_left

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
                        font_size: '20sp'
                        text: 'Repeat section'

            Button:
                size_hint_y:0.9
                id: getout_button
                size: self.texture_size
                valign: 'top'
                halign: 'center'
                disabled: False
                on_press: 
                    root.skip_section()
                    
                BoxLayout:
                    padding: 5
                    size: self.parent.size
                    pos: self.parent.pos
                    
                    Label:
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
                on_press: 
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

            Label:
                id: instruction_left
                size_hint_x: 0.4
                size: self.texture_size
                text_size: self.size
                halign: 'left'
                valign: 'middle'
                markup: True

            BoxLayout:
                orientation: 'vertical'
                size_hint_x: 1.3
                 
                Label:
                    id: instruction_top
                    size_hint_y: 0.2
                    size: self.texture_size
                    #font_size: '16sp'
                    text_size: self.size
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
                padding: 10
                size_hint_x: 0.3
                  
                Button:
                    id: action_button
                    size_hint_y: 0.9
                    size: self.texture_size
                    valign: 'middle'
                    halign: 'center'
                    disabled: False
                    on_press: 
                        root.next_instruction()
                        
                    BoxLayout:
                        padding: 5
                        size: self.parent.size
                        pos: self.parent.pos
                        
                        Label:
                            font_size: '20sp'
                            text: 'Next'
                        
            
""")

class MeasurementScreenClass(Screen):
    
    instruction_top = ObjectProperty()
    instruction_left = ObjectProperty()
    image_select = ObjectProperty()
    action_button = ObjectProperty()
    go_to_next_screen = False
    
    sub_screen_count = 0
    axis = StringProperty()
    
    def __init__(self, **kwargs):
        super(MeasurementScreenClass, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']

    def on_pre_enter(self):
        
        if self.axis == 'X':
            self.screen_x_1()
        elif self.axis == 'Y':
            self.screen_y_1()

    def refresh_screen(self):
        self.sub_screen_count = 0
        if self.axis == 'X':
            self.screen_x_1()
        elif self.axis == 'Y':
            self.screen_y_1()

    def screen_x_1(self):
        self.instruction_left.text = '[color=000000][b]' + self.axis + ' measurement: [/b]\n\nUse a tape measure to find the position of the Z head.\n\n' \
                            'Lay the measure in the rail. Push the end up to the carriage [b](1)[/b], and measure off the end plate [b](2)[/b].[/color]'
        self.instruction_top.text = ''
        self.instruction_top.size_hint_y = 0
        self.instruction_left.size_hint_x = 0.4
        self.image_select.source = "./asmcnc/calibration_app/img/x_measurement_img_1.PNG"

    def screen_x_2(self):
        self.instruction_top.text = '[color=000000]The tape end [b](1)[/b] must push up against the guard post under the Z head [b](2)[/b].[/color]'
        self.instruction_left.text = ''
        self.instruction_top.size_hint_y = 0.2
        self.instruction_left.size_hint_x = 0        
        self.image_select.source = "./asmcnc/calibration_app/img/x_measurement_img_2.PNG"
        
    def screen_x_3(self):
        self.instruction_top.text = '[color=000000]Use the home end plate [b](1)[/b] as an edge [b](2)[/b] to measure against.[/color]'
        self.instruction_left.text = ''
        self.instruction_top.size_hint_y = 0.2
        self.instruction_left.size_hint_x = 0       
        self.image_select.source = "./asmcnc/calibration_app/img/x_measurement_img_3.PNG"
        
    def screen_y_1(self):
        self.instruction_top.text = '[color=000000][b]Y measurement:[/b] lay tape on top of bench [b](1)[/b], threading underneath the X beam [b](2)[/b].' \
                            'Tape end should be hooked at the home end [b](3)[/b], so that the lowest measurement number is at the home end [b](3)[/b].[/color]'
        self.instruction_left.text = ''
        self.instruction_top.size_hint_y = 0.2
        self.instruction_left.size_hint_x = 0
        self.image_select.source = "./asmcnc/calibration_app/img/y_measurement_img_1.PNG"
    
    def screen_y_2(self):
        self.instruction_left.text = '[color=000000]Use a scraper blade [b](1)[/b], or block, pushed against the inside surface of the beam [b](2)[/b] ' \
                            'to take a measurement of the beam\'s position against the tape measure.[/color]'
        self.instruction_top.text = ''
        self.instruction_top.size_hint_y = 0
        self.instruction_left.size_hint_x = 0.4
        self.image_select.source = "./asmcnc/calibration_app/img/y_measurement_img_2.PNG"
    
    def next_instruction(self):
        
        if self.axis == 'X':
            if self.sub_screen_count == 0:
                self.screen_x_2()
                self.sub_screen_count = 1
            elif self.sub_screen_count == 1:
                self.screen_x_3()
                self.sub_screen_count = 2
            elif self.sub_screen_count == 2:
                self.next_screen()
                
        if self.axis == 'Y':
            if self.sub_screen_count == 0:
                self.screen_y_2()
                self.sub_screen_count = 1
            elif self.sub_screen_count == 1: 
                self.next_screen()
    
    def skip_to_lobby(self):
        self.sm.current = 'lobby'
        
    def repeat_section(self):
        
        if self.axis == 'X':
            if self.sub_screen_count >= 1: 
                self.refresh_screen()
            else: 
                self.sm.current = 'prep'
        if self.axis == 'Y':
            if self.sub_screen_count >= 1: 
                self.refresh_screen()
            else:
                if not self.sm.has_screen('distance1x'):
                    distance_screen1x = screen_distance_1_x.DistanceScreen1Class(name = 'distance1x', screen_manager = self.sm, machine = self.m)
                    self.sm.add_widget(distance_screen1x)
                self.sm.current = 'distance1x'
    
    def skip_section(self):
        self.next_screen()
        
    def next_screen(self):
        self.sub_screen_count = 0
        if not self.sm.has_screen('backlash'):
            backlash_screen = screen_backlash.BacklashScreenClass(name = 'backlash', screen_manager = self.sm, machine = self.m)
            self.sm.add_widget(backlash_screen)

        self.sm.get_screen('backlash').axis = self.axis         # pass across axis variable

        if self.axis == 'X':
            self.sm.get_screen('backlash').screen_x_1() # these don't work if returning from wait screen
        elif self.axis == 'Y':
            self.sm.get_screen('backlash').screen_y_1()
        
        self.sm.current = 'backlash'