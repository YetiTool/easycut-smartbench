"""
Created on 19 Aug 2017

@author: Ed
"""
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from asmcnc.skavaUI import (
    widget_status_bar,
)

Builder.load_string(
    """

#:import hex kivy.utils.get_color_from_hex

<DiagnosticsScreen>:

    status_container:status_container
    
    limit_x_label:limit_x_label
    limit_X_label:limit_X_label
    limit_y_label:limit_y_label
    limit_Y_label:limit_Y_label
    limit_z_label:limit_z_label
    probe_label:probe_label
    dust_shoe_cover_label:dust_shoe_cover_label

    BoxLayout:
        padding: 0
        spacing: 0
        orientation: "vertical"

        BoxLayout:
            padding: 0
            spacing: 0
            orientation: "horizontal"

            Label:
                font_size: str(0.01875 * app.width) + 'sp'
                text: 'LED ring:'
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                text: 'Red'
                on_press: root.led('RED')
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                text: 'Green'
                on_press: root.led('GREEN')
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                text: 'Blue'
                on_press: root.led('BLUE')

            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                text: 'OFF'
                on_press: root.led('off')

            Label:
                font_size: str(0.01875 * app.width) + 'sp'
                id: probe_label
                text: 'Probe'
            Label:
                font_size: str(0.01875 * app.width) + 'sp'
                id: dust_shoe_cover_label
                text: 'Dust cover'
                
        BoxLayout:
            padding: 0
            spacing: 0
            orientation: "horizontal"

            Label:
                font_size: str(0.01875 * app.width) + 'sp'
                text: 'X axis:'
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                text: '-'
                on_press: root.move('x-')
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                text: '+'
                on_press: root.move('x+')
            Label:
                font_size: str(0.01875 * app.width) + 'sp'
                id: limit_x_label
                text: 'X Min'
            Label:
                font_size: str(0.01875 * app.width) + 'sp'
                id: limit_X_label
                text: 'X Max'

        BoxLayout:
            padding: 0
            spacing: 0
            orientation: "horizontal"

            Label:
                font_size: str(0.01875 * app.width) + 'sp'
                text: 'Y axis:'
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                text: '-'
                on_press: root.move('y-')
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                text: '+'
                on_press: root.move('y+')
            Label:
                font_size: str(0.01875 * app.width) + 'sp'
                id: limit_y_label
                text: 'Y Min'
            Label:
                font_size: str(0.01875 * app.width) + 'sp'
                id: limit_Y_label
                text: 'Y Max'

        BoxLayout:
            padding: 0
            spacing: 0
            orientation: "horizontal"

            Label:
                font_size: str(0.01875 * app.width) + 'sp'
                text: 'Z axis:'
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                text: '-'
                on_press: root.move('z-')
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                text: '+'
                on_press: root.move('z+')
            Label:
                font_size: str(0.01875 * app.width) + 'sp'
                id: limit_z_label
                text: 'Z Min'
            Label:
                font_size: str(0.01875 * app.width) + 'sp'
                text: ''

        Button:
            font_size: str(0.01875 * app.width) + 'sp'
            text: 'Return to factory settings'
            on_press: root.return_to_home()
            
        BoxLayout:
            id: status_container

"""
)


class DiagnosticsScreen(Screen):
    def __init__(self, **kwargs):
        super(DiagnosticsScreen, self).__init__(**kwargs)
        self.m = kwargs["machine"]
        self.sm = kwargs["screen_manager"]
        self.status_container.add_widget(
            widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm)
        )
        Clock.schedule_interval(self.limit_switch_check, 0.2)

    def on_enter(self):
        self.m.disable_limit_switches()

    def on_leave(self):
        self.m.enable_limit_switches()

    def led(self, command):
        self.m.set_led_colour(command)

    def move(self, case):
        xy_distance = 4
        z_distance = 2
        xy_feed = 200
        z_feed = 100
        if case == "x-":
            self.m.jog_relative("X-", str(xy_distance), xy_feed)
        if case == "x+":
            self.m.jog_relative("X", str(xy_distance), xy_feed)
        if case == "y-":
            self.m.jog_relative("Y-", str(xy_distance), xy_feed)
        if case == "y+":
            self.m.jog_relative("Y", str(xy_distance), xy_feed)
        if case == "z-":
            self.m.jog_relative("Z-", str(z_distance), z_feed)
        if case == "z+":
            self.m.jog_relative("Z", str(z_distance), z_feed)

    def limit_switch_check(self, dt):
        switch_states = self.m.get_switch_states()
        if "limit_x" in switch_states:
            self.limit_x_label.text = "X min - OK"
        else:
            self.limit_x_label.text = "X min"
        if "limit_X" in switch_states:
            self.limit_X_label.text = "X max - OK"
        else:
            self.limit_X_label.text = "X max"
        if "limit_y" in switch_states:
            self.limit_y_label.text = "Y min - OK"
        else:
            self.limit_y_label.text = "Y min"
        if "limit_Y" in switch_states:
            self.limit_Y_label.text = "Y max - OK"
        else:
            self.limit_Y_label.text = "Y max"
        if "limit_z" in switch_states:
            self.limit_z_label.text = "Z min - OK"
        else:
            self.limit_z_label.text = "Z min"
        if "probe" in switch_states:
            self.probe_label.text = "Probe - OK"
        else:
            self.probe_label.text = "Probe"
        if "dust_shoe_cover_on" in switch_states:
            self.dust_shoe_cover_label.text = "Dust cover - OK"
        else:
            self.dust_shoe_cover_label.text = "Dust cover"

    def return_to_home(self):
        self.sm.current = "factory_settings"
