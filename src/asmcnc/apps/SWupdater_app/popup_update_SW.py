"""
@author Letty
Info pop-up for SW Update app
"""

from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window

from asmcnc.core_UI.components.labels.base_label import LabelBase
from asmcnc.core_UI.utils import color_provider


class PopupBetaUpdate(Widget):
    def __init__(self, screen_manager, wifi_or_usb, **kwargs):
        super(PopupBetaUpdate, self).__init__(**kwargs)
        self.sm = screen_manager

        description = (
            "The update you are trying to install is a beta release.\n\n"
            + "This is a version of the software that allows our developers and product testers to "
            + "try out new features and identify any bugs before the next customer release.\n\n"
            + "This release might not be stable, and it is recommended that you wait until the full "
            + "update. If you decide to update and you have any issues, please contact Yeti Tool support.\n\n"
            + "Do you want to continue?"
        )

        def do_update(*args):
            if wifi_or_usb == "wifi":
                self.sm.get_screen("update").get_sw_update_over_wifi()
            elif wifi_or_usb == "usb":
                self.sm.get_screen("update").get_sw_update_over_usb()

        if Window.height >= 800: #Console 10"
            image_source = "./asmcnc/apps/shapeCutter_app/img/error_icon_scaled_up.png"
        else:
            image_source = "./asmcnc/apps/shapeCutter_app/img/error_icon.png"
        img = Image(
            source=image_source,
            allow_stretch=False
        )
        label = LabelBase(
            size_hint_y=2.0,
            font_size=str(15.0 / 800.0 * Window.width) + "sp",
            text_size=(620.0 / 800.0 * Window.width, None),
            halign="center",
            valign="middle",
            text=description,
            color=color_provider.get_rgba("black"),
            padding=[0, 0],
            markup=True,
        )

        ok_button = Button(text="[b]Yes[/b]", markup=True, font_size = str(15.0 / 800 * Window.width) + "sp")
        ok_button.background_normal = ""
        ok_button.background_color = color_provider.get_rgba("green")
        back_button = Button(text="[b]No[/b]", markup=True, font_size = str(15.0 / 800 * Window.width) + "sp")
        back_button.background_normal = ""
        back_button.background_color = color_provider.get_rgba("red")

        btn_layout = BoxLayout(
            orientation="horizontal", spacing= 15.0 / 800.0 * Window.width, padding=[
                                                                                0,
                                                                                5.0 / 480.0 * Window.height, 
                                                                                0, 
                                                                                0]
        )
        btn_layout.add_widget(back_button)
        btn_layout.add_widget(ok_button)

        layout_plan = BoxLayout(
            orientation="vertical", spacing= 10.0 / 800.0 * Window.width, padding=[
                                                                                30.0 / 800.0 * Window.width, 
                                                                                20.0 / 480.0 * Window.height, 
                                                                                30.0 / 800.0 * Window.width, 
                                                                                0]
        )
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)

        popup = Popup(
            title="Warning!",
            title_color=color_provider.get_rgba("black"),
            title_size=str(20.0 / 800.0 * Window.width) + "sp",
            content=layout_plan,
            size_hint=(None, None),
            size=(
                700.0 / 800.0 * Window.width, 
                450.0 / 480.0 * Window.height
                ),
            auto_dismiss=False,
        )

        popup.separator_color = color_provider.get_rgba("red")
        popup.separator_height = str(4.0 / 480 * Window.height) + "dp"
        popup.background = "./asmcnc/apps/shapeCutter_app/img/popup_background.png"

        ok_button.bind(on_press=popup.dismiss)
        ok_button.bind(on_press=do_update)
        back_button.bind(on_press=popup.dismiss)

        popup.open()
