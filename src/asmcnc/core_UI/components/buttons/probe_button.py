from kivy.uix.button import Button
from asmcnc.skavaUI.screen_probing import ProbingScreen
from kivy.uix.image import Image


class ProbeButton(Button):
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

    def __init__(self, router_machine, screen_manager, localization):
        super(ProbeButton, self).__init__()

        self.sm = screen_manager
        self.m = router_machine
        self.l = localization

        self.image = Image(source="./asmcnc/skavaUI/img/z_probe.png", size = self.size, pos = self.pos, allow_stretch = True)
        self.add_widget(self.image)

        self.bind(size=self.update_image_size)
        self.bind(pos=self.update_image_pos)

        # When the button is pressed, open the popup
        self.bind(on_press=self.open_screen)

        # When the probe_z_coord is updated, close the popup
        self.m.bind(probe_z_coord=self.close_screen)

        self.probing_screen = ProbingScreen(name = 'probing', screen_manager = self.sm, machine = self.m, localization = self.l)
        if not self.sm.has_screen('probing'):
            self.sm.add_widget(self.probing_screen)

    def update_image_size(self, instance, value):
        self.image.size = value

    def update_image_pos(self, instance, value):
        self.image.pos = value

    def open_screen(self, *args):
        print("Opening probing screen")
        self.return_screen = self.sm.current # Store screen where button present (for returning to it after probing)
        self.sm.current = 'probing'

    def close_screen(self, *args):
        print("Closing probing screen")
        self.sm.current = self.sm.return_to_screen

