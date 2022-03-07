from kivy.lang import Builder
from kivy.uix.widget import Widget
from asmcnc.comms.yeti_grbl_protocol.c_defines import *

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

        self.motor_name_dict = {TMC_X1:'X', TMC_Y1:'Y1', TMC_Y2:'Y2'}
        self.current_current = self.m.TMC_motor[self.motor].ActiveCurrentScale
        self.current_current_label.text = self.motor_name_dict[self.motor] + ' = ' + str(self.current_current)

    def current_up(self):
        if self.current_current != 31:
            self.current_current += 1
            self.m.send_command_to_motor('SET ACTIVE CURRENT ' + self.motor_name_dict[self.motor] + ' ' + str(self.current_current), motor=self.motor, command=SET_ACTIVE_CURRENT, value=self.current_current)
            self.current_current_label.text = self.motor_name_dict[self.motor] + ' = ' + str(self.current_current)

    def current_down(self):
        if self.current_current != 0:
            self.current_current -= 1
            self.m.send_command_to_motor('SET ACTIVE CURRENT ' + self.motor_name_dict[self.motor] + ' ' + str(self.current_current), motor=self.motor, command=SET_ACTIVE_CURRENT, value=self.current_current)
            self.current_current_label.text = self.motor_name_dict[self.motor] + ' = ' + str(self.current_current)

    def reset_current(self):
        self.current_current = self.m.TMC_motor[self.motor].ActiveCurrentScale
        self.m.send_command_to_motor('SET ACTIVE CURRENT ' + self.motor_name_dict[self.motor] + ' ' + str(self.current_current), motor=self.motor, command=SET_ACTIVE_CURRENT, value=self.current_current)
        self.current_current_label.text = self.motor_name_dict[self.motor] + ' = ' + str(self.current_current)
