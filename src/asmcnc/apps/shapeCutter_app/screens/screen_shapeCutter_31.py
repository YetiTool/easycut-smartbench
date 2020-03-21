'''
Created on 5 March 2020
Screen 31 for the Shape Cutter App

@author: Letty
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import MetricsBase
from kivy.properties import StringProperty, ObjectProperty
from kivy.clock import Clock

from asmcnc.apps.shapeCutter_app.screens import widget_sC31_xy_move, widget_sC31_z_setgo, widget_sC31_z_move, widget_sC_work_coordinates
from asmcnc.apps.shapeCutter_app.screens import popup_input_error

Builder.load_string("""

<ShapeCutter31ScreenClass>

    info_button: info_button
    xy_move_container: xy_move_container
    z_move_container: z_move_container
    z_set_go_container: z_set_go_container
    work_coords_container: work_coords_container
    
    BoxLayout:
        size_hint: (None,None)
        width: dp(800)
        height: dp(480)
        padding: 0
        spacing: 0
        orientation: "vertical"

        BoxLayout:
            size_hint: (None,None)
            width: dp(800)
            height: dp(90)
            padding: 0
            spacing: 0
            orientation: "horizontal"

            Button:
                size_hint: (None,None)
                height: dp(90)
                width: dp(142)
                on_press: root.prepare()
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/apps/shapeCutter_app/img/prepare_tab_blue.png"
                        size: self.parent.size
                        stretch: True
            Button:
                size_hint: (None,None)
                height: dp(90)
                width: dp(142)
                on_press: root.load()
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/apps/shapeCutter_app/img/load_tab_blue.png"
                        size: self.parent.size
                        stretch: True
            Button:
                size_hint: (None,None)
                height: dp(90)
                width: dp(142)
                on_press: root.define()
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/apps/shapeCutter_app/img/define_job_tab_blue.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
            Button:
                size_hint: (None,None)
                height: dp(90)
                width: dp(142)
                on_press: root.position()
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/apps/shapeCutter_app/img/position_tab_grey.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
            Button:
                size_hint: (None,None)
                height: dp(90)
                width: dp(142)
                on_press: root.check()
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/apps/shapeCutter_app/img/check_tab_blue.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
            Button:
                size_hint: (None,None)
                height: dp(90)
                width: dp(90)
                on_press: root.exit()
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/apps/shapeCutter_app/img/exit_cross.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True                    
                    
        BoxLayout:
            size_hint: (None,None)
            padding: 0
            height: dp(390)
            width: dp(800)
            canvas:
                Rectangle: 
                    pos: self.pos
                    size: self.size
                    source: "./asmcnc/apps/shapeCutter_app/img/background.png"
            
            BoxLayout:
                orientation: "vertical"
                padding: 0
                spacing: 0
                    
                BoxLayout: #Header
                    size_hint: (None,None)
                    height: dp(60)
                    width: dp(800)
                    padding: (20,0,0,0)
                    orientation: "horizontal"
                    
                    BoxLayout: #Screen number
                        size_hint: (None,None)
                        padding: 0
                        height: dp(40)
                        width: dp(40)
                        canvas:
                            Rectangle: 
                                pos: self.pos
                                size: self.size
                                source: "./asmcnc/apps/shapeCutter_app/img/number_box.png"
                        Label:
                            text: root.screen_number
                            valign: "middle"
                            halign: "center"
                            font_size: 26
                            markup: True
                                
                                
                        
                    BoxLayout: #Title
                        size_hint: (None,None)
                        height: dp(60)
                        width: dp(740)
                        padding: (20,20,0,0)
                        
                        Label:
                            text: root.title_label
                            color: 0,0,0,1
                            font_size: 28
                            markup: True
                            halign: "left"
                            valign: "bottom"
                            text_size: self.size
                            size: self.parent.size
                            pos: self.parent.pos
                        
                    
                BoxLayout: #Body
                    size_hint: (None,None)
                    height: dp(330)
                    width: dp(800)
                    padding: 0,0,0,0
                    orientation: "horizontal"
                    
                    BoxLayout: # move widget
                        id: xy_move_container
                        size_hint: (None,None)
                        height: dp(330)
                        width: dp(280)
                        padding: (20,0,0,5) 
                        orientation: "vertical"                                         
                                            
                    BoxLayout: # Z move & common move widget
                        size_hint: (None,None)
                        height: dp(330)
                        width: dp(395)
                        padding: (0,0,0,10)
                        orientation: "vertical"
                        BoxLayout: 
                            size_hint: (None,None)
                            height: dp(260)
                            width: dp(395)
                            padding: (15,0,15,0)
                            orientation: "horizontal"
                            BoxLayout: # common move
                                id: z_set_go_container
                                size_hint: (None, None)
                                height: dp(260)
                                width: dp(165)
                            BoxLayout: # Z move
                                id: z_move_container
                                size_hint: (None, None)
                                height: dp(260)
                                width: dp(200)
                        
                        BoxLayout: 
                            id: work_coords_container
                            size_hint: (None,None)
                            height: dp(60)
                            width: dp(395)
                            padding: (0,15,40,5)

                    BoxLayout: #action box
                        size_hint: (None,None)
                        height: dp(310)
                        width: dp(125)
                        padding: 0,0,0,34
                        spacing: 34
                        orientation: "vertical"
                        
                        BoxLayout: 
                            size_hint: (None,None)
                            height: dp(67)
                            width: dp(88)
                            padding: (24,0,24,34)
                            Button:
                                id: info_button
                                size_hint: (None,None)
                                height: dp(40)
                                width: dp(40)
                                background_color: hex('#F4433600')
                                opacity: 1
                                on_press: root.get_info()
                                BoxLayout:
                                    padding: 0
                                    size: self.parent.size
                                    pos: self.parent.pos
                                    Image:
                                        source: "./asmcnc/apps/shapeCutter_app/img/info_icon.png"
                                        center_x: self.parent.center_x
                                        y: self.parent.y
                                        size: self.parent.width, self.parent.height
                                        allow_stretch: True

                        Button: 
                            size_hint: (None,None)
                            height: dp(67)
                            width: dp(88)
                            background_color: hex('#F4433600')
                            on_press: root.go_back()
                            BoxLayout:
                                padding: 0
                                size: self.parent.size
                                pos: self.parent.pos
                                Image:
                                    source: "./asmcnc/apps/shapeCutter_app/img/arrow_back.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True
                        Button: 
                            size_hint: (None,None)
                            height: dp(67)
                            width: dp(88)
                            background_color: hex('#F4433600')
                            on_press: root.next_screen()
                            BoxLayout:
                                padding: 0
                                size: self.parent.size
                                pos: self.parent.pos
                                Image:
                                    source: "./asmcnc/apps/shapeCutter_app/img/arrow_next.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True               

""")

class ShapeCutter31ScreenClass(Screen):
    
    info_button = ObjectProperty()
    
    screen_number = StringProperty("[b]31[/b]")
    title_label = StringProperty("[b]Set job Z datum[/b]")
    user_instructions = StringProperty()
    
    def __init__(self, **kwargs):
        super(ShapeCutter31ScreenClass, self).__init__(**kwargs)
        self.shapecutter_sm = kwargs['shapecutter']
        self.m=kwargs['machine']
        self.j=kwargs['job_parameters']

        self.xy_move_widget = widget_sC31_xy_move.SC31XYMove(machine=self.m, screen_manager=self.shapecutter_sm.sm, job_parameters = self.j)
        self.xy_move_container.add_widget(self.xy_move_widget)
        
        self.z_set_go_widget = widget_sC31_z_setgo.SC31ZSetGo(machine=self.m, screen_manager=self.shapecutter_sm.sm, )
        self.z_set_go_container.add_widget(self.z_set_go_widget)
        
        self.z_move_widget = widget_sC31_z_move.SC31ZMove(machine=self.m, screen_manager=self.shapecutter_sm.sm, job_parameters = self.j)
        self.z_move_container.add_widget(self.z_move_widget)

        self.work_coords_widget = widget_sC_work_coordinates.WorkCoordinates(machine=self.m, screen_manager=self.shapecutter_sm.sm)
        self.work_coords_container.add_widget(self.work_coords_widget)

    def on_pre_enter(self):
        self.info_button.opacity = 1
        self.z_set_go_widget.set_jog_speeds()

# Action buttons
    def get_info(self):
        pass
    
    def go_back(self):
        if not self.m.state().startswith('Jog'):
            self.shapecutter_sm.previous_screen()
        else:
            pass
    
    def next_screen(self):
        if not self.m.state().startswith('Jog'):
            self.bounding_box_test()
        else:
            pass
    
# Tab functions

    def prepare(self):
        if not self.m.state().startswith('Jog'):
            self.shapecutter_sm.prepare_tab()
        else:
            pass  
    

    def load(self):

        if not self.m.state().startswith('Jog'):
            self.shapecutter_sm.load_tab()
        else:
            pass  

    
    def define(self):

        if not self.m.state().startswith('Jog'):
            self.shapecutter_sm.define_tab()
        else:
            pass  
    
    def position(self):
        
        if not self.m.state().startswith('Jog'):
            self.shapecutter_sm.position_tab()
        else:
            pass  

    
    def check(self):
        
        if not self.m.state().startswith('Jog'):
            self.shapecutter_sm.check_tab()
        else:
            pass 
    
    def exit(self):
        self.shapecutter_sm.exit_shapecutter()
 
    def bounding_box_test(self):
        bounds_output = self.j.is_job_within_bounds()
        
        if bounds_output == True:
            self.shapecutter_sm.next_screen()
        else: 
            description = "The job is not within the bounds of SmartBench.\n\n" + \
            bounds_output + '\n\n' + \
            "Please go back and re-set your job datums."
            popup_input_error.PopupInputError(self.shapecutter_sm, description)