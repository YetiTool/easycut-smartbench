from datetime import datetime

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_string("""
<GeberitCutterScreen>:

    BoxLayout:
        orientation: 'horizontal'

        canvas:
            Color:
                rgba: hex('#E2E2E2FF')
            Rectangle:
                size: self.size
                pos: self.pos

""")

def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + message)

class GeberitCutterScreen(Screen):

    def __init__(self, **kwargs):
        super(GeberitCutterScreen, self).__init__(**kwargs)

        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.l = kwargs['localization']
