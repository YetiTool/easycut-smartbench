from kivy.uix.widget import Widget
from kivy.lang import Builder

from asmcnc.core_UI.job_go.popups.popup_yetipilot_settings import PopupYetiPilotSettings


Builder.load_string("""

<YetiPilotWidget>:
    
    yetipilot_two_tone:yetipilot_two_tone
    switch:switch
    yp_toggle_img:yp_toggle_img
    profile_label:profile_label
    profile_selection:profile_selection
    bl: bl

    BoxLayout:
        orientation: 'horizontal'
        size: self.parent.size
        pos: self.parent.pos
        padding: [10,8]

        
        BoxLayout:
            orientation: 'vertical'
            size_hint_x: 0.25
            spacing: 10

            Label:
                id: yetipilot_two_tone
                size_hint_y: 0.6
                markup: True
                halign: 'center'
                text_size: self.size
                font_size: '20sp'
                valign: "bottom"
                font: 'Roboto Bold'

            BoxLayout: 
                id: bl
                size_hint_y: 0.4
                padding: [14.09649122,0]

                ToggleButton:
                    id: switch
                    size_hint: (None, None)
                    size: ('64dp', '29dp')
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
            padding: [0,0]
            size_hint_x: 0.05
            
            BoxLayout:
                size_hint_x: None
                width: '2dp'
                canvas:
                    Color:
                        rgba: hex('#ccccccff')
                    Rectangle:
                        pos: self.pos
                        size: self.size

        BoxLayout:
            orientation: 'vertical'
            size_hint_x: 0.6
            padding: [0,0]
            spacing: 10
            Label: 
                id: profile_label
                size_hint_y: 0.6
                color: hex('#333333ff')
                markup: True
                halign: 'left'
                text_size: self.size
                bold: True
                font_size: '18sp'
                valign: "bottom"

            Label:
                id: profile_selection
                size_hint_y: 0.4
                color: hex('#333333ff')
                markup: True
                halign: 'left'
                text_size: self.size
                font_size: '15sp'
                valign: "middle"

        BoxLayout: 
            size_hint_x: 0.1
            padding: [0,0,10,0]
            Button:
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
                        allow_stretch: False



                
""")

class YetiPilotWidget(Widget):

    def __init__(self, **kwargs):
        super(YetiPilotWidget, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']
        self.l = kwargs['localization']
        self.m = kwargs['machine']
        self.db = kwargs['database']
        self.yp = kwargs['yetipilot']

        self.disable_yeti_pilot()
        # self.yetipilot_two_tone.text = '[b][color=2196f3ff]YetiPilot[/b][/color]' # [/color][color=333333ff]
        self.yetipilot_two_tone.text = '[b][color=1976d2ff]YetiPilot[/b][/color]' # [/color][color=333333ff] 
        self.profile_label.text = self.l.get_str("Profile")

    def toggle_button_img(self, state):
        self.yp_toggle_img.source = './asmcnc/core_UI/job_go/img/yp_toggle_%s.png' % (('on' if state=="down" else 'off'))

    def switch_reflects_yp(self):
        self.switch.state = "down" if self.yp.use_yp else "normal"
        self.toggle_button_img(self.switch.state)

    def toggle_yeti_pilot(self, switch):
        if switch.state=="down":
            self.yp.enable()
            self.open_yp_settings()
        else: 
            self.yp.disable()

        self.toggle_button_img(switch.state)

    def disable_yeti_pilot(self):
        self.switch.state = "normal"
        self.toggle_yeti_pilot(self.switch)

    def open_yp_settings(self):
        PopupYetiPilotSettings(self.sm, self.l, self.m, self.db, self.yp, version=self.yp.standard_profiles, closing_func=self.update_profile_selection)

    def update_profile_selection(self, *args):
        if self.yp.standard_profiles:
            self.profile_selection.text = self.yp.material + "; " + self.yp.diameter + " " + self.yp.tool
        else:
            self.profile_selection.text = self.l.get_str("Advanced profile") + ": " + str(self.yp.target_ld) + " W"