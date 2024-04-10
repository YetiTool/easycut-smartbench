from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen

from asmcnc.core_UI.ScreenDesigner.add_widget_popup import AddWidgetPopup


class ScreenTemplateApp(App):
    def __init__(self, **kwargs):
        super(ScreenTemplateApp, self).__init__(**kwargs)

    def build(self):


        sm = ScreenManager()
        template = Screen(name='template')
        base_layout = FloatLayout()
        template.add_widget(base_layout)

        sm.add_widget(template)

        designer_popup = AddWidgetPopup(base_layout)

        return sm

if __name__ == '__main__':
    ScreenTemplateApp().run()
