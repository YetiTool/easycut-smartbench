"""
Created on 2 March 2020
Tutorial Screen for the Shape Cutter App

@author: Letty
"""
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import MetricsBase
from kivy.properties import StringProperty, ObjectProperty
from kivy.clock import Clock
from asmcnc.apps.shapeCutter_app.screens import popup_info
from asmcnc.core_UI.popups import InfoPopup

Builder.load_string(
    """

<ShapeCutterTutorialScreenClass>

    info_button: info_button
    user_instructions: user_instructions
    back_arrow: back_arrow
    next_arrow: next_arrow
    
    prepare_tab: prepare_tab
    load_tab: load_tab 
    define_tab: define_tab
    position_tab: position_tab
    check_tab: check_tab

    BoxLayout:
        size_hint: (None,None)
        width: app.get_scaled_width(800.0)
        height: app.get_scaled_height(480.0)
        padding: 0
        spacing: 0
        orientation: "vertical"

        BoxLayout:
            size_hint: (None,None)
            width: app.get_scaled_width(800.0)
            height: app.get_scaled_height(90.0)
            padding: 0
            spacing: 0
            orientation: "horizontal"

            Button:
                font_size: app.get_scaled_sp('15.0sp')
                id: prepare_tab
                size_hint: (None,None)
                height: app.get_scaled_height(90.0)
                width: app.get_scaled_width(142.0)
                disabled: True
                on_press: root.prepare()
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/apps/shapeCutter_app/img/prepare_tab_blue.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
            Button:
                font_size: app.get_scaled_sp('15.0sp')
                id: load_tab
                size_hint: (None,None)
                height: app.get_scaled_height(90.0)
                width: app.get_scaled_width(142.0)
                disabled: True
                on_press: root.load()
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/apps/shapeCutter_app/img/load_tab_blue.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
            Button:
                font_size: app.get_scaled_sp('15.0sp')
                id: define_tab
                size_hint: (None,None)
                height: app.get_scaled_height(90.0)
                width: app.get_scaled_width(142.0)
                disabled: True
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
                font_size: app.get_scaled_sp('15.0sp')
                id: position_tab
                size_hint: (None,None)
                height: app.get_scaled_height(90.0)
                width: app.get_scaled_width(142.0)
                disabled: True
                on_press: root.position()
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/apps/shapeCutter_app/img/position_tab_blue.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
            Button:
                font_size: app.get_scaled_sp('15.0sp')
                id: check_tab
                size_hint: (None,None)
                height: app.get_scaled_height(90.0)
                width: app.get_scaled_width(142.0)
                disabled: True
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
                font_size: app.get_scaled_sp('15.0sp')
                size_hint: (None,None)
                height: app.get_scaled_height(90.0)
                width: app.get_scaled_width(90.0)
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
            height: app.get_scaled_height(390.0)
            width: app.get_scaled_width(800.0)
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
                    height: app.get_scaled_height(60.0)
                    width: app.get_scaled_width(800.0)
                    padding: app.get_scaled_tuple([20.0, 0.0, 0.0, 0.0])
                    orientation: "horizontal"
                    
                    BoxLayout: #Screen number
                        size_hint: (None,None)
                        padding: 0
                        height: app.get_scaled_height(40.0)
                        width: app.get_scaled_width(40.0)
                        canvas:
                            Rectangle: 
                                pos: self.pos
                                size: self.size
                                source: "./asmcnc/apps/shapeCutter_app/img/info_icon.png"
                        
                    BoxLayout: #Title
                        size_hint: (None,None)
                        height: app.get_scaled_height(60.0)
                        width: app.get_scaled_width(740.0)
                        padding: app.get_scaled_tuple([20.0, 20.0, 0.0, 0.0])
                        
                        Label:
                            text: root.title_label
                            color: 0,0,0,1
                            font_size: app.get_scaled_width(28.0)
                            markup: True
                            halign: "left"
                            valign: "bottom"
                            text_size: self.size
                            size: self.parent.size
                            pos: self.parent.pos
                        
                    
                BoxLayout: #Body
                    size_hint: (None,None)
                    height: app.get_scaled_height(330.0)
                    width: app.get_scaled_width(800.0)
                    padding: app.get_scaled_tuple([0.0, 20.0, 0.0, 0.0])
                    orientation: "horizontal"
                    
                    BoxLayout: #text box
                        size_hint: (None,None)
                        height: app.get_scaled_height(310.0)
                        width: app.get_scaled_width(675.0)
                        padding: app.get_scaled_tuple([80.0, 0.0, 0.0, 0.0])
                        
                        Label:
                            id: user_instructions
                            color: 0,0,0,1
                            font_size: app.get_scaled_width(20.0)
                            markup: True
                            halign: "left"
                            valign: "top"
                            text_size: self.size
                            size: self.parent.size
                            pos: self.parent.pos

                    BoxLayout: #action box
                        size_hint: (None,None)
                        height: app.get_scaled_height(310.0)
                        width: app.get_scaled_width(125.0)
                        padding: app.get_scaled_tuple([0.0, 0.0, 0.0, 34.0])
                        spacing: app.get_scaled_width(34.0)
                        orientation: "vertical"
                        
                        BoxLayout: 
                            size_hint: (None,None)
                            height: app.get_scaled_height(66.9999999998)
                            width: app.get_scaled_width(88.0)
                            padding: app.get_scaled_tuple([24.0, 0.0, 24.0, 34.0])
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
                            id: back_arrow
                            size_hint: (None,None)
                            height: app.get_scaled_height(66.9999999998)
                            width: app.get_scaled_width(88.0)
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
                            font_size: app.get_scaled_sp('15.0sp')
                            id: next_arrow
                            size_hint: (None,None)
                            height: app.get_scaled_height(66.9999999998)
                            width: app.get_scaled_width(88.0)
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

"""
)


