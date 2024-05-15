# -*- coding: utf-8 -*-


'''
Unicode test screen

'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty

Builder.load_string("""

<ScreenClass>:

    canvas:
        Color: 
            rgba: hex('##FAFAFA')
        Rectangle: 
            size: self.size
            pos: self.pos
             
    BoxLayout:
        orientation: 'horizontal'
        padding: app.get_scaled_tuple([90, 50])
        spacing: 0
        size_hint_x: 1

        BoxLayout:
            orientation: 'vertical'
            size_hint_x: 0.8

            Label:
                text_size: self.size
                font_size: app.get_scaled_sp('40sp')
                halign: 'center'
                valign: 'middle'
                text: root.string_test
                markup: 'True'
                color: [0,0,0,1]
""")


class ScreenClass(Screen):
    
    string_test = "" #"유니코드에 대해"

    def __init__(self, **kwargs):
        
        super(ScreenClass, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']

