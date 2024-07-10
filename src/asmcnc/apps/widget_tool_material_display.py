from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

import kivy.utils

from asmcnc.core_UI import scaling_utils
from asmcnc.core_UI.utils import color_provider


class ToolMaterialDisplayWidget(BoxLayout):
    padding = (dp(3), dp(3), dp(3), dp(3))

    def __init__(self, config, **kwargs):
        super(ToolMaterialDisplayWidget, self).__init__(**kwargs)

        self.config = config

        self.material_text = ""
        self.tool_text = ""

        # Set the background color
        background_color = color_provider.get_rgba("shapes_white")
        with self.canvas.before:
            Color(*background_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(pos=self.update_rect, size=self.update_rect)

        self.tool_material_label = Label(text="", halign="left", valign="top",
                                         font_size=scaling_utils.get_scaled_sp("13sp"),
                                         color=color_provider.get_rgba("black"), center_y=self.center_y)
        self.tool_material_label.bind(size=self.tool_material_label.setter("text_size"))

        self.add_widget(self.tool_material_label)

        config.bind(active_profile=self.on_active_profile)

        self.update_tool_material_label()

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_active_profile(self, *args):
        self.material_text = self.config.active_profile.material.description
        self.tool_text = self.config.active_cutter.description
        self.update_tool_material_label()

    def update_tool_material_label(self):
        self.tool_material_label.text = "Material: {}\nTool:\n{}".format(self.material_text, self.tool_text)
