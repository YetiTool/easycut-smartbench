from kivy.lang import Builder
from kivy.uix.widget import Widget

Builder.load_string("""
<DrywallShapeDisplay>

    shape_dims_image:shape_dims_image
    shape_toolpath_image:shape_toolpath_image

    d_input:d_input
    l_input:l_input
    r_input:r_input
    x_input:x_input
    y_input:y_input
    x_datum_input:x_datum_input
    y_datum_input:y_datum_input

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
                    id: x_datum_input
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
                    id: y_datum_input
                    font_size: dp(25)
                    halign: 'center'
                    input_filter: 'int'
                    multiline: False
                    size: self.parent.size
                    pos: self.parent.pos
                    background_color: (0,0,0,0)

""")


class DrywallShapeDisplay(Widget):

    image_filepath = "./asmcnc/apps/drywall_cutter_app/img/"

    def __init__(self, **kwargs):
        super(DrywallShapeDisplay, self).__init__(**kwargs)

        self.dwt_config = kwargs['dwt_config']

        self.d_input.bind(text=self.d_input_change)
        self.l_input.bind(text=self.l_input_change)
        self.r_input.bind(text=self.r_input_change)
        self.x_input.bind(text=self.x_input_change)
        self.y_input.bind(text=self.y_input_change)
        self.x_datum_input.bind(text=self.x_datum_input_change)
        self.y_datum_input.bind(text=self.y_datum_input_change)

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
            self.enable_input(self.x_datum_input, (278, 27))
            self.enable_input(self.y_datum_input, (438, 196))
        else:
            self.disable_input(self.d_input)

        if shape in ['square', 'rectangle']:
            if shape == 'square':
                self.enable_input(self.r_input, (421, 311))
                self.enable_input(self.x_input, (86, 175))
                self.enable_input(self.y_input, (248, 327))
                self.enable_input(self.x_datum_input, (365, 35))
                self.enable_input(self.y_datum_input, (433, 113))
            else:
                if rotation == 'horizontal':
                    self.enable_input(self.r_input, (463, 311))
                    self.enable_input(self.x_input, (43, 175))
                    self.enable_input(self.y_input, (248, 327))
                    self.enable_input(self.x_datum_input, (407, 35))
                    self.enable_input(self.y_datum_input, (451, 114))
                else:
                    self.enable_input(self.r_input, (419, 333))
                    self.enable_input(self.x_input, (98, 155))
                    self.enable_input(self.y_input, (248, 331))
                    self.enable_input(self.x_datum_input, (367, 10))
                    self.enable_input(self.y_datum_input, (430, 63))
        else:
            self.disable_input(self.r_input)
            self.disable_input(self.x_input)
            self.disable_input(self.y_input)

        if shape == 'line':
            if rotation == 'horizontal':
                self.enable_input(self.l_input, (250, 228))
                self.enable_input(self.x_datum_input, (424, 75))
                self.enable_input(self.y_datum_input, (460, 195))
            else:
                self.enable_input(self.l_input, (178, 173))
                self.enable_input(self.x_datum_input, (281, 3))
                self.enable_input(self.y_datum_input, (385, 56))
        else:
            self.disable_input(self.l_input)

        if shape == 'geberit':
            self.enable_input(self.x_datum_input, (360, 19))
            self.enable_input(self.y_datum_input, (425, 77))

    def enable_input(self, text_input, pos):
        text_input.disabled = False
        text_input.opacity = 1
        text_input.parent.opacity = 1
        text_input.parent.pos = pos

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
        self.dwt_config.on_parameter_change('canvas_shape_dims.x', float(value or 0))

    def y_input_change(self, instance, value):
        self.dwt_config.on_parameter_change('canvas_shape_dims.y', float(value or 0))

    def x_datum_input_change(self, instance, value):
        self.dwt_config.on_parameter_change('datum_position.x', float(value or 0))

    def y_datum_input_change(self, instance, value):
        self.dwt_config.on_parameter_change('datum_position.y', float(value or 0))
