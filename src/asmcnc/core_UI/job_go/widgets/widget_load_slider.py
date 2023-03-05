from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.button import  Button
from functools import partial
from kivy.graphics import Color


Builder.load_string("""

<RoundedButton@Button>:
    background_color: 0,0,0,0
    canvas.before:
        Color:
            rgba: hex('#ccccccff')
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(10), dp(10)]


<LoadSliderWidget>:
    load_label:load_label
    min_label:min_label
    max_label:max_label
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
            font_size: '22sp'
            size_hint_y: 0.3

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.2
            padding: [15,0]

            Label: 
                id: min_label
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
                id: max_label
                text: "1000 W"
                color: 0, 0, 0, 1
                markup: True
                halign: "center" 
                valign: "middle"
                size_hint_x: 0.1
                font_size: '14sp'

        BoxLayout:
            id: button_container
            size_hint_y: 0.5
            orientation: 'horizontal'
            spacing: 5
            padding: [5,15,5,20]
            # buttons made in init

                
""")

class RoundedButton(Button):
    pass

dark_grey = [51 / 255., 51 / 255., 51 / 255., 1.]

class LoadSliderWidget(Widget):


    def __init__(self, **kwargs):
        super(LoadSliderWidget, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']
        # self.l = kwargs['localization']
        self.yp = kwargs['yetipilot']

        self.load_label.color = dark_grey
        self.min_label.color = dark_grey
        self.max_label.color = dark_grey

        self.power_slider.value = self.yp.target_ld
        self.on_slider_value_change()

        self.make_buttons(self.button_container, self.power_slider, -100)
        self.make_buttons(self.button_container, self.power_slider, -10)
        self.make_buttons(self.button_container, self.power_slider, +10)
        self.make_buttons(self.button_container, self.power_slider, +100)

    def make_buttons(self, container, slider, val):
        btn_str = str(val) if val < 0 else "+" + str(val)
        button_adjust_func = partial(self.button_adjust_slider, val)
        container.add_widget(RoundedButton(text=btn_str, on_press=button_adjust_func, color=dark_grey))

    def button_adjust_slider(self, val, instance=None):
        if 400 <= self.power_slider.value + val <= 1000: self.power_slider.value+=val

    def on_slider_value_change(self):
        self.load_label.text = "[b]" + str(int(self.power_slider.value)) + " W" + "[/b]" 
        self.yp.target_ld = int(self.power_slider.value)