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
    
    auto_dismiss: True
    size_hint: (None,None)
    size: (577, 301)
    title: ''
    separator_height: 0
    background: './asmcnc/apps/drywall_cutter_app/img/cutting_depths_popup.png'
    
    on_touch_down: root.on_touch()

    # BoxLayout:
    #     id: boxlayout
    #     orientation: 'vertical'
    #     size_hint: (None, None)
    #     size: (577, 301)
    #     pos_hint: {'y': -0.05}
    #     x: -10
    #     # pos: (-10,-100)
    #     padding: 0
    #     margin: 0
    #     
    #     canvas:
    #         Color:
    #             rgba: hex('#FF0000')
    #         Rectangle:
    #             size: self.size
    #             pos: self.pos
        
        
    
    FloatLayout:
        size_hint: (None, None)
        size: (577, 301)
        pos_hint: {'y': -0.05}
        # canvas:
        #     Color:
        #         rgba: hex('#0000FF')
        #     Rectangle:
        #         size: self.size
        #         pos: self.pos
                
        Label:
            #size_hint: (1, 0.12)
            pos_hint: {'x': -0.39, 'y': 0.45}
            text: 'Cutting depths'
            font_size: '20sp'
            # canvas:
            #     Color:
            #         rgba: hex('#00FF00')
            #     Rectangle:
            #         size: self.size
            #         pos: self.pos
            
        Image:
            id: material_graphic
            source: "./asmcnc/apps/drywall_cutter_app/img/material_graphic.png"
            pos_hint: {'center_x': 0.45}
            y: self.parent.y
            size: self.parent.size
            allow_stretch: True 
            
        Image:
            id: pass_depths_graphic
            source: "./asmcnc/apps/drywall_cutter_app/img/pass_depths.png"
            pos_hint: {'center_x': 0.45}
            y: self.parent.y
            size: self.parent.size
            allow_stretch: True 
            
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
                text: 'Auto pass'
                font_size: '16sp'
                color: 0,0,0,1
                text_size: (75, None)
            CheckBox:
                id: auto_pass_checkbox
                size_hint: (0.3,1)
                active: True
                background_checkbox_normal: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                on_active: root.on_checkbox_active()
            
            Label:
                text: 'Depth per pass'
                font_size: '16sp'
                color: 0,0,0,1
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
        
""")


class CuttingDepthsPopup(Popup):
    def __init__(self, localization, keyboard, **kwargs):
        super(CuttingDepthsPopup, self).__init__(**kwargs)
        self.l = localization
        self.kb = keyboard

        self.text_inputs = [self.material_thickness, self.bottom_offset, self.total_cut_depth, self.depth_per_pass]
        self.kb.setup_text_inputs(self.text_inputs)
        self.open()

    def on_touch(self):
        for text_input in self.text_inputs:
            text_input.focus = False

    def on_checkbox_active(self):
        if self.auto_pass_checkbox.active:
            self.depth_per_pass.disabled = True
        else:
            self.depth_per_pass.disabled = False