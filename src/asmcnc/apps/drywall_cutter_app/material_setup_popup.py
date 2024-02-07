from kivy.uix.popup import Popup
from kivy.lang import Builder
import math
from kivy.uix.image import Image

Builder.load_string("""
<CuttingDepthsPopup>:
    float_layout:float_layout
    cutter_layout:cutter_layout
    
    material_graphic:material_graphic
    material_thickness:material_thickness
    bottom_offset:bottom_offset
    total_cut_depth:total_cut_depth
    depth_per_pass:depth_per_pass
    auto_pass_checkbox:auto_pass_checkbox
    
    title_label:title_label
    material_thickness_label:material_thickness_label
    bottom_offset_label:bottom_offset_label
    total_cut_depth_label:total_cut_depth_label
    auto_pass_label:auto_pass_label
    depth_per_pass_label:depth_per_pass_label
    cut_depth_warning:cut_depth_warning
    pass_depth_warning:pass_depth_warning
    
    cutter_graphic:cutter_graphic
    total_cut_depth_arrow:total_cut_depth_arrow
    
    confirm_button:confirm_button
    
    auto_dismiss: False
    size_hint: (None,None)
    size: (577, 301)
    title: ''
    separator_height: 0
    background: './asmcnc/apps/drywall_cutter_app/img/cutting_depths_popup.png'
    
    on_touch_down: root.on_touch()

    FloatLayout:
        id: float_layout
        size_hint: (None, None)
        size: (577, 301)
        pos_hint: {'y': -0.05}
                
        Label:
            id: title_label
            pos_hint: {'x': -0.39, 'y': 0.45}
            text: 'Cutting depths'
            font_size: '20sp'
            color: hex('#F9F9F9')
        
        Label:
            id: Z0
            pos_hint: {'x': 0.0375, 'y': 0.21}
            text: 'Z0'
            font_size: '20sp'
            color: hex('#333333')
            
        Image:
            id: material_graphic
            source: "./asmcnc/apps/drywall_cutter_app/img/material_graphic.png"
            pos_hint: {'center_x': 0.45}
            y: self.parent.y
            size: self.parent.size
            allow_stretch: True 
        
        Label:
            id: material_thickness_label
            pos_hint: {'x': -0.42, 'y': 0.23}
            text: ''
            font_size: '16sp'
            color: hex('#333333')
            text_size: (75, None)
            
        Image:
            id: material_thickness_dims
            source: "./asmcnc/apps/drywall_cutter_app/img/material_thickness_dims.png"
            pos_hint: {'center_x': 0.45}
            y: self.parent.y
            size: self.parent.size
            allow_stretch: True
            
        TextInput:
            id: material_thickness
            pos_hint: {'x': 0.165, 'y': 0.68}
            padding_y: [self.height / 2.0 - (self.line_height / 2.0) * len(self._lines), 0]
            halign: 'center'
            size_hint: (.12, .1)
            text_size: self.size
            font_size: '16sp'
            markup: True
            multiline: False
            text: ''
            input_filter: 'float'
        
        Label:
            id: bottom_offset_label
            pos_hint: {'x': -0.42, 'y': -0.075}
            text: ''
            font_size: '16sp'
            color: hex('#333333')
            text_size: (75, None)
            
        Image:
            id: bottom_offset_graphic
            source: "./asmcnc/apps/drywall_cutter_app/img/bottom_offset_graphic.png"
            pos_hint: {'center_x': 0.45}
            y: self.parent.y
            size: self.parent.size
            allow_stretch: True
        
        TextInput:
            id: bottom_offset
            pos_hint: {'x': 0.165, 'y': 0.37}
            padding_y: [self.height / 2.0 - (self.line_height / 2.0) * len(self._lines), 0]
            halign: 'center'
            size_hint: (.12, .1)
            text_size: self.size
            font_size: '16sp'
            markup: True
            multiline: False
            text: ''
            input_filter: 'float' 
        
        Image:
            id: total_cut_depth_dims
            source: "./asmcnc/apps/drywall_cutter_app/img/total_cut_depth_dims.png"
            pos_hint: {'center_x': 0.45}
            y: self.parent.y
            size: self.parent.size
            allow_stretch: True
        
        Label:
            id: total_cut_depth_label
            pos_hint: {'x': -0.42, 'y': -0.275}
            text: ''
            font_size: '16sp'
            color: hex('#333333')
            text_size: (75, None)
            
        TextInput:
            id: total_cut_depth
            pos_hint: {'x': 0.165, 'y': 0.165}
            padding_y: [self.height / 2.0 - (self.line_height / 2.0) * len(self._lines), 0]
            halign: 'center'
            size_hint: (.12, .1)
            text_size: self.size
            font_size: '16sp'
            markup: True
            multiline: False
            text: ''
            disabled: True
            
        StencilView:
            size: self.parent.size
            pos: self.parent.pos
            
            FloatLayout:
                id: cutter_layout
                size: self.parent.size
                pos: self.parent.pos
                
                Image:
                    id: total_cut_depth_arrow
                    source: "./asmcnc/apps/drywall_cutter_app/img/total_cut_depth_bottom_arrow.png"
                    pos_hint: {'center_x': 0.45, 'y': 0.225}
                    y: self.parent.y
                    size: self.parent.size
                    allow_stretch: True
                
                Image:
                    id: cutter_graphic
                    source: "./asmcnc/apps/drywall_cutter_app/img/cutter_graphic.png"
                    pos_hint: {'center_x': 0.45, 'y': 0.225}
                    # y: self.parent.y
                    size: self.parent.size
                    allow_stretch: True 
        
        Label:
            id: cut_depth_warning
            pos_hint: {'x': -0.335, 'y': -0.4}
            text: ''
            font_size: '14sp'
            markup: True
            color: hex('#FF0000')
            text_size: (175, None)
        
        Label:
            id: pass_depth_warning
            pos_hint: {'x': 0.2525, 'y': -0.1}
            text: ''
            font_size: '14sp'
            markup: True
            color: hex('#FF0000')
            text_size: (150, None) 
        
        GridLayout:
            rows: 2
            cols: 2
            pos_hint: {'x': 0.6, 'y': -0.2}
            row_force_default: True
            col_force_default: True
            row_default_height: 50
            col_default_width: 100
            
            
            Label:
                id: auto_pass_label
                text: ''
                font_size: '16sp'
                color: hex('#333333')
                text_size: (75, None)
            CheckBox:
                id: auto_pass_checkbox
                size_hint: (0.3,1)
                active: True
                background_checkbox_normal: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                on_active: root.on_checkbox_active()
            
            Label:
                id: depth_per_pass_label
                text: ''
                font_size: '16sp'
                color: hex('#333333')
                text_size: (75, None)
                
            TextInput:
                id: depth_per_pass
                padding_y: [self.height / 2.0 - (self.line_height / 2.0) * len(self._lines), 0]
                halign: 'center'
                size_hint: (0, 0)
                text_size: self.size
                font_size: '16sp'
                markup: True
                multiline: False
                text: ''
                disabled: True
                input_filter: 'float' 
                
        BoxLayout:
            orientation: 'horizontal'
            pos_hint: {'x': 0.625, 'y': 0.075}
            size_hint: (None, None)
            size: (189,23)
            spacing: 0.025*app.width

            Button:
                id: cancel_button
                on_press: root.cancel()
                size_hint: (None,None)
                width: dp(83)
                height: dp(23)
                background_color: [0,0,0,0]
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/apps/drywall_cutter_app/img/cancel_button.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

            Button:
                id: confirm_button
                on_press: root.confirm()
                size_hint: (None,None)
                width: dp(86)
                height: dp(23)
                background_color: [0,0,0,0]
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/apps/drywall_cutter_app/img/confirm_button.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
        
""")


