from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

Builder.load_string("""
#:import LabelBase asmcnc.core_UI.components.labels.base_label

<WidgetSpindleHealthCheck>

    title_text : title_text
    body_text : body_text
    switch : switch
    yp_toggle_img : yp_toggle_img

    BoxLayout: 
        orientation: "horizontal"
        padding:[dp(0.025)*app.width, dp(0.0416666666667)*app.height]

        BoxLayout: 
            orientation: "vertical"
            size_hint_x: 0.88
            spacing:0.00416666666667*app.height

            LabelBase: 
                id: title_text
                size_hint_y: 0.15
                text: "Spindle motor health check"
                color: [0,0,0,1]
                font_size: str(0.03*app.width) + 'sp'
                halign: "left"
                # valign: "top"
                markup: True
                text_size: self.size

            LabelBase: 
                id: body_text
                size_hint_y: 0.85
                text: ""
                color: [0,0,0,1]
                font_size: str(0.0225*app.width) + 'sp'
                halign: "left"
                valign: "top"
                markup: True
                text_size: self.size

        BoxLayout: 
            size_hint_x: 0.12
            padding:[0, 0, 0, dp(0.104166666667)*app.height]
            spacing: 0
            orientation: 'vertical'

            BoxLayout: 
                size_hint_y: 0.9
                Image:
                    source: "./asmcnc/apps/maintenance_app/img/health_check_with_shadow.png"
                    allow_stretch: False

            BoxLayout: 
                size_hint_y: 0.1
                padding:[dp(0.0125)*app.width, 0, 0, 0]

                ToggleButton:
                    font_size: str(0.01875 * app.width) + 'sp'
                    id: switch
                    size_hint: (None, None)
                    size: (dp(app.get_scaled_width(64)), dp(app.get_scaled_height(29)))
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
                            allow_stretch: True

"""
)


class WidgetSpindleHealthCheck(BoxLayout):
    def __init__(self, **kwargs):
        super(WidgetSpindleHealthCheck, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.m = kwargs["machine"]
        self.l = kwargs["localization"]
        self.set_switch_state_to_health_check()
        self.toggle_yeti_pilot_availability(self.switch)
        self.update_strings()

    def set_switch_state_to_health_check(self):
        self.switch.state = (
            "down" if self.m.is_spindle_health_check_active() else "normal"
        )

    def toggle_button_img(self, state):
        self.yp_toggle_img.source = "./asmcnc/core_UI/job_go/img/yp_toggle_%s.png" % (
            "on" if state == "down" else "off"
        )

    def toggle_yeti_pilot_availability(self, switch):
        self.toggle_button_img(switch.state)
        health_check = switch.state == "down"
        self.m.write_spindle_health_check_settings(health_check)

    def update_strings(self):
        self.title_text.text = self.l.get_bold("Spindle motor health check")
        self.body_text.text = (
            "[color=e64a19ff]"
            + self.l.get_str(
                "Disable this if your tool is not rated to at least 24,000 rpm."
            )
            + "\n\n"
            + "[/color]"
            + self.l.get_str(
                "The health check will run the spindle at 24,000 rpm for 6 seconds before every job."
            )
            + "\n\n"
            + self.l.get_str(
                "This checks that your Spindle motor is working correctly, and calibrates it for YetiPilot."
            )
            + "\n\n"
            + self.l.get_str(
                "If you disable this, there will not be an option to use YetiPilot during a job."
            )
            + "\n\n"
        )
