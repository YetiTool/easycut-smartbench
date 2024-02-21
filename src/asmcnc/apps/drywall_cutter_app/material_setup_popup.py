from kivy.uix.popup import Popup
from kivy.lang import Builder
import math
from kivy.uix.image import Image
from kivy.clock import Clock
from asmcnc.core_UI.components import FloatInput

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
    size: (dp(app.get_scaled_width(577)), dp(app.get_scaled_height(301)))
    title: ''
    separator_height: 0
    background: './asmcnc/apps/drywall_cutter_app/img/cutting_depths_popup.png'

    FloatLayout:
        id: float_layout
        size_hint: (None, None)
        size: (dp(app.get_scaled_width(577)), dp(app.get_scaled_height(301)))
        pos_hint: {'y': -0.05}
                
        Label:
            id: title_label
            pos_hint: {'x': -0.39, 'y': 0.45}
            text: 'Cutting depths'
            font_size: app.get_scaled_sp('20sp')
            color: hex('#F9F9F9')
        
        Label:
            id: Z0
            pos_hint: {'x': 0.0375, 'y': 0.21}
            text: 'Z0'
            font_size: app.get_scaled_sp('20sp')
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
            font_size: app.get_scaled_sp('16sp')
            color: hex('#333333')
            text_size: (dp(app.get_scaled_width(75)), None)
            
        Image:
            id: material_thickness_dims
            source: "./asmcnc/apps/drywall_cutter_app/img/material_thickness_dims.png"
            pos_hint: {'center_x': 0.45}
            y: self.parent.y
            size: self.parent.size
            allow_stretch: True
            
        FloatInput:
            id: material_thickness
            pos_hint: {'x': 0.165, 'y': 0.68}
            padding_y: [self.height / 2.0 - (self.line_height / 2.0) * len(self._lines), 0]
            halign: 'center'
            size_hint: (.12, .1)
            text_size: self.size
            font_size: app.get_scaled_sp('16sp')
            markup: True
            multiline: False
            text: ''
            input_filter: 'float'
        
        Label:
            id: bottom_offset_label
            pos_hint: {'x': -0.42, 'y': -0.075}
            text: ''
            font_size: app.get_scaled_sp('16sp')
            color: hex('#333333')
            text_size: (dp(app.get_scaled_width(75)), None)
            
        Image:
            id: bottom_offset_graphic
            source: "./asmcnc/apps/drywall_cutter_app/img/bottom_offset_graphic.png"
            pos_hint: {'center_x': 0.45}
            y: self.parent.y
            size: self.parent.size
            allow_stretch: True
        
        FloatInput:
            id: bottom_offset
            pos_hint: {'x': 0.165, 'y': 0.37}
            padding_y: [self.height / 2.0 - (self.line_height / 2.0) * len(self._lines), 0]
            halign: 'center'
            size_hint: (.12, .1)
            text_size: self.size
            font_size: app.get_scaled_sp('16sp')
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
            font_size: app.get_scaled_sp('16sp')
            color: hex('#333333')
            text_size: (dp(app.get_scaled_width(75)), None)
            
        FloatInput:
            id: total_cut_depth
            pos_hint: {'x': 0.165, 'y': 0.165}
            padding_y: [self.height / 2.0 - (self.line_height / 2.0) * len(self._lines), 0]
            halign: 'center'
            size_hint: (.12, .1)
            text_size: self.size
            font_size: app.get_scaled_sp('16sp')
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
            font_size: app.get_scaled_sp('14sp')
            markup: True
            color: hex('#FF0000')
            text_size: (dp(app.get_scaled_width(175)), None)
        
        Label:
            id: pass_depth_warning
            pos_hint: {'x': 0.2525, 'y': -0.1}
            text: ''
            font_size: app.get_scaled_sp('14sp')
            markup: True
            color: hex('#FF0000')
            text_size: (dp(app.get_scaled_width(150)), None) 
        
        GridLayout:
            rows: 2
            cols: 2
            pos_hint: {'x': 0.6, 'y': -0.2}
            row_force_default: True
            col_force_default: True
            row_default_height: dp(app.get_scaled_height(50))
            col_default_width: dp(app.get_scaled_width(100))
            
            
            Label:
                id: auto_pass_label
                text: ''
                font_size: app.get_scaled_sp('16sp')
                color: hex('#333333')
                text_size: (dp(app.get_scaled_width(75)), None)
            CheckBox:
                id: auto_pass_checkbox
                size_hint: (0.3,1)
                active: True
                background_checkbox_normal: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                on_active: root.on_checkbox_active()
            
            Label:
                id: depth_per_pass_label
                text: ''
                font_size: app.get_scaled_sp('16sp')
                color: hex('#333333')
                text_size: (dp(app.get_scaled_width(75)), None)
                
            FloatInput:
                id: depth_per_pass
                padding_y: [self.height / 2.0 - (self.line_height / 2.0) * len(self._lines), 0]
                halign: 'center'
                size_hint: (0, 0)
                text_size: self.size
                font_size: app.get_scaled_sp('16sp')
                markup: True
                multiline: False
                text: ''
                disabled: True
                input_filter: 'float' 
                
        BoxLayout:
            orientation: 'horizontal'
            pos_hint: {'x': 0.625, 'y': 0.075}
            size_hint: (None, None)
            size: (dp(app.get_scaled_width(189)),dp(app.get_scaled_height(23)))
            spacing: dp(app.get_scaled_width(20))

            Button:
                id: cancel_button
                on_press: root.cancel()
                size_hint: (None,None)
                width: dp(app.get_scaled_width(83))
                height: dp(app.get_scaled_height(23))
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
                width: dp(app.get_scaled_width(86))
                height: dp(app.get_scaled_height(23))
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
    soft_limit_total_cut_depth = 62

    def __init__(self, localization, keyboard, dwt_config, **kwargs):
        super(CuttingDepthsPopup, self).__init__(**kwargs)
        self.l = localization
        self.kb = keyboard
        self.dwt_config = dwt_config

        self.bind(on_touch_down=self.on_touch)
        self.previous_text_input_focused = None

        self.pass_depth_lines = []

        self.float_layout.remove_widget(self.cut_depth_warning)
        self.float_layout.remove_widget(self.pass_depth_warning)

        # This resolves the 'weakly-referenced' objects exception by preventing garbage collection
        self.refs = [self.cut_depth_warning.__self__, self.pass_depth_warning.__self__]

        self.text_inputs = [self.material_thickness, self.bottom_offset, self.total_cut_depth, self.depth_per_pass]
        self.kb.setup_text_inputs(self.text_inputs)
        for text_input in self.text_inputs:
            text_input.bind(focus=self.text_on_focus)
            text_input.bind(text=self.update_text)
        self.depth_per_pass.bind(text=self.calculate_depth_per_pass)

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

    def get_safe_float(self, val):
        try:
            return float(val)
        except:
            return 0.0

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

    def on_touch(self, instance, touch):
        for text_input in self.text_inputs:
            if not text_input.collide_point(touch.x, touch.y):
                text_input.focus = False
                self.previous_text_input_focused = None
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

    def update_graphic_position(self):
        upper_limit = 0.225  # Value at which the cutter sits at the top of the material
        lower_limit = -0.035  # Value at which the cutter sits at the bottom surface of the material
        range = upper_limit - lower_limit
        bottom_offset = self.get_safe_float(self.bottom_offset.text)
        material_thickness = self.get_safe_float(self.material_thickness.text)
        ratio = 0 if material_thickness == 0 else bottom_offset / material_thickness
        cutter_y = lower_limit - (range * ratio)
        self.cutter_graphic.pos_hint['y'] = cutter_y
        self.total_cut_depth_arrow.pos_hint['y'] = cutter_y
        self.float_layout.do_layout()
        self.cutter_layout.do_layout()

    def update_text(self, instance, value):
        cutter_max_depth_total = self.dwt_config.active_cutter.max_depth_total
        # Calculate total cut depth and handle inputs
        if instance == self.material_thickness or instance == self.bottom_offset:
            # Update warning label text
            if self.soft_limit_total_cut_depth < cutter_max_depth_total:
                max_cut_depth = self.soft_limit_total_cut_depth
                self.cut_depth_warning.text = self.cut_depth_warning_soft_limit
            else:
                max_cut_depth = cutter_max_depth_total
                self.cut_depth_warning.text = self.cut_depth_warning_cutter_max

            material_thickness = self.get_safe_float(self.material_thickness.text)
            bottom_offset = self.get_safe_float(self.bottom_offset.text)

            # Make sure material thickness is never negative
            if material_thickness < 0:
                self.material_thickness.text = '0'
                material_thickness = 0

            # Make sure bottom offset is never bigger than material thickness
            if abs(bottom_offset) > material_thickness:
                if bottom_offset < 0:
                    if self.material_thickness.text == '':
                        self.bottom_offset.text = ''
                        bottom_offset = material_thickness
                    else:
                        self.bottom_offset.text = '-' + self.material_thickness.text
                        bottom_offset = -material_thickness

            self.total_cut_depth.text = str(material_thickness + bottom_offset)
            self.update_graphic_position()
            self.calculate_depth_per_pass(self.depth_per_pass, self.auto_pass_checkbox.active)

            try:
                if float(self.total_cut_depth.text) > max_cut_depth:
                    self.float_layout.add_widget(self.cut_depth_warning)
                elif float(self.total_cut_depth.text) <= 0:
                    self.cut_depth_warning.text = self.cut_depth_warning_zero
                    self.float_layout.add_widget(self.cut_depth_warning)
                else:
                    self.float_layout.remove_widget(self.cut_depth_warning)
            except:
                pass

            self.disable_confirm_button()


    def disable_confirm_button(self):
        children = self.float_layout.children
        if self.cut_depth_warning in children or self.pass_depth_warning in children:
            self.confirm_button.disabled = True
            self.confirm_button.opacity = 0.5
        else:
            self.confirm_button.disabled = False
            self.confirm_button.opacity = 1
        self.float_layout.do_layout()

    def generate_pass_depth_lines(self, number_of_passes):
        upper_limit = 0.0825  # Value at which the line sits at the top of the material
        lower_limit = -0.175  # Value at which the line sits at the bottom surface of the material
        line_range = upper_limit - lower_limit
        material_thickness = self.get_safe_float(self.material_thickness.text)
        depth_per_pass = self.get_safe_float(self.depth_per_pass.text)
        ratio = 0 if material_thickness == 0 else depth_per_pass / material_thickness
        singular_cut = 0 if self.depth_per_pass.text == "" else round(ratio * line_range, 4)
        for pass_line in self.pass_depth_lines:
            self.cutter_layout.remove_widget(pass_line)
        if self.total_cut_depth.text != "0.0":
            for i in range(0, int(number_of_passes)):
                line_depth = upper_limit - (singular_cut * (i + 1))
                cutter_limit = lower_limit - (-0.035 - self.cutter_graphic.pos_hint['y'])
                if line_depth < cutter_limit:
                    line_depth = cutter_limit

                img = Image(source="./asmcnc/apps/drywall_cutter_app/img/pass_depth_line.png",
                            allow_stretch=True,
                            pos_hint={'center_x': 0.45, 'y': line_depth})

                self.cutter_layout.add_widget(img)
                self.pass_depth_lines.append(img)
        self.cutter_layout.do_layout()

    def calculate_depth_per_pass(self, *args):
        max_cut_depth_per_pass = self.dwt_config.active_cutter.max_depth_per_pass
        if self.auto_pass_checkbox.active:

            depth_per_pass = max_cut_depth_per_pass
            number_of_passes = 0 if depth_per_pass == 0 else math.ceil(self.get_safe_float(self.total_cut_depth.text) / depth_per_pass)

            if depth_per_pass > max_cut_depth_per_pass:
                self.depth_per_pass.text = str(max_cut_depth_per_pass)
            else:
                self.depth_per_pass.text = str(round(depth_per_pass, 1))
            try:
                if depth_per_pass <= 0:
                    self.pass_depth_warning.text = self.pass_depth_warning_zero
                    self.float_layout.add_widget(self.pass_depth_warning)
                else:
                    self.float_layout.remove_widget(self.pass_depth_warning)
            except:
                pass
            self.disable_confirm_button()
            self.generate_pass_depth_lines(number_of_passes)
        else:
            depth_per_pass = self.get_safe_float(self.depth_per_pass.text)
            try:
                if depth_per_pass > max_cut_depth_per_pass:
                    self.pass_depth_warning.text = self.pass_depth_warning_cutter_max
                    self.float_layout.add_widget(self.pass_depth_warning)
                elif depth_per_pass <= 0:
                    self.pass_depth_warning.text = self.pass_depth_warning_zero
                    self.float_layout.add_widget(self.pass_depth_warning)
                else:
                    self.float_layout.remove_widget(self.pass_depth_warning)
            except:
                pass
            self.disable_confirm_button()
            number_of_passes = 0 if depth_per_pass == 0 else math.ceil(self.get_safe_float(self.total_cut_depth.text) / depth_per_pass)
            self.generate_pass_depth_lines(number_of_passes)


    def confirm(self):
        material_thickness = self.get_safe_float(self.material_thickness.text)
        bottom_offset = self.get_safe_float(self.bottom_offset.text)
        depth_per_pass = self.get_safe_float(self.depth_per_pass.text)

        self.dwt_config.active_config.cutting_depths.material_thickness = material_thickness
        self.dwt_config.active_config.cutting_depths.bottom_offset = bottom_offset
        self.dwt_config.active_config.cutting_depths.depth_per_pass = depth_per_pass
        self.dwt_config.active_config.cutting_depths.auto_pass = self.auto_pass_checkbox.active
        self.dismiss()

    def cancel(self):
        self.dismiss()

    def validate_inputs(self):
        material_thickness = self.get_safe_float(self.material_thickness.text)
        bottom_offset = self.get_safe_float(self.bottom_offset.text)
        total_cut_depth = self.get_safe_float(self.total_cut_depth.text)
        depth_per_pass = self.get_safe_float(self.depth_per_pass.text)
        auto_pass_checkbox = self.auto_pass_checkbox.active
        max_cut_depth_per_pass = self.dwt_config.active_cutter.max_depth_per_pass

        # Check for negative material thickness
        if material_thickness < 0:
            return False

        # The bottom offset should never have a greater value than the material thickness if negative
        if abs(bottom_offset) > material_thickness:
            if bottom_offset < 0:
                return False

        if total_cut_depth < 0 or total_cut_depth > self.soft_limit_total_cut_depth:
            return False

        if total_cut_depth != material_thickness + bottom_offset:
            return False

        if depth_per_pass > max_cut_depth_per_pass or depth_per_pass <= 0:
            return False

        return True
