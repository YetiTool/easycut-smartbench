"""
@author archiejarvis on 24/05/2023
"""

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock


from random import uniform


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
        Clock.schedule_interval(lambda dt: self.randomise_text(), 1)

    def randomise_text(self):
        text = 'Mx: ' + str(uniform(0, 100))

        self.ids.random_text_label.text = text