from kivy.uix.popup import Popup
from kivy.lang import Builder

Builder.load_string("""
<CuttingDepthsPopup>:
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
    
    auto_dismiss: False
    size_hint: (None,None)
    size: (577, 301)
    title: ''
    separator_height: 0
    background: './asmcnc/apps/drywall_cutter_app/img/cutting_depths_popup.png'
    
    on_touch_down: root.on_touch()

    FloatLayout:
        size_hint: (None, None)
        size: (577, 301)
        pos_hint: {'y': -0.05}
                
        Label:
            id: title_label
            #size_hint: (1, 0.12)
            pos_hint: {'x': -0.39, 'y': 0.45}
            text: 'Cutting depths'
            font_size: '20sp'
            color: hex('#F9F9F9')
            
        Image:
            id: material_graphic
            source: "./asmcnc/apps/drywall_cutter_app/img/material_graphic.png"
            pos_hint: {'center_x': 0.45}
            y: self.parent.y
            size: self.parent.size
            allow_stretch: True 
            
        # Image:
        #     id: pass_depths_graphic
        #     source: "./asmcnc/apps/drywall_cutter_app/img/pass_depth_line.png"
        #     pos_hint: {'center_x': 0.45}
        #     y: self.parent.y
        #     size: self.parent.size
        #     allow_stretch: True 
        
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
            font_size: '20sp'
            markup: True
            multiline: False
            text: ''
            input_filter: 'int'
        
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
            font_size: '20sp'
            markup: True
            multiline: False
            text: ''
            input_filter: 'int' 
        
        Image:
            id: total_cut_depth_dims
            source: "./asmcnc/apps/drywall_cutter_app/img/total_cut_depth_dims.png"
            pos_hint: {'center_x': 0.45}
            y: self.parent.y
            size: self.parent.size
            allow_stretch: True
        
        Image:
            id: total_cut_depth_dims
            source: "./asmcnc/apps/drywall_cutter_app/img/total_cut_depth_bottom_arrow.png"
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
            font_size: '20sp'
            markup: True
            multiline: False
            text: ''
            disabled: True
            
        Image:
            id: cutter_graphic
            source: "./asmcnc/apps/drywall_cutter_app/img/cutter_graphic.png"
            pos_hint: {'center_x': 0.45}
            y: self.parent.y
            size: self.parent.size
            allow_stretch: True 
        
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
                font_size: '20sp'
                markup: True
                multiline: False
                text: ''
                disabled: True
                input_filter: 'int' 
                
        BoxLayout:
            orientation: 'horizontal'
            pos_hint: {'x': 0.625, 'y': 0.075}
            size_hint: (0.2,0.1)
            spacing: 0.025*app.width

            Button:
                id: cancel_button
                on_press: root.cancel()
                background_normal: "./asmcnc/apps/drywall_cutter_app/img/cancel_button.png"
                background_down: "./asmcnc/apps/drywall_cutter_app/img/cancel_button.png"
                size_hint: (None,None)
                width: dp(83)
                height: dp(23)

            Button:
                id: confirm_button
                on_press: root.confirm()
                background_normal: "./asmcnc/apps/drywall_cutter_app/img/confirm_button.png"
                background_down: "./asmcnc/apps/drywall_cutter_app/img/confirm_button.png"
                size_hint: (None,None)
                width: dp(86)
                height: dp(23)
        
""")


class CuttingDepthsPopup(Popup):
    def __init__(self, localization, keyboard, **kwargs):
        super(CuttingDepthsPopup, self).__init__(**kwargs)
        self.l = localization
        self.kb = keyboard

        self.text_inputs = [self.material_thickness, self.bottom_offset, self.total_cut_depth, self.depth_per_pass]
        self.kb.setup_text_inputs(self.text_inputs)
        for text_input in self.text_inputs:
            text_input.bind(text=self.update_text)
        self.update_strings()
        self.open()

    def update_strings(self):
        self.title_label.text = self.l.get_str("Cutting depths")
        self.material_thickness_label.text = self.l.get_str("Material thickness")
        self.bottom_offset_label.text = self.l.get_str("Bottom offset")
        self.total_cut_depth_label.text = self.l.get_str("Total cut depth")
        self.auto_pass_label.text = self.l.get_str("Auto pass")
        self.depth_per_pass_label.text = self.l.get_str("Depth per pass")

    def on_touch(self):
        for text_input in self.text_inputs:
            text_input.focus = False

    def on_checkbox_active(self):
        if self.auto_pass_checkbox.active:
            self.depth_per_pass.disabled = True
        else:
            self.depth_per_pass.disabled = False

    def update_text(self, instance, value):
        print(value)

    def confirm(self):
        self.dismiss()

    def cancel(self):
        self.dismiss()
