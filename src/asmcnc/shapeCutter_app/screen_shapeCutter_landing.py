'''
Created on 19 February 2020
Landing Screen for the Shape Cutter App

@author: Letty
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_string("""

<ShapeCutterLandingScreenClass>:

    user_instruction: user_instruction
    
    canvas:
        Color: 
            rgba: hex('#FFFFFF')
        Rectangle: 
            size: self.size
            pos: self.pos
             
    BoxLayout:
        orientation: 'horizontal'
        padding: 90,50
        spacing: 0
        size_hint_x: 1

        BoxLayout:
            orientation: 'vertical'
            size_hint_x: 0.8
             
            Label:
                size_hint_y: 1
                font_size: '35sp'
                text: '[color=263238]Welcome to the Shape Cutter[/color]'
                markup: True

            Label:
                id: user_instruction
                size_hint_y: 2
                text_size: self.size
                font_size: '18sp'
                halign: 'center'
                valign: 'middle'
                markup: True

            Label:
                text_size: self.size
                font_size: '18sp'
                halign: 'center'
                valign: 'middle'
                text: '[color=546E7A]Select a shape to cut...[/color]'
                markup: True
                
            BoxLayout:
                orientation: 'horizontal'
                padding: 0, 0
                spacing: 20
            
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
                        root.skip_to_lobby()
                        
                    BoxLayout:
                        padding: 5
                        size: self.parent.size
                        pos: self.parent.pos
                        
                        Label:
                            #size_hint_y: 1
                            font_size: '20sp'
                            text: '[color=455A64]No[/color]'
                            markup: True

                Button:
                    size_hint_y:0.9
                    id: getout_button
                    size: self.texture_size
                    valign: 'top'
                    halign: 'center'
                    disabled: False
                    background_normal: ''
                    background_color: hex('#C5E1A5')
                    on_press: 
                        root.next_screen()
                        
                    BoxLayout:
                        padding: 5
                        size: self.parent.size
                        pos: self.parent.pos
                        
                        Label:
                            #size_hint_y: 1
                            font_size: '20sp'
                            text: '[color=455A64]Yes[/color]'
                            markup: True
            
""")

class ShapeCutterLandingScreenClass(Screen):
    
    user_instruction = ObjectProperty()
    
    def __init__(self, **kwargs):
        super(ShapeCutterLandingScreenClass, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        
        self.user_instruction.text  = ''

    def skip_to_lobby(self):
        self.sm.current = 'lobby'
        
    def next_screen(self):
        pass

    def on_leave(self):
        self.sm.remove_widget(self.sm.get_screen('shapeCutter_landing'))