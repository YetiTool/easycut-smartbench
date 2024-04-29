from collections import OrderedDict

from kivy.metrics import dp
from kivy.properties import DictProperty, ObjectProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image
from asmcnc.comms.logging_system.logging_system import Logger


"""
This is a custom widget that is used to create a dropdown menu with images.

The images are loaded from a dictionary that is passed to the widget.

The image_dict parameter should have the following format:
{
    'key': {
        'image_path': 'path/to/image.png',
        'other_key_where_required': 'value',
    }, ...
}

The callback parameter should be a function that you want to be called when an image is pressed.

The key_name parameter should be the name of the key that you want to be passed to the callback function. 
Pass 'key' if you want the key to be passed.
"""


class ImageButton(ButtonBehavior, Image):
    pass


class ImageDropDown(DropDown):
    def __init__(self, image_dict, callback, key_name, **kwargs):
        super(ImageDropDown, self).__init__(**kwargs)

        try:
            sorted_cutter_list = sorted(image_dict.items(), key=lambda x: (x[1]['type'], x[1]['size']))
            image_dict = OrderedDict(sorted_cutter_list)
        except KeyError:  # working through the wrong dict...wait for the next one
            pass
        for key in image_dict.keys():
            image = ImageButton(
                source=image_dict[key]['image_path'],
                allow_stretch=True,
                size_hint_y=None,
                height=dp(75),
            )

            image.bind(on_release=self.dismiss)

            if key_name == 'key':
                image.bind(on_press=lambda x, k=key: callback(k))
            else:
                # https://stackoverflow.com/questions/2295290/what-do-lambda-function-closures-capture
                image.bind(on_press=lambda x, k=key: callback(image_dict[k][key_name]))

            self.add_widget(image)


class ImageDropDownButton(ButtonBehavior, Image):
    image_dict = DictProperty({})
    callback = ObjectProperty(None)
    key_name = StringProperty('')
    dropdown = None

    def __init__(self, **kwargs):
        super(ImageDropDownButton, self).__init__(**kwargs)

        self.bind(image_dict=self.on_property)
        self.bind(callback=self.on_property)
        self.bind(key_name=self.on_property)

    def on_property(self, *args):
        # this is needed because the properties are set in the kv file, and they don't always get set at the same time
        # idk how to do it better @Lettie any ideas?
        if self.callback == ObjectProperty(None) or self.key_name == StringProperty(
                '') or self.image_dict == DictProperty({}):
            return

        self.dropdown = ImageDropDown(self.image_dict, self.callback, self.key_name)

    def on_release(self):
        self.dropdown.open(self)


