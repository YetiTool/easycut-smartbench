from kivy.metrics import dp
from kivy.properties import DictProperty, ObjectProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image


class ImageButton(ButtonBehavior, Image):
    pass


class ImageDropDown(DropDown):
    def __init__(self, image_dict, callback, key_name, **kwargs):
        super(ImageDropDown, self).__init__(**kwargs)

        for key in image_dict.keys():
            image = ImageButton(
                source=image_dict[key]['image_path'],
                allow_stretch=True,
                size_hint_y=None,
                height=dp(75),
            )

            image.bind(on_release=self.dismiss)

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
        # this is needed because the properties are set in the kv file
        # idk how to do it better
        if self.callback == ObjectProperty(None) or self.key_name == StringProperty(
                '') or self.image_dict == DictProperty({}):
            return

        self.dropdown = ImageDropDown(self.image_dict, self.callback, self.key_name)

    def on_release(self):
        self.dropdown.open(self)
