from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from asmcnc.comms.localization import Localization
from asmcnc.core_UI.new_popups.popup_bases import (
    PopupBase,
    PopupWarningTitle,
    PopupScrollableBody,
)
from asmcnc.core_UI.utils import color_provider


class SpindleHealthCheckPopup(PopupBase):

    def __init__(self, machine, callback, **kwargs):
        super(SpindleHealthCheckPopup, self).__init__(**kwargs)
        self.machine = machine
        self.localisation = Localization()
        self.title = PopupWarningTitle(size_hint_y=0.15, localisation=self.localisation)
        self.root_layout.add_widget(self.title)
        text = (
            self.localisation.get_str(
                "SmartBench will lift the spindle motor and attempt to turn it on."
            )
            + "\n\n"
            + self.localisation.get_str("The spindle motor may spin at high speeds.")
            + "\n\n"
            + self.localisation.get_str(
                "Ensure both the power cable and data cable for the spindle motor are securely connected."
            )
            + "\n\n"
            + self.localisation.get_str(
                "Do not proceed until the spindle motor is clamped safely in the Z Head, and the dust shoe plug is fitted."
            )
            + "\n\n"
            + self.localisation.get_str("Do you want to continue?")
        )
        body = PopupScrollableBody(text=text, size_hint_y=0.7)
        self.root_layout.add_widget(body)
        button_layout = BoxLayout(size_hint_y=0.15, spacing=dp(20))
        button_layout.add_widget(
            Button(
                text=self.localisation.get_bold("No"),
                on_press=self.dismiss,
                background_color=color_provider.get_rgba("red"),
                background_normal="",
                font_size=20,
                markup=True,
            )
        )
        button_layout.add_widget(
            Button(
                text=self.localisation.get_bold("Yes"),
                on_press=callback,
                background_color=color_provider.get_rgba("green"),
                background_normal="",
                font_size=20,
                markup=True,
            )
        )
        self.root_layout.add_widget(button_layout)


if __name__ == "__main__":
    from kivy.base import runTouchApp

    popup = SpindleHealthCheckPopup(machine=None, size_hint=(0.8, 0.8))
    popup.open()
    runTouchApp()
