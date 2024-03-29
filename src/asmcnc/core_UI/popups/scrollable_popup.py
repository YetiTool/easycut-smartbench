from kivy.base import runTouchApp
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.scrollview import ScrollView

from asmcnc.core_UI import scaling_utils


class PopupBase(ModalView):
    def __init__(self, **kwargs):
        super(PopupBase, self).__init__(**kwargs)
        self.background = ""


class ScrollablePopupBase(PopupBase):
    def __init__(self, text, **kwargs):
        super(ScrollablePopupBase, self).__init__(**kwargs)
        root_layout = BoxLayout(orientation="vertical")
        separator = PopupSeparator(text="Error", background_color=[1, 1, 1, 1], size_hint_y=0.15)
        root_layout.add_widget(separator)

        scroll_view = ScrollView()
        label = Label(
            text=text,
            markup=True,
            font_size=scaling_utils.get_scaled_sp("15sp"),
            color=[0, 0, 0, 1],
        )
        scroll_view.add_widget(label)
        root_layout.add_widget(scroll_view)

        self.add_widget(root_layout)


class PopupSeparator(BoxLayout):
    def __init__(self, text, **kwargs):
        super(PopupSeparator, self).__init__(**kwargs)

        self.orientation = "vertical"

        image_label_layout = BoxLayout(orientation="horizontal", size_hint_x=0.15)
        image = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon_scaled_up.png")
        label = Label(text=text, color=[0, 0, 0, 1], font_size=scaling_utils.get_scaled_sp("18sp"))
        image_label_layout.add_widget(image)
        image_label_layout.add_widget(label)

        separator_line = BoxLayout(background_color=[1, 0, 0, 1], size_hint_y=None, height=dp(2))

        self.add_widget(image_label_layout)
        self.add_widget(separator_line)


class JobValidationPopup(ScrollablePopupBase):
    def __init__(self, text, **kwargs):
        super(JobValidationPopup, self).__init__(text, **kwargs)


if __name__ == "__main__":
    popup = JobValidationPopup(
        text="This is a test popup. It is a test popup that is used to test the popup functionality.\n",
        size_hint=(0.8, 0.8),
    )
    popup.open()
    runTouchApp()
