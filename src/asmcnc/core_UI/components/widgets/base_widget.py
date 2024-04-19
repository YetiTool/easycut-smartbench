from kivy.uix.widget import Widget

from asmcnc.core_UI.hoverable import HoverBehavior


class WidgetBase(Widget, HoverBehavior):
    """
    The WidgetBase class is the base class for all our widgets we use in our screens and apps.
    It offers base functionality that every widget needs.

    Base classes:
     - kivy.uix.widget.Widget
     - asmcnc.core_UI.hoverable.HoverBehaviour
    """
    def __init__(self, **kwargs):
        super(WidgetBase, self).__init__(**kwargs)
