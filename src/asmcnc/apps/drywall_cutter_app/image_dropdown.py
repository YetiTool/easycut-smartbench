from collections import OrderedDict

from kivy.metrics import dp
from kivy.properties import DictProperty, ObjectProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image
from asmcnc.comms.logging_system.logging_system import Logger
from asmcnc import paths



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
    disable_if_1_option = False

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

        if self.disable_if_1_option:
            self.disabled = len(self.image_dict) < 2

    def on_release(self):
        self.dropdown.open(self)

    def set_image(self, image_path):
        self.source = image_path

    def set_image_dict(self, image_dict):
        self.image_dict = image_dict

    def set_key(self, key):
        self.key_name = key


class ToolSelectionDropDown(ImageDropDownButton):
    def __init__(self, **kwargs):
        super(ToolSelectionDropDown, self).__init__(**kwargs)
        self.source = paths.get_resource('tool_6mm.png')
        self.key_name = 'cutter_path'
        self.screen = None


class ShapeSelectionDropDown(ImageDropDownButton):
    def __init__(self, **kwargs):
        super(ShapeSelectionDropDown, self).__init__(**kwargs)
        self.source = paths.get_resource('square_shape_button.png')
        self.key_name = 'key'
        self.screen = None


class ToolPathSelectionDropDown(ImageDropDownButton):
    def __init__(self, **kwargs):
        super(ToolPathSelectionDropDown, self).__init__(**kwargs)
        self.source = paths.get_resource('toolpath_offset_inside_button.png')
        self.key_name = 'key'
        self.screen = None
        self.disable_if_1_option = True
