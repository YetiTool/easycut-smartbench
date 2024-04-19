from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.image import Image

from asmcnc.core_UI.hoverable import HoverBehavior


class ButtonBase(Button, HoverBehavior):
    """
    The ButtonBase class is the base class for all our buttons we use in our screens and apps.
    It offers base functionality that every button needs e.g. setting the size so that every button looks the same.

    Base classes:
     - kivy.uix.button.Button
     - asmcnc.core_UI.hoverable.HoverBehaviour
    """
    def __init__(self, **kwargs):
        super(ButtonBase, self).__init__(**kwargs)


class ImageButtonBase(ButtonBehavior, Image, HoverBehavior):
    """
    The ImageButton class is a button that uses an image as its background.

    Base classes:
     - kivy.uix.image.Image
     - kivy.uix.behaviors.ButtonBehavior

    Additional notes:
    This is an abstract class and must not be instantiated directly!
    """
    def __init__(self, **kwargs):
        super(ImageButtonBase, self).__init__(**kwargs)
