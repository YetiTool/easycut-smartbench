from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock

Builder.load_string("""
<ZHeadQCDB2>:

    Label:
        text: 'Updating database...'
        font_size: dp(50)

""")

class ZHeadQCDB2(Screen):
    def __init__(self, **kwargs):
        super(ZHeadQCDB2, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']

    def on_enter(self):
        # Temporary solution, simulate update by waiting
        Clock.schedule_once(self.enter_next_screen, 3)

    def enter_next_screen(self, dt):
        self.sm.current = 'qcDB3'