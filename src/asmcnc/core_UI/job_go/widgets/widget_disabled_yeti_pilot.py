from kivy.uix.widget import Widget
from kivy.lang import Builder
from asmcnc.core_UI.job_go.screens.screen_spindle_health_check import SpindleHealthCheckActiveScreen

Builder.load_string("""

<DisabledYetiPilotWidget>:
    
    text_container:text_container
    title_label:title_label
    body_label:body_label

    button_container:button_container
    health_check_button:health_check_button
    health_check_button_img:health_check_button_img

    BoxLayout:
        orientation: 'horizontal'
        size: self.parent.size
        pos: self.parent.pos
        padding: [10,8,10,8]

        BoxLayout:
            id: text_container
            size_hint_x: 0.85
            orientation: 'vertical'
            padding: [2,0,5,0]
            spacing: 0
            Label: 
                id: title_label
                size_hint_y: 0.3
                color: hex('#333333ff')
                markup: True
                halign: 'left'
                text_size: self.size
                bold: True
                font_size: '17sp'
                valign: "bottom"

            Label:
                id: body_label
                size_hint_y: 0.7
                color: hex('#333333ff')
                markup: True
                halign: 'left'
                text_size: self.size
                font_size: '15sp'
                valign: "middle"

        BoxLayout: 
            id: button_container
            size_hint_x: 0.15

            Button:
                id: health_check_button
                size_hint_x: 1
                disabled: False
                background_color: hex('#F4433600')

                on_press:
                    root.run_spindle_health_check()

                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        id: health_check_button_img
                        # source: "./asmcnc/core_UI/job_go/img/spindle_check_silver.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: False
                
""")

class DisabledYPCase:
    DISABLED = 0
    FAILED_AND_CAN_RUN_AGAIN = 1
    FAILED = 2

class DisabledYetiPilotWidget(Widget):

    health_check_enabled_img = "./asmcnc/core_UI/job_go/img/spindle_check_silver.png"
    health_check_disabled_img = "./asmcnc/core_UI/job_go/img/spindle_check_disabled.png"

    def __init__(self, **kwargs):
        super(DisabledYetiPilotWidget, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']
        self.l = kwargs['localization']
        self.m = kwargs['machine']
        self.db = kwargs['database']
        self.yp = kwargs['yetipilot']

        self.yp.disable()
        self.update_strings()

    def set_version(self, case):

        self.update_strings(case=case)

        if case != DisabledYPCase.DISABLED:
            self.text_container.size_hint_x = 0.85
            self.button_container.opacity = 1
            self.button_container.size_hint_x = 0.15

        else:
            self.text_container.size_hint_x = 1
            self.button_container.opacity = 0
            self.button_container.size_hint_x = 0

        if case == DisabledYPCase.FAILED_AND_CAN_RUN_AGAIN:
            self.health_check_button.disabled = False
            self.health_check_button_img.source = self.health_check_enabled_img

        else:
            self.health_check_button.disabled = True
            self.health_check_button_img.source = self.health_check_disabled_img

    def update_strings(self, case = "disabled"):

        self.title_label.text = self.l.get_str("YetiPilot is disabled")

        if case == DisabledYPCase.DISABLED:
            self.body_label.text =  self.l.get_str("Enable Spindle motor health check in the Maintenance app to change this.")

        else:
            self.body_label.text =  self.l.get_str("Spindle motor health check failed.")
        
            if case == DisabledYPCase.FAILED_AND_CAN_RUN_AGAIN:
                self.body_label.text += "\n"
                self.body_label.text += self.l.get_str("Re-run before job start to enable YetiPilot.")

    def run_spindle_health_check(self):
        if not self.sm.has_screen('spindle_health_check_active'):
            shc_screen = SpindleHealthCheckActiveScreen(name='spindle_health_check_active',
                                                        screen_manager=self.sm, machine=self.m, localization=self.l)
            self.sm.add_widget(shc_screen)
        self.sm.current = 'spindle_health_check_active'









