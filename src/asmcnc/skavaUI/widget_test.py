import os
os.environ['KIVY_GL_BACKEND'] = 'sdl2'

import math
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, ListProperty, BooleanProperty

Builder.load_string("""

#:import hex kivy.utils.get_color_from_hex

<Test>:

    BoxLayout:
        size: root.size
        padding: 20
        orientation: 'vertical'
        
        canvas:
            Color: 
                rgba: 0.5,1,1,1

        TextInput:
            id: text_1
            text: "My TextInput"
            size_hint_x: 1
            font_size:24
            on_touch_up:
                self.select_all()
            
        Label:
            text: 'HELLO'
            size_hint_x: 1

""")

class Test(Widget):

    def __init__(self, **kwargs):
        super(Test, self).__init__(**kwargs)

    #https://gitlab.com/kivymd/KivyMD/issues/45
    def on_touch_up(self, touch):
        if self.collide_point(touch.x, touch.y):
            return True


class MyApp(App):

    def build(self):
        print ("MyApp")
        return Test()


if __name__ == '__main__':
    MyApp().run()
