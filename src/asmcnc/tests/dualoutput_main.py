# Using Kivy Framework, this example module provides a basic touchscreen interface 
# on official RasPi 3 touchscreen.
# A button press runs a separate python app (dualoutput_sub.py)
# which is configured to run through RasPi HMDI output.
# It is important to note that both instances are unconnected - this is an undesirable
# sideffect of trying to get 2 different results on 2 different outputs on the RasPi 3.
# Comms between the two instances, if needed, is a separate topic ;-)

from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '440')
import os
os.environ["KIVY_BCM_DISPMANX_ID"] = "4" #LCD 

from  kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.base import runTouchApp
import subprocess


Builder.load_string("""

<TouchScreen>:

    BoxLayout:
        orientation: 'vertical'
        padding: 30
        spacing: 30
        Label:
            text: 'Click button to run HDMI app'
        Button:
            text: 'Run HDMI output'
            on_release: root.hdmi_go()
                    
""")

class TouchScreen(Screen):

    def hdmi_go(self):
        print 'opening projector sequence'
        subprocess.Popen("python dualoutput_sub.py", stdout=subprocess.PIPE, shell=True)

runTouchApp(TouchScreen())