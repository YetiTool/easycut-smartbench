from kivy.app import App
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
        padding: app.get_scaled_tuple([20.0, 0])

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
                padding: app.get_scaled_tuple([120.0, 0, 0, 0])

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
        self.usm = App.get_running_app().user_settings_manager

        # dust_shoe_detection:
        self.usm.bind(dust_shoe_detection=lambda i, value: setattr(self.dust_shoe_switch, 'active', value))
        self.dust_shoe_switch.bind(active=lambda i, value: self.usm.set_value('dust_shoe_detection', value))
        self.dust_shoe_switch.active = self.usm.get_value('dust_shoe_detection')

        self.update_strings()

    def update_strings(self):
        self.dust_shoe_title_label.text = self.l.get_bold(self.usm.get_title('dust_shoe_detection'))
        self.dust_shoe_info_label.text = self.l.get_str(self.usm.get_description('dust_shoe_detection'))
