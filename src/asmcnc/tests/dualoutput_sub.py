# Example app to demonstrate kivy output on RasPi 3 HDMI
# Simple label counter ticks up to infinity

import os
os.environ["KIVY_BCM_DISPMANX_ID"] = "5" #HDMI 

from  kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.base import runTouchApp
from kivy.clock import Clock
from kivy.properties import NumericProperty # @UnresolvedImport (for Eclipse users)


Builder.load_string("""

<HDMITestScreen>:

    Label:
        font_size: 50
        text: str(root.label_number)                    

""")

class HDMITestScreen(Screen):

    label_number = NumericProperty(0)

    def __init__(self, **kwargs):
        super(HDMITestScreen, self).__init__(**kwargs)
        Clock.schedule_interval(self.increment_label_number, 1)

    def increment_label_number(self, dt):
        self.label_number += 1
        
runTouchApp(HDMITestScreen())