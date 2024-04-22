from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from asmcnc.comms.localization import Localization
from asmcnc.core_UI import scaling_utils
from asmcnc.core_UI.new_popups import popup_bases
from asmcnc.core_UI.utils import color_provider


class SpindleLoadAlertPopup(popup_bases.PopupBase):
    def __init__(self, **kwargs):
        super(SpindleLoadAlertPopup, self).__init__(**kwargs)
        localisation = Localization()

        title = popup_bases.PopupTitle(title_text=localisation.get_bold("Spindle read error"),
                                       image_path=popup_bases.ERROR_ICON_PATH,
                                       separator_colour=color_provider.get_rgba("red"),
                                       size_hint_y=0.15, localisation=localisation)
        self.root_layout.add_widget(title)

        body_layout = BoxLayout(orientation="vertical", size_hint_y=0.7)


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