class ToolSelectionDropDown(ImageDropDownButton):
    """
    This class is a custom widget that is used to create a dropdown menu with images of tools.
    By default, it's setup for the Drywall Cutter App, but it can be used for other apps as well.
    Use setter methods to set up for other apps.
    """
    def __init__(self, **kwargs):
        super(ToolSelectionDropDown, self).__init__(**kwargs)
        self.key_name = 'cutter_path'
        self.current_shape = None
        self.config = None

        # Setting defaults for the Drywall Cutter App
        self.source = './asmcnc/apps/drywall_cutter_app/config/cutters/images/tool_6mm.png'
        self.shape_cutter_filter = dict(
            # shape=[allowed cutters]
            # e.g. geberit=[8, 6]
            # e.g. circle=[] # all cutters allowed
            circle=[],
            square=[],
            line=[],
            geberit=[8, 6]
        )
        self.tool_list = {
            'Drywalltec  \xc3\xb8 -  60\xc2\xb0 2 flute V-groove  L19': {
                'cutter_path': 'tool_60deg.json',
                'type': 'V-groove',
                'image_path': './asmcnc/apps/drywall_cutter_app/config/cutters/images/tool_60deg.png',
                'size': 60
            },
            'Drywalltec  \xc3\xb8 -  45\xc2\xb0 2 flute V-groove  L19': {
                'cutter_path': 'tool_45deg.json',
                'type': 'V-groove',
                'image_path': './asmcnc/apps/drywall_cutter_app/config/cutters/images/tool_45deg.png',
                'size': 45
            },
            'Drywalltec  \xc3\xb8 6 mm 2 flute End mill Upcut L13': {
                'cutter_path': 'tool_6mm.json',
                'type': 'End mill upcut',
                'image_path': './asmcnc/apps/drywall_cutter_app/config/cutters/images/tool_6mm.png',
                'size': 6
            },
            'Drywalltec  \xc3\xb8 -  90\xc2\xb0 2 flute V-groove  L19': {
                'cutter_path': 'tool_90deg.json',
                'type': 'V-groove',
                'image_path': './asmcnc/apps/drywall_cutter_app/config/cutters/images/tool_90deg.png',
                'size': 90
            },
            'Drywalltec  \xc3\xb8 8 mm 2 flute End mill Upcut L26': {
                'cutter_path': 'tool_8mm.json',
                'type': 'End mill upcut',
                'image_path': './asmcnc/apps/drywall_cutter_app/config/cutters/images/tool_8mm.png',
                'size': 8
            }
        }

        self.restore_image_dict()  # populate the image_dict with all tools

    def set_cutter_filter(self, shape_cutter_filter):
        # method to set the cutter filter for each shape. Use this method for instances other than DWT
        # shape_cutter_filter should be a dictionary with the same format as self.shape_cutter_filter in the constructor
        try:
            self.shape_cutter_filter = shape_cutter_filter
        except KeyError:
            Logger.error('Shape cutter filter not in correct format. Unable to set cutter filter. Using default cutter filter.')

    def set_tool_list(self, tool_list):
        # method to set the tool list. Use this method for instances other than DWT
        # tool_list should be a dictionary with the same format as self.tool_list in the constructor
        try:
            self.tool_list = tool_list
        except KeyError:
            Logger.error('Tool list not in correct format. Unable to set tool list. Using default tool list.')

    def set_default_image(self, default_image_path):
        # method to set the default image. Use this method for instances other than DWT
        # default_image_path should be a string with the path to the default image
        self.source = default_image_path

    def set_current_shape(self, shape):
        # method to set the current shape in this class, so that the tool selection can be filtered
        # shape should be a string with the name of the shape
        self.current_shape = shape
        self.filter_available_tools()

        # if current tool is not available for the new shape, set to first available tool
        if self.config.active_config.cutter_type not in self.image_dict:
            self.config.active_config.cutter_type = list(self.image_dict.keys())[0]
            Logger.warning('Current tool not available for shape. Setting to first available tool.')

    def get_tool_list(self):
        return self.tool_list

    def get_cutter_filter(self):
        return self.shape_cutter_filter

    def restore_image_dict(self):
        self.image_dict = self.get_tool_list()

    def filter_available_tools(self):
        # method to filter the available tools based on the current shape
        if self.current_shape not in self.get_cutter_filter():
            Logger.error('Shape {} not defined in cutter_filter. Unable to filter tool selection'.format(self.current_shape))
            return

        self.restore_image_dict()  # get all tools back

        for key in self.image_dict.keys():
            # remove tools that are not in the shape's allowed cutters
            if (self.image_dict[key]['size'] not in self.shape_cutter_filter[self.current_shape] and
                    self.shape_cutter_filter[self.current_shape] != []):
                del self.image_dict[key]


class ShapeSelectionDropDown(ImageDropDownButton):
    def __init__(self, **kwargs):
        super(ShapeSelectionDropDown, self).__init__(**kwargs)
        self.source = './asmcnc/apps/drywall_cutter_app/img/square_shape_button.png'
        self.key_name = 'key'
        self.image_dict = dict(
            circle={
                'image_path': './asmcnc/apps/drywall_cutter_app/img/circle_shape_button.png',
            }, square={
                'image_path': './asmcnc/apps/drywall_cutter_app/img/square_shape_button.png',
            }, line={
                'image_path': './asmcnc/apps/drywall_cutter_app/img/line_shape_button.png',
            }, geberit={
                'image_path': './asmcnc/apps/drywall_cutter_app/img/geberit_shape_button.png',
            }, rectangle={
                'image_path': './asmcnc/apps/drywall_cutter_app/img/rectangle_shape_button.png',
            })


class ToolPathSelectionDropDown(ImageDropDownButton):
    def __init__(self, **kwargs):
        super(ToolPathSelectionDropDown, self).__init__(**kwargs)
        self.source = './asmcnc/apps/drywall_cutter_app/img/toolpath_offset_inside_button.png'
        self.key_name = 'key'
        self.image_dict = dict(
            inside={
                'image_path': './asmcnc/apps/drywall_cutter_app/img/toolpath_offset_inside_button.png',
            }, outside={
                'image_path': './asmcnc/apps/drywall_cutter_app/img/toolpath_offset_outside_button.png',
            }, on={
                'image_path': './asmcnc/apps/drywall_cutter_app/img/toolpath_offset_on_button.png',
            })
