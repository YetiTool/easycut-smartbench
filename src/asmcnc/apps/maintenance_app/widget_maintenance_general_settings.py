from kivy.lang import Builder
from kivy.uix.widget import Widget

Builder.load_string("""

<GeneralSettingsWidget>

    dust_shoe_title_label:dust_shoe_title_label
    dust_shoe_info_label:dust_shoe_info_label

    dust_shoe_switch:dust_shoe_switch

    BoxLayout:
        size: self.parent.size
        pos: self.parent.pos
        orientation: 'vertical'
        padding: [dp(0.025)*app.width, 0]

        BoxLayout:
            size_hint_y: 0.4
            orientation: 'horizontal'

            BoxLayout:
                orientation: 'vertical'
                size_hint_x: 2

                Label:
                    id: dust_shoe_title_label
                    color: [0,0,0,1]
                    font_size: str(0.03*app.width) + 'sp'
                    halign: "left"
                    markup: True
                    text_size: self.size

                Label:
                    id: dust_shoe_info_label
                    color: [0,0,0,1]
                    font_size: str(0.0225*app.width) + 'sp'
                    halign: "left"
                    markup: True
                    text_size: self.size

            BoxLayout:
                padding: [dp(0.15)*app.width, 0, 0, 0]

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
