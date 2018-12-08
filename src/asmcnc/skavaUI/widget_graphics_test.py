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

<GraphicsTest>:

    BoxLayout:
        padding: 20
        spacing: 20
        size: root.size
        pos: root.pos

        canvas:
            Color: 
                rgba: 0.5,1,1,1
            Line:
                points: root.points             

""")

class GraphicsTest(Widget):

    points = ListProperty([(500, 500),
                          [300, 300, 500, 300],
                          [500, 400, 600, 400]])


    def __init__(self, **kwargs):
        super(GraphicsTest, self).__init__(**kwargs)


class MyApp(App):

    def build(self):
        print ("MyApp")
        return GraphicsTest()


if __name__ == '__main__':
    MyApp().run()
