from  kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.base import runTouchApp
from kivy.clock import Clock

from functools import partial


Builder.load_string("""

<ClockArgTest>:
    
    button:button
    
    FloatLayout:

        Button:
            id: button
            text: 'dog.jpg'
            pos_hint: {'center_x':0.5, 'center_y': .5}
            size_hint: None, None            
            height: 200
            width: 200

""")


class ClockArgTest(Screen):

    other = "poo"

    def __init__(self, **kwargs):
        super(ClockArgTest, self).__init__(**kwargs)
        Clock.schedule_once(partial(self.change_name, 'cat', self.other), 2)

        
    def change_name(self, animal, other_variable, *largs):
        self.button.text = other_variable


runTouchApp(ClockArgTest())