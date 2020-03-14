'''
Created on 4 March 202
Screen 23 for the Shape Cutter App

@author: Letty
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import MetricsBase
from kivy.properties import StringProperty, ObjectProperty

from asmcnc.apps.shapeCutter_app.screens import popup_info

Builder.load_string("""

<ShapeCutter24ScreenClass>

    info_button: info_button
    unit_toggle: unit_toggle
    # unit_label: unit_label
    step_down_units: step_down_units
    stock_bottom_offset_units: stock_bottom_offset_units
    finishing_passes: finishing_passes
    stock_bottom_offset: stock_bottom_offset
    step_down: step_down 
    

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
                        source: "./asmcnc/apps/shapeCutter_app/img/define_job_tab_grey.png"
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
                        source: "./asmcnc/apps/shapeCutter_app/img/position_tab_blue.png"
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
                    padding: 0,20,0,0
                    orientation: "horizontal"
                    
                    BoxLayout: #text box
                        size_hint: (None,None)
                        height: dp(310)
                        width: dp(675)
                        padding: 80,0,0,0
                        orientation: "vertical"
                    
                        BoxLayout: #text box
                            size_hint: (None,None)
                            height: dp(55)
                            width: dp(675)
                            padding: 0,0,0,0
                            orientation: "vertical"                       

                        BoxLayout: #image & text entry box
                            size_hint: (None,None)
                            height: dp(255)
                            width: dp(595)
                            padding:0,0,0,21
                            orientation: "horizontal"
                                    
                            BoxLayout:
                                orientation: 'vertical'
                                size_hint: (None,None)
                                width: dp(595)
                                height: dp(255)
                                padding: (0,0,0,50)
                                spacing: 20
                                pos: self.parent.pos
                                
                                # BL horizontal
                                    # Toggle button
                                BoxLayout:
                                    size_hint: (None,None)
                                    height: dp(32)
                                    width: dp(595)
                                    padding: (342,0,170,0)                
                                    orientation: "horizontal"
                                                    
#                                     ToggleButton:
#                                         id: unit_toggle
#                                         size_hint: (None,None)
#                                         height: dp(30)
#                                         width: dp(75)
#                                         background_color: hex('#F4433600')
#                                         center: self.parent.center
#                                         pos: self.parent.pos
#                                         on_press: root.toggle_units()
#         
#                                         BoxLayout:
#                                             height: dp(30)
#                                             width: dp(75)
#                                             canvas:
#                                                 Rectangle: 
#                                                     pos: self.parent.pos
#                                                     size: self.parent.size
#                                                     source: "./asmcnc/apps/shapeCutter_app/img/mm_inches_toggle.png"  
#                                         Label:
#                                             id: unit_label
#                                             text: "mm"
#                                             color: 1,1,1,1
#                                             font_size: 20
#                                             markup: True
#                                             halign: "center"
#                                             valign: "middle"
#                                             text_size: self.size
#                                             size: self.parent.size
#                                             pos: self.parent.pos                       
                                    Switch:
                                        id: unit_toggle
                                        size_hint: (None,None)
                                        height: dp(32)
                                        width: dp(83)
                                        background_color: hex('#F4433600')
                                        center: self.parent.center
                                        pos: self.parent.pos
                                        on_active: root.toggle_units()
                                        active_norm_pos: max(0., min(1., (int(self.active) + self.touch_distance / sp(41))))
                                        canvas.after:
                                            Color:
                                                rgb: 1,1,1
                                            Rectangle:
                                                source: './asmcnc/apps/shapeCutter_app/img/slider_bg_mm.png' if unit_toggle.active else './asmcnc/apps/shapeCutter_app/img/slider_bg_inch.png' 
                                                # make or download your background jpg
                                                size: sp(83), sp(32)
                                                pos: int(self.center_x - sp(41)), int(self.center_y - sp(16))                        
                                         
                                            Rectangle:
                                                #id: switch_rectangle
                                                source: './asmcnc/apps/shapeCutter_app/img/slider_fg_inch.png' if unit_toggle.active else './asmcnc/apps/shapeCutter_app/img/slider_fg_mm.png'
                                                # make or download your slider jpg
                                                size: sp(43), sp(32)
                                                pos: int(self.center_x - sp(41) + self.active_norm_pos * sp(41)), int(self.center_y - sp(16))
                            
                                BoxLayout: #dimension 1
                                    size_hint: (None,None)
                                    height: dp(35)
                                    width: dp(595)
                                    padding: (0,0,20,0)                   
                                    orientation: "horizontal"
                                    
                                    Label: 
                                        text: "Stock bottom offset"
                                        color: 0,0,0,1
                                        font_size: 20
                                        markup: True
                                        halign: "left"
                                        valign: "middle"
                                        text_size: self.size
                                        size: self.parent.size
                                        pos: self.parent.pos
                                                                  
                                    BoxLayout: 
                                        size_hint: (None,None)
                                        height: dp(35)
                                        width: dp(113)
                                        padding: (10,0,0,0)
                                                    
                                        TextInput: 
                                            id: stock_bottom_offset
                                            valign: 'top'
                                            halign: 'center'
                                            text_size: self.size
                                            font_size: '20sp'
                                            markup: True
                                            input_filter: 'float'
                                            multiline: False
                                            text: ''
                                    BoxLayout: 
                                        size_hint: (None,None)
                                        height: dp(35)
                                        width: dp(150)
                                        padding: (10,0,10,0)
                                        Label: 
                                            id: stock_bottom_offset_units
                                            text: "units"
                                            color: 0,0,0,1
                                            font_size: 20
                                            markup: True
                                            halign: "left"
                                            valign: "middle"
                                            text_size: self.size
                                            size: self.parent.size
                                            pos: self.parent.pos                      
                                
                                BoxLayout: #dimension 2
                                    size_hint: (None,None)
                                    height: dp(35)
                                    width: dp(595)
                                    padding: (0,0,20,0)                   
                                    orientation: "horizontal"
                                    
                                    Label: 
                                        text: "Step down"
                                        color: 0,0,0,1
                                        font_size: 20
                                        markup: True
                                        halign: "left"
                                        valign: "middle"
                                        text_size: self.size
                                        size: self.parent.size
                                        pos: self.parent.pos
                                                                  
                                    BoxLayout: 
                                        size_hint: (None,None)
                                        height: dp(35)
                                        width: dp(113)
                                        padding: (10,0,0,0)
                                                    
                                        TextInput: 
                                            id: step_down
                                            valign: 'top'
                                            halign: 'center'
                                            text_size: self.size
                                            font_size: '20sp'
                                            markup: True
                                            input_filter: 'float'
                                            multiline: False
                                            text: ''                           
                                    BoxLayout: 
                                        size_hint: (None,None)
                                        height: dp(35)
                                        width: dp(150)
                                        padding: (10,0,10,0)
                                        Label: 
                                            id: step_down_units
                                            color: 0,0,0,1
                                            font_size: 20
                                            markup: True
                                            halign: "left"
                                            valign: "middle"
                                            text_size: self.size
                                            size: self.parent.size
                                            pos: self.parent.pos
                                BoxLayout: #dimension 3
                                    size_hint: (None,None)
                                    height: dp(35)
                                    width: dp(595)
                                    padding: (0,0,20,0)                   
                                    orientation: "horizontal"
                                    
                                    Label: 
                                        text: "Finishing passes"
                                        color: 0,0,0,1
                                        font_size: 20
                                        markup: True
                                        halign: "left"
                                        valign: "middle"
                                        text_size: self.size
                                        size: self.parent.size
                                        pos: self.parent.pos
                                                                  
                                    BoxLayout: 
                                        size_hint: (None,None)
                                        height: dp(35)
                                        width: dp(113)
                                        padding: (10,0,0,0)
                                                    
                                        TextInput: 
                                            id: finishing_passes
                                            valign: 'top'
                                            halign: 'center'
                                            text_size: self.size
                                            font_size: '20sp'
                                            markup: True
                                            input_filter: 'int'
                                            multiline: False
                                            text: ''                                                                
                                    BoxLayout: 
                                        size_hint: (None,None)
                                        height: dp(35)
                                        width: dp(150)
                                        padding: (10,0,10,0)
                                        Label: 
                                            text: "passes"
                                            color: 0,0,0,1
                                            font_size: 20
                                            markup: True
                                            halign: "left"
                                            valign: "middle"
                                            text_size: self.size
                                            size: self.parent.size
                                            pos: self.parent.pos

                                BoxLayout: # reminder
                                    size_hint: (None,None)
                                    height: dp(60)
                                    width: dp(595)
                                    padding: (0,10,60,0)                   
                                    orientation: "horizontal"
                                    
                                    Label: 
                                        text: ""
                                        color: 0,0,0,1
                                        font_size: 20
                                        markup: True
                                        halign: "left"
                                        valign: "top"
                                        text_size: self.size
                                        size: self.parent.size
                                        pos: self.parent.pos

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

class ShapeCutter24ScreenClass(Screen):

    
    info_button = ObjectProperty()
    
    screen_number = StringProperty("[b]24[/b]")
    title_label = StringProperty("[b]Enter strategy parameters[/b]")
    user_instructions = StringProperty("")
    
    def __init__(self, **kwargs):
        super(ShapeCutter24ScreenClass, self).__init__(**kwargs)
        self.shapecutter_sm = kwargs['shapecutter']
        self.m=kwargs['machine']
        self.j=kwargs['job_parameters']

    def on_pre_enter(self):
        self.info_button.opacity = 1
    
        self.stock_bottom_offset.text = "{:.2f}".format(float(self.j.parameter_dict["strategy parameters"]["stock bottom offset"]))
        self.step_down.text = "{:.2f}".format(float(self.j.parameter_dict["strategy parameters"]["step down"]))
        self.finishing_passes.text = "{:.2f}".format(float(self.j.parameter_dict["strategy parameters"]["finishing passes"]))

        if self.j.parameter_dict["strategy parameters"]["units"] == "inches":
            self.unit_toggle.active = True
            self.stock_bottom_offset_units.text = "inches"
            self.step_down_units.text = "inches"

        elif self.j.parameter_dict["strategy parameters"]["units"] == "mm":
            self.unit_toggle.active = False
            self.stock_bottom_offset_units.text = "mm"
            self.step_down_units.text = "mm"

# Action buttons       

    def get_info(self):
        info = "[b]Stock Bottom Offset:[/b] Determines the final machine depth offset from the bottom of your stock.\n\n" \
        "[b]Step Down:[/b] Specifies the maximum step down between Z-levels.\n\n" \
        "[b]Finishing Passes:[/b] Specifies the number of finishing passes."
        popup_info.PopupInfo(self.shapecutter_sm, info)
            
    def go_back(self):
        self.shapecutter_sm.previous_screen()
    
    def next_screen(self):
        self.check_dimensions()
    
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
        
# Screen specific

    def toggle_units(self):

        if self.unit_toggle.active == True:
            self.j.parameter_dict["strategy parameters"]["units"] = "inches"
            self.stock_bottom_offset_units.text = "inches"
            self.step_down_units.text = "inches"
            
            if not (self.stock_bottom_offset.text == ""): self.stock_bottom_offset.text = "{:.2f}".format(float(self.stock_bottom_offset.text) / 25.4)
            if not (self.step_down.text == ""): self.step_down.text = "{:.2f}".format(float(self.step_down.text) / 25.4)

        elif self.unit_toggle.active == False:
            self.j.parameter_dict["strategy parameters"]["units"] = "mm"
            self.stock_bottom_offset_units.text = "mm"
            self.step_down_units.text = "mm"
            
            if not (self.stock_bottom_offset.text == ""): self.stock_bottom_offset.text = "{:.2f}".format(float(self.stock_bottom_offset.text) * 25.4)
            if not (self.step_down.text == ""): self.step_down.text = "{:.2f}".format(float(self.step_down.text) * 25.4)

    def check_dimensions(self):
        if not self.stock_bottom_offset.text == "" and not self.step_down.text == "" \
        and not self.finishing_passes.text == "":
            self.j.parameter_dict["strategy parameters"]["stock bottom offset"] = float(self.stock_bottom_offset.text)
            self.j.parameter_dict["strategy parameters"]["step down"] = float(self.step_down.text)
            self.j.parameter_dict["strategy parameters"]["finishing passes"] = float(self.finishing_passes.text)
            
            if self.unit_toggle.active == True:
                self.j.parameter_dict["strategy parameters"]["units"] = "inches"
    
            elif self.unit_toggle.active == False:
                self.j.parameter_dict["strategy parameters"]["units"] = "mm"       

            #self.j.parameter_dict["strategy parameters"]["units"] = self.unit_label.text
            self.shapecutter_sm.next_screen()
        else:
            pass