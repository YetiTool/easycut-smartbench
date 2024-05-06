"""
Created on 19 February 2020
Landing Screen for the Shape Cutter App

@author: Letty
"""
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from asmcnc.apps.shapeCutter_app.screens import popup_info
from asmcnc.core_UI.popups import InfoPopup

Builder.load_string(
    """

<ShapeCutterLandingScreenClass>:
    
    BoxLayout:
        height: app.get_scaled_height(800.000000002)
        width: app.get_scaled_width(480.0)
        canvas:
            Rectangle: 
                pos: self.pos
                size: self.size
                source: "./asmcnc/apps/shapeCutter_app/img/landing_background.png"

        BoxLayout:
            padding: 0
            spacing: 0
            orientation: "vertical"       
                
            Label:
                size_hint: (None,None)
                height: app.get_scaled_height(90.0)
                width: app.get_scaled_width(800.0)
                text: "Welcome to Shape Cutter"
                font_size: app.get_scaled_width(30.0)
                halign: "center"
                valign: "bottom"
                markup: True
                   
                    
            BoxLayout:
                size_hint: (None,None)
                width: app.get_scaled_width(800.0)
                height: app.get_scaled_height(140.0)
                padding: 0
                spacing: 0
                Label:
                    size_hint: (None,None)
                    height: app.get_scaled_height(170.0)
                    width: app.get_scaled_width(800.0)
                    halign: "center"
                    valign: "middle"
                    text: "Select a shape to cut..."
                    color: 0,0,0,1
                    font_size: app.get_scaled_width(26.0)
                    markup: True

            BoxLayout:
                size_hint: (None,None)
                width: app.get_scaled_width(800.0)
                height: app.get_scaled_height(170.0)
                padding: app.get_scaled_tuple([180.0, 0.0, 180.0, 30.0])
                spacing: 0
                orientation: 'horizontal'
                pos: self.parent.pos                
                
                BoxLayout:
                    size_hint: (None,None)
                    width: app.get_scaled_width(220.0)
                    height: app.get_scaled_height(170.0)
                    padding: app.get_scaled_tuple([25.0, 0.0, 27.0, 0.0])
                    pos: self.parent.pos
                    
                    # Circle button
                    Button:
                        font_size: app.get_scaled_sp('15.0sp')
                        size_hint: (None,None)
                        height: app.get_scaled_height(168.0)
                        width: app.get_scaled_width(168.0)
                        background_color: hex('#F4433600')
                        center: self.parent.center
                        pos: self.parent.pos
                        on_press: root.cut_circle()
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                source: "./asmcnc/apps/shapeCutter_app/img/cut_circle.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True
                BoxLayout:
                    size_hint: (None,None)
                    width: app.get_scaled_width(220.0)
                    height: app.get_scaled_height(170.0)
                    padding: app.get_scaled_tuple([27.0, 0.0, 25.0, 0.0])
                    pos: self.parent.pos
                    
                    # rectangle button
                    Button:
                        font_size: app.get_scaled_sp('15.0sp')
                        size_hint: (None,None)
                        height: app.get_scaled_height(168.0)
                        width: app.get_scaled_width(168.0)
                        background_color: hex('#F4433600')
                        center: self.parent.center
                        pos: self.parent.pos
                        on_press: root.cut_rectangle()
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                source: "./asmcnc/apps/shapeCutter_app/img/cut_rectangle.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True  
            # Info button
            BoxLayout:
                size_hint: (None,None)
                width: app.get_scaled_width(800.0)
                height: app.get_scaled_height(80.0000000002)
                padding: app.get_scaled_tuple([20.0, 0.0, 0.0, 20.0])
                spacing: app.get_scaled_width(680.0)
                orientation: 'horizontal'
                pos: self.parent.pos
                Button:
                    font_size: app.get_scaled_sp('15.0sp')
                    id: info_button
                    size_hint: (None,None)
                    height: app.get_scaled_height(40.0)
                    width: app.get_scaled_width(40.0)
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
                    font_size: app.get_scaled_sp('15.0sp')
                    id: exit_button
                    size_hint: (None,None)
                    height: app.get_scaled_height(40.0)
                    width: app.get_scaled_width(40.0)
                    background_color: hex('#F4433600')
                    opacity: 1
                    on_press: root.exit()
                    BoxLayout:
                        padding: 0
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            source: "./asmcnc/apps/shapeCutter_app/img/exit_icon.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True                             
"""
)


class ShapeCutterLandingScreenClass(Screen):
    info_button = ObjectProperty()

    def __init__(self, **kwargs):
        super(ShapeCutterLandingScreenClass, self).__init__(**kwargs)
        self.shapecutter_sm = kwargs["shapecutter"]
        self.m = kwargs["machine"]
        self.j = kwargs["job_parameters"]

    def on_pre_enter(self):
        self.m.get_grbl_settings()

    def get_info(self):
        description = "If this is your first time using the app, please go to the tutorial.\n\n" \
                            "If you need help or support, please visit customer support at www.yetitool.com/support"
        InfoPopup(sm=self.shapecutter_sm, m=self.m, l=self.m.l,
                  main_string=description,
                  popup_width=400,
                  popup_height=380,
                  button_layout_padding=[50,20,50,0],
                  main_layout_padding=[50,20,50,20],
                  main_label_padding=[20,20],
                  main_label_size_hint_y=1,
                  button_one_text="Tutorial",
                  button_one_callback=self.shapecutter_sm.tutorial,
                  button_one_background_color=[0.141, 0.596, 0.957, 1],
                  button_two_text="Ok",
                  button_two_callback=None,
                  button_two_background_color=[76 / 255., 175 / 255., 80 / 255., 1.]).open()

    def cut_rectangle(self):
        self.j.shape_dict["shape"] = "rectangle"
        self.next_screen()

    def cut_circle(self):
        self.j.shape_dict["shape"] = "circle"
        self.next_screen()

    def next_screen(self):
        self.shapecutter_sm.next_screen()

    def exit(self):
        self.shapecutter_sm.exit_shapecutter()
