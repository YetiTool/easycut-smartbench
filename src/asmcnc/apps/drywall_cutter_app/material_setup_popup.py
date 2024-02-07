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

        Image:
            id: total_cut_depth_arrow
            source: "./asmcnc/apps/drywall_cutter_app/img/total_cut_depth_bottom_arrow.png"
            pos_hint: {'center_x': 0.45, 'y': 0.225}
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
            
        StencilView:  # Prevents the images from going off the popup
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

    def confirm(self):
        self.dismiss()

    def cancel(self):
        self.dismiss()

    def on_touch(self):
        pass