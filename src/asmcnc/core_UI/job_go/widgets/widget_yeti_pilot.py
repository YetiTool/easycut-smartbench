from kivy.uix.widget import Widget
from kivy.lang import Builder
from asmcnc.core_UI.job_go.popups.popup_yetipilot_settings import PopupYetiPilotSettings

from asmcnc.comms.model_manager import ModelManagerSingleton

Builder.load_string(
    """

<YetiPilotWidget>:
    
    yetipilot_two_tone:yetipilot_two_tone
    switch:switch
    yp_toggle_img:yp_toggle_img
    profile_label:profile_label
    profile_selection:profile_selection
    bl: bl
    yp_cog_button:yp_cog_button

    BoxLayout:
        orientation: 'horizontal'
        size: self.parent.size
        pos: self.parent.pos
        padding:[dp(0.0125)*app.width, dp(0.0166666666667)*app.height, dp(0.0125)*app.width, dp(0.0166666666667)*app.height]

        
        BoxLayout:
            orientation: 'vertical'
            size_hint_x: 0.25
            spacing:0.0208333333333*app.height

            Label:
                id: yetipilot_two_tone
                size_hint_y: 0.5
                markup: True
                halign: 'center'
                text_size: self.size
                font_size: str(0.025*app.width) + 'sp'
                valign: "bottom"

            BoxLayout: 
                id: bl
                size_hint_y: 0.5
                padding:[dp(0.017620614025)*app.width, 0]

                ToggleButton:
                    font_size: str(0.01875 * app.width) + 'sp'
                    id: switch
                    size_hint: (None, None)
                    size: (dp(64.0/800)*app.width, dp(29.0/480)*app.height)
                    background_normal: ''
                    background_down: ''
                    on_press: root.toggle_yeti_pilot(self)

                    BoxLayout:
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            id: yp_toggle_img
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: False

        BoxLayout:
            padding:[0, 0]
            size_hint_x: 0.025
            
            BoxLayout:
                size_hint_x: None
                width: 0.0025*app.width
                canvas:
                    Color:
                        rgba: hex('#ccccccff')
                    Rectangle:
                        pos: self.pos
                        size: self.size

        BoxLayout:
            orientation: 'vertical'
            size_hint_x: 0.6
            padding:[dp(0.0025)*app.width, 0, dp(0.00625)*app.width, 0]
            spacing: 0
            Label: 
                id: profile_label
                size_hint_y: 0.4
                color: hex('#333333ff')
                markup: True
                halign: 'left'
                text_size: self.size
                bold: True
                font_size: str(0.0225*app.width) + 'sp'
                valign: "bottom"

            Label:
                id: profile_selection
                size_hint_y: 0.6
                color: hex('#333333ff')
                markup: True
                halign: 'left'
                text_size: self.size
                font_size: str(0.0175*app.width) + 'sp'
                valign: "middle"

        BoxLayout: 
            size_hint_x: 0.1
            padding:[0, 0, dp(0.0125)*app.width, 0]
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                id: yp_cog_button
                background_normal: ''
                on_press: root.open_yp_settings()
                BoxLayout:
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/core_UI/job_go/img/yp_profiles_cog.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True



                
"""
)


class YetiPilotWidget(Widget):
    yp_settings_popup = None

    def __init__(self, **kwargs):
        super(YetiPilotWidget, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.l = kwargs["localization"]
        self.m = kwargs["machine"]
        self.db = kwargs["database"]
        self.yp = kwargs["yetipilot"]
        self.disable_yeti_pilot()
        self.yetipilot_two_tone.text = "[b][color=1976d2ff]YetiPilot[/b][/color]"
        self.profile_label.text = self.l.get_str("Profile")

        self.model_manager = ModelManagerSingleton()

    def toggle_button_img(self, state):
        self.yp_toggle_img.source = "./asmcnc/core_UI/job_go/img/yp_toggle_%s.png" % (
            "on" if state == "down" else "off"
        )

    def switch_reflects_yp(self):
        self.switch.state = "down" if self.yp.use_yp else "normal"
        self.toggle_button_img(self.switch.state)

    def toggle_yeti_pilot(self, switch):
        if switch.state == "down":
            self.yp.enable()
            if not self.model_manager.is_machine_drywall():
                self.open_yp_settings()
        else:
            self.yp.disable()
        self.toggle_button_img(switch.state)

    def disable_yeti_pilot(self):
        self.switch.state = "normal"
        self.toggle_yeti_pilot(self.switch)

    def open_yp_settings(self):
        self.yp_settings_popup = PopupYetiPilotSettings(
            self.sm,
            self.l,
            self.m,
            self.db,
            self.yp,
            version=not self.yp.using_advanced_profile,
            closing_func=self.update_profile_selection,
        )

    def update_profile_selection(self, *args):
        if self.yp.using_basic_profile:
            if self.yp.active_profile is None:
                self.disable_yeti_pilot()
                return
            self.profile_selection.text = (
                self.yp.get_active_material_type()
                + "; "
                + self.yp.get_active_cutter_diameter()
                + ", "
                + self.yp.get_active_cutter_type()
            )
        elif self.yp.using_advanced_profile:
            if not self.m.has_spindle_health_check_passed():
                self.disable_yeti_pilot()
                return
            self.profile_selection.text = (
                self.l.get_str("Advanced profile")
                + ": "
                + str(int(self.yp.get_total_target_power()))
                + " W"
            )
