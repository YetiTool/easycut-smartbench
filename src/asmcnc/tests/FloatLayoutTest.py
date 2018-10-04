from  kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.base import runTouchApp
from kivy.clock import Clock



Builder.load_string("""

<FloatLayoutTestScreen>:
    
    FloatLayout:

        Button:
#             text: 'dog.jpg'
#             pos_hint: {'center_x':0.5, 'center_y': .5}
            size_hint: None, None            
            height: 200
            width: 200
        Label:
            text: 'dog.jpg'

""")

class FloatLayoutTestScreen(Screen):

    def __init__(self, **kwargs):
        super(FloatLayoutTestScreen, self).__init__(**kwargs)

runTouchApp(FloatLayoutTestScreen())