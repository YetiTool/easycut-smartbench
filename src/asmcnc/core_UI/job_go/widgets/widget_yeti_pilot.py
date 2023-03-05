from kivy.uix.widget import Widget
from kivy.lang import Builder

from asmcnc.core_UI.job_go.popups.popup_yetipilot_settings import PopupYetiPilotSettings


Builder.load_string("""
<YetiPilotWidget>:
    
    yetipilot_two_tone:yetipilot_two_tone
    switch:switch
    profile_label:profile_label
    profile_selection:profile_selection

    BoxLayout:
        orientation: 'horizontal'
        size: self.parent.size
        pos: self.parent.pos
        padding: [10,8]
        
        BoxLayout:
            orientation: 'vertical'
            size_hint_x: 0.25
            spacing: 5
            Label:
                id: yetipilot_two_tone
                size_hint_y: 0.6
                text: '[b]YetiPilot[/b]'
                color: 0, 0, 0, 1
                markup: True
                halign: 'left'
                text_size: self.size
                font_size: '20sp'
                
            BoxLayout:
                size_hint_y: 0.4
                Switch:
                    id: switch
                    on_active: root.toggle_yeti_pilot(self)

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
            Label: 
                id: profile_label
                color: [0,0,0,1]
                markup: True
                halign: 'left'
                text_size: self.size
                bold: True
                font_size: '15sp'

            Label:
                id: profile_selection
                text: "MDF; 3mm 2 flue upcut spiral"
                color: [0,0,0,1]
                markup: True
                halign: 'left'
                text_size: self.size
                font_size: '15sp'

        BoxLayout: 
            size_hint_x: 0.1
            padding: [0,0,10,0]
            Button:
                background_normal: ''
                on_press: self.open_yp_settings()
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

    '''
    To do: 

    - Link cog to popup
    - Localization hooks for profile
    - hook material and cutter selections from YP
    - text colours & formatting
    - switch looks crap
    '''


    def __init__(self, **kwargs):
        super(YetiPilotWidget, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']
        self.l = kwargs['localization']
        self.m = kwargs['machine']
        self.db = kwargs['database']
        self.yp = kwargs['yetipilot']

        self.disable_yeti_pilot()
        self.yetipilot_two_tone.text = '[b][color=2196f3ff]Yeti[/color][color=333333ff]Pilot[/b][/color]'
        self.profile_label.text = self.l.get_str("Profile")

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
        PopupYetiPilotSettings(self.sm, self.l, self.m, self.db, self.yp, version=self.yp.standard_profiles)


    def update_profile_selection(self):
        self.profile_selection.text = ""






    # # DOES NOT WORK
    # def update_toggle_img(self, on_off):
    #     self.switch.canvas.children[-1].source = './asmcnc/core_UI/job_go/img/'+ on_off + '_toggle_fg.png' # slider 
    #     self.switch.canvas.children[2].source = './asmcnc/core_UI/job_go/img/'+ on_off + '_toggle_bg.png' # background

        
