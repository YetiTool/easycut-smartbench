from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from asmcnc.core_UI import scaling_utils
from asmcnc.core_UI.utils import color_provider


class ToolMaterialDisplayWidget(BoxLayout):
    padding = (dp(3), dp(3), dp(3), dp(3))

    def __init__(self, config, **kwargs):
        super(ToolMaterialDisplayWidget, self).__init__(**kwargs)

        self.material_text = "MDF"
        self.tool_text = ""

        self.tool_material_label = Label(text="Tool:", halign="left", valign="top",
                                         font_size=scaling_utils.get_scaled_sp("13sp"),
                                         color=color_provider.get_rgba("black"), center_y=self.center_y)
        self.tool_material_label.bind(size=self.tool_material_label.setter("text_size"))

        self.add_widget(self.tool_material_label)

        config.bind(active_cutter=self.on_active_cutter)

    def on_active_cutter(self, instance, value):
        self.tool_text = value.tool_id
        self.update_tool_material_label()

    def on_active_material(self, instance, value):
        self.material_text = value
        self.update_tool_material_label()

    def update_tool_material_label(self):
        self.tool_material_label.text = "Tool:\n{}\nMaterial: {}".format(self.tool_text, self.material_text)
