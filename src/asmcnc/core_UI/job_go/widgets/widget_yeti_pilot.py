from kivy.uix.widget import Widget
from kivy.lang import Builder

from asmcnc.core_UI.job_go.popups.popup_yetipilot_settings import PopupYetiPilotSettings


Builder.load_string("""
<YetiPilotWidget>:
    switch:switch
    BoxLayout:
        orientation: 'horizontal'
        size: self.parent.size
        pos: self.parent.pos
        padding: 10
        
        BoxLayout:
            size_hint_x: 0.6
            spacing: 5
            Label:
                text: '[b]YetiPilot[/b]'
                color: 0, 0, 0, 1
                markup: True
                
            Switch:
                id: switch
                on_active: root.toggle_yeti_pilot(self)
                
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

    def switch_reflects_yp(self):
        self.switch.active = self.yp.use_yp

    def toggle_yeti_pilot(self, switch):
        if switch.active:
            self.yp.enable()
            self.open_yp_settings()
        else: 
            self.yp.disable()

    def disable_yeti_pilot(self):
        self.switch.active = False
        self.toggle_yeti_pilot(self.switch)

    def open_yp_settings(self):
        PopupYetiPilotSettings(self.sm, self.l)

    # # DOES NOT WORK
    # def update_toggle_img(self, on_off):
    #     self.switch.canvas.children[-1].source = './asmcnc/core_UI/job_go/img/'+ on_off + '_toggle_fg.png' # slider 
    #     self.switch.canvas.children[2].source = './asmcnc/core_UI/job_go/img/'+ on_off + '_toggle_bg.png' # background

        
