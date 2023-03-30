from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import RoundedRectangle

Builder.load_string("""

<WidgetSpindleHealthCheck>

    title_text : title_text
    body_text : body_text
    switch : switch
    yp_toggle_img : yp_toggle_img

    BoxLayout: 
        orientation: "horizontal"
        padding: 20

        BoxLayout: 
            orientation: "vertical"
            size_hint_x: 0.9
            spacing: 2

            Label: 
                id: title_text
                size_hint_y: 0.15
                text: "Spindle motor health check"
                color: [0,0,0,1]
                font_size: "24sp"
                halign: "left"
                # valign: "top"
                markup: True
                text_size: self.size

            Label: 
                id: body_text
                size_hint_y: 0.85
                text: ""
                color: [0,0,0,1]
                font_size: "18sp"
                halign: "left"
                valign: "top"
                markup: True
                text_size: self.size

        BoxLayout: 
            size_hint_x: 0.1
            padding: [0,0,0,50]

            ToggleButton:
                id: switch
                size_hint: (None, None)
                size: ('64dp', '29dp')
                background_normal: ''
                background_down: ''
                on_press: root.toggle_yeti_pilot_availability(self)

                BoxLayout:
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        id: yp_toggle_img
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: False

""")


class WidgetSpindleHealthCheck(BoxLayout):

    def __init__(self, **kwargs):
        super(WidgetSpindleHealthCheck, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        self.l=kwargs['localization']

        self.switch.state = "normal"
        self.toggle_yeti_pilot_availability(self.switch)

        self.update_strings()

    def toggle_button_img(self, state):
        self.yp_toggle_img.source = './asmcnc/core_UI/job_go/img/yp_toggle_%s.png' % (('on' if state=="down" else 'off'))

    def toggle_yeti_pilot_availability(self, switch):
        self.toggle_button_img(switch.state)

    def update_strings(self):

        self.title_text.text = self.l.get_bold("Spindle motor health check")

        self.body_text.text = \
            "[color=e64a19ff]" + \
            self.l.get_str("Disable this if your tool is not rated to at least 24,000 rpm.") + "\n\n" + \
            "[/color]" + \
            self.l.get_str("The health check will run the spindle at 24,000 rpm for 5 seconds before every job.") + "\n\n" + \
            self.l.get_str("This checks that your Spindle motor is working correctly, and calibrates it for YetiPilot.") + "\n\n" + \
            self.l.get_str("If you disable this, there will not be an option to use YetiPilot during a job.") + "\n\n"

