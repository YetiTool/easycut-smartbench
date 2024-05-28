from kivy.base import runTouchApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from asmcnc.comms.localization import Localization
from asmcnc.core_UI import scaling_utils
from asmcnc.core_UI.new_popups.popup_bases import (
    PopupBase,
    PopupErrorTitle,
    PopupScrollableBody,
)
from asmcnc.core_UI.utils import color_provider


def get_text_from_list(text_list):
    """Get a string from a list of strings, each string in the list will be on a new line.

    For usage in an RstDocument, where new lines are not automatically added.
    :param text_list: A list of strings to concatenate.
    :return: A string with each element of the list on a new line."""
    return "\n\n".join(text_list)


class JobValidationPopup(PopupBase):
    """Popup that displays a list of issues found while validating a job.
    :param text: The text to display in the popup."""

    def __init__(self, text, **kwargs):
        super(JobValidationPopup, self).__init__(**kwargs)
        localisation = Localization()
        title = PopupErrorTitle(size_hint_y=0.15, localisation=localisation)
        self.root_layout.add_widget(title)
        sub_title = Label(
            text=localisation.get_str(
                "While checking your job, these issues were found:"
            ),
            size_hint_y=0.1,
            color=color_provider.get_rgba("black"),
            font_size=scaling_utils.get_scaled_sp("16sp"),
            valign="middle",
        )
        sub_title.bind(size=sub_title.setter("text_size"))
        self.root_layout.add_widget(sub_title)
        body = PopupScrollableBody(text=text, size_hint_y=0.6)
        self.root_layout.add_widget(body)
        button_layout = BoxLayout(size_hint_y=0.15)
        button_layout.add_widget(
            Button(
                text=localisation.get_bold("Ok"),
                on_press=self.dismiss,
                background_color=color_provider.get_rgba("green"),
                background_normal="",
                font_size=scaling_utils.get_scaled_sp("15sp"),
                markup=True,
            )
        )
        self.root_layout.add_widget(button_layout)


if __name__ == "__main__":
    popup = JobValidationPopup(
        text="This is a REALLY LONG STRING\n\n" * 20, size_hint=(0.8, 0.8)
    )
    popup.open()
    runTouchApp()
