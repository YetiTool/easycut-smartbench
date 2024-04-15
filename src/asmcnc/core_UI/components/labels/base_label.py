from kivy.app import App
from kivy.uix.label import Label

from asmcnc.core_UI.hoverable import HoverBehavior


class LabelBase(Label, HoverBehavior):
    def __init__(self, **kwargs):
        super(LabelBase, self).__init__(**kwargs)
        # get Localization instance from App
        self.l = App.get_running_app().l

