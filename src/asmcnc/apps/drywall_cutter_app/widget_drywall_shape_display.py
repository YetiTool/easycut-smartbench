from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.clock import Clock
from asmcnc.core_UI.components import FloatInput  # Required for the builder string
import re

Builder.load_string("""
<DrywallShapeDisplay>

    shape_dims_image:shape_dims_image
    shape_toolpath_image:shape_toolpath_image

    unit_switch:unit_switch

    d_input:d_input
    l_input:l_input
    r_input:r_input
    x_input:x_input
    y_input:y_input
    x_datum_label:x_datum_label
    y_datum_label:y_datum_label

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

            Switch:
                id: unit_switch
                size: dp(83), dp(32)
                size_hint: (None, None)
                pos: self.parent.pos[0] + self.parent.size[0] - self.size[0] - dp(3), self.parent.pos[1] + dp(3)

            BoxLayout:
                size: dp(70), dp(40)
                size_hint: (None, None)

                canvas.before:
                    Color:
                        rgba: hex('#E5E5E5FF')
                    Rectangle:
                        pos: self.x + 5, self.y + 5
                        size: self.width - 10, self.height - 10

                FloatInput:
                    id: d_input
                    font_size: dp(25)
                    halign: 'center'
                    multiline: False
                    size: self.parent.size
                    pos: self.parent.pos
                    background_color: (0,0,0,0)

            Label:
                text: 'D'
                font_size: dp(25)
                pos: d_input.pos[0] - self.width, d_input.pos[1] + dp(3)
                opacity: d_input.opacity
                color: 0,0,0,1
                size: self.texture_size
                size_hint: (None, None)

            BoxLayout:
                size: dp(70), dp(40)
                size_hint: (None, None)

                canvas.before:
                    Color:
                        rgba: hex('#E5E5E5FF')
                    Rectangle:
                        pos: self.x + 5, self.y + 5
                        size: self.width - 10, self.height - 10

                FloatInput:
                    id: l_input
                    font_size: dp(25)
                    halign: 'center'
                    multiline: False
                    size: self.parent.size
                    pos: self.parent.pos
                    background_color: (0,0,0,0)

            Label:
                text: 'L'
                font_size: dp(25)
                pos: l_input.pos[0] - self.width, l_input.pos[1] + dp(3)
                opacity: l_input.opacity
                color: 0,0,0,1
                size: self.texture_size
                size_hint: (None, None)

            BoxLayout:
                size: dp(70), dp(40)
                size_hint: (None, None)

                canvas.before:
                    Color:
                        rgba: hex('#E5E5E5FF')
                    Rectangle:
                        pos: self.x + 5, self.y + 5
                        size: self.width - 10, self.height - 10

                FloatInput:
                    id: r_input
                    font_size: dp(25)
                    halign: 'center'
                    multiline: False
                    size: self.parent.size
                    pos: self.parent.pos
                    background_color: (0,0,0,0)

            Label:
                text: 'R'
                font_size: dp(25)
                pos: r_input.pos[0] - self.width, r_input.pos[1] + dp(3)
                opacity: r_input.opacity
                color: 0,0,0,1
                size: self.texture_size
                size_hint: (None, None)

            BoxLayout:
                size: dp(70), dp(40)
                size_hint: (None, None)

                canvas.before:
                    Color:
                        rgba: hex('#E5E5E5FF')
                    Rectangle:
                        pos: self.x + 5, self.y + 5
                        size: self.width - 10, self.height - 10

                FloatInput:
                    id: x_input
                    font_size: dp(25)
                    halign: 'center'
                    multiline: False
                    size: self.parent.size
                    pos: self.parent.pos
                    background_color: (0,0,0,0)

            Label:
                text: 'X'
                font_size: dp(25)
                pos: x_input.pos[0] - self.width, x_input.pos[1] + dp(3)
                opacity: x_input.opacity
                color: 0,0,0,1
                size: self.texture_size
                size_hint: (None, None)

            BoxLayout:
                size: dp(70), dp(40)
                size_hint: (None, None)

                canvas.before:
                    Color:
                        rgba: hex('#E5E5E5FF')
                    Rectangle:
                        pos: self.x + 5, self.y + 5
                        size: self.width - 10, self.height - 10

                FloatInput:
                    id: y_input
                    font_size: dp(25)
                    halign: 'center'
                    multiline: False
                    size: self.parent.size
                    pos: self.parent.pos
                    background_color: (0,0,0,0)

            Label:
                text: 'Y'
                font_size: dp(25)
                pos: y_input.pos[0] - self.width, y_input.pos[1] + dp(3)
                opacity: y_input.opacity
                color: 0,0,0,1
                size: self.texture_size
                size_hint: (None, None)

            Label:
                id: x_datum_label
                font_size: dp(25)
                size: dp(150), dp(40)
                size_hint: (None, None)
                text: 'X:'
                color: 0,0,0,1
                halign: 'left'

                canvas.before:
                    Color:
                        rgba: hex('#F9F9F988')
                    Rectangle:
                        pos: self.x + 15, self.y + 5
                        size: self.texture_size

            Label:
                id: y_datum_label
                font_size: dp(25)
                size: dp(150), dp(40)
                size_hint: (None, None)
                text: 'Y:'
                color: 0,0,0,1

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

            Label:
                id: machine_state_label
                font_size: dp(20)
                size: self.texture_size[0], dp(40)
                size_hint: (None, None)
                pos: self.parent.pos[0] + self.parent.size[0] - self.texture_size[0] - dp(5), self.parent.size[1] - self.height + dp(10)
                text: 'Test'
                color: 0,0,0,1

""")


class DrywallShapeDisplay(Widget):

    image_filepath = "./asmcnc/apps/drywall_cutter_app/img/"

    swapping_lengths = False

    def __init__(self, **kwargs):
        super(DrywallShapeDisplay, self).__init__(**kwargs)

        self.m = kwargs['machine']
        self.sm = kwargs['screen_manager']
        self.dwt_config = kwargs['dwt_config']
        self.kb = kwargs['kb']

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

        self.m.s.bind(m_state=self.display_machine_state)

        Clock.schedule_interval(self.poll_position, 0.1)

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

    def poll_position(self, dt):
        # Maths from Ed, documented here https://docs.google.com/spreadsheets/d/1X37CWF8bsXeC0dY-HsbwBu_QR6N510V-5aPTnxwIR6I/edit#gid=677510108
        current_x = round(self.m.x_wco() + (self.m.get_dollar_setting(130) - self.m.limit_switch_safety_distance) - self.m.laser_offset_tool_clearance_to_access_edge_of_sheet, 2)
        current_y = round(self.m.y_wco() + (self.m.get_dollar_setting(131) - self.m.limit_switch_safety_distance) - (self.m.get_dollar_setting(27) - self.m.limit_switch_safety_distance), 2)
        self.x_datum_label.text = 'X: ' + str(current_x)
        self.y_datum_label.text = 'Y: ' + str(current_y)

    def display_machine_state(self, obj, value):
        self.machine_state_label.text = value
