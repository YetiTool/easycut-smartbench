from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from mock.mock import MagicMock

from asmcnc.comms.localization import Localization
from asmcnc.core_UI import scaling_utils
from asmcnc.core_UI.new_popups import popup_bases
from asmcnc.core_UI.utils import color_provider

RED = color_provider.get_rgba("red")
BLACK = color_provider.get_rgba("black")
GREEN = color_provider.get_rgba("green")

MAIN_STRING = (
    "SmartBench failed to read the data from the SC2 Spindle motor, which is needed to measure the load. "
    "Please check that you are using your SC2 Spindle motor, and the data cable is properly secured.\n\n"
    "If this problem persists, please submit a support ticket containing the exported diagnostics file, "
    "either via the QR code or visit www.yetitool.com/support > Submit a ticket."
)


class SpindleLoadAlertPopup(popup_bases.PopupBase):
    """A popup that appears when the spindle load cannot be read. This popup allows the user to cancel the job or
    continue without YetiPilot. The user can also export the diagnostics file to a USB."""
    auto_dismiss = False
    localisation = Localization()

    def __init__(self, **kwargs):  # TODO: Organise this class
        super(SpindleLoadAlertPopup, self).__init__(**kwargs)
        self.machine = App.get_running_app().machine
        self.sm = App.get_running_app().sm

        title = popup_bases.PopupTitle(
            title_text=self.localisation.get_str("Spindle read error"),
            image_path=popup_bases.ERROR_ICON_PATH,
            separator_colour=RED,
            size_hint_y=0.15,
            localisation=self.localisation,
        )
        self.root_layout.add_widget(title)

        body_layout = BoxLayout(size_hint_y=0.7, spacing=dp(10))

        text_layout = BoxLayout(size_hint_x=0.8, padding=[0, scaling_utils.get_scaled_dp_height(10), 0, 0])
        text_label = Label(
            text=MAIN_STRING,
            font_size=scaling_utils.get_scaled_sp("15sp"),
            color=BLACK,
            valign="top",
        )
        text_label.bind(size=text_label.setter("text_size"))
        text_layout.add_widget(text_label)

        qr_code_layout_wrapper = BoxLayout(size_hint_x=0.2, orientation="vertical")
        qr_code_layout = BoxLayout(orientation="vertical", size_hint_y=0.8)
        qr_code_image = Image(source="./asmcnc/core_UI/image_library/qr_codes/submit_support_ticket_qr.png", size_hint_y=0.65)
        qr_code_layout.add_widget(qr_code_image)
        export_button = Button(
            text=self.localisation.get_bold("Export diagnostics file to USB"),
            background_color=GREEN,
            background_normal="",
            font_size=scaling_utils.get_scaled_sp("13sp"),
            size_hint_x=None,
            size_hint_y=0.35,
            halign="center",
            valign="center",
            on_press=self.export_diagnostics_file,
            markup=True,
        )
        qr_code_image.bind(width=export_button.setter("width"))
        export_button.bind(size=export_button.setter("text_size"))
        qr_code_layout.add_widget(export_button)

        spacer = BoxLayout(size_hint_y=0.2)
        qr_code_layout_wrapper.add_widget(qr_code_layout)
        qr_code_layout_wrapper.add_widget(spacer)

        body_layout.add_widget(text_layout)
        body_layout.add_widget(qr_code_layout_wrapper)
        self.root_layout.add_widget(body_layout)

        button_layout = BoxLayout(size_hint_y=0.15, spacing=dp(100))
        button_layout.add_widget(
            Button(
                text=self.localisation.get_bold("Cancel job"),
                on_press=self.cancel_job,
                background_color=RED,
                background_normal="",
                font_size=scaling_utils.get_scaled_sp("15sp"),
                markup=True,
            )
        )
        button_layout.add_widget(
            Button(
                text=self.localisation.get_bold("Continue without YetiPilot"),
                on_press=self.continue_without_yetipilot,
                background_color=RED,
                background_normal="",
                font_size=scaling_utils.get_scaled_sp("15sp"),
                markup=True,
            )
        )
        self.root_layout.add_widget(button_layout)

    def cancel_job(self, *args):
        self.machine.stop_from_soft_stop_cancel()
        self.machine.s.is_ready_to_assess_spindle_for_shutdown = True  # allow spindle overload assessment to resume
        self.sm.get_screen("job_incomplete").prep_this_screen(
            "cancelled", event_number=False
        )
        self.sm.current = "job_incomplete"
        self.dismiss()

    def continue_without_yetipilot(self, *args):
        App.get_running_app().yetipilot.disable()
        self.machine._grbl_resume()
        self.dismiss()

    def export_diagnostics_file(self, *args):
        pass


if __name__ == "__main__":
    class TestApp(App):
        sm = MagicMock()
        machine = MagicMock()

        def build(self):
            return SpindleLoadAlertPopup(size_hint=(0.8, 0.8))

    TestApp().run()
