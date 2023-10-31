from kivy.lang import Builder
from kivy.uix.widget import Widget

Builder.load_string("""
<DrywallShapeDisplay>

    shape_dims_image:shape_dims_image

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
                id: shape_dims_image
                opacity: 0
                size: self.parent.size
                pos: self.parent.pos

""")


class DrywallShapeDisplay(Widget):

    image_filepath = "./asmcnc/apps/drywall_cutter_app/img/"

    dims_image_filepath_dict = {
        "Circle":image_filepath + "circle_dims.png",
        "Square":image_filepath + "square_dims.png",
        "Rectangle":image_filepath + "rectangle_horizontal_dims.png",
        "Line":image_filepath + "line_horizontal_dims.png",
        "Geberit":image_filepath + "geberit_vertical_dims.png"
    }

    def __init__(self, **kwargs):
        super(DrywallShapeDisplay, self).__init__(**kwargs)

    def select_shape(self, shape):
        self.shape_dims_image.source = self.dims_image_filepath_dict[shape]
        self.shape_dims_image.opacity = 1
