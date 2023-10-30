from kivy.lang import Builder
from kivy.uix.widget import Widget

Builder.load_string("""
<DrywallShapeDisplay>

    BoxLayout:
        size: self.parent.size
        pos: self.parent.pos

        Image:
            source: "./asmcnc/apps/drywall_cutter_app/img/canvas_with_logo.png"
            center_x: self.parent.center_x
            y: self.parent.y
            size: self.parent.width, self.parent.height
            allow_stretch: True

""")


class DrywallShapeDisplay(Widget):

    shape_image_filepath_dict = {

    }

    def __init__(self, **kwargs):
        super(DrywallShapeDisplay, self).__init__(**kwargs)

    def select_shape(self, shape):
        print(shape)
