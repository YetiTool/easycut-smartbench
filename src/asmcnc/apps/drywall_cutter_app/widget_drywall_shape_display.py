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

    d_input_validation_label:d_input_validation_label
    l_input_validation_label:l_input_validation_label
    r_input_validation_label:r_input_validation_label
    x_input_validation_label:x_input_validation_label
    y_input_validation_label:y_input_validation_label
    x_datum_label:x_datum_label
    x_datum_validation_label:x_datum_validation_label
    y_datum_label:y_datum_label
    y_datum_validation_label:y_datum_validation_label

    bumper_bottom_image:bumper_bottom_image
    bumper_left_image:bumper_left_image
    bumper_right_image:bumper_right_image
    bumper_top_image:bumper_top_image
    
    on_touch_down: root.on_touch()

    config_name_label:config_name_label

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
                    input_filter: 'float'
                    multiline: False
                    size: self.parent.size
                    pos: self.parent.pos
                    background_color: (0,0,0,0)

            Label:
                id: d_input_validation_label
                font_size: dp(15)
                size: d_input.size
                size_hint: (None, None)
                pos: d_input.pos[0], d_input.pos[1] - dp(30)
                color: 1,0,0,1
                halign: 'left'
                opacity: 0

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
                    input_filter: 'float'
                    multiline: False
                    size: self.parent.size
                    pos: self.parent.pos
                    background_color: (0,0,0,0)

            Label:
                id: l_input_validation_label
                font_size: dp(15)
                size: l_input.size
                size_hint: (None, None)
                pos: l_input.pos[0], l_input.pos[1] - dp(30)
                color: 1,0,0,1
                halign: 'left'
                opacity: 0

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
                    input_filter: 'float'
                    multiline: False
                    size: self.parent.size
                    pos: self.parent.pos
                    background_color: (0,0,0,0)

            Label:
                id: r_input_validation_label
                font_size: dp(15)
                size: r_input.size
                size_hint: (None, None)
                pos: r_input.pos[0], r_input.pos[1] - dp(30)
                color: 1,0,0,1
                halign: 'left'
                opacity: 0

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
                    input_filter: 'float'
                    multiline: False
                    size: self.parent.size
                    pos: self.parent.pos
                    background_color: (0,0,0,0)

            Label:
                id: x_input_validation_label
                font_size: dp(15)
                size: x_input.size
                size_hint: (None, None)
                pos: x_input.pos[0], x_input.pos[1] - dp(30)
                color: 1,0,0,1
                halign: 'left'
                opacity: 0

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
                    input_filter: 'float'
                    multiline: False
                    size: self.parent.size
                    pos: self.parent.pos
                    background_color: (0,0,0,0)

            Label:
                id: y_input_validation_label
                font_size: dp(15)
                size: y_input.size
                size_hint: (None, None)
                pos: y_input.pos[0], y_input.pos[1] - dp(30)
                color: 1,0,0,1
                halign: 'left'
                opacity: 0

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
                size: x_datum_label.size
                size_hint: (None, None)
                pos: x_datum_label.pos[0], x_datum_label.pos[1] - dp(20)
                color: 1,0,0,1
                halign: 'left'
                opacity: 0

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
                size: y_datum_label.size
                size_hint: (None, None)
                pos: y_datum_label.pos[0], y_datum_label.pos[1] - dp(35)
                color: 1,0,0,1
                halign: 'left'
                opacity: 0

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

            # TextInput instead of Label, as there is no way to left align a Label in a FloatLayout
            TextInput:
                id: config_name_label
                font_size: dp(20)
                size: self.parent.width, dp(40)
                size_hint: (None, None)
                pos: self.parent.pos[0], self.parent.size[1] - self.height + dp(7)
                multiline: False
                background_color: (0,0,0,0)
                disabled_foreground_color: (0,0,0,1)
                disabled: True

