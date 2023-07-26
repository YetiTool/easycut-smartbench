from datetime import datetime

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_string("""
<GeberitCutterScreen>:

    BoxLayout:
        orientation: 'horizontal'

        canvas.before:
            Color:
                rgba: hex('#E2E2E2FF')
            Rectangle:
                size: self.size
                pos: self.pos

        BoxLayout:
            size_hint_x: 0.3
            orientation: 'vertical'
            spacing: dp(10)
            padding: dp(10)
                    
            Label:
                size_hint_y: 0.3
                text: 'Geberit cutter'
                color: 0,0,0,1
                font_size: dp(28)

            Button

            Button

            TextInput:
                size_hint_y: 0.4
                font_size: dp(23)
                multiline: False
                hint_text: 'Enter filename'

            Button

        BoxLayout:
            orientation: 'vertical'

            BoxLayout:
                size_hint_y: 0.3
                orientation: 'horizontal'

                BoxLayout:
                    orientation: 'vertical'
                    spacing: dp(10)
                    padding: dp(10)

                    BoxLayout:
                        orientation: 'horizontal'
                        spacing: dp(10)

                        TextInput:
                            font_size: dp(20)
                            multiline: False
                            hint_text: 'Stock length'
                            input_filter: 'int'

                        TextInput:
                            font_size: dp(20)
                            multiline: False
                            hint_text: 'Stock width'
                            input_filter: 'int'

                        TextInput:
                            font_size: dp(20)
                            multiline: False
                            hint_text: 'Stock depth'
                            input_filter: 'int'

                    BoxLayout:
                        orientation: 'horizontal'
                        spacing: dp(10)

                        TextInput:
                            font_size: dp(20)
                            multiline: False
                            hint_text: 'Feed'
                            input_filter: 'int'

                        TextInput:
                            font_size: dp(20)
                            multiline: False
                            hint_text: 'Speed'
                            input_filter: 'int'

                        TextInput:
                            font_size: dp(20)
                            multiline: False
                            hint_text: 'Pass depth'
                            input_filter: 'int'

                        TextInput:
                            font_size: dp(20)
                            multiline: False
                            hint_text: '# of passes'
                            input_filter: 'int'

                Button:
                    size_hint_x: 0.2
                    background_color: [0,0,0,0]
                    on_press: root.quit_to_lobby()
                    BoxLayout:
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            source: "./asmcnc/apps/shapeCutter_app/img/exit_cross.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True

            BoxLayout:
                padding: [dp(0), dp(0), dp(10), dp(10)]

                BoxLayout:
                    canvas.before:
                        Color:
                            rgba: .5, .5, .5, 1
                        Line:
                            width: 2
                            rectangle: self.x, self.y, self.width, self.height

                    canvas:
                        Color:
                            rgba: 1,1,1,1
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

    def quit_to_lobby(self):
        self.sm.current = 'lobby'
