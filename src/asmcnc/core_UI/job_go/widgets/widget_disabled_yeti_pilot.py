from kivy.uix.widget import Widget
from kivy.lang import Builder

Builder.load_string("""

<DisabledYetiPilotWidget>:
    
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
        padding: [10,8,10,8]

        BoxLayout:
            orientation: 'vertical'
            padding: [2,0,5,0]
            spacing: 0
            Label: 
                id: profile_label
                size_hint_y: 0.4
                color: hex('#333333ff')
                markup: True
                halign: 'left'
                text_size: self.size
                bold: True
                font_size: '18sp'
                valign: "bottom"

            Label:
                id: profile_selection
                size_hint_y: 0.6
                color: hex('#333333ff')
                markup: True
                halign: 'left'
                text_size: self.size
                font_size: '14sp'
                valign: "middle"
                
""")

class DisabledYetiPilotWidget(Widget):

    def __init__(self, **kwargs):
        super(DisabledYetiPilotWidget, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']
        self.l = kwargs['localization']
        self.m = kwargs['machine']
        self.db = kwargs['database']
        self.yp = kwargs['yetipilot']

        self.yp.disable()









