from kivy.uix.button import Button
from asmcnc.skavaUI.screen_probing import ProbingScreen


class ProbeButton(Button):
    background_normal = "./asmcnc/skavaUI/img/z_probe.png"

    def __init__(self, router_machine, screen_manager, localization):
        super(ProbeButton, self).__init__()

        self.sm = screen_manager
        self.m = router_machine
        self.l = localization

        # When the button is pressed, open the popup
        self.bind(on_press=self.open_screen)

        # When the probe_z_coord is updated, close the popup
        self.m.bind(probe_z_coord=self.close_screen)

        if not self.sm.has_screen('probing'):
            self.probing_screen = ProbingScreen(name = 'probing', screen_manager = self.sm, machine = self.m, localization = self.l)
            self.sm.add_widget(self.probing_screen)

    def open_screen(self, *args):
        print("Opening probing screen")
        self.sm.current = 'probing'

    def close_screen(self, *args):
        print("Closing probing screen")
        self.sm.current = self.sm.return_to_screen

