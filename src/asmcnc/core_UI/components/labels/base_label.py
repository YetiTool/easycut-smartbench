from kivy.app import App
from kivy.uix.label import Label

from asmcnc.core_UI.hoverable import HoverBehavior


class LabelBase(Label, HoverBehavior):
    """
    Description:
    This is the base class for all labels that we use in our apps. It offers base functionality that every label needs.
    """
    def __init__(self, **kwargs):
        super(LabelBase, self).__init__(**kwargs)
        # get Localization instance from App
        # not needed yet, as Labels don't take care of their text themselves
        # self.l = App.get_running_app().l

