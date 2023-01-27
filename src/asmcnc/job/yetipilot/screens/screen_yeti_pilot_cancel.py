from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_string("""
<YetiPilotCancelScreen>:
    alarm_title : alarm_title
    icon_container : icon_container
    icon : icon

    canvas:
        Color: 
            rgba: [1, 1, 1, 1]
        Rectangle: 
            size: self.size
            pos: self.pos
            
    BoxLayout:
        orientation: 'vertical'
        padding: 0
        spacing: 0
        size_hint: (None, None)
        height: dp(480)
        width: dp(800)
        # Alarm header
        BoxLayout: 
            padding: [dp(15),0,dp(15),0]
            spacing: 0
            size_hint: (None, None)
            height: dp(50)
            width: dp(800)
            orientation: 'horizontal'
            Label:
                id: alarm_title
                size_hint: (None, None)
                color: [0,0,0,1]
                font_size: '30sp'
                markup: True
                halign: 'left'
                height: dp(50)
                width: dp(770)
                text_size: self.size
        # Red underline
        BoxLayout: 
            padding: [dp(10),0,dp(10),0]
            spacing: 0
            size_hint: (None, None)
            height: dp(5)
            width: dp(800)
            Image:
                id: red_underline
                source: "./asmcnc/skavaUI/img/red_underline.png"
                center_x: self.parent.center_x
                y: self.parent.y
                size: self.parent.width, self.parent.height
                allow_stretch: True
        # Image and text
        BoxLayout: 
            padding: [0,dp(35),0,0]
            spacing: 0
            size_hint: (None, None)
            height: dp(435)
            width: dp(800)
            orientation: 'vertical'
            BoxLayout: 
                id: icon_container
                padding: [dp(335),0,0,0]
                size_hint: (None, None)
                height: dp(130)
                width: dp(800)       
                Image:
                    id: icon
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True
                    size_hint: (None, None)
                    height: dp(130)
                    width: dp(130)
                    source: './asmcnc/core_UI/sequence_alarm/img/alarm_icon.png'
            
            BoxLayout:
                size_hint: None, None
                width: dp(800)
                height: dp(240)
                orientation: 'horizontal'
                
                BoxLayout:
                    size_hint: None, None
                    width: dp(150)
                    Image:
                        source: 'asmcnc/job/yetipilot/screens/img/qr_code.png'
            
                BoxLayout:
                    id: description container
                    spacing: 20
                    size_hint: (None, None)
                    width: dp(500)
                    height: dp(290)
                    orientation: 'vertical'
                    
                    Label:
                        color: 0,0,0,1
                        text: 'The job has been cancelled because YetiPilot is active, and cannot adjust the feed rate below 10%.'
                        halign: 'center'
                        width: dp(500)
                        size_hint: None, None
                        text_size: self.width, None
                        height: self.texture_size[1]
                        font_size: dp(16)
                        
                    Label:
                        color: 0,0,0,1
                        text: 'This may be because of a problem (eg. blunt cutter) or that the feed in the job file is set too high.'
                        halign: 'center'
                        width: dp(500)
                        size_hint: None, None
                        text_size: self.width, None
                        height: self.texture_size[1]
                        font_size: dp(16)
                        
                    Label:
                        color: 0,0,0,1
                        text: 'More information can be found on on our knowledge base here: https://www.yetitool.com/support/knowledge-base/smartbench1-precision-features-precision-pro'
                        halign: 'center'
                        width: dp(500)
                        size_hint: None, None
                        text_size: self.width, None
                        height: self.texture_size[1]
                        font_size: dp(16)
                
                BoxLayout:
                    size_hint: None, None
                    width: dp(150)
                    Image:
                        source: 'asmcnc/apps/systemTools_app/img/exit_system_tools.png'
        
            BoxLayout:
                size_hint: None, None
                height: dp(50)
""")


class YetiPilotCancelScreen(Screen):
    def __init__(self, **kwargs):
        super(YetiPilotCancelScreen, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']
        self.set_text()

    def set_text(self):
        self.alarm_title.text = 'Job cancelled: feed rate limit reached'
