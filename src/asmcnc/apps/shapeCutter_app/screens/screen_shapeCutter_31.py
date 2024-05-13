"""
Created on 5 March 2020
Screen 31 for the Shape Cutter App

@author: Letty
"""
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import MetricsBase
from kivy.properties import StringProperty, ObjectProperty
from kivy.clock import Clock
from asmcnc.apps.shapeCutter_app.screens import (
    widget_sC31_xy_move,
    widget_sC31_z_setgo,
    widget_sC31_z_move,
    widget_sC_work_coordinates,
)
from asmcnc.apps.shapeCutter_app.screens import popup_input_error, popup_info
from asmcnc.core_UI.popups import InfoPopup

Builder.load_string(
    """

<ShapeCutter31ScreenClass>

    info_button: info_button
    xy_move_container: xy_move_container
    z_move_container: z_move_container
    z_set_go_container: z_set_go_container
    work_coords_container: work_coords_container
    
    BoxLayout:
        size_hint: (None,None)
        width: dp(1.0*app.width)
        height: dp(1.0*app.height)
        padding: 0
        spacing: 0
        orientation: "vertical"

        BoxLayout:
            size_hint: (None,None)
            width: dp(1.0*app.width)
            height: dp(0.1875*app.height)
            padding: 0
            spacing: 0
            orientation: "horizontal"

            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint: (None,None)
                height: dp(0.1875*app.height)
                width: dp(0.1775*app.width)
                on_press: root.prepare()
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/apps/shapeCutter_app/img/prepare_tab_blue.png"
                        size: self.parent.size
                        allow_stretch: True
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint: (None,None)
                height: dp(0.1875*app.height)
                width: dp(0.1775*app.width)
                on_press: root.load()
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/apps/shapeCutter_app/img/load_tab_blue.png"
                        size: self.parent.size
                        allow_stretch: True
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint: (None,None)
                height: dp(0.1875*app.height)
                width: dp(0.1775*app.width)
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
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint: (None,None)
                height: dp(0.1875*app.height)
                width: dp(0.1775*app.width)
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
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint: (None,None)
                height: dp(0.1875*app.height)
                width: dp(0.1775*app.width)
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
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint: (None,None)
                height: dp(0.1875*app.height)
                width: dp(0.1125*app.width)
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
            height: dp(0.8125*app.height)
            width: dp(1.0*app.width)
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
                    height: dp(0.125*app.height)
                    width: dp(1.0*app.width)
                    padding:[dp(0.025)*app.width, 0, 0, 0]
                    orientation: "horizontal"
                    
                    BoxLayout: #Screen number
                        size_hint: (None,None)
                        padding: 0
                        height: dp(0.0833333333333*app.height)
                        width: dp(0.05*app.width)
                        canvas:
                            Rectangle: 
                                pos: self.pos
                                size: self.size
                                source: "./asmcnc/apps/shapeCutter_app/img/number_box.png"
                        Label:
                            text: root.screen_number
                            valign: "middle"
                            halign: "center"
                            font_size: 0.0325*app.width
                            markup: True
                                
                                
                        
                    BoxLayout: #Title
                        size_hint: (None,None)
                        height: dp(0.125*app.height)
                        width: dp(0.925*app.width)
                        padding:[dp(0.025)*app.width, dp(0.0416666666667)*app.height, 0, 0]
                        
                        Label:
                            text: root.title_label
                            color: color_provider.get_rgba("black")
                            font_size: 0.035*app.width
                            markup: True
                            halign: "left"
                            valign: "bottom"
                            text_size: self.size
                            size: self.parent.size
                            pos: self.parent.pos
                        
                    
                BoxLayout: #Body
                    size_hint: (None,None)
                    height: dp(0.6875*app.height)
                    width: dp(1.0*app.width)
                    padding:[0, 0, 0, 0]
                    orientation: "horizontal"
                    
                    BoxLayout: # move widget
                        id: xy_move_container
                        size_hint: (None,None)
                        height: dp(0.6875*app.height)
                        width: dp(0.35*app.width)
                        padding:[dp(0.025)*app.width, 0, 0, dp(0.0104166666667)*app.height]
                        orientation: "vertical"                                         
                                            
                    BoxLayout: # Z move & common move widget
                        size_hint: (None,None)
                        height: dp(0.6875*app.height)
                        width: dp(0.49375*app.width)
                        padding:[0, 0, 0, dp(0.0208333333333)*app.height]
                        orientation: "vertical"
                        BoxLayout: 
                            size_hint: (None,None)
                            height: dp(0.541666666667*app.height)
                            width: dp(0.49375*app.width)
                            padding:[dp(0.01875)*app.width, 0, dp(0.01875)*app.width, 0]
                            orientation: "horizontal"
                            BoxLayout: # common move
                                id: z_set_go_container
                                size_hint: (None, None)
                                height: dp(0.541666666667*app.height)
                                width: dp(0.20625*app.width)
                            BoxLayout: # Z move
                                id: z_move_container
                                size_hint: (None, None)
                                height: dp(0.541666666667*app.height)
                                width: dp(0.25*app.width)
                        
                        BoxLayout: 
                            id: work_coords_container
                            size_hint: (None,None)
                            height: dp(0.125*app.height)
                            width: dp(0.49375*app.width)
                            padding:[0, dp(0.03125)*app.height, dp(0.05)*app.width, dp(0.0104166666667)*app.height]

                    BoxLayout: #action box
                        size_hint: (None,None)
                        height: dp(0.645833333333*app.height)
                        width: dp(0.15625*app.width)
                        padding:[0, 0, 0, dp(0.0708333333333)*app.height]
                        spacing:0.0708333333333*app.height
                        orientation: "vertical"
                        
                        BoxLayout: 
                            size_hint: (None,None)
                            height: dp(0.139583333333*app.height)
                            width: dp(0.11*app.width)
                            padding:[dp(0.03)*app.width, 0, dp(0.03)*app.width, dp(0.0708333333333)*app.height]
                            Button:
                                font_size: str(0.01875 * app.width) + 'sp'
                                id: info_button
                                size_hint: (None,None)
                                height: dp(0.0833333333333*app.height)
                                width: dp(0.05*app.width)
                                background_color: color_provider.get_rgba("transparent")
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
                            font_size: str(0.01875 * app.width) + 'sp'
                            size_hint: (None,None)
                            height: dp(0.139583333333*app.height)
                            width: dp(0.11*app.width)
                            background_color: color_provider.get_rgba("transparent")
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
                            font_size: str(0.01875 * app.width) + 'sp'
                            size_hint: (None,None)
                            height: dp(0.139583333333*app.height)
                            width: dp(0.11*app.width)
                            background_color: color_provider.get_rgba("transparent")
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

"""
)


