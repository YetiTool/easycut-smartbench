import inspect

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

from asmcnc.comms.localization import Localization
from asmcnc.core_UI.ScreenDesigner.add_widget_popup import AddWidgetPopup


class ScreenDesignerApp(App):

    width = Window.width
    height = Window.height if Window.height == 480 else Window.height - 32

    def __init__(self, **kwargs):
        super(ScreenDesignerApp, self).__init__(**kwargs)

    def build(self):
        l = Localization()
        sm = ScreenManager()
        template = Screen(name='template')
        base_layout = FloatLayout()
        template.add_widget(base_layout)

        sm.add_widget(template)

        designer_popup = AddWidgetPopup(sm, l, base_layout)

        return sm


if __name__ == '__main__':
    ScreenDesignerApp().run()
