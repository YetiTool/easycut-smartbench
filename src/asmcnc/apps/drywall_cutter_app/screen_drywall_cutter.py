from datetime import datetime

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_string("""
<DrywallCutterScreen>:

    Button:
        on_press: root.quit_to_lobby()
        text: 'Quit'

""")

def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + message)

class DrywallCutterScreen(Screen):

    def __init__(self, **kwargs):
        super(DrywallCutterScreen, self).__init__(**kwargs)

        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.l = kwargs['localization']
        self.gtg = kwargs['geometry_to_gcode']

    def quit_to_lobby(self):
        self.sm.current = 'lobby'
