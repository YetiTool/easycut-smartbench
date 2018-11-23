import os
os.environ['KIVY_GL_BACKEND'] = 'sdl2'

import kivy
from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
from kivy.app import App

from asmcnc.skavaUI import widget_vj_polygon

class MyApp(App):
    ''' Test harness '''

    def build(self):
        return widget_vj_polygon.PolygonVJ()


if __name__ == '__main__':
    MyApp().run()
