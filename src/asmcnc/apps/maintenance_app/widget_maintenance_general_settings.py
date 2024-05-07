from kivy.lang import Builder
from kivy.uix.widget import Widget

Builder.load_string("""
#:import color_provider asmcnc.core_UI.utils.color_provider

<GeneralSettingsWidget>

    dust_shoe_title_label:dust_shoe_title_label
    dust_shoe_info_label:dust_shoe_info_label

    dust_shoe_switch:dust_shoe_switch

    BoxLayout:
        size: self.parent.size
        pos: self.parent.pos
        orientation: 'vertical'
        padding: app.get_scaled_tuple([20.0, 0.0])

        BoxLayout:
            size_hint_y: 0.4
            orientation: 'horizontal'

            BoxLayout:
                orientation: 'vertical'
                size_hint_x: 2

                Label:
                    id: dust_shoe_title_label
                    color: color_provider.get_rgba("black")
                    font_size: app.get_scaled_sp('24.0sp')
                    halign: "left"
                    markup: True
                    text_size: self.size

                Label:
                    id: dust_shoe_info_label
                    color: color_provider.get_rgba("black")
                    font_size: app.get_scaled_sp('18.0sp')
                    halign: "left"
                    markup: True
                    text_size: self.size

            BoxLayout:
                padding: app.get_scaled_tuple([120.0, 0.0, 0.0, 0.0])

                Switch:
                    id: dust_shoe_switch

        BoxLayout

"""
)


class GeneralSettingsWidget(Widget):
    def __init__(self, **kwargs):
        super(GeneralSettingsWidget, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.m = kwargs["machine"]
        self.l = kwargs["localization"]
        self.update_strings()

    def update_strings(self):
        self.dust_shoe_title_label.text = self.l.get_bold("Dust shoe plug detection")
        self.dust_shoe_info_label.text = self.l.get_str("When activated, the dust shoe needs to be inserted when starting the spindle or running jobs.")
