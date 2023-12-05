"""
Created on 17 January 2020
Warning to remind user to remove their tape measure before homing the machine
@author: Letty
"""
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import Screen

Builder.load_string(
    """
<TapeMeasureScreenClass>:
    
    alert_label:alert_label
    canvas:
        Color: 
            rgba: hex('#FFFFFF')
        Rectangle: 
            size: self.size
            pos: self.pos
             
    BoxLayout:
        orientation: 'horizontal'
        padding:[dp(0.1)*app.width, dp(0.0625)*app.height]
        spacing: 0
        size_hint_x: 1
        BoxLayout:
            orientation: 'vertical'
            size_hint_x: 0.8
            
#             Label:
#                 text_size: self.size
#                 font_size: '40sp'
#                 halign: 'center'
#                 valign: 'middle'
#                 text: '[color=455A64]TAPE MEASURE ALERT![/color]'
#                 markup: 'True'
#                 #size_hint_y: 0.2
            
            Image:
                id: image_measure
                source: "./asmcnc/calibration_app/img/tape_measure_alert.png"
                center_x: self.parent.center_x
                center_y: self.parent.center_y
                size: self.parent.width, self.parent.height
                allow_stretch: True
                size_hint_y: 1.4
            Label:
                id: alert_label
                text_size: self.size
                font_size: str(0.03*app.width) + 'sp'
                halign: 'center'
                valign: 'middle'
                text: '[color=455A64]PLEASE REMOVE YOUR TAPE MEASURE FROM THE MACHINE NOW.[/color]'
                markup: 'True'
                #size_hint_y: 0.2
        
            AnchorLayout:
                Button:
                    font_size: str(0.01875 * app.width) + 'sp'
                    #size: self.texture_size
                    size_hint_y: 0.8
                    size_hint_x: 0.35
                    valign: 'top'
                    halign: 'center'
                    background_normal: ''
                    background_color: hex('#EF9A9A')
                    disabled: False
                    on_press: 
                        root.next_screen()
    
                    BoxLayout:
                        padding:[dp(0.00625)*app.width, dp(0.0104166666667)*app.height]
                        size: self.parent.size
                        pos: self.parent.pos
                        
                        Label:
                            font_size: str(0.0325*app.width) + 'sp'
                            text: '[color=FFFFFF]Ok, continue...[/color]'
                            markup: 'True'
                
"""
)


class TapeMeasureScreenClass(Screen):
    return_to_screen = StringProperty()
    alert_label = ObjectProperty()

    def __init__(self, **kwargs):
        super(TapeMeasureScreenClass, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.alert_label.text = """[color=455A64]
TAPE MEASURE WARNING!
Please remove your tape measure from the machine now.[/color]"""

    def next_screen(self):
        self.sm.current = self.return_to_screen