class ShapeCutter31ScreenClass(Screen):
    info_button = ObjectProperty()
    screen_number = StringProperty("[b]31[/b]")
    title_label = StringProperty("[b]Set job Z datum[/b]")
    user_instructions = StringProperty()

    def __init__(self, **kwargs):
        super(ShapeCutter31ScreenClass, self).__init__(**kwargs)
        self.shapecutter_sm = kwargs["shapecutter"]
        self.m = kwargs["machine"]
        self.l = kwargs["localization"]
        self.j = kwargs["job_parameters"]
        self.xy_move_widget = widget_sC31_xy_move.SC31XYMove(
            machine=self.m,
            localization=self.l,
            screen_manager=self.shapecutter_sm.sm,
            job_parameters=self.j,
        )
        self.xy_move_container.add_widget(self.xy_move_widget)
        self.z_set_go_widget = widget_sC31_z_setgo.SC31ZSetGo(
            machine=self.m, screen_manager=self.shapecutter_sm.sm
        )
        self.z_set_go_container.add_widget(self.z_set_go_widget)
        self.z_move_widget = widget_sC31_z_move.SC31ZMove(
            machine=self.m, screen_manager=self.shapecutter_sm.sm, job_parameters=self.j
        )
        self.z_move_container.add_widget(self.z_move_widget)
        self.work_coords_widget = widget_sC_work_coordinates.WorkCoordinates(
            machine=self.m, screen_manager=self.shapecutter_sm.sm
        )
        self.work_coords_container.add_widget(self.work_coords_widget)

    def on_pre_enter(self):
        self.info_button.opacity = 1
        self.z_set_go_widget.set_jog_speeds()

# Action buttons
    def get_info(self):
        info = """Move the machine by using the arrow buttons.

Use the Z0 button to set the datum using the touchplate.

Use the SET button to manually set the datum.

Use the GO button to move the machine to the datum. """
        InfoPopup(sm=self.shapecutter_sm, m=self.m, l=self.m.l,
                  main_string=info,
                  popup_width=500,
                  popup_height=400,
                  main_label_size_delta=140).open()

    def go_back(self):
        if not self.m.state().startswith("Jog"):
            self.shapecutter_sm.previous_screen()
        else:
            pass

    def next_screen(self):
        if not self.m.state().startswith("Jog"):
            self.bounding_box_test()
        else:
            pass
    
# Tab functions

    def prepare(self):
        if not self.m.state().startswith("Jog"):
            self.shapecutter_sm.prepare_tab()
        else:
            pass

    def load(self):
        if not self.m.state().startswith("Jog"):
            self.shapecutter_sm.load_tab()
        else:
            pass

    def define(self):
        if not self.m.state().startswith("Jog"):
            self.shapecutter_sm.define_tab()
        else:
            pass

    def position(self):
        if not self.m.state().startswith("Jog"):
            self.shapecutter_sm.position_tab()
        else:
            pass

    def check(self):
        if not self.m.state().startswith("Jog"):
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
            description = (
                "The job is not within the bounds of SmartBench."
                + bounds_output
                + "\n\n"
                + "Please go back and re-set your job datums."
            )
            popup_input_error.PopupBoundary(self.shapecutter_sm, description)
