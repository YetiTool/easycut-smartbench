from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.clock import Clock

from asmcnc.apps.drywall_cutter_app.config.config_options import ToolpathOffsetOptions
from asmcnc.comms.logging_system.logging_system import Logger
import re

from asmcnc.core_UI import scaling_utils

Builder.load_string("""
#:import FloatInput asmcnc.core_UI.components.text_inputs.float_input.FloatInput
#:import scaling_utils asmcnc.core_UI.scaling_utils
<DrywallShapeDisplay>

    shape_dims_image:shape_dims_image
    shape_toolpath_image:shape_toolpath_image

    unit_switch:unit_switch

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

    config_name_label:config_name_label
    machine_state_label:machine_state_label

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
                allow_stretch: True

            Image:
                id: shape_toolpath_image
                opacity: 0
                size: self.parent.size
                pos: self.parent.pos
                allow_stretch: True

            Image:
                id: shape_dims_image
                opacity: 0
                size: self.parent.size
                pos: self.parent.pos
                allow_stretch: True

            Switch:
                id: unit_switch
                size: scaling_utils.get_scaled_tuple((dp(83), dp(32)))
                size_hint: (None, None)
                pos: self.parent.pos[0] + self.parent.size[0] - self.size[0] - scaling_utils.get_scaled_width(dp(9)), self.parent.pos[1] + scaling_utils.get_scaled_height(dp(6))

            BoxLayout:
                size: scaling_utils.get_scaled_tuple((dp(90), dp(40)))
                size_hint: (None, None)

                canvas.before:
                    Color:
                        rgba: hex('#E5E5E5FF')
                    Rectangle:
                        pos: self.x + scaling_utils.get_scaled_width(2.5), self.y + scaling_utils.get_scaled_height(5)
                        size: self.width - scaling_utils.get_scaled_width(5), self.height - scaling_utils.get_scaled_height(10)

                FloatInput:
                    id: d_input
                    font_size: scaling_utils.get_scaled_width(dp(25))
                    halign: 'center'
                    multiline: False
                    size: self.parent.size
                    pos: self.parent.pos
                    background_color: (0,0,0,0)

            Label:
                text: 'D'
                font_size: scaling_utils.get_scaled_width(dp(25))
                pos: d_input.pos[0] - self.width - scaling_utils.get_scaled_width(2.5), d_input.pos[1] + scaling_utils.get_scaled_height(dp(3))
                opacity: d_input.opacity
                color: 0,0,0,1
                size: self.texture_size
                size_hint: (None, None)

            Label:
                id: d_input_validation_label
                font_size: scaling_utils.get_scaled_width(dp(15))
                size: d_input.size
                size_hint: (None, None)
                pos: d_input.pos[0], d_input.pos[1] - scaling_utils.get_scaled_height(dp(30))
                color: 1,0,0,1
                halign: 'left'
                opacity: 0

            BoxLayout:
                size: scaling_utils.get_scaled_tuple((dp(90), dp(40)))
                size_hint: (None, None)

                canvas.before:
                    Color:
                        rgba: hex('#E5E5E5FF')
                    Rectangle:
                        pos: self.x + scaling_utils.get_scaled_width(2.5), self.y + scaling_utils.get_scaled_height(5)
                        size: self.width - scaling_utils.get_scaled_width(5), self.height - scaling_utils.get_scaled_height(10)

                FloatInput:
                    id: l_input
                    font_size: scaling_utils.get_scaled_width(dp(25))
                    halign: 'center'
                    multiline: False
                    size: self.parent.size
                    pos: self.parent.pos
                    background_color: (0,0,0,0)

            Label:
                text: 'L'
                font_size: scaling_utils.get_scaled_width(dp(25))
                pos: l_input.pos[0] - self.width - scaling_utils.get_scaled_width(2.5), l_input.pos[1] + scaling_utils.get_scaled_height(dp(3))
                opacity: l_input.opacity
                color: 0,0,0,1
                size: self.texture_size
                size_hint: (None, None)

            Label:
                id: l_input_validation_label
                font_size: scaling_utils.get_scaled_width(dp(15))
                size: l_input.size
                size_hint: (None, None)
                pos: l_input.pos[0], l_input.pos[1] - scaling_utils.get_scaled_height(dp(30))
                color: 1,0,0,1
                halign: 'left'
                opacity: 0

            BoxLayout:
                size: scaling_utils.get_scaled_tuple((dp(90), dp(40)))
                size_hint: (None, None)

                canvas.before:
                    Color:
                        rgba: hex('#E5E5E5FF')
                    Rectangle:
                        pos: self.x + scaling_utils.get_scaled_width(2.5), self.y + scaling_utils.get_scaled_height(5)
                        size: self.width - scaling_utils.get_scaled_width(5), self.height - scaling_utils.get_scaled_height(10)

                FloatInput:
                    id: r_input
                    font_size: scaling_utils.get_scaled_width(dp(25))
                    halign: 'center'
                    multiline: False
                    size: self.parent.size
                    pos: self.parent.pos
                    background_color: (0,0,0,0)

            Label:
                text: 'R'
                font_size: scaling_utils.get_scaled_width(dp(25))
                pos: r_input.pos[0] - self.width - scaling_utils.get_scaled_width(2.5), r_input.pos[1] + scaling_utils.get_scaled_height(dp(3))
                opacity: r_input.opacity
                color: 0,0,0,1
                size: self.texture_size
                size_hint: (None, None)

            Label:
                id: r_input_validation_label
                font_size: scaling_utils.get_scaled_width(dp(15))
                size: r_input.size
                size_hint: (None, None)
                pos: r_input.pos[0], r_input.pos[1] - scaling_utils.get_scaled_height(dp(30))
                color: 1,0,0,1
                halign: 'left'
                opacity: 0

            BoxLayout:
                size: scaling_utils.get_scaled_tuple((dp(90), dp(40)))
                size_hint: (None, None)

                canvas.before:
                    Color:
                        rgba: hex('#E5E5E5FF')
                    Rectangle:
                        pos: self.x + scaling_utils.get_scaled_width(2.5), self.y + scaling_utils.get_scaled_height(5)
                        size: self.width - scaling_utils.get_scaled_width(5), self.height - scaling_utils.get_scaled_height(10)

                FloatInput:
                    id: x_input
                    font_size: scaling_utils.get_scaled_width(dp(25))
                    halign: 'center'
                    multiline: False
                    size: self.parent.size
                    pos: self.parent.pos
                    background_color: (0,0,0,0)

            Label:
                text: 'X'
                font_size: scaling_utils.get_scaled_width(dp(25))
                pos: x_input.pos[0] - self.width - scaling_utils.get_scaled_width(2.5), x_input.pos[1] + scaling_utils.get_scaled_height(dp(3))
                opacity: x_input.opacity
                color: 0,0,0,1
                size: self.texture_size
                size_hint: (None, None)

            Label:
                id: x_input_validation_label
                font_size: scaling_utils.get_scaled_width(dp(15))
                size: x_input.size
                size_hint: (None, None)
                pos: x_input.pos[0], x_input.pos[1] - scaling_utils.get_scaled_height(dp(30))
                color: 1,0,0,1
                halign: 'left'
                opacity: 0

            BoxLayout:
                size: scaling_utils.get_scaled_tuple((dp(90), dp(40)))
                size_hint: (None, None)

                canvas.before:
                    Color:
                        rgba: hex('#E5E5E5FF')
                    Rectangle:
                        pos: self.x + 2.5, self.y + 5
                        size: self.width - scaling_utils.get_scaled_width(5), self.height - scaling_utils.get_scaled_height(10)

                FloatInput:
                    id: y_input
                    font_size: scaling_utils.get_scaled_width(dp(25))
                    halign: 'center'
                    multiline: False
                    size: self.parent.size
                    pos: self.parent.pos
                    background_color: (0,0,0,0)

            Label:
                text: 'Y'
                font_size: scaling_utils.get_scaled_width(dp(25))
                pos: y_input.pos[0] - self.width - 2.5, y_input.pos[1] + scaling_utils.get_scaled_height(dp(3))
                opacity: y_input.opacity
                color: 0,0,0,1
                size: self.texture_size
                size_hint: (None, None)

            Label:
                id: y_input_validation_label
                font_size: scaling_utils.get_scaled_width(dp(15))
                size: y_input.size
                size_hint: (None, None)
                pos: y_input.pos[0], y_input.pos[1] - scaling_utils.get_scaled_height(dp(30))
                color: 1,0,0,1
                halign: 'left'
                opacity: 0

            Label:
                id: x_datum_label
                font_size: scaling_utils.get_scaled_width(dp(25))
                size: scaling_utils.get_scaled_tuple((dp(150), dp(40)))
                size_hint: (None, None)
                text: 'X:'
                color: 0,0,0,1
                halign: 'left'

            Label:
                id: x_datum_validation_label
                font_size: scaling_utils.get_scaled_width(dp(15))
                size: x_datum_label.size
                size_hint: (None, None)
                pos: x_datum_label.pos[0], x_datum_label.pos[1] - scaling_utils.get_scaled_height(dp(20))
                color: 1,0,0,1
                halign: 'left'
                opacity: 0

            Label:
                id: y_datum_label
                font_size: scaling_utils.get_scaled_width(dp(25))
                size: scaling_utils.get_scaled_tuple((dp(150), dp(40)))
                size_hint: (None, None)
                text: 'Y:'
                color: 0,0,0,1

            Label:
                id: y_datum_validation_label
                font_size: scaling_utils.get_scaled_width(dp(15))
                size: y_datum_label.size
                size_hint: (None, None)
                pos: y_datum_label.pos[0], y_datum_label.pos[1] - scaling_utils.get_scaled_height(dp(35))
                color: 1,0,0,1
                halign: 'left'
                opacity: 0

            Image:
                id: bumper_bottom_image
                source: "./asmcnc/apps/drywall_cutter_app/img/bumper_bottom_green.png"
                size: self.parent.size
                pos: self.parent.pos
                allow_stretch: True

            Image:
                id: bumper_left_image
                source: "./asmcnc/apps/drywall_cutter_app/img/bumper_left_green.png"
                size: self.parent.size
                pos: self.parent.pos
                allow_stretch: True

            Image:
                id: bumper_right_image
                source: "./asmcnc/apps/drywall_cutter_app/img/bumper_right_green.png"
                size: self.parent.size
                pos: self.parent.pos
                allow_stretch: True

            Image:
                id: bumper_top_image
                source: "./asmcnc/apps/drywall_cutter_app/img/bumper_top_green.png"
                size: self.parent.size
                pos: self.parent.pos
                allow_stretch: True

            # TextInput instead of Label, as there is no way to left align a Label in a FloatLayout
            TextInput:
                id: config_name_label
                font_size: scaling_utils.get_scaled_width(dp(20))
                size: self.parent.width, scaling_utils.get_scaled_height(dp(40))
                size_hint: (None, None)
                pos: self.parent.pos[0] + scaling_utils.get_scaled_width(dp(5)), self.parent.size[1] - self.height + scaling_utils.get_scaled_height(dp(5))
                multiline: False
                background_color: (0,0,0,0)
                disabled_foreground_color: (0,0,0,1)
                disabled: True

            Label:
                id: machine_state_label
                font_size: scaling_utils.get_scaled_width(dp(20))
                size: self.texture_size[0], scaling_utils.get_scaled_height(dp(40))
                size_hint: (None, None)
                pos: self.parent.pos[0] + self.parent.size[0] - self.texture_size[0] - scaling_utils.get_scaled_width(dp(10)), self.parent.size[1] - self.height + scaling_utils.get_scaled_height(dp(5))
                text: 'Test'
                color: 0,0,0,1

""")


