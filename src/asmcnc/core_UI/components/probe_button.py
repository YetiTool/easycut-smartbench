from kivy.uix.button import Button


class ProbeButton(Button):
    size_hint_y = 1
    background_normal = "./asmcnc/skavaUI/img/z_probe.png"

    def __init__(self, router_machine):
        super(ProbeButton, self).__init__()

        self.router_machine = router_machine

        # When the button is pressed, open the popup
        self.bind(on_press=self.open_popup)

        # When the probe_z_coord is updated, close the popup
        self.router_machine.bind(probe_z_coord=self.close_popup)


    def open_popup(self, *args):
        print("Opening popup")
        self.router_machine.probe_z()

    def close_popup(self, *args):
        print("Closing popup")

