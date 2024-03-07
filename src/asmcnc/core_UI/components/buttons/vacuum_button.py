import os
from functools import partial

from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty

from asmcnc.core_UI import path_utils
from asmcnc.core_UI.components.buttons.button_base import ImageButtonBase
from asmcnc.core_UI.components.widgets.blinking_widget import BlinkingWidget

SKAVA_UI_PATH = path_utils.get_path("skavaUI")[0]  # bug with get_path currently returns a list
SKAVA_UI_IMG_PATH = os.path.join(SKAVA_UI_PATH, "img")
VACUUM_ON_IMAGE = os.path.join(SKAVA_UI_IMG_PATH, "vac_on.png")
VACUUM_OFF_IMAGE = os.path.join(SKAVA_UI_IMG_PATH, "extraction_off.png")


class VacuumButton(ImageButtonBase, BlinkingWidget):
    """A custom button widget used for vacuum functionality."""

    source = StringProperty(VACUUM_OFF_IMAGE)
    allow_stretch = BooleanProperty(True)

    def __init__(self, router_machine, serial_connection, **kwargs):
        super(VacuumButton, self).__init__(**kwargs)

        self.router_machine = router_machine
        self.serial_connection = serial_connection

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
        Clock.schedule_once(partial(self.__update_image_source, value))
        self.blinking = value

    def __update_image_source(self, value, *args):
        self.source = VACUUM_ON_IMAGE if value else VACUUM_OFF_IMAGE