class ShapeCutterTutorialScreenClass(Screen):
    info_button = ObjectProperty()
    screen_number = StringProperty("[b]I[/b]")
    title_label = StringProperty("[b]Using the app[/b]")
    instructions_list = [
        "Use the Back and Next buttons to move through each section.\n\n",
        """Use the navigation tabs to move between sections.

""",
        "Press the [b]i[/b] if you need more information.\n\n",
        "For more help, see the video at www.yetitool.com/support",
    ]

    def __init__(self, **kwargs):
        super(ShapeCutterTutorialScreenClass, self).__init__(**kwargs)
        self.shapecutter_sm = kwargs["shapecutter"]
        self.m = kwargs["machine"]

    def on_pre_enter(self):
        self.user_instructions.text = ""
        self.info_button.disabled = True
        self.next_arrow.disabled = True
        self.back_arrow.disabled = True

    def on_enter(self):
        Clock.schedule_once(lambda dt: self.append_instructions(0), 0.5)
        Clock.schedule_once(lambda dt: self.flashy_arrows(), 1)
        Clock.schedule_once(lambda dt: self.append_instructions(1), 3.5)
        Clock.schedule_once(lambda dt: self.flashy_tabs(), 4)
        Clock.schedule_once(lambda dt: self.append_instructions(2), 7)
        Clock.schedule_once(lambda dt: self.flashy_info(), 7.5)
        Clock.schedule_once(lambda dt: self.append_instructions(3), 10)
        Clock.schedule_once(lambda dt: self.enable_buttons(), 10)

    def append_instructions(self, n):
        self.user_instructions.text = self.user_instructions.text + str(
            self.instructions_list[n]
        )

    def flashy_arrows(self):
        arrow_flash = Clock.schedule_interval(lambda dt: arrow_opacity(), 0.2)
        Clock.schedule_once(lambda dt: cancel_arrow_flash(), 1.9)

        def arrow_opacity():
            if self.next_arrow.opacity == 1:
                self.next_arrow.opacity = 0.6
                self.back_arrow.opacity = 0.6
            else:
                self.next_arrow.opacity = 1
                self.back_arrow.opacity = 1

        def cancel_arrow_flash():
            Clock.unschedule(arrow_flash)
            self.next_arrow.opacity = 1
            self.back_arrow.opacity = 1

    def flashy_tabs(self):
        self.flash_counter = 0
        tab_flash = Clock.schedule_interval(lambda dt: tab_opacity(), 0.4)

        def tab_opacity():
            if self.flash_counter == 0:
                self.flash_counter = 1
                self.prepare_tab.opacity = 0.6
            elif self.flash_counter == 1:
                self.flash_counter = 2
                self.prepare_tab.opacity = 1
                self.load_tab.opacity = 0.6
            elif self.flash_counter == 2:
                self.flash_counter = 3
                self.load_tab.opacity = 1
                self.define_tab.opacity = 0.6
            elif self.flash_counter == 3:
                self.flash_counter = 4
                self.define_tab.opacity = 1
                self.position_tab.opacity = 0.6
            elif self.flash_counter == 4:
                self.flash_counter = 5
                self.position_tab.opacity = 1
                self.check_tab.opacity = 0.6
            elif self.flash_counter == 5:
                self.flash_counter = 0
                self.check_tab.opacity = 1
                cancel_tab_flash()

        def cancel_tab_flash():
            Clock.unschedule(tab_flash)


# Action buttons       

    def flashy_info(self):
        info_flash = Clock.schedule_interval(lambda dt: info_opacity(), 0.2)
        Clock.schedule_once(lambda dt: cancel_info_flash(), 1.9)

        def info_opacity():
            if self.info_button.opacity == 1:
                self.info_button.opacity = 0.4
            else:
                self.info_button.opacity = 1

        def cancel_info_flash():
            Clock.unschedule(info_flash)
            self.info_button.opacity = 1

    def enable_buttons(self):
        self.info_button.disabled = False
        self.next_arrow.disabled = False
        self.back_arrow.disabled = False

    def get_info(self):
        info = """Hi there! I'm a pop-up!.

If you get stuck, I'm here to give you some handy hints and tips ;). 

Happy shaping!"""
        InfoPopup(sm=self.shapecutter_sm, m=self.m, l=self.m.l,
                  main_string=info,
                  popup_width=500,
                  popup_height=400,
                  main_label_size_delta=140).open()

    def go_back(self):
        self.shapecutter_sm.previous_screen()

    def next_screen(self):
        self.shapecutter_sm.next_screen()
    
# Tab functions

    def prepare(self):
        self.shapecutter_sm.prepare_tab()

    def load(self):
        self.shapecutter_sm.load_tab()

    def define(self):
        self.shapecutter_sm.define_tab()

    def position(self):
        self.shapecutter_sm.position_tab()

    def check(self):
        self.shapecutter_sm.check_tab()

    def exit(self):
        self.shapecutter_sm.exit_shapecutter()

# Tutorial specific functions

    def arrows(self):
        pass

    def nav_tabs(self):
        pass

    def info_button(self):
        pass

    def more_help(self):
        pass
