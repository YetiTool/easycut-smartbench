'''
Created on 31 March 2021
@author: Letty
'''
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from asmcnc.skavaUI import widget_status_bar

# Kivy UI builder:
Builder.load_string("""
<AlarmScreen3>:
    status_container : status_container
    description_label : description_label
    next_button : next_button
    camera_img : camera_img
    next_button : next_button
    # usb_img : usb_img

    BoxLayout: 
        size_hint: (None,None)
        width: dp(800)
        height: dp(480)
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
                padding: [20,10]
                Label:
                    id: description_label
                    font_size: '16sp'
                    color: [0,0,0,1]
                    markup: True
                    halign: 'left'
                    valign: 'top'
                    text_size: self.size
                    size: self.size
            # Buttons
            BoxLayout: 
                padding: [10,0,10,10]
                size_hint: (None, None)
                height: dp(132)
                width: dp(800)
                orientation: 'horizontal'
                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(132)
                    width: dp(244.5)
                    padding: [0, 0, 184.5, 0]
                    Button:
                        size_hint: (None,None)
                        height: dp(52)
                        width: dp(60)
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
                    height: dp(132)
                    width: dp(291)
                    padding: [0,0,0,52]
                    Button:
                        id: next_button
                        background_normal: "./asmcnc/skavaUI/img/next.png"
                        background_down: "./asmcnc/skavaUI/img/next.png"
                        border: [dp(14.5)]*4
                        size_hint: (None,None)
                        width: dp(291)
                        height: dp(79)
                        on_press: root.next_screen()
                        text: 'Next...'
                        font_size: root.default_font_size
                        color: hex('#f9f9f9ff')
                        markup: True
                        center: self.parent.center
                        pos: self.parent.pos
                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(132)
                    width: dp(244.5)
                    padding: [193.5, 0, 0, 0]
    FloatLayout:
        Image:
            id: camera_img
            x: 660
            y: 321.60
            size_hint: None, None
            height: 100
            width: 120
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
""")

class AlarmScreen3(Screen):

    for_support = True
    default_font_size = 30

    def __init__(self, **kwargs):
        self.a = kwargs.pop('alarm_manager')
        super(AlarmScreen3, self).__init__(**kwargs)

        self.status_bar_widget = widget_status_bar.StatusBar(screen_manager=self.a.sm, machine=self.a.m)
        self.status_container.add_widget(self.status_bar_widget)
        self.status_bar_widget.cheeky_color = '#1976d2'\

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
            self.a.sm.current = 'alarm_4'
        else:
            self.a.sm.current = 'alarm_2'


    def prev_screen(self):
        if self.for_support:
            self.a.sm.current = 'alarm_2'
        else:
            self.a.sm.get_screen('alarm_5').return_to_screen = 'alarm_1'
            self.a.sm.current = 'alarm_5'


    def update_font_size(self, value):
        if len(value.text) < 12:
            value.font_size = self.default_font_size
        elif len(value.text) > 15: 
            value.font_size = self.default_font_size - 2
        if len(value.text) > 20: 
            value.font_size = self.default_font_size - 4
        if len(value.text) > 22: 
            value.font_size = self.default_font_size - 5