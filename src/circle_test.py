from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen

from asmcnc.core_UI import path_utils


class CircleTest(App):
    def __init__(self, **kwargs):
        super(CircleTest, self).__init__(**kwargs)

    img = Image(source=path_utils.get_path('circle_dims.png'))
    scr = Screen(name='test')
    scr.add_widget(img)
    sm = ScreenManager()
    sm.add_widget(scr)
    sm.current = 'test'

    def build(self):
        return self.sm


if __name__ == '__main__':
    CircleTest().run()



