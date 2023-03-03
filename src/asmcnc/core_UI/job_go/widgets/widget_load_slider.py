from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.button import  Button
from functools import partial


Builder.load_string("""
<LoadSliderWidget>:
    load_label:load_label
    power_slider:power_slider
    button_container:button_container
    BoxLayout:
        orientation: 'vertical'
        size: self.parent.size
        pos: self.parent.pos
        padding: 0
        Label:
            id: load_label
            text: "900 W" 
            markup: True
            halign: "center" 
            valign: "middle"
            color: 0, 0, 0, 1
            font_size: '20sp'

        BoxLayout:
            orientation: 'horizontal'

            Label: 
                text: "400 W"
                color: 0, 0, 0, 1
                markup: True
                halign: "center" 
                valign: "middle"
                size_hint_x: 0.1
                font_size: '14sp'

            Slider:
                id: power_slider
                min: 400
                max: 1000
                step: 10
                on_value: root.on_slider_value_change()
                size_hint_x: 0.8

            Label: 
                text: "1000 W"
                color: 0, 0, 0, 1
                markup: True
                halign: "center" 
                valign: "middle"
                size_hint_x: 0.1
                font_size: '14sp'

        BoxLayout:
            id: button_container
            orientation: 'horizontal'
            # buttons made in init

                
""")

class LoadSliderWidget(Widget):
    def __init__(self, **kwargs):
        super(LoadSliderWidget, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']
        # self.l = kwargs['localization']
        # self.yp = kwargs['yetipilot']

        self.power_slider.value = 700
        self.on_slider_value_change()

        self.make_buttons(self.button_container, self.power_slider, -100)
        self.make_buttons(self.button_container, self.power_slider, -10)
        self.make_buttons(self.button_container, self.power_slider, +10)
        self.make_buttons(self.button_container, self.power_slider, +100)

    def make_buttons(self, container, slider, val):
        button_adjust_func = partial(self.button_adjust_slider, val)
        container.add_widget(Button(text=str(val), on_press=button_adjust_func))

    def button_adjust_slider(self, val, instance=None):
        self.power_slider.value+=val

    def on_slider_value_change(self):
        self.load_label.text = "[b]" + str(int(self.power_slider.value)) + " W" + "[/b]" 