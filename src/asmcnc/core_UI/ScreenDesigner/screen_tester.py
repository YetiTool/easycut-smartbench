from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

from asmcnc.core_UI.ScreenDesigner.add_widget_popup import AddWidgetPopup
from asmcnc.core_UI.ScreenDesigner.generated_screens.new_screen import NewScreen
from asmcnc.core_UI.hoverable import InspectorSingleton



class ScreenTemplateApp(App):
    def __init__(self, **kwargs):
        super(ScreenTemplateApp, self).__init__(**kwargs)

    def build(self):

        sm = ScreenManager()
        template = NewScreen(name='NewScreen')
        sm.add_widget(template)

        designer_popup = AddWidgetPopup(template.children[0])
        inspector = InspectorSingleton()
        inspector.widget = template.children[0]

        return sm

if __name__ == '__main__':
    ScreenTemplateApp().run()
