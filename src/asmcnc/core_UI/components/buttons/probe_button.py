from asmcnc.core_UI.components.buttons.button_base import ButtonBase
from asmcnc.skavaUI.screen_probing import ProbingScreen
from asmcnc.core_UI import path_utils as pu
from kivy.uix.image import Image
import os


class ProbeButton(ButtonBase):
    """
    A custom button widget used for probing functionality.

    When pressed, it opens the probing screen.

    Args:
        router_machine (RouterMachine): An instance of the RouterMachine class.
        screen_manager (ScreenManager): An instance of the ScreenManager class.
        localization (Localization): An instance of the Localization class.
    """

    background_normal = ""
    background_down = ""
    background_color = (0, 0, 0, 0)

    def __init__(self, router_machine, screen_manager, localization, fast_probe = False):
        super(ProbeButton, self).__init__()

        self.sm = screen_manager
        self.m = router_machine
        self.l = localization
        self.fp = fast_probe

        self.return_screen = None
        
        self.image = Image(source=pu.get_path("z_probe.png"), size = self.size, pos = self.pos, allow_stretch = True)
        self.add_widget(self.image)

        self.bind(size=self.update_image_size)
        self.bind(pos=self.update_image_pos)

        self.bind(on_press=self.open_screen)

    def update_image_size(self, instance, value):
        self.image.size = value

    def update_image_pos(self, instance, value):
        self.image.pos = value

    def open_screen(self, *args):
        self.return_screen = self.sm.current
        self.probing_screen = ProbingScreen(name = 'probing', screen_manager = self.sm, machine = self.m, localization = self.l, fast_probe = self.fp)
        self.probing_screen.parent_button = self
        self.sm.add_widget(self.probing_screen)
        self.sm.current = 'probing'

    def close_screen(self, *args):
        self.sm.current = self.return_screen
        if hasattr(self, 'probing_screen'):
            self.sm.remove_widget(self.probing_screen)
