from kivy.core.window import Window

"""
Created on 31 March 2021
@author: Letty
"""
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from asmcnc.skavaUI import widget_status_bar

Builder.load_string(
    """
<AlarmScreen3>:
    status_container : status_container
    description_label : description_label
    next_button : next_button
    camera_img : camera_img
    next_button : next_button
    # usb_img : usb_img

    BoxLayout: 
        size_hint: (None,None)
        width: dp(1.0*app.width)
        height: dp(1.0*app.height)
        orientation: 'vertical'
        canvas:
            Color:
                rgba: [1,1,1,1]
            Rectangle:
                size: self.size
                pos: self.pos
        BoxLayout:
            id: status_container 
            size_hint_y: 0.08
        BoxLayout:
            size_hint_y: 0.92
            orientation: 'vertical'
            BoxLayout: 
                orientation: 'vertical'
                padding:[dp(0.025)*app.width, dp(0.0208333333333)*app.height]
                Label:
                    id: description_label
                    font_size: str(0.02*app.width) + 'sp'
                    color: [0,0,0,1]
                    markup: True
                    halign: 'left'
                    valign: 'top'
                    text_size: self.size
                    size: self.size
            # Buttons
            BoxLayout: 
                padding:[dp(0.0125)*app.width, 0, dp(0.0125)*app.width, dp(0.0208333333333)*app.height]
                size_hint: (None, None)
                height: dp(0.275*app.height)
                width: dp(1.0*app.width)
                orientation: 'horizontal'
                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(0.275*app.height)
                    width: dp(0.305625*app.width)
                    padding:[0, 0, dp(0.230625)*app.width, 0]
                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        size_hint: (None,None)
                        height: dp(0.108333333333*app.height)
                        width: dp(0.075*app.width)
                        background_color: hex('#F4433600')
                        center: self.parent.center
                        pos: self.parent.pos
                        on_press: root.prev_screen()
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                source: "./asmcnc/apps/systemTools_app/img/back_to_menu.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True
                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(0.275*app.height)
                    width: dp(0.36375*app.width)
                    padding:[0, 0, 0, dp(0.108333333333)*app.height]
                    Button:
                        id: next_button
                        background_normal: "./asmcnc/skavaUI/img/next.png"
                        background_down: "./asmcnc/skavaUI/img/next.png"
                        border: [dp(14.5)]*4
                        size_hint: (None,None)
                        width: dp(0.36375*app.width)
                        height: dp(0.164583333333*app.height)
                        on_press: root.next_screen()
                        text: 'Next...'
                        font_size: root.default_font_size
                        color: hex('#f9f9f9ff')
                        markup: True
                        center: self.parent.center
                        pos: self.parent.pos
                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(0.275*app.height)
                    width: dp(0.305625*app.width)
                    padding:[dp(0.241875)*app.width, 0, 0, 0]
    FloatLayout:
        Image:
            id: camera_img
            x: 660.0 / 800 * app.width 
            y: 321.60 / 480 * app.height
            size_hint: None, None
            height: dp(100.0/480.0)*app.height
            width: 0.15*app.width
            allow_stretch: True
            opacity: 1
    # FloatLayout:
 #        Image:
 #          id: usb_img
 #            x: 680
 #            y: 238.6
 #            size_hint: None, None
 #            height: 63
 #            width: 100
 #            allow_stretch: True
"""
)


class AlarmScreen3(Screen):
    for_support = True
    default_font_size = 30.0 / 800.0 * Window.width

    def __init__(self, **kwargs):
        super(AlarmScreen3, self).__init__(**kwargs)
        self.a = kwargs["alarm_manager"]
        self.status_bar_widget = widget_status_bar.StatusBar(
            screen_manager=self.a.sm, machine=self.a.m
        )
        self.status_container.add_widget(self.status_bar_widget)
        self.status_bar_widget.cheeky_color = "#1976d2"
        self.camera_img.source = "./asmcnc/core_UI/sequence_alarm/img/camera_light.png"
        self.next_button.text = self.a.l.get_str("Next") + "..."
        # self.usb_img.source = "./asmcnc/core_UI/sequence_alarm/img/usb_empty_light.png"

    def on_pre_enter(self):
        if self.for_support:
            self.next_button.text = self.a.l.get_str("Next") + "..."
            self.update_font_size(self.next_button)
            self.camera_img.opacity = 1
            self.a.download_alarm_report()
        else:
            self.next_button.text = self.a.l.get_str("Get support")
            self.update_font_size(self.next_button)
            self.camera_img.opacity = 0

    def next_screen(self):
        if self.for_support:
            self.a.sm.current = "alarm_4"
        else:
            self.a.sm.current = "alarm_2"

    def prev_screen(self):
        if self.for_support:
            self.a.sm.current = "alarm_2"
        else:
            self.a.sm.get_screen("alarm_5").return_to_screen = "alarm_1"
            self.a.sm.current = "alarm_5"

    def update_font_size(self, value):
        text_length = self.a.l.get_text_length(value.text)
        if text_length < 12:
            value.font_size = self.default_font_size
        elif text_length > 15:
            value.font_size = self.default_font_size - 0.0025 * Window.width
        if text_length > 20:
            value.font_size = self.default_font_size - 0.005 * Window.width
        if text_length > 22:
            value.font_size = self.default_font_size - 0.00625 * Window.width
