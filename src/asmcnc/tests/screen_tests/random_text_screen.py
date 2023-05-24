"""
@author archiejarvis on 24/05/2023
"""

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock


Builder.load_string("""
<RandomTextScreen>:
    BoxLayout:
        Label:
            id: random_text_label
            color: [1, 0, 0, 1]
            text: ''
            
""")


class RandomTextScreen(Screen):
    def __init__(self, **kwargs):
        super(RandomTextScreen, self).__init__(**kwargs)
        Clock.schedule_interval(self.randomise_text, 0.1)

    def randomise_text(self, dt):
        text = 'Mx: ' + str(dt)

        self.ids.random_text_label.text = text