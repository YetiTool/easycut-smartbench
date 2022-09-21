from kivy.lang import Builder
from kivy.uix.widget import Widget
from asmcnc.comms.yeti_grbl_protocol.c_defines import *
from asmcnc.skavaUI import popup_info

Builder.load_string("""
<CurrentAdjustmentWidget>

    current_current_label:current_current_label

    BoxLayout:
        size: self.parent.size
        pos: self.parent.pos      
        
        orientation: "vertical"
        
        Button:
            on_press: root.current_up()
            background_color: 1, 1, 1, 0 
            BoxLayout:
                padding: 2
                size: self.parent.size
                pos: self.parent.pos      
                Image:
                    id: speed_image
                    source: "./asmcnc/skavaUI/img/feed_speed_up.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True  
       
        Label:
            id: current_current_label
        
        Button:
            on_press: root.current_down()
            background_color: 1, 1, 1, 0 
            BoxLayout:
                padding: 2
                size: self.parent.size
                pos: self.parent.pos      
                Image:
                    id: speed_image
                    source: "./asmcnc/skavaUI/img/feed_speed_down.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

""")
    

class CurrentAdjustmentWidget(Widget):

    def __init__(self, **kwargs):
        super(CurrentAdjustmentWidget, self).__init__(**kwargs)

        self.m = kwargs['m']
        self.motor = kwargs['motor']
        self.l = kwargs['localization']
        self.systemtools_sm = kwargs['systemtools']

        self.motor_name_dict = {TMC_X1:'X1', TMC_X2:'X2', TMC_Y1:'Y1', TMC_Y2:'Y2', TMC_Z:'Z'}
        self.current_current = self.m.TMC_motor[self.motor].ActiveCurrentScale
        self.current_current_label.text = self.motor_name_dict[self.motor] + ' = ' + str(self.current_current)

    def current_up(self):

        if self.m.state().startswith('Idle'):
            if self.current_current != 31:
                self.current_current += 1
                self.m.set_motor_current("Z", self.current_current)
                self.current_current_label.text = self.motor_name_dict[self.motor] + ' = ' + str(self.current_current)

        else:
            popup_info.PopupError(self.systemtools_sm, self.l, "Can't change current when not Idle!")

    def current_down(self):

        if self.m.state().startswith('Idle'):
            if self.current_current != 0:
                self.current_current -= 1
                self.m.set_motor_current("Z", self.current_current)
                self.current_current_label.text = self.motor_name_dict[self.motor] + ' = ' + str(self.current_current)

        else:
            popup_info.PopupError(self.systemtools_sm, self.l, "Can't change current when not Idle!")

    def reset_current(self):
        self.current_current = self.m.TMC_motor[self.motor].ActiveCurrentScale
        self.m.set_motor_current("Z", self.current_current)
        self.current_current_label.text = self.motor_name_dict[self.motor] + ' = ' + str(self.current_current)