""")


class DrywallShapeDisplay(Widget):

    image_filepath = "./asmcnc/apps/drywall_cutter_app/img/"

    swapping_lengths = False

    def __init__(self, **kwargs):
        super(DrywallShapeDisplay, self).__init__(**kwargs)

        self.m = kwargs['machine']
        self.sm = kwargs['screen_manager']
        self.dwt_config = kwargs['dwt_config']
        self.engine = kwargs['engine']
        self.kb = kwargs['keyboard']

        self.d_input.bind(text=self.d_input_change) # Diameter of circle
        self.l_input.bind(text=self.l_input_change) # Length of line
        self.r_input.bind(text=self.r_input_change) # Radius of corners
        self.x_input.bind(text=self.x_input_change) # Square/rectangle x length
        self.y_input.bind(text=self.y_input_change) # Square/rectangle y length

        self.text_inputs = [self.d_input, self.l_input, self.r_input, self.x_input, self.y_input]
        self.kb.setup_text_inputs(self.text_inputs)

        Clock.schedule_interval(self.check_datum_and_extents, 0.1)

    def on_touch(self):
        for text_input in self.text_inputs:
            text_input.focus = False

    def select_shape(self, shape, rotation, swap_lengths=False):
        shape = shape.lower() # in case it's a test config with a capital letter
        image_source = self.image_filepath + shape
        if shape in ['rectangle', 'line']:
            image_source += "_" + rotation
        self.shape_dims_image.source = image_source + "_dims.png"
        self.shape_dims_image.opacity = 1

        if swap_lengths:
            self.swapping_lengths = True
            x = self.x_input.text
            y = self.y_input.text
            self.x_input.text = y
            self.y_input.text = x
            self.swapping_lengths = False

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
                    self.place_widget(self.x_datum_label, (397, 35))
                    self.place_widget(self.y_datum_label, (416, 114))
                else:
                    self.enable_input(self.r_input, (419, 333))
                    self.enable_input(self.x_input, (98, 155))
                    self.enable_input(self.y_input, (248, 331))
                    self.place_widget(self.x_datum_label, (235, 20))
                    self.place_widget(self.y_datum_label, (395, 63))
        else:
            self.disable_input(self.r_input)
            self.disable_input(self.x_input)
            self.disable_input(self.y_input)

        if shape == 'line':
            if rotation == 'horizontal':
                self.enable_input(self.l_input, (250, 228))
                self.place_widget(self.x_datum_label, (414, 75))
                self.place_widget(self.y_datum_label, (425, 195))
            else:
                self.enable_input(self.l_input, (178, 173))
                self.place_widget(self.x_datum_label, (270, 20))
                self.place_widget(self.y_datum_label, (350, 56))
        else:
            self.disable_input(self.l_input)

        if shape == 'geberit':
            self.place_widget(self.x_datum_label, (360, 19))
            self.place_widget(self.y_datum_label, (390, 77))

        self.dwt_config.on_parameter_change('rotation', rotation)

    def enable_input(self, text_input, pos):
        text_input.parent.pos = pos
        text_input.disabled = False
        text_input.opacity = 1
        text_input.parent.opacity = 1

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
        # On startup it seems to call these functions and set everything to 0, so check that drywall app is open
        if self.sm.current == 'drywall_cutter':
            value = self.remove_negatives(instance, value)
            self.dwt_config.on_parameter_change('canvas_shape_dims.d', float(value or 0))

    def l_input_change(self, instance, value):
        if self.sm.current == 'drywall_cutter':
            value = self.remove_negatives(instance, value)
            self.dwt_config.on_parameter_change('canvas_shape_dims.l', float(value or 0))

    def r_input_change(self, instance, value):
        if self.sm.current == 'drywall_cutter':
            value = self.remove_negatives(instance, value)
            self.dwt_config.on_parameter_change('canvas_shape_dims.r', float(value or 0))

    def x_input_change(self, instance, value):
        if self.sm.current == 'drywall_cutter':
            value = self.remove_negatives(instance, value)
            self.do_rectangle_checks()
            self.dwt_config.on_parameter_change('canvas_shape_dims.x', float(value or 0))

    def y_input_change(self, instance, value):
        if self.sm.current == 'drywall_cutter':
            value = self.remove_negatives(instance, value)
            self.do_rectangle_checks()
            self.dwt_config.on_parameter_change('canvas_shape_dims.y', float(value or 0))

    def do_rectangle_checks(self):
        if not self.swapping_lengths:
            if self.rotation_required():
                self.sm.get_screen('drywall_cutter').rotate_shape(swap_lengths=False)
            if self.rectangle_with_equal_sides():
                toolpath = self.dwt_config.active_config.toolpath_offset
                self.sm.get_screen('drywall_cutter').select_shape('square')
                self.sm.get_screen('drywall_cutter').select_toolpath(toolpath)

    def rotation_required(self):
        if self.dwt_config.active_config.shape_type.lower() == "rectangle":
            if self.dwt_config.active_config.rotation == "vertical":
                return float(self.x_input.text or 0) < float(self.y_input.text or 0)
            else:
                return float(self.x_input.text or 0) > float(self.y_input.text or 0)
        else:
            return False
        
    def rectangle_with_equal_sides(self):
        if "rectangle" in self.shape_dims_image.source:
            if self.x_input.text and self.y_input.text:
                if float(self.x_input.text) == float(self.y_input.text):
                    return True
        return False

    def remove_negatives(self, instance, value):
        if value.startswith("-"):
            # Stop user inputting negative values
            instance.text = ""
            value = ""
        return value

    def check_datum_and_extents(self, dt):
        # All maths in this function from Ed, documented here https://docs.google.com/spreadsheets/d/1X37CWF8bsXeC0dY-HsbwBu_QR6N510V-5aPTnxwIR6I/edit#gid=677510108
        current_x = round(self.m.x_wco() + (self.m.get_dollar_setting(130) - self.m.limit_switch_safety_distance) - self.m.laser_offset_tool_clearance_to_access_edge_of_sheet, 2)
        current_y = round(self.m.y_wco() + (self.m.get_dollar_setting(131) - self.m.limit_switch_safety_distance) - (self.m.get_dollar_setting(27) - self.m.limit_switch_safety_distance), 2)
        self.x_datum_label.text = 'X: ' + str(current_x)
        self.y_datum_label.text = 'Y: ' + str(current_y)

        if self.dwt_config.active_config.datum_position.x != self.m.x_wco():
            self.dwt_config.active_config.datum_position.x = self.m.x_wco()

        if self.dwt_config.active_config.datum_position.y != self.m.y_wco():
            self.dwt_config.active_config.datum_position.y = self.m.y_wco()

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

        self.x_datum_validation_label.opacity = 0
        self.y_datum_validation_label.opacity = 0
        # Set bumper colours based on whether anything crosses a boundary, and show validation labels
        if x_min_clearance < 0:
            self.bumper_bottom_image.source = "./asmcnc/apps/drywall_cutter_app/img/bumper_bottom_red.png"
            self.x_datum_validation_label.text = 'MIN: ' + str(round(abs(x_min_clearance) + current_x, 2))
            self.x_datum_validation_label.opacity = 1
        else:
            self.bumper_bottom_image.source = "./asmcnc/apps/drywall_cutter_app/img/bumper_bottom_green.png"

        if y_min_clearance < 0:
            self.bumper_right_image.source = "./asmcnc/apps/drywall_cutter_app/img/bumper_right_red.png"
            self.y_datum_validation_label.text = 'MIN: ' + str(round(abs(y_min_clearance) + current_y, 2))
            self.y_datum_validation_label.opacity = 1
        else:
            self.bumper_right_image.source = "./asmcnc/apps/drywall_cutter_app/img/bumper_right_green.png"

        if x_max_clearance < 0:
            self.bumper_top_image.source = "./asmcnc/apps/drywall_cutter_app/img/bumper_top_red.png"
            self.x_datum_validation_label.text = 'MAX: ' + str(round(current_x - abs(x_max_clearance), 2))
            self.x_datum_validation_label.opacity = 1
        else:
            self.bumper_top_image.source = "./asmcnc/apps/drywall_cutter_app/img/bumper_top_green.png"

        if y_max_clearance < 0:
            self.bumper_left_image.source = "./asmcnc/apps/drywall_cutter_app/img/bumper_left_red.png"
            self.y_datum_validation_label.text = 'MAX: ' + str(round(current_y - abs(y_max_clearance), 2))
            self.y_datum_validation_label.opacity = 1
        else:
            self.bumper_left_image.source = "./asmcnc/apps/drywall_cutter_app/img/bumper_left_green.png"

        x_machine_range = self.m.get_dollar_setting(130) - 2 * self.m.limit_switch_safety_distance
        y_machine_range = self.m.get_dollar_setting(131) - 2 * self.m.limit_switch_safety_distance
        clearance_between_limit_edge = 1
        x_practical_range = x_machine_range - 2 * clearance_between_limit_edge
        y_practical_range = y_machine_range - 2 * clearance_between_limit_edge

        # Now show a message if any dimensions are too big
        d_limit = min(x_machine_range, y_machine_range)
        if current_shape == 'circle' and float(self.d_input.text or 0) > d_limit:
            self.d_input_validation_label.text = 'MAX: ' + str(d_limit)
            self.d_input_validation_label.opacity = 1
        else:
            self.d_input_validation_label.opacity = 0

        if current_shape in ['square', 'rectangle']:
            x_limit = x_practical_range
            y_limit = y_practical_range
            r_limit = min(x_limit, y_limit) / 2
            # Because square is limited by the smaller dimension
            square_limit = min(x_limit, y_limit)

            if current_shape == 'square':
                self.x_input_validation_label.opacity = 0
                if float(self.y_input.text or 0) > square_limit:
                    self.y_input_validation_label.text = 'MAX: ' + str(square_limit)
                    self.y_input_validation_label.opacity = 1
                else:
                    self.y_input_validation_label.opacity = 0
            else:
                if float(self.x_input.text or 0) > x_limit:
                    self.x_input_validation_label.text = 'MAX: ' + str(x_limit)
                    self.x_input_validation_label.opacity = 1
                else:
                    self.x_input_validation_label.opacity = 0

                if float(self.y_input.text or 0) > y_limit:
                    self.y_input_validation_label.text = 'MAX: ' + str(y_limit)
                    self.y_input_validation_label.opacity = 1
                else:
                    self.y_input_validation_label.opacity = 0

            if float(self.r_input.text or 0) > r_limit:
                self.r_input_validation_label.text = 'MAX: ' + str(r_limit)
                self.r_input_validation_label.opacity = 1
            else:
                self.r_input_validation_label.opacity = 0
        else:
            self.r_input_validation_label.opacity = 0
            self.x_input_validation_label.opacity = 0
            self.y_input_validation_label.opacity = 0

        if current_shape == 'line':
            if "horizontal" in self.shape_dims_image.source:
                if float(self.l_input.text or 0) > y_practical_range:
                    self.l_input_validation_label.text = 'MAX: ' + str(y_practical_range)
                    self.l_input_validation_label.opacity = 1
                else:
                    self.l_input_validation_label.opacity = 0
            else:
                if float(self.l_input.text or 0) > x_practical_range:
                    self.l_input_validation_label.text = 'MAX: ' + str(x_practical_range)
                    self.l_input_validation_label.opacity = 1
                else:
                    self.l_input_validation_label.opacity = 0
        else:
            self.l_input_validation_label.opacity = 0

    def are_inputs_valid(self):
        # Logic defined by Benji here https://docs.google.com/spreadsheets/d/1X37CWF8bsXeC0dY-HsbwBu_QR6N510V-5aPTnxwIR6I/edit#gid=1512963755

        # First check if any validation label is visible, meaning something is out of bounds
        if 1 in [self.d_input_validation_label.opacity,
                 self.l_input_validation_label.opacity,
                 self.r_input_validation_label.opacity,
                 self.x_input_validation_label.opacity,
                 self.y_input_validation_label.opacity,
                 self.x_datum_validation_label.opacity,
                 self.y_datum_validation_label.opacity]:
            return False

        # Ensure roundedness is not too large
        if self.dwt_config.active_config.shape_type.lower() == "square":
            if float(self.r_input.text or 0) > float(self.y_input.text or 0) / 2:
                return False
        elif self.dwt_config.active_config.shape_type.lower() == "rectangle":
            if float(self.r_input.text or 0) > (min(float(self.x_input.text or 0), float(self.y_input.text or 0)) / 2):
                return False

        # Otherwise check hardcoded min values
        if self.dwt_config.active_config.shape_type.lower() == "circle":
            if self.dwt_config.active_config.toolpath_offset.lower() ==  "inside":
                return float(self.d_input.text or 0) >= 0.1 + self.dwt_config.active_cutter.diameter
            else:
                return float(self.d_input.text or 0) >= 0.1

        elif self.dwt_config.active_config.shape_type.lower() == "square":
            if self.dwt_config.active_config.toolpath_offset.lower() ==  "inside":
                return float(self.y_input.text or 0) >= 0.1 + self.dwt_config.active_cutter.diameter
            elif self.dwt_config.active_config.toolpath_offset.lower() ==  "outside":
                return float(self.y_input.text or 0) >= 1
            else:
                return float(self.y_input.text or 0) >= 0.1

        elif self.dwt_config.active_config.shape_type.lower() == "rectangle":
            if self.dwt_config.active_config.toolpath_offset.lower() ==  "inside":
                return (float(self.x_input.text or 0) >= 0.1 + self.dwt_config.active_cutter.diameter) and (float(self.y_input.text or 0) >= 0.1 + self.dwt_config.active_cutter.diameter)
            elif self.dwt_config.active_config.toolpath_offset.lower() ==  "outside":
                return (float(self.x_input.text or 0) >= 1) and (float(self.y_input.text or 0) >= 1)
            else:
                return (float(self.x_input.text or 0) >= 0.1) and (float(self.y_input.text or 0) >= 0.1)

        elif self.dwt_config.active_config.shape_type.lower() == "line":
            return float(self.l_input.text or 0) >= 0.1

        else:
            return True