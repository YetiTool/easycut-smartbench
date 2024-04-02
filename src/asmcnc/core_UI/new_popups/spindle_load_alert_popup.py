from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from asmcnc.comms.localization import Localization
from asmcnc.core_UI import scaling_utils
from asmcnc.core_UI.new_popups.popup_bases import PopupBase, PopupErrorTitle


class SpindleLoadAlertPopup(PopupBase):
    def __init__(self, **kwargs):
        super(SpindleLoadAlertPopup, self).__init__(**kwargs)
        localisation = Localization()

        title = PopupErrorTitle(size_hint_y=0.15, localisation=localisation)
        self.root_layout.add_widget(title)

        sub_title = Label(text=localisation.get_str("SmartBench has detected that the spindle is not sending valid "
                                                    "load data. Please check the spindle connection!"),
                          size_hint_y=0.7, color=(0, 0, 0, 1), font_size=scaling_utils.get_scaled_sp("16sp"),
                          valign="middle", halign="center")
        sub_title.bind(size=sub_title.setter("text_size"))
        self.root_layout.add_widget(sub_title)

        button_layout = BoxLayout(size_hint_y=0.15)
        button_layout.add_widget(Button(text=localisation.get_bold("Ok"), on_press=self.dismiss,
                                        background_color=[230 / 255., 74 / 255., 25 / 255., 1.], background_normal="",
                                        font_size=scaling_utils.get_scaled_sp("15sp"), markup=True))
        self.root_layout.add_widget(button_layout)


if __name__ == "__main__":
    from kivy.base import runTouchApp

    popup = SpindleLoadAlertPopup(size_hint=(0.8, 0.8))
    popup.open()
    runTouchApp()
