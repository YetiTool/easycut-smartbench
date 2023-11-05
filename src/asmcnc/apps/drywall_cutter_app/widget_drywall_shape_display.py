from kivy.lang import Builder
from kivy.uix.widget import Widget

Builder.load_string("""
<DrywallShapeDisplay>

    shape_dims_image:shape_dims_image
    shape_toolpath_image:shape_toolpath_image

    d_input:d_input

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

""")


class DrywallShapeDisplay(Widget):

    image_filepath = "./asmcnc/apps/drywall_cutter_app/img/"

    def __init__(self, **kwargs):
        super(DrywallShapeDisplay, self).__init__(**kwargs)

        self.dwt_config = kwargs['dwt_config']

        self.d_input.bind(text = self.update_d)

    def select_shape(self, shape, rotation):
        image_source = self.image_filepath + shape
        if shape in ['rectangle', 'line']:
            image_source += "_" + rotation
        self.shape_dims_image.source = image_source + "_dims.png"

        self.shape_dims_image.opacity = 1

        if shape == 'circle':
            self.d_input.disabled = False
            self.d_input.opacity = 1
            self.d_input.parent.opacity = 1
            self.d_input.parent.pos = (470, 310)
        else:
            self.d_input.disabled = True
            self.d_input.opacity = 0
            self.d_input.parent.opacity = 0


        if shape == 'square':
            pass
        elif shape == 'rectangle':
            pass
        elif shape == 'line':
            pass
        elif shape == 'geberit':
            pass

    def select_toolpath(self, shape, toolpath, rotation):
        if shape in ['line', 'geberit']:
            self.shape_toolpath_image.opacity = 0
        else:
            if shape == 'rectangle':
                self.shape_toolpath_image.source = self.image_filepath + shape + "_" + rotation + "_" + toolpath + "_toolpath.png"
            else:
                self.shape_toolpath_image.source = self.image_filepath + shape + "_" + toolpath + "_toolpath.png"
            self.shape_toolpath_image.opacity = 1

    def update_d(self, instance, value):
        self.dwt_config.on_parameter_change('canvas_shape_dims.d', float(value or 0))
