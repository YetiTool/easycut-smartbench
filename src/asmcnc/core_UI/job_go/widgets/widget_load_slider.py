from functools import partial

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.widget import Widget

Builder.load_string(
    """

<PowerAdjustButtons@Button>:
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
            markup: True
            halign: "center" 
            valign: "middle"
            color: color_provider.get_rgba("black")
            font_size: str(0.0275*app.width) + 'sp'
            size_hint_y: 0.3

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.2
            padding:[dp(0.01875)*app.width, 0]

            Label: 
                id: min_label
                color: color_provider.get_rgba("black")
                markup: True
                halign: "center" 
                valign: "middle"
                size_hint_x: 0.1
                font_size: str(0.0175*app.width) + 'sp'

            Slider:
                id: power_slider
                # min: 400
                max: 1000
                step: 10
                size_hint_x: 0.8

            Label: 
                id: max_label
                color: color_provider.get_rgba("black")
                markup: True
                halign: "center" 
                valign: "middle"
                size_hint_x: 0.1
                font_size: str(0.0175*app.width) + 'sp'

        BoxLayout:
            id: button_container
            size_hint_y: 0.5
            orientation: 'horizontal'
            spacing:0.00625*app.width
            padding:[dp(0.00625)*app.width, dp(0.03125)*app.height, dp(0.00625)*app.width, dp(0.0416666666667)*app.height]
            # buttons made in init

                
"""
)


class PowerAdjustButtons(Button):
    pass


dark_grey = [51 / 255.0, 51 / 255.0, 51 / 255.0, 1.0]


class LoadSliderWidget(Widget):
    def __init__(self, **kwargs):
        super(LoadSliderWidget, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.yp = kwargs["yetipilot"]
        self.load_label.color = dark_grey
        self.min_label.color = dark_grey
        self.max_label.color = dark_grey
        try:
            self.power_slider.min = self.yp.get_free_load()
        except:
            self.power_slider.min = 390
        self.power_slider.value = self.yp.get_total_target_power()
        self.on_slider_value_change()
        self.power_slider.bind(value=self.on_slider_value_change)
        self.min_label.text = str(int(self.power_slider.min)) + " W"
        self.max_label.text = str(int(self.power_slider.max)) + " W"
        self.make_buttons(self.button_container, self.power_slider, -100)
        self.make_buttons(self.button_container, self.power_slider, -10)
        self.make_buttons(self.button_container, self.power_slider, +10)
        self.make_buttons(self.button_container, self.power_slider, +100)

    def make_buttons(self, container, slider, val):
        btn_str = str(val) if val < 0 else "+" + str(val)
        button_adjust_func = partial(self.button_adjust_slider, val)
        container.add_widget(
            PowerAdjustButtons(
                text=btn_str, on_press=button_adjust_func, color=dark_grey,
                font_size=str(15.0/800.0*Window.width) + 'sp'
            )
        )

    def button_adjust_slider(self, val, instance=None):
        if (
            self.power_slider.min
            <= self.power_slider.value + val
            <= self.power_slider.max
        ):
            self.power_slider.value += val

    def on_slider_value_change(self, instance=None, value=None):
        self.load_label.text = "[b]" + str(int(self.power_slider.value)) + " W" + "[/b]"
        tool_load = int(self.power_slider.value) - self.yp.get_free_load()
        self.yp.set_tool_load(tool_load)
