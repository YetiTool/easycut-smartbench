from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from asmcnc.core_UI.components.base_label import LabelBase
from asmcnc.core_UI.hoverable import InspectorSingleton


# from asmcnc.core_UI.components.base_label import LabelBase


class AddWidgetPopup(Popup):
    def __init__(self, widget):
        super(AddWidgetPopup, self).__init__(title='Add widget',
                                            size_hint=(None, None),
                                            size=(400, 300),
                                            pos=(200, 150))
        self.inspector = InspectorSingleton()
        self.inspector.bind(on_show_popup=self.open_me)
        self.widget_to_add_to = widget
        self.main_layout = FloatLayout()
        self.add_widget(self.main_layout)
        self.btn_ok = Button(size=(50, 50), size_hint=(None, None), pos=(self.x + 340, self.y - 50), text='Add')
        self.btn_ok.bind(on_press=self.add_widget_to_selection)
        self.main_layout.add_widget(self.btn_ok)
        self.btn_cancel = Button(size=(50, 50), size_hint=(None, None), pos=(self.x + 10, self.y - 50), text='Cancel')
        self.btn_cancel.bind(on_press=self.dismiss)
        self.main_layout.add_widget(self.btn_cancel)

    def open_me(self, *args):
        self.open()

    def add_widget_to_selection(self, *args):
        w = self.inspector.widget
        tmp = LabelBase(text='Inspector Widget was here!',
                    size_hint=(None, None),
                    size=(250, dp(20)),
                    font_size=dp(20),
                    pos=(60, 70),
                    # pos=(w.x + 10, w.y + 10),
                    color=(0.1, 1, 0.1, 1))
        w.add_widget(tmp)
        self.dismiss()