class CuttingDepthsPopup(Popup):

    def __init__(self, localization, keyboard, dwt_config, **kwargs):
        super(CuttingDepthsPopup, self).__init__(**kwargs)
        self.l = localization
        self.kb = keyboard
        self.dwt_config = dwt_config

        self.pass_depth_lines = []

        self.float_layout.remove_widget(self.cut_depth_warning)
        self.float_layout.remove_widget(self.pass_depth_warning)

        # This resolves the 'weakly-referenced' objects exception by preventing garbage collection
        self.refs = [self.cut_depth_warning.__self__, self.pass_depth_warning.__self__]

        self.text_inputs = [self.material_thickness, self.bottom_offset, self.total_cut_depth, self.depth_per_pass]
        self.kb.setup_text_inputs(self.text_inputs)

        # Defining the error messages in one place since they need to be changed throughout the popup
        self.pass_depth_warning_cutter_max = "[color=#FF0000]" + self.l.get_str("Max depth per pass for this tool is") \
                                             + " Xmm[/color]".replace("X",
                                                                      str(self.dwt_config.active_cutter.max_depth_per_pass))
        self.pass_depth_warning_zero = "[color=#FF0000]" + self.l.get_str("Depth per pass must be greater than 0") \
                                           + "[/color]"

        self.cut_depth_warning_soft_limit = "[color=#FF0000]" + self.l.get_str("Max allowable cut is") + \
                                            " Xmm[/color]".replace("X", str(self.soft_limit_total_cut_depth))
        self.cut_depth_warning_cutter_max = "[color=#FF0000]" + self.l.get_str("Max depth of tool is") + \
                                            " Xmm[/color]".replace("X",
                                                                   str(self.dwt_config.active_cutter.max_depth_total))
        self.cut_depth_warning_zero = "[color=#FF0000]" + self.l.get_str("Total cut depth must be greater than 0") \
                                          + "[/color]"

        self.update_strings()

    def on_open(self):
        self.load_active_config()

    def load_active_config(self):
        self.material_thickness.text = str(self.dwt_config.active_config.cutting_depths.material_thickness)
        self.bottom_offset.text = str(self.dwt_config.active_config.cutting_depths.bottom_offset)
        self.auto_pass_checkbox.active = self.dwt_config.active_config.cutting_depths.auto_pass
        self.depth_per_pass.text = str(self.dwt_config.active_config.cutting_depths.depth_per_pass)

    def update_strings(self):
        self.title_label.text = self.l.get_str("Cutting depths")
        self.material_thickness_label.text = self.l.get_str("Material thickness")
        self.bottom_offset_label.text = self.l.get_str("Bottom offset")
        self.total_cut_depth_label.text = self.l.get_str("Total cut depth")
        self.auto_pass_label.text = self.l.get_str("Auto pass")
        self.depth_per_pass_label.text = self.l.get_str("Depth per pass")
        self.pass_depth_warning.text = self.pass_depth_warning_cutter_max
        self.cut_depth_warning.text = self.cut_depth_warning_soft_limit

    def on_touch(self):
        for text_input in self.text_inputs:
            text_input.focus = False
            if text_input.text != '':
                try:
                    text_input.text = str(float(text_input.text))
                except:
                    pass
            else:
                text_input.text = str(float(0))

    def on_checkbox_active(self):
        if self.auto_pass_checkbox.active:
            self.depth_per_pass.disabled = True
            self.depth_per_pass.text = self.depth_per_pass.hint_text
            self.depth_per_pass.hint_text = ''
        else:
            self.depth_per_pass.disabled = False
            self.depth_per_pass.hint_text = self.depth_per_pass.text
            self.depth_per_pass.text = ''

    def confirm(self):
        self.dismiss()

    def cancel(self):
        self.dismiss()
