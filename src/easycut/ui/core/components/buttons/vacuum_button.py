import os
from functools import partial

from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.image import Image

from asmcnc import paths
from asmcnc.core_UI.components.buttons.button_base import ImageButtonBase
from asmcnc.core_UI.components.widgets.blinking_widget import FastBlinkingWidget

EXTRACTOR_IMAGE = os.path.join(paths.SKAVA_UI_IMG_PATH, "extraction_on.png")
RED_NO_SIGN_IMAGE = os.path.join(paths.SKAVA_UI_IMG_PATH, "off_icon.png")


class VacuumButton(ImageButtonBase, FastBlinkingWidget):
    """A custom button widget used for vacuum functionality."""

    source = StringProperty(EXTRACTOR_IMAGE)
    allow_stretch = BooleanProperty(True)

    def __init__(self, router_machine, serial_connection, **kwargs):
        super(VacuumButton, self).__init__(**kwargs)

        self.router_machine = router_machine
        self.serial_connection = serial_connection

        self.overlay_image = Image(source=RED_NO_SIGN_IMAGE, pos_hint={"center_x": 0.75, "center_y": 0.25},
                                   size_hint=(None, None), size=(self.width / 2, self.height / 2))
        self.bind(pos=self.__update_overlay_image, size=self.__update_overlay_image)
        self.add_widget(self.overlay_image)

        self.serial_connection.bind(vacuum_on=self.__on_vacuum_on)
        self.bind(on_press=self.__on_press)

    def __update_overlay_image(self, *args):
        """
        Update the overlay image, so it stays in the same position relative to the button.
        :param args:
        :return:
        """
        self.overlay_image.pos = (self.right - self.overlay_image.width, self.top - self.overlay_image.height)

    def __on_press(self, *args):
        """
        Handles what happens when the button is pressed.
        If the vacuum is off, it turns it on.
        If the vacuum is on, it turns it off.

        :return: None
        """
        if not self.serial_connection.vacuum_on:
            self.router_machine.turn_on_vacuum()
        else:
            self.router_machine.turn_off_vacuum()

    def __on_vacuum_on(self, instance, value):
        """
        Callback for the vacuum_on event. Changes the button image and starts/stops the blinking.

        :param instance: the instance of the variable that changed
        :param value: the new value of the vacuum_on property from SerialConnection
        :return:
        """
        Clock.schedule_once(partial(self.__update_image, value))

    def __update_image(self, value, *args):
        """
        Update the opacity of the overlay image and the blinking.
        Called from Clock.schedule_once as otherwise the image wouldn't update properly.

        :param value: the new value of the vacuum_on property from SerialConnection
        :param args: unused dt argument from clock
        :return:
        """
        self.overlay_image.opacity = 0 if value else 1
        self.blinking = value