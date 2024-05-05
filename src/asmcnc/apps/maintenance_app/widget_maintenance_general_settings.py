from kivy.lang import Builder
from kivy.uix.widget import Widget

Builder.load_string("""
#:import color_provider asmcnc.core_UI.utils.color_provider

<GeneralSettingsWidget>

    dust_shoe_title_label:dust_shoe_title_label
    dust_shoe_info_label:dust_shoe_info_label
    interrupt_bars_title_label:interrupt_bars_title_label
    interrupt_bars_info_label:interrupt_bars_info_label

    dust_shoe_switch:dust_shoe_switch
    interrupt_bars_switch:interrupt_bars_switch

    ScrollView:
        size: self.parent.size
        pos: self.parent.pos
        orientation: 'vertical'
        
        # Add any extra settings here, just like the examples below
        GridLayout:
            id: settings_scroll_view
            cols: 1
            size_hint_y: None
            height: self.minimum_height
            padding: [dp(0.025)*app.width, 0]
            
            # Dust shoe plug detection
            BoxLayout:
                size_hint_y: None
                orientation: 'horizontal'
    
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: 2
    
                    Label:
                        id: dust_shoe_title_label
                        color: color_provider.get_rgba("black")
                        font_size: str(0.03*app.width) + 'sp'
                        halign: "left"
                        markup: True
                        text_size: self.size
    
                    Label:
                        id: dust_shoe_info_label
                        color: color_provider.get_rgba("black")
                        font_size: str(0.0225*app.width) + 'sp'
                        halign: "left"
                        markup: True
                        text_size: self.size
    
                BoxLayout:
                    padding: [dp(0.15)*app.width, 0, 0, 0]
    
                    Switch:
                        id: dust_shoe_switch
            
            # Interrupt bars activation
            BoxLayout:
                size_hint_y: None
                orientation: 'horizontal'

                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: 2

                    Label:
                        id: interrupt_bars_title_label
                        color: color_provider.get_rgba("black")
                        font_size: str(0.03*app.width) + 'sp'
                        halign: "left"
                        markup: True
                        text_size: self.size

                    Label:
                        id: interrupt_bars_info_label
                        color: color_provider.get_rgba("black")
                        font_size: str(0.0225*app.width) + 'sp'
                        halign: "left"
                        markup: True
                        text_size: self.size

                BoxLayout:
                    padding: [dp(0.15)*app.width, 0, 0, 0]

                    Switch:
                        id: interrupt_bars_switch

"""
)


class GeneralSettingsWidget(Widget):
    def __init__(self, **kwargs):
        super(GeneralSettingsWidget, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.m = kwargs["machine"]
        self.l = kwargs["localization"]
        self.sett = kwargs["settings"]
        self.update_strings()

        self.interrupt_bars_switch.active = self.sett.interrupt_bars_active
        self.interrupt_bars_switch.bind(active=self.toggle_interrupt_bars)

    def update_strings(self):
        self.dust_shoe_title_label.text = self.l.get_bold("Dust shoe plug detection")
        self.dust_shoe_info_label.text = self.l.get_str("When activated, the dust shoe needs to be inserted when starting the spindle or running jobs.")

        self.interrupt_bars_title_label.text = self.l.get_bold("Interrupt bars activation")
        self.interrupt_bars_info_label.text = self.l.get_str("When disabled, the interrupt bars will not work.")

    def toggle_interrupt_bars(self, instance, value):
        if value:
            self.sett.enable_interrupt_bars()
        else:
            self.sett.disable_interrupt_bars()
