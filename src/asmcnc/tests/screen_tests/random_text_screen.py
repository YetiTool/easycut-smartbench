"""
@author archiejarvis on 24/05/2023
"""

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock


from string import ascii_lowercase, ascii_uppercase, digits
import random
import threading
import time

Builder.load_string("""
<RandomTextScreen>:
    BoxLayout:
        Label:
            id: random_text_label
            color: [1, 1, 1, 1]
            text: ''
            
            
""")


class RandomTextScreen(Screen):

    option_i = 0
    options = [
        '199%',
        '200%'
    ]

    length_i = 0

    def __init__(self, **kwargs):
        super(RandomTextScreen, self).__init__(**kwargs)
        # Clock.schedule_interval(self.randomise_text, 0.1)
        # # self.set_text_from_options()

        threading.Thread(target=self.clock_thread).start()

    def clock_thread(self):
        while True:
            Clock.schedule_once(self.set_text_by_length, 0.1)
            time.sleep(0.1)

    def randomise_text(self, dt=None):
        text = 'Mx: ' + str(dt)

        self.ids.random_text_label.text = text

    def set_text_from_options(self, dt=None):
        self.ids.random_text_label.text = self.options[self.option_i]

        if self.option_i == len(self.options) - 1:
            self.option_i = 0
        else:
            self.option_i += 1

        Clock.schedule_once(self.set_text_from_options, 1)

    def set_text_by_length(self, dt=None):
        text = ''.join(random.choice(ascii_lowercase + ascii_uppercase + digits + ' ') for _ in range(self.length_i))

        self.ids.random_text_label.text = text

        if self.length_i == 20:
            self.length_i = 0
        else:
            self.length_i += 1
