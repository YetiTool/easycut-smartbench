from enum import Enum
from kivy.graphics import Color, Line
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.rst import RstDocument
from kivy.uix.scrollview import ScrollView
from kivy.utils import get_color_from_hex

from asmcnc.core_UI import scaling_utils
from asmcnc.core_UI.utils import color_provider


class PopupBase(ModalView):
    """Base class for all popups in the app. This class is meant to be subclassed and not used directly.
    Add widgets to the root_layout to add content to the popup.
    Use the PopupTitle class to add a title to the popup.

    :param kwargs: Kwargs to pass to the ModalView constructor."""

    def __init__(self, **kwargs):
        super(PopupBase, self).__init__(**kwargs)
        self.background = ""

        self.root_layout = GridLayout(cols=1, spacing=dp(10), padding=[dp(20), dp(10), dp(20), dp(10)])
        self.add_widget(self.root_layout)


class PopupTitle(BoxLayout):
    """Title bar for popups. Contains an icon and a title. This class is meant to be subclassed and not used
    directly."""

    def __init__(self, title_text, image_path, separator_colour, **kwargs):
        super(PopupTitle, self).__init__(**kwargs)
        self.separator_colour = separator_colour

        self.orientation = "vertical"

        image_label_layout = BoxLayout(orientation="horizontal", size_hint_y=0.85,
                                       padding=[0, dp(10), 0, dp(10)])
        image = Image(source=image_path, size_hint_x=None, width=dp(40))
        image_label_layout.add_widget(image)

        spacer = BoxLayout(size_hint=(0.01, 1))
        image_label_layout.add_widget(spacer)

        self.label = Label(text=title_text, color=get_color_from_hex("#000000"), font_size=20)
        self.label.bind(size=self.on_label_size)
        image_label_layout.add_widget(self.label)

        self.add_widget(image_label_layout)

        self.bind(size=self.update_separator_line)

    def update_separator_line(self, instance, value):
        self.canvas.before.clear()  # Clear previous drawing
        with self.canvas.before:
            Color(*self.separator_colour)
            Line(points=[self.x + 2, self.y, self.x + self.width - 2, self.y], width=dp(2), cap="square")

    def on_label_size(self, instance, value):
        self.label.pos = (self.label.pos[0], self.label.pos[1] + 5)  # Cheat way to center the label
        self.label.text_size = (self.label.size[0], None)


class PopupErrorTitle(PopupTitle):
    """Title bar for error popups. Contains an icon and a title."""

    def __init__(self, localisation, **kwargs):
        super(PopupErrorTitle, self).__init__(localisation.get_str("Error!"),
                                              "./asmcnc/apps/shapeCutter_app/img/error_icon_scaled_up.png",
                                              (1, 0, 0, 1), **kwargs)


class PopupWarningTitle(PopupTitle):
    """Title bar for error popups. Contains an icon and a title."""

    def __init__(self, localisation, **kwargs):
        super(PopupWarningTitle, self).__init__(localisation.get_str("Warning!"),
                                                "./asmcnc/apps/shapeCutter_app/img/error_icon_scaled_up.png",
                                                color_provider.get_rgba("red"), **kwargs)


scroll_view_kv = """
<ScrollView>:
    bar_width: app.get_scaled_width(6.0)
    _handle_y_pos: (self.right - self.bar_width - self.bar_margin) if self.bar_pos_y == 'right' else (self.x + self.bar_margin), self.y + self.height * self.vbar[0]
    _handle_y_size: min(self.bar_width, self.width), self.height * self.vbar[1]
    _handle_x_pos: self.x + self.width * self.hbar[0], (self.y + self.bar_margin) if self.bar_pos_x == 'bottom' else (self.top - self.bar_margin - self.bar_width)
    _handle_x_size: self.width * self.hbar[1], min(self.bar_width, self.height)
    canvas.after:
        Color:
            rgba: [0, 0, 0, 0.2] if (self.do_scroll_y and self.viewport_size[1] > self.height) else [0, 0, 0, 0]
        Rectangle:
            pos: root._handle_y_pos or (0, 0)
            size: root._handle_y_size or (0, 0)
        Color:
            rgba: [0, 0, 0, 0.2] if (self.do_scroll_x and self.viewport_size[0] > self.width) else [0, 0, 0, 0]
        Rectangle:
            pos: root._handle_x_pos or (0, 0)
            size: root._handle_x_size or (0, 0)
"""

Builder.load_string(scroll_view_kv)  # Overwrite the default ScrollView styling to change colour and width of scrollbar


class PopupScrollableBody(ScrollView):
    """Body of a popup that contains a scrollable text area"""

    def __init__(self, text, **kwargs):
        super(PopupScrollableBody, self).__init__(**kwargs)

        rst_doc = RstDocument(text=text, markup=True, font_size=scaling_utils.get_scaled_sp("15sp"),
                              background_color=get_color_from_hex("#f3f3f3"))
        self.add_widget(rst_doc)