class DrywallShapeDisplay(Widget):

    image_filepath = "./asmcnc/apps/drywall_cutter_app/img/"

    swapping_lengths = False

    X_MIN = 0
    X_MAX = 1250

    Y_MIN = 0
    Y_MAX = 2500

    def __init__(self, **kwargs):
        super(DrywallShapeDisplay, self).__init__(**kwargs)

        self.m = kwargs['machine']
        self.sm = kwargs['screen_manager']
        self.dwt_config = kwargs['dwt_config']
        self.engine = kwargs['engine']
        self.kb = kwargs['kb']
        self.localization = kwargs['localization']
        self.cs = kwargs['cs']

        # machine position and state updates from serial_connection:
        self.x_coord = 0
        self.y_coord = 0
        self.m.s.bind(m_state=lambda i, value: self.update_state(value))
        self.m.s.bind(m_x=lambda i, value: self.update_x_datum(value))
        self.m.s.bind(m_y=lambda i, value: self.update_y_datum(value))

        self.d_input.bind(focus=self.text_input_change) # Diameter of circle
        self.l_input.bind(focus=self.text_input_change) # Length of line
        self.r_input.bind(focus=self.text_input_change) # Radius of corners
        self.x_input.bind(focus=self.text_input_change) # Square/rectangle x length
        self.y_input.bind(focus=self.text_input_change) # Square/rectangle y length

        self.text_inputs = [self.d_input, self.l_input, self.r_input, self.x_input, self.y_input]
        self.kb.setup_text_inputs(self.text_inputs)

        self.input_letter_dict = {
            self.d_input:'d',
            self.l_input:'l',
            self.r_input:'r',
            self.x_input:'x',
            self.y_input:'y'
        }

        # Show custom switch image
        self.unit_switch.canvas.children[5].source = "./asmcnc/apps/drywall_cutter_app/img/unit_toggle.png"
        self.unit_switch.bind(active=self.toggle_units)

        self.dwt_config.bind(active_config_name=self.on_config_name_change)
        self.on_config_name_change(self.dwt_config, self.dwt_config.active_config_name)

    def update_x_datum(self, value):
        """
        Is called when the x datum of the machine changes. E.g. running, jogging, after homing...
        value has the new x_datum
        """
        self.x_coord = value + self.m.laser_offset_x_value
        Clock.schedule_once(lambda dt: self.check_datum_and_extents(), 0.1)

    def update_y_datum(self, value):
        """
        Is called when the y datum of the machine changes. E.g. running, jogging, after homing...
        value has the new y_datum
        """
        self.y_coord = value + self.m.laser_offset_y_value
        Clock.schedule_once(lambda dt: self.check_datum_and_extents(), 0.1)

    def update_state(self, value):
        """
        Updates the machine_state_label with the value from serial_connection
        """
        self.machine_state_label.text = value

    def select_shape(self, shape, rotation, swap_lengths=False):
        shape = shape.lower() # in case it's a test config with a capital letter
        image_source = self.image_filepath + shape
        if shape in ['rectangle', 'line', 'geberit']:
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
            self.enable_input(self.d_input, scaling_utils.get_scaled_tuple((458, 310)))
            self.place_widget(self.x_datum_label, scaling_utils.get_scaled_tuple((278, 27)))
            self.place_widget(self.y_datum_label, scaling_utils.get_scaled_tuple((403, 196)))
            self.place_widget(self.y_datum_validation_label, (self.y_datum_label.x,
                                                              self.y_datum_label.y - scaling_utils.get_scaled_height(35)))
        else:
            self.disable_input(self.d_input)

        if shape in ['square', 'rectangle']:
            if shape == 'square':
                self.enable_input(self.r_input, scaling_utils.get_scaled_tuple((411, 311)))
                self.disable_input(self.x_input)
                self.enable_input(self.y_input, scaling_utils.get_scaled_tuple((238, 327)))
                self.place_widget(self.x_datum_label, scaling_utils.get_scaled_tuple((365, 55)))
                self.place_widget(self.y_datum_label, scaling_utils.get_scaled_tuple((398, 113)))
                self.place_widget(self.y_datum_validation_label, (self.y_datum_label.x,
                                                                  self.y_datum_label.y - scaling_utils.get_scaled_height(35)))
            else:
                if rotation == 'horizontal':
                    self.enable_input(self.r_input, scaling_utils.get_scaled_tuple((453, 311)))
                    self.enable_input(self.x_input, scaling_utils.get_scaled_tuple((33, 175)))
                    self.enable_input(self.y_input, scaling_utils.get_scaled_tuple((238, 327)))
                    self.place_widget(self.x_datum_label, scaling_utils.get_scaled_tuple((397, 55)))
                    self.place_widget(self.y_datum_label, scaling_utils.get_scaled_tuple((416, 114)))
                    self.place_widget(self.y_datum_validation_label, (self.y_datum_label.x,
                                                                      self.y_datum_label.y - scaling_utils.get_scaled_height(35)))
                else:
                    self.enable_input(self.r_input, scaling_utils.get_scaled_tuple((409, 333)))
                    self.enable_input(self.x_input, scaling_utils.get_scaled_tuple((78, 155)))
                    self.enable_input(self.y_input, scaling_utils.get_scaled_tuple((238, 331)))
                    self.place_widget(self.x_datum_label, scaling_utils.get_scaled_tuple((235, 20)))
                    self.place_widget(self.y_datum_label, scaling_utils.get_scaled_tuple((395, 63)))
                    self.place_widget(self.y_datum_validation_label, (self.y_datum_label.x,
                                                                      self.y_datum_label.y - scaling_utils.get_scaled_height(35)))
        else:
            self.disable_input(self.r_input)
            self.disable_input(self.x_input)
            self.disable_input(self.y_input)

        if shape == 'line':
            if rotation == 'horizontal':
                self.enable_input(self.l_input, scaling_utils.get_scaled_tuple((240, 228)))
                self.place_widget(self.x_datum_label, scaling_utils.get_scaled_tuple((414, 75)))
                self.place_widget(self.y_datum_label, scaling_utils.get_scaled_tuple((422, 195)))
                self.place_widget(self.y_datum_validation_label, (self.y_datum_label.x,
                                                                  self.y_datum_label.y - scaling_utils.get_scaled_height(35)))
            else:
                self.enable_input(self.l_input, scaling_utils.get_scaled_tuple((158, 173)))
                self.place_widget(self.x_datum_label, scaling_utils.get_scaled_tuple((275, 20)))
                self.place_widget(self.y_datum_label, scaling_utils.get_scaled_tuple((350, 70)))
                self.place_widget(self.y_datum_validation_label, (self.y_datum_label.x,
                                                                  self.y_datum_label.y - scaling_utils.get_scaled_height(20)))  # closer to Y_datum
        else:
            self.disable_input(self.l_input)

        if shape == 'geberit':
            if rotation == 'horizontal':
                self.place_widget(self.x_datum_label, scaling_utils.get_scaled_tuple((407, 46)))
                self.place_widget(self.y_datum_label, scaling_utils.get_scaled_tuple((416, 125)))
                self.place_widget(self.y_datum_validation_label, (self.y_datum_label.pos[0],
                                                                  self.y_datum_label.pos[1] - scaling_utils.get_scaled_height(35)))
            else:
                self.place_widget(self.x_datum_label, scaling_utils.get_scaled_tuple((360, 47)))
                self.place_widget(self.y_datum_label, scaling_utils.get_scaled_tuple((390, 94)))
                self.place_widget(self.y_datum_validation_label, (self.y_datum_label.pos[0],
                                                                  self.y_datum_label.pos[1] - scaling_utils.get_scaled_height(20)))

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

    def text_input_change(self, instance, *args):
        # On startup it seems to call this function and set everything to 0, so check that drywall app is open
        # Also check that the input matches a valid positive float, to allow user to correct mistakes
        if self.sm.current == 'drywall_cutter' and re.match(r'^\d*\.\d+$', instance.text):
            self.do_rectangle_checks()
            self.dwt_config.on_parameter_change('canvas_shape_dims.' + self.input_letter_dict[instance], float(instance.text or 0))

    def do_rectangle_checks(self):
        if not self.swapping_lengths:
            if self.rotation_required():
                self.sm.get_screen('drywall_cutter').rotate_shape(swap_lengths=False)
            if self.rectangle_with_equal_sides() and False: # DISABLE
                toolpath = self.sm.get_screen('drywall_cutter').cut_offset_selection.text
                self.sm.get_screen('drywall_cutter').shape_selection.text = 'square'
                self.sm.get_screen('drywall_cutter').cut_offset_selection.text = toolpath

    def rotation_required(self):
        if self.dwt_config.active_config.shape_type.lower() == "rectangle":
            if self.dwt_config.active_config.rotation == "vertical":
                return float(self.x_input.text or 0) < float(self.y_input.text or 0)
            else:
                return float(self.x_input.text or 0) > float(self.y_input.text or 0)
        else:
            return False
        
    def rectangle_with_equal_sides(self):
        if self.dwt_config.active_config.shape_type.lower() == "rectangle":
            if self.x_input.text and self.y_input.text:
                if float(self.x_input.text) == float(self.y_input.text):
                    return True
        return False

    def toggle_units(self, instance, value):
        instance.active = True
        # self.dwt_config.on_parameter_change('units', 'mm' if value else 'inch')

    def check_datum_and_extents(self):
        # All maths in this function from Ed, documented here https://docs.google.com/spreadsheets/d/1X37CWF8bsXeC0dY-HsbwBu_QR6N510V-5aPTnxwIR6I/edit#gid=677510108

        # DATUM/POSITION COORDINATES
        # Coordinates were originally the current datum position, m.[]_wco()
        # Now we've set them to be the live machine coordinates so that you can see coords update as you move the machine around
        # I've put both options here, so we can comment in/out as Ed & Az change their minds about what they want (:

        # x_coord = self.m.x_wco()
        # y_coord = self.m.y_wco()

        # x and y coord will be retrieved via event

        # REST OF THIS FUNCTION

        # Get current x/y values & shape clearances
        current_shape = self.dwt_config.active_config.shape_type.lower()
        current_x, current_y = self.cs.drywall_tec_position.get_x(), self.cs.drywall_tec_position.get_y()
        current_laser_x, current_laser_y = self.cs.drywall_tec_laser_position.get_x(), self.cs.drywall_tec_laser_position.get_y()

        tool_offset_value = self.tool_offset_value()
        x_min_clearance, y_min_clearance, x_max_clearance, y_max_clearance = self.get_x_y_clearances(current_shape, self.x_coord, self.y_coord, tool_offset_value)

        # Update canvas elements
        self.set_datum_position_label(current_laser_x, current_laser_y)
        self.update_bumpers_and_validation_labels(current_shape, current_laser_x, current_laser_y, x_min_clearance, y_min_clearance, x_max_clearance, y_max_clearance)

    # Check_datum_and_extents sub-functions below this comment:

    def get_current_x_y(self, x_coord, y_coord, revert=False):
        """
        converts machine_coordinates to and from dwt_coordinates
        revert=False => machine -> dwt (for labels and configuration files)
        revert=True => dwt -> machine (for set_datum())
        """
        offset_x = round(self.m.get_dollar_setting(130)
                          - self.m.limit_switch_safety_distance
                          - self.m.laser_offset_tool_clearance_to_access_edge_of_sheet, 2)
        offset_y = round(self.m.get_dollar_setting(131) - self.m.get_dollar_setting(27), 2)
        if revert:
            current_x = x_coord - offset_x
            current_y = y_coord - offset_y
        else:
            current_x = x_coord + offset_x
            current_y = y_coord + offset_y
        return current_x, current_y

    def set_datum_position_label(self, current_x, current_y):
        self.x_datum_label.text = 'X: ' + str(round(current_x, 1))
        self.y_datum_label.text = 'Y: ' + str(round(current_y, 1))

    def tool_offset_value(self):
        # Account for cutter size
        cutter_radius = (self.dwt_config.active_cutter.dimensions.diameter or 0) / 2  # if angled cutter, get 0
        if self.dwt_config.active_config.toolpath_offset == ToolpathOffsetOptions.INSIDE.value:
            tool_offset_value = -cutter_radius
        elif self.dwt_config.active_config.toolpath_offset == ToolpathOffsetOptions.OUTSIDE.value:
            tool_offset_value = cutter_radius
        else:
            tool_offset_value = 0

        return tool_offset_value

    def get_x_y_clearances(self, current_shape, x_coord, y_coord, tool_offset_value):
        # Calculate shape's extent from datum using shape type and input dimensions
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
            if "horizontal" in self.dwt_config.active_config.rotation:
                x_dim = 0
                y_dim = float(self.l_input.text or 0)
            else:
                x_dim = float(self.l_input.text or 0)
                y_dim = 0
        elif current_shape == 'geberit':
            x_dim, y_dim, x_min, y_min = self.engine.get_custom_shape_extents()

        # Calculate shape's distances from every edge
        x_min_clearance = x_coord + x_min + self.m.get_dollar_setting(130) - self.m.limit_switch_safety_distance
        y_min_clearance = y_coord + y_min + self.m.get_dollar_setting(131) - self.m.limit_switch_safety_distance
        x_max_clearance = -(x_coord + x_dim) - self.m.limit_switch_safety_distance
        y_max_clearance = -(y_coord + y_dim) - self.m.limit_switch_safety_distance

        return x_min_clearance, y_min_clearance, x_max_clearance, y_max_clearance

    def update_bumpers_and_validation_labels(self, current_shape, current_x, current_y,
                                            x_min_clearance, y_min_clearance, x_max_clearance, y_max_clearance):
        # I think this function could be broken down & refactored as well, but I don't need to address it right now.

        self.x_datum_validation_label.opacity = 0
        self.y_datum_validation_label.opacity = 0

        # Set bumper colours based on whether anything crosses a boundary, and show validation labels
        if x_min_clearance < 0:
            self.bumper_bottom_image.source = "./asmcnc/apps/drywall_cutter_app/img/bumper_bottom_red.png"
            x_datum_min = round(abs(x_min_clearance) + current_x, 2)
            if self.X_MIN < x_datum_min < self.X_MAX:
                self.x_datum_validation_label.text = 'MIN: ' + str(x_datum_min)
                self.x_datum_validation_label.opacity = 1
        else:
            self.bumper_bottom_image.source = "./asmcnc/apps/drywall_cutter_app/img/bumper_bottom_green.png"

        if y_min_clearance < 0:
            self.bumper_right_image.source = "./asmcnc/apps/drywall_cutter_app/img/bumper_right_red.png"
            y_datum_min = round(abs(y_min_clearance) + current_y, 2)
            if self.Y_MIN < y_datum_min < self.Y_MAX:
                self.y_datum_validation_label.text = 'MIN: ' + str(y_datum_min)
                self.y_datum_validation_label.opacity = 1
        else:
            self.bumper_right_image.source = "./asmcnc/apps/drywall_cutter_app/img/bumper_right_green.png"

        if x_max_clearance < 0:
            self.bumper_top_image.source = "./asmcnc/apps/drywall_cutter_app/img/bumper_top_red.png"
            x_datum_max = round(current_x - abs(x_max_clearance), 2)
            if self.X_MIN < x_datum_max < self.X_MAX:
                self.x_datum_validation_label.text = 'MAX: ' + str(x_datum_max)
                self.x_datum_validation_label.opacity = 1
        else:
            self.bumper_top_image.source = "./asmcnc/apps/drywall_cutter_app/img/bumper_top_green.png"

        if y_max_clearance < 0:
            self.bumper_left_image.source = "./asmcnc/apps/drywall_cutter_app/img/bumper_left_red.png"
            y_datum_max = round(current_y - abs(y_max_clearance), 2)
            if self.Y_MIN < y_datum_max < self.Y_MAX:
                self.y_datum_validation_label.text = 'MAX: ' + str(y_datum_max)
                self.y_datum_validation_label.opacity = 1
        else:
            self.bumper_left_image.source = "./asmcnc/apps/drywall_cutter_app/img/bumper_left_green.png"

       # Now show a message if any dimensions are too big
        d_limit = self.X_MAX
        if current_shape == 'circle' and float(self.d_input.text or 0) > d_limit:
            self.d_input_validation_label.text = 'MAX: ' + str(d_limit)
            self.d_input_validation_label.opacity = 1
        else:
            self.d_input_validation_label.opacity = 0

        if current_shape in ['square', 'rectangle']:
            x_limit = self.X_MAX
            y_limit = self.Y_MAX
            dims = self.dwt_config.active_config.canvas_shape_dims

            if current_shape == 'square':
                self.x_input_validation_label.opacity = 0
                # Because square is limited by the smaller dimension
                square_limit = min(x_limit, y_limit)
                r_limit = dims.y / 2
                if float(self.y_input.text or 0) > square_limit:
                    self.y_input_validation_label.text = 'MAX: ' + str(square_limit)
                    self.y_input_validation_label.opacity = 1
                else:
                    self.y_input_validation_label.opacity = 0
            else:
                r_limit = min(dims.x, dims.y) / 2
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
            if "horizontal" in self.dwt_config.active_config.rotation:
                if float(self.l_input.text or 0) > self.Y_MAX:
                    self.l_input_validation_label.text = 'MAX: ' + str(self.Y_MAX)
                    self.l_input_validation_label.opacity = 1
                else:
                    self.l_input_validation_label.opacity = 0
            else:
                if float(self.l_input.text or 0) > self.X_MAX:
                    self.l_input_validation_label.text = 'MAX: ' + str(self.X_MAX)
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
            if self.dwt_config.active_config.toolpath_offset.lower() == "inside":
                return float(self.d_input.text or 0) >= 0.1 + self.dwt_config.active_cutter.dimensions.diameter
            else:
                return float(self.d_input.text or 0) >= 0.1

        elif self.dwt_config.active_config.shape_type.lower() == "square":
            if self.dwt_config.active_config.toolpath_offset.lower() == "inside":
                return float(self.y_input.text or 0) >= 0.1 + self.dwt_config.active_cutter.dimensions.diameter
            elif self.dwt_config.active_config.toolpath_offset.lower() == "outside":
                return float(self.y_input.text or 0) >= 1
            else:
                return float(self.y_input.text or 0) >= 0.1

        elif self.dwt_config.active_config.shape_type.lower() == "rectangle":
            if self.dwt_config.active_config.toolpath_offset.lower() == "inside":
                return (float(self.x_input.text or 0) >= 0.1 + self.dwt_config.active_cutter.dimensions.diameter) and (
                            float(self.y_input.text or 0) >= 0.1 + self.dwt_config.active_cutter.dimensions.diameter)
            elif self.dwt_config.active_config.toolpath_offset.lower() == "outside":
                return (float(self.x_input.text or 0) >= 1) and (float(self.y_input.text or 0) >= 1)
            else:
                return (float(self.x_input.text or 0) >= 0.1) and (float(self.y_input.text or 0) >= 0.1)

        elif self.dwt_config.active_config.shape_type.lower() == "line":
            return float(self.l_input.text or 0) >= 0.1

        else:
            return True

    def get_steps_to_validate(self):
        steps = []

        x_min_clearance, y_min_clearance, x_max_clearance, y_max_clearance = self.get_x_y_clearances(
            self.dwt_config.active_config.shape_type.lower(), self.x_coord, self.y_coord, self.tool_offset_value())

        if not self.x_input.disabled and float(self.x_input.text or 0) > self.X_MAX:
            steps.append(
                self.localization.get_str(
                    "Your N input is too large."
                ).replace("N", "X")
                + "\n\n"
                + self.localization.get_bold(
                    "Try reducing the 'N' input."
                ).replace("N", "X")
                + "\n\n"
            )

        if not self.y_input.disabled and float(self.y_input.text or 0) > self.Y_MAX:
            steps.append(
                self.localization.get_str(
                    "Your N input is too large."
                ).replace("N", "Y")
                + "\n\n"
                + self.localization.get_bold(
                    "Try reducing the 'N' input."
                ).replace("N", "Y")
                + "\n\n"
            )

        if x_min_clearance < 0:
            steps.append(
                self.localization.get_str(
                    "The job extent over-reaches the N axis at the home end."
                ).replace("N", "X")
                + "\n\n"
                + self.localization.get_bold(
                    "Try positioning the machine's N datum further away from home."
                ).replace("N", "X")
                + "\n\n"
            )

        if y_min_clearance < 0:
            steps.append(
                self.localization.get_str(
                    "The job extent over-reaches the N axis at the home end."
                ).replace("N", "Y")
                + "\n\n"
                + self.localization.get_bold(
                    "Try positioning the machine's N datum further away from home."
                ).replace("N", "Y")
                + "\n\n"
            )

        if x_max_clearance < 0:
            steps.append(
                self.localization.get_str(
                    "The job extent over-reaches the N axis at the far end."
                ).replace("N", "X")
                + "\n\n"
                + self.localization.get_bold(
                    "Try positioning the machine's N datum closer to home."
                ).replace("N", "X")
                + "\n\n"
            )

        if y_max_clearance < 0:
            steps.append(
                self.localization.get_str(
                    "The job extent over-reaches the N axis at the far end."
                ).replace("N", "Y")
                + "\n\n"
                + self.localization.get_bold(
                    "Try positioning the machine's N datum closer to home."
                ).replace("N", "Y")
                + "\n\n"
            )

        if self.dwt_config.active_config.shape_type.lower() == "square":
            # ensure roundness not too large
            if float(self.r_input.text or 0) > float(self.y_input.text or 0) / 2:
                steps.append(
                    self.localization.get_str(
                        "The radius value is too large."
                    )
                    + "\n\n"
                    + self.localization.get_bold(
                        "Try reducing the 'R' input."
                    )
                    + "\n\n"
                )

            # ensure the square is not too small
            if self.dwt_config.active_config.toolpath_offset.lower() == "inside":
                if float(self.y_input.text or 0) <= 0.1 + self.dwt_config.active_cutter.dimensions.diameter:
                    steps.append(
                        self.localization.get_str(
                            "The square is too small."
                        )
                        + "\n\n"
                        + self.localization.get_bold(
                            "Try increasing the 'Y' input."
                        )
                        + "\n\n"
                    )
            elif self.dwt_config.active_config.toolpath_offset.lower() == "outside":
                if float(self.y_input.text or 0) <= 1:
                    steps.append(
                        self.localization.get_str(
                            "The square is too small."
                        )
                        + "\n\n"
                        + self.localization.get_bold(
                            "Try increasing the 'Y' input."
                        )
                        + "\n\n"
                    )
            else:
                if float(self.y_input.text or 0) <= 0.1:
                    steps.append(
                        self.localization.get_str(
                            "The square is too small."
                        )
                        + "\n\n"
                        + self.localization.get_bold(
                            "Try increasing the 'Y' input."
                        )
                        + "\n\n"
                    )
        elif self.dwt_config.active_config.shape_type.lower() == "rectangle":
            if float(self.r_input.text or 0) > (min(float(self.x_input.text or 0), float(self.y_input.text or 0)) / 2):
                steps.append(
                    self.localization.get_str(
                        "The radius value is too large."
                    )
                    + "\n\n"
                    + self.localization.get_bold(
                        "Try reducing the 'R' input."
                    )
                    + "\n\n"
                )

            if self.dwt_config.active_config.toolpath_offset.lower() == "inside":
                if (float(self.x_input.text or 0) <= 0.1 + self.dwt_config.active_cutter.dimensions.diameter) or (
                        float(self.y_input.text or 0) <= 0.1 + self.dwt_config.active_cutter.dimensions.diameter):
                    steps.append(
                        self.localization.get_str(
                            "The rectangle's sides are too small."
                        )
                        + "\n\n"
                        + self.localization.get_bold(
                            "Try increasing the 'X' and 'Y' inputs."
                        )
                        + "\n\n"
                    )
            elif self.dwt_config.active_config.toolpath_offset.lower() == "outside":
                if (float(self.x_input.text or 0) <= 1) or (float(self.y_input.text or 0) <= 1):
                    steps.append(
                        self.localization.get_str(
                            "The rectangle's sides are too small."
                        )
                        + "\n\n"
                        + self.localization.get_bold(
                            "Try increasing the 'X' and 'Y' inputs."
                        )
                        + "\n\n"
                    )
            else:
                if (float(self.x_input.text or 0) <= 0.1) or (float(self.y_input.text or 0) <= 0.1):
                    steps.append(
                        self.localization.get_str(
                            "The rectangle's sides are too small."
                        )
                        + "\n\n"
                        + self.localization.get_bold(
                            "Try increasing the 'X' and 'Y' inputs."
                        )
                        + "\n\n"
                    )
        elif self.dwt_config.active_config.shape_type.lower() == "circle":
            if self.dwt_config.active_config.toolpath_offset.lower() == "inside":
                if float(self.d_input.text or 0) <= 0.1 + self.dwt_config.active_cutter.dimensions.diameter:
                    steps.append(
                        self.localization.get_str(
                            "The circle's diameter is too small."
                        )
                        + "\n\n"
                        + self.localization.get_bold(
                            "Try increasing the 'D' input."
                        )
                        + "\n\n"
                    )
            else:
                if float(self.d_input.text or 0) <= 0.1:
                    steps.append(
                        self.localization.get_str(
                            "The circle's diameter is too small."
                        )
                        + "\n\n"
                        + self.localization.get_bold(
                            "Try increasing the 'D' input."
                        )
                        + "\n\n"
                    )
        elif self.dwt_config.active_config.shape_type.lower() == "line":
            if float(self.l_input.text or 0) <= 0.1:
                steps.append(
                    self.localization.get_str(
                        "The line is too small."
                    )
                    + "\n\n"
                    + self.localization.get_bold(
                        "Try increasing the 'L' input."
                    )
                    + "\n\n"

                )

        return steps

    def on_config_name_change(self, instance, value):
        Logger.debug("Setting config label to: " + value)
        self.config_name_label.text = "New Configuration" if value == "temp_config.json" else value
