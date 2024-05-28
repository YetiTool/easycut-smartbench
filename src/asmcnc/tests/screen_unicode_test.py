"""
Unicode test screen

"""

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty

Builder.load_string(
    """

<ScreenClass>:

    canvas:
        Color: 
            rgba: hex('##FAFAFA')
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
                text_size: self.size
                font_size: '40sp'
                halign: 'center'
                valign: 'middle'
                text: root.string_test
                markup: 'True'
                color: [0,0,0,1]
"""
)


class ScreenClass(Screen):
    string_test = ""

    def __init__(self, **kwargs):
        self.sm = kwargs.pop("screen_manager")
        self.m = kwargs.pop("machine")
        super(ScreenClass, self).__init__(**kwargs)
