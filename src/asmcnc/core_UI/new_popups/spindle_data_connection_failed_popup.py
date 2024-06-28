from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from asmcnc.comms.localization import Localization
from asmcnc.core_UI import scaling_utils
from asmcnc.core_UI.new_popups.popup_bases import PopupBase, PopupErrorTitle


body_text = """SmartBench failed to read the data from the SC2 Spindle motor, which is needed to measure the load. Please check that you are using your SC2 Spindle motor, and the data cable is properly secured.

If this problem persists, please submit a support ticket containing the exported diagnostics file, either via the QR code or visit www.yetitool.com/support > Submit a ticket.

You can also skip exporting the report, but there is a risk the error will happen again."""


class SpindleDataConnectionFailedPopup(PopupBase):
    """Popup shown to the user when the spindle data connection fails."""

    def __init__(self, **kwargs):
        super(SpindleDataConnectionFailedPopup, self).__init__(**kwargs)

        localisation = Localization()

        title = PopupErrorTitle(localisation=localisation, size_hint_y=0.15)
        self.root_layout.add_widget(title)

        body_layout = BoxLayout(size_hint_y=0.7)
        self.root_layout.add_widget(body_layout)

        description_and_qr_layout = BoxLayout(orientation="horizontal", size_hint_x=0.5)
        body_layout.add_widget(description_and_qr_layout)

        description_layout = BoxLayout(orientation="vertical", size_hint_x=0.7)
        description_and_qr_layout.add_widget(description_layout)

        qr_layout = BoxLayout(orientation="vertical", size_hint_x=0.3)
        description_and_qr_layout.add_widget(qr_layout)

        description_text = Label(text=body_text, color=(0, 0, 0, 1), font_size=scaling_utils.get_scaled_sp("15sp"))
        description_text.bind(size=description_text.setter("text_size"))

        description_layout.add_widget(description_text)

        button_layout = BoxLayout(size_hint_y=0.15)
        self.root_layout.add_widget(button_layout)


if __name__ == "__main__":
    from kivy.base import runTouchApp

    popup = SpindleDataConnectionFailedPopup(size_hint=(0.8, 0.8))
    popup.open()
    runTouchApp()
