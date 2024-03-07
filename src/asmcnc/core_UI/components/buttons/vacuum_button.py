import os
from functools import partial

from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.image import Image

from asmcnc.core_UI import path_utils
from asmcnc.core_UI.components.buttons.button_base import ImageButtonBase
from asmcnc.core_UI.components.widgets.blinking_widget import BlinkingWidget

SKAVA_UI_PATH = path_utils.get_path("skavaUI")[0]  # bug with get_path currently returns a list
SKAVA_UI_IMG_PATH = os.path.join(SKAVA_UI_PATH, "img")
VACUUM_ON_IMAGE = os.path.join(SKAVA_UI_IMG_PATH, "extraction_on.png")
RED_NO_SIGN = os.path.join(SKAVA_UI_IMG_PATH, "red_no_sign.png")


class VacuumButton(ImageButtonBase, BlinkingWidget):
    """A custom button widget used for vacuum functionality."""

    source = StringProperty(VACUUM_ON_IMAGE)
    allow_stretch = BooleanProperty(True)

    def __init__(self, router_machine, serial_connection, **kwargs):
        super(VacuumButton, self).__init__(**kwargs)

        self.router_machine = router_machine
        self.serial_connection = serial_connection

        self.overlay_image = Image(source=RED_NO_SIGN, pos_hint={"center_x": 0.75, "center_y": 0.25},
                                   size_hint=(0.25, 0.25))
        self.add_widget(self.overlay_image)

        self.serial_connection.bind(vacuum_on=self.__on_vacuum_on)
        self.bind(on_press=self.__on_press)

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
        self.blinking = value

    def __update_image(self, value, *args):
        """
        Updates the overlay image's opacity based on the vacuum_on property.
        :param value: the new value of the vacuum_on property from SerialConnection
        :param args: unused dt parameter from Clock
        :return: None
        """
        self.overlay_image.opacity = 0 if value else 1