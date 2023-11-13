from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.clock import Clock

Builder.load_string("""
<DrywallShapeDisplay>

    shape_dims_image:shape_dims_image
    shape_toolpath_image:shape_toolpath_image

    d_input:d_input
    l_input:l_input
    r_input:r_input
    x_input:x_input
    y_input:y_input
    x_datum_label:x_datum_label
    x_datum_validation_label:x_datum_validation_label
    y_datum_label:y_datum_label
    y_datum_validation_label:y_datum_validation_label

    bumper_bottom_image:bumper_bottom_image
    bumper_left_image:bumper_left_image
    bumper_right_image:bumper_right_image
    bumper_top_image:bumper_top_image

    BoxLayout:
        size: self.parent.size
        pos: self.parent.pos

        FloatLayout:
            size: self.parent.size
            pos: self.parent.pos

            Image:
                source: "./asmcnc/apps/drywall_cutter_app/img/canvas_with_logo.png"
                size: self.parent.size
                pos: self.parent.pos

            Image:
                id: shape_toolpath_image
                opacity: 0
                size: self.parent.size
                pos: self.parent.pos

            Image:
                id: shape_dims_image
                opacity: 0
                size: self.parent.size
                pos: self.parent.pos

            BoxLayout:
                size: dp(70), dp(40)
                size_hint: (None, None)

                canvas.before:
                    Color:
                        rgba: hex('#E5E5E5FF')
                    Rectangle:
                        pos: self.x + 5, self.y + 5
                        size: self.width - 10, self.height - 10

                TextInput:
                    id: d_input
                    font_size: dp(25)
                    halign: 'center'
                    input_filter: 'int'
                    multiline: False
                    size: self.parent.size
                    pos: self.parent.pos
                    background_color: (0,0,0,0)

            BoxLayout:
                size: dp(70), dp(40)
                size_hint: (None, None)

                canvas.before:
                    Color:
                        rgba: hex('#E5E5E5FF')
                    Rectangle:
                        pos: self.x + 5, self.y + 5
                        size: self.width - 10, self.height - 10

                TextInput:
                    id: l_input
                    font_size: dp(25)
                    halign: 'center'
                    input_filter: 'int'
                    multiline: False
                    size: self.parent.size
                    pos: self.parent.pos
                    background_color: (0,0,0,0)

            BoxLayout:
                size: dp(70), dp(40)
                size_hint: (None, None)

                canvas.before:
                    Color:
                        rgba: hex('#E5E5E5FF')
                    Rectangle:
                        pos: self.x + 5, self.y + 5
                        size: self.width - 10, self.height - 10

                TextInput:
                    id: r_input
                    font_size: dp(25)
                    halign: 'center'
                    input_filter: 'int'
                    multiline: False
                    size: self.parent.size
                    pos: self.parent.pos
                    background_color: (0,0,0,0)

            BoxLayout:
                size: dp(70), dp(40)
                size_hint: (None, None)

                canvas.before:
                    Color:
                        rgba: hex('#E5E5E5FF')
                    Rectangle:
                        pos: self.x + 5, self.y + 5
                        size: self.width - 10, self.height - 10

                TextInput:
                    id: x_input
                    font_size: dp(25)
                    halign: 'center'
                    input_filter: 'int'
                    multiline: False
                    size: self.parent.size
                    pos: self.parent.pos
                    background_color: (0,0,0,0)

            BoxLayout:
                size: dp(70), dp(40)
                size_hint: (None, None)

                canvas.before:
                    Color:
                        rgba: hex('#E5E5E5FF')
                    Rectangle:
                        pos: self.x + 5, self.y + 5
                        size: self.width - 10, self.height - 10

                TextInput:
                    id: y_input
                    font_size: dp(25)
                    halign: 'center'
                    input_filter: 'int'
                    multiline: False
                    size: self.parent.size
                    pos: self.parent.pos
                    background_color: (0,0,0,0)

            Label:
                id: x_datum_label
                font_size: dp(25)
                size: dp(150), dp(40)
                size_hint: (None, None)
                text: 'X:'
                color: 0,0,0,1
                halign: 'left'

            Label:
                id: x_datum_validation_label
                font_size: dp(15)
                size: dp(150), dp(40)
                size_hint: (None, None)
                pos: x_datum_label.pos[0], x_datum_label.pos[1] - dp(20)
                text: 'MAX: Test'
                color: 1,0,0,1
                halign: 'left'

            Label:
                id: y_datum_label
                font_size: dp(25)
                size: dp(150), dp(40)
                size_hint: (None, None)
                text: 'Y:'
                color: 0,0,0,1

            Label:
                id: y_datum_validation_label
                font_size: dp(15)
                size: dp(150), dp(40)
                size_hint: (None, None)
                pos: y_datum_label.pos[0], y_datum_label.pos[1] - dp(35)
                text: 'MAX: Test'
                color: 1,0,0,1
                halign: 'left'

            Image:
                id: bumper_bottom_image
                source: "./asmcnc/apps/drywall_cutter_app/img/bumper_bottom_green.png"
                size: self.parent.size
                pos: self.parent.pos

            Image:
                id: bumper_left_image
                source: "./asmcnc/apps/drywall_cutter_app/img/bumper_left_green.png"
                size: self.parent.size
                pos: self.parent.pos

            Image:
                id: bumper_right_image
                source: "./asmcnc/apps/drywall_cutter_app/img/bumper_right_green.png"
                size: self.parent.size
                pos: self.parent.pos

            Image:
                id: bumper_top_image
                source: "./asmcnc/apps/drywall_cutter_app/img/bumper_top_green.png"
                size: self.parent.size
                pos: self.parent.pos

""")


class DrywallShapeDisplay(Widget):

    image_filepath = "./asmcnc/apps/drywall_cutter_app/img/"

    def __init__(self, **kwargs):
        super(DrywallShapeDisplay, self).__init__(**kwargs)

        self.m = kwargs['machine']
        self.sm = kwargs['screen_manager']
        self.dwt_config = kwargs['dwt_config']
        self.engine = kwargs['engine']

        self.d_input.bind(text=self.d_input_change)
        self.l_input.bind(text=self.l_input_change)
        self.r_input.bind(text=self.r_input_change)
        self.x_input.bind(text=self.x_input_change)
        self.y_input.bind(text=self.y_input_change)

        Clock.schedule_interval(self.check_datum_and_extents, 0.1)

    def select_shape(self, shape, rotation, swap_lengths=False):
        image_source = self.image_filepath + shape
        if shape in ['rectangle', 'line']:
            image_source += "_" + rotation
        self.shape_dims_image.source = image_source + "_dims.png"
        self.shape_dims_image.opacity = 1

        if swap_lengths:
            x = self.x_input.text
            y = self.y_input.text
            self.x_input.text = y
            self.y_input.text = x

        if shape == 'circle':
            self.enable_input(self.d_input, (468, 310))
            self.place_widget(self.x_datum_label, (278, 27))
            self.place_widget(self.y_datum_label, (403, 196))
        else:
            self.disable_input(self.d_input)

        if shape in ['square', 'rectangle']:
            if shape == 'square':
                self.enable_input(self.r_input, (421, 311))
                self.disable_input(self.x_input)
                self.enable_input(self.y_input, (248, 327))
                self.place_widget(self.x_datum_label, (365, 35))
                self.place_widget(self.y_datum_label, (398, 113))
            else:
                if rotation == 'horizontal':
                    self.enable_input(self.r_input, (463, 311))
                    self.enable_input(self.x_input, (43, 175))
                    self.enable_input(self.y_input, (248, 327))
                    self.place_widget(self.x_datum_label, (407, 35))
                    self.place_widget(self.y_datum_label, (416, 114))
                else:
                    self.enable_input(self.r_input, (419, 333))
                    self.enable_input(self.x_input, (98, 155))
                    self.enable_input(self.y_input, (248, 331))
                    self.place_widget(self.x_datum_label, (367, 10))
                    self.place_widget(self.y_datum_label, (395, 63))
        else:
            self.disable_input(self.r_input)
            self.disable_input(self.x_input)
            self.disable_input(self.y_input)

        if shape == 'line':
            if rotation == 'horizontal':
                self.enable_input(self.l_input, (250, 228))
                self.place_widget(self.x_datum_label, (424, 75))
                self.place_widget(self.y_datum_label, (425, 195))
            else:
                self.enable_input(self.l_input, (178, 173))
                self.place_widget(self.x_datum_label, (281, 3))
                self.place_widget(self.y_datum_label, (350, 56))
        else:
            self.disable_input(self.l_input)

        if shape == 'geberit':
            self.place_widget(self.x_datum_label, (360, 19))
            self.place_widget(self.y_datum_label, (390, 77))

    def enable_input(self, text_input, pos):
        text_input.disabled = False
        text_input.opacity = 1
        text_input.parent.opacity = 1
        text_input.parent.pos = pos

    def place_widget(self, widget, pos):
        widget.pos = pos

    def disable_input(self, text_input):
        text_input.disabled = True
        text_input.opacity = 0
        text_input.parent.opacity = 0

    def select_toolpath(self, shape, toolpath, rotation):
        if shape in ['line', 'geberit']:
            self.shape_toolpath_image.opacity = 0
        else:
            if shape == 'rectangle':
                self.shape_toolpath_image.source = self.image_filepath + shape + "_" + rotation + "_" + toolpath + "_toolpath.png"
            else:
                self.shape_toolpath_image.source = self.image_filepath + shape + "_" + toolpath + "_toolpath.png"
            self.shape_toolpath_image.opacity = 1

    def d_input_change(self, instance, value):
        self.dwt_config.on_parameter_change('canvas_shape_dims.d', float(value or 0))

    def l_input_change(self, instance, value):
        self.dwt_config.on_parameter_change('canvas_shape_dims.l', float(value or 0))

    def r_input_change(self, instance, value):
        self.dwt_config.on_parameter_change('canvas_shape_dims.r', float(value or 0))

    def x_input_change(self, instance, value):
        if self.rotation_required():
            self.sm.get_screen('drywall_cutter').rotate_shape(swap_lengths=False)
        self.dwt_config.on_parameter_change('canvas_shape_dims.x', float(value or 0))

    def y_input_change(self, instance, value):
        if self.rotation_required():
            self.sm.get_screen('drywall_cutter').rotate_shape(swap_lengths=False)
        self.dwt_config.on_parameter_change('canvas_shape_dims.y', float(value or 0))

    def rotation_required(self):
        if "rectangle" in self.shape_dims_image.source:
            if "vertical" in self.shape_dims_image.source:
                return float(self.x_input.text or 0) < float(self.y_input.text or 0)
            else:
                return float(self.x_input.text or 0) > float(self.y_input.text or 0)
        else:
            return False

    def check_datum_and_extents(self, dt):
        # Maths from Ed, documented here https://docs.google.com/spreadsheets/d/1X37CWF8bsXeC0dY-HsbwBu_QR6N510V-5aPTnxwIR6I/edit#gid=677510108
        current_x = round(self.m.x_wco() + (self.m.get_dollar_setting(130) - self.m.limit_switch_safety_distance) - self.m.laser_offset_tool_clearance_to_access_edge_of_sheet, 2)
        current_y = round(self.m.y_wco() + (self.m.get_dollar_setting(131) - self.m.limit_switch_safety_distance) - (self.m.get_dollar_setting(27) - self.m.limit_switch_safety_distance), 2)
        self.x_datum_label.text = 'X: ' + str(current_x)
        self.y_datum_label.text = 'Y: ' + str(current_y)

        # Account for cutter size
        cutter_radius = self.dwt_config.active_cutter.diameter / 2
        if self.dwt_config.active_config.toolpath_offset == 'inside':
            tool_offset_value = -cutter_radius
        elif self.dwt_config.active_config.toolpath_offset == 'outside':
            tool_offset_value = cutter_radius
        else:
            tool_offset_value = 0

        # Calculate shape's extent from datum using shape type and input dimensions
        current_shape = self.dwt_config.active_config.shape_type.lower()
        if current_shape == 'circle':
            x_min = y_min = -(float(self.d_input.text or 0) / 2) - tool_offset_value
            x_dim = y_dim = (float(self.d_input.text or 0) / 2) + tool_offset_value
        elif current_shape in ['square', 'rectangle']:
            x_min = y_min = -tool_offset_value
            y_dim = float(self.y_input.text or 0) + tool_offset_value
            # As square only uses y input it needs a separate condition
            if current_shape == 'square':
                x_dim = y_dim
            elif current_shape == 'rectangle':
                x_dim = float(self.x_input.text or 0) + tool_offset_value
        elif current_shape == 'line':
            x_min = y_min = 0
            if "horizontal" in self.shape_dims_image.source:
                x_dim = 0
                y_dim = float(self.l_input.text or 0)
            else:
                x_dim = float(self.l_input.text or 0)
                y_dim = 0
        elif current_shape == 'geberit':
            x_dim, y_dim, x_min, y_min = self.engine.get_custom_shape_extents()

        # Calculate shape's distances from every edge
        x_min_clearance = self.m.x_wco() + x_min + self.m.get_dollar_setting(130) - self.m.limit_switch_safety_distance
        y_min_clearance = self.m.y_wco() + y_min + self.m.get_dollar_setting(131) - self.m.limit_switch_safety_distance
        x_max_clearance = -(self.m.x_wco() + x_dim) - self.m.limit_switch_safety_distance
        y_max_clearance = -(self.m.y_wco() + y_dim) - self.m.limit_switch_safety_distance

        # Set bumper colours based on whether anything crosses a boundary
        if x_min_clearance < 0:
            self.bumper_bottom_image.source = "./asmcnc/apps/drywall_cutter_app/img/bumper_bottom_red.png"
        else:
            self.bumper_bottom_image.source = "./asmcnc/apps/drywall_cutter_app/img/bumper_bottom_green.png"

        if y_min_clearance < 0:
            self.bumper_right_image.source = "./asmcnc/apps/drywall_cutter_app/img/bumper_right_red.png"
        else:
            self.bumper_right_image.source = "./asmcnc/apps/drywall_cutter_app/img/bumper_right_green.png"

        if x_max_clearance < 0:
            self.bumper_top_image.source = "./asmcnc/apps/drywall_cutter_app/img/bumper_top_red.png"
        else:
            self.bumper_top_image.source = "./asmcnc/apps/drywall_cutter_app/img/bumper_top_green.png"

        if y_max_clearance < 0:
            self.bumper_left_image.source = "./asmcnc/apps/drywall_cutter_app/img/bumper_left_red.png"
        else:
            self.bumper_left_image.source = "./asmcnc/apps/drywall_cutter_app/img/bumper_left_green.png"
