from datetime import datetime

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_string("""
<DrywallCutterScreen>:

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'horizontal'
            padding: dp(5)
            spacing: dp(10)

            Button:
                size_hint_x: 7
                text: 'Home'

            Button:
                size_hint_x: 7
                text: 'File'

            Button:
                size_hint_x: 7
                text: 'Tool'

            Button:
                size_hint_x: 7
                text: 'Shape'

            Button:
                size_hint_x: 7
                text: 'Rotate'

            Button:
                size_hint_x: 7
                text: 'Cut on line'
                text_size: self.size
                halign: 'center'
                valign: 'middle'

            Button:
                size_hint_x: 7
                text: 'Material setup'
                text_size: self.size
                halign: 'center'
                valign: 'middle'

            Button:
                size_hint_x: 15
                text: 'STOP'

            Button:
                size_hint_x: 7
                on_press: root.quit_to_lobby()
                text: 'Quit'

        BoxLayout:
            size_hint_y: 5
            orientation: 'horizontal'
            padding: dp(5)
            spacing: dp(10)

            BoxLayout:
                size_hint_x: 55

                canvas:
                    Color:
                        rgba: hex('#E5E5E5FF')
                    Rectangle:
                        size: self.size
                        pos: self.pos

            BoxLayout:
                size_hint_x: 23
                orientation: 'vertical'
                spacing: dp(10)

                BoxLayout:
                    size_hint_y: 31

                    canvas:
                        Color:
                            rgba: hex('#E5E5E5FF')
                        Rectangle:
                            size: self.size
                            pos: self.pos

                BoxLayout:
                    size_hint_y: 7
                    orientation: 'horizontal'
                    spacing: dp(10)

                    Button:
                        text: 'Simulate'

                    Button:
                        text: 'Save'

                    Button:
                        text: 'Run'

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
