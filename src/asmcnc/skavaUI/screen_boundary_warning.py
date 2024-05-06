"""
Created on 25 Feb 2019

@author: Letty

This screen checks the users job, and allows them to review any errors 
"""
from kivy.lang import Builder
from kivy.properties import (
    StringProperty,
)
from kivy.uix.screenmanager import Screen

Builder.load_string(
    """

<BoundaryWarningScreen>:
    
    title_label: title_label
    quit_button: quit_button

    canvas:
        Color: 
            rgba: hex('#E5E5E5FF')
        Rectangle: 
            size: self.size
            pos: self.pos

    BoxLayout:
        orientation: 'vertical'
        padding: 0
        spacing: 0

        BoxLayout:
            size_hint_y: 0.7

        Label:
            id: title_label
            size_hint_y: 1.04
            size_hint_x: 1
            markup: True
            valign: 'center'
            halign: 'center'
            size: self.texture_size
            text_size: self.size
            color: hex('#333333ff')
            font_size: app.get_scaled_sp('36.0sp')

        BoxLayout:
            orientation: 'horizontal'
            padding: 0
            spacing: app.get_scaled_width(40.0)
            size_hint_y: 6.77

            BoxLayout:
                orientation: 'vertical'
                size_hint_x: 1
                spacing: 0
                padding: app.get_scaled_tuple([20.0, 20.0])

                Label:
                    size_hint_y: 3
                    size: self.texture_size
                    text_size: self.size
                    color: hex('#333333ff')
                    font_size: app.get_scaled_sp('20.0sp')
                    halign: 'center'
                    valign: 'middle'
                    text: root.check_outcome
                    markup: True
                    
                BoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: 1
                    padding: app.get_scaled_tuple([24.5, 0.0])

                    Button:
                        id: quit_button
                        on_press: root.quit_to_home()
                        text: root.exit_label
                        background_normal: "./asmcnc/skavaUI/img/next.png"
                        background_down: "./asmcnc/skavaUI/img/next.png"
                        border: app.get_scaled_tuple([14.5, 14.5, 14.5, 14.5])
                        size_hint: (None,None)
                        width: app.get_scaled_width(291.0)
                        height: app.get_scaled_height(78.9999999998)
                        font_size: app.get_scaled_sp('28.0sp')
                        color: hex('#f9f9f9ff')
                        markup: True
                        center: self.parent.center
                        pos: self.parent.pos
            
            BoxLayout:
                size_hint_x: 1
                orientation: 'vertical'
                spacing: app.get_scaled_width(5.00000000002)
                padding: app.get_scaled_tuple([0.0, 0.0, 20.0, 20.0])
                                
                ScrollView:
                    size_hint: 1, 1
                    pos_hint: {'center_x': .5, 'center_y': .5}
                    do_scroll_x: True
                    do_scroll_y: True
                    scroll_type: ['content']
                    
                    RstDocument:
                        text: root.display_output
                        background_color: hex('#E5E5E5FF')
                        base_font_size: app.get_scaled_sp('31.0sp')

                BoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: 0.15                       
"""
)


class BoundaryWarningScreen(Screen):
    check_outcome = StringProperty()
    display_output = StringProperty()
    exit_label = StringProperty()
    entry_screen = StringProperty()
    job_box_details = []

    def __init__(self, **kwargs):
        super(BoundaryWarningScreen, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.m = kwargs["machine"]
        self.l = kwargs["localization"]
        self.update_strings()

    def on_enter(self):
        self.check_outcome = (
            self.l.get_bold("WARNING")
            + "[b]:[/b]\n"
            + self.l.get_bold("Job is not within machine bounds!")
            + "\n\n"
            + self.l.get_str(
                "Please set datum appropriately, so that job boundaries are within SmartBench limits."
            )
        )
        self.write_boundary_output()

    def write_boundary_output(self):
        self.display_output = (
            self.l.get_bold("DETAILS OF BOUNDARY CONFLICT")
            + "\n\n"
            + "\n\n".join(map(str, self.job_box_details))
        )

    def quit_to_home(self):
        self.sm.current = "home"

    def on_leave(self):
        self.display_output = ""
        self.job_box_details = []

    def update_strings(self):
        self.title_label.text = self.l.get_str("Job Outside Machine Limits")
        self.quit_button.text = self.l.get_str("Return")
