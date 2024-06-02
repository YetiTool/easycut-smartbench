import os
from functools import partial

from kivy.clock import Clock
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.image import Image

from asmcnc import paths
from asmcnc.core_UI.components.buttons.button_base import ImageButtonBase
from asmcnc.core_UI.components.widgets.blinking_widget import FastBlinkingWidget, BlinkingWidget

SPINDLE_ON_IMAGE = os.path.join(paths.SKAVA_UI_IMG_PATH, "spindle_on.png")
SPINDLE_OFF_IMAGE = os.path.join(paths.SKAVA_UI_IMG_PATH, "spindle_off.png")
RED_NO_SIGN_IMAGE = os.path.join(paths.SKAVA_UI_IMG_PATH, "off_icon.png")


class SpindleButton(ImageButtonBase, BlinkingWidget):
    """A custom button widget used for spindle functionality."""

    source = StringProperty(SPINDLE_OFF_IMAGE)
    allow_stretch = BooleanProperty(True)

    def __init__(self, router_machine, serial_connection, screen_manager, **kwargs):
        super(SpindleButton, self).__init__(**kwargs)

        self.router_machine = router_machine
        self.serial_connection = serial_connection
        self.screen_manager = screen_manager

        self.overlay_image = Image(source=RED_NO_SIGN_IMAGE, pos_hint={"center_x": 0.75, "center_y": 0.25},
                                   size_hint=(None, None), size=(self.width / 2, self.height / 2))
        self.bind(pos=self.__update_overlay_image, size=self.__update_overlay_image)
        self.add_widget(self.overlay_image)

        self.serial_connection.bind(spindle_on=self.__on_spindle_on)
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
        If the spindle is off, it shows the safety popup.
        If the spindle is on, it turns it off.

        :return: None
        """
        if not self.serial_connection.spindle_on:
            self.screen_manager.pm.show_spindle_safety_popup(None, self.router_machine.turn_on_spindle)
        else:
            self.router_machine.turn_off_spindle()

    def __on_spindle_on(self, instance, value):
        """
        Callback for the spindle_on event. Changes the overlay image opacity and starts/stops the blinking.

        :param instance: the instance of the variable that changed
        :param value: the new value of the spindle_on property from SerialConnection
        :return: None
        """
        Clock.schedule_once(partial(self.__update_images, value))

    def __update_images(self, value, *args):
        """
        Update the button image and the overlay image opacity.
        Called from Clock.schedule_once as otherwise the image wouldn't update properly.

        :param value: the new value of the spindle_on property from SerialConnection
        :param args:
        :return: None
        """
        self.overlay_image.opacity = 0 if value else 1
        self.source = SPINDLE_ON_IMAGE if value else SPINDLE_OFF_IMAGE
        self.blinking = value
