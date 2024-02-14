from kivy.uix.button import Button


class ProbeButton(Button):
    # background_color = (244. / 255, 43. / 255, 36. / 255, 1)
    background_normal = "./asmcnc/skavaUI/img/z_probe.png"

    def __init__(self, router_machine):
        super(ProbeButton, self).__init__()

        self.router_machine = router_machine

        # When the probe_z_coord is updated, close the popup
        self.router_machine.bind(probe_z_coord=self.close_popup)
        self.bind(on_press=self.open_popup)

    def open_popup(self, *args):
        print("Opening popup")
        self.router_machine.probe_z()

    def close_popup(self, *args):
        print("Closing popup")

