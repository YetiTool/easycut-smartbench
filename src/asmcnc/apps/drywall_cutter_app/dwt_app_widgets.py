from kivy.metrics import dp
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image


class ImageButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(ImageButton, self).__init__(**kwargs)


class DryWallImageDropDown(DropDown):
    def __init__(self, name_and_image_dict, callback, **kwargs):
        super(DryWallImageDropDown, self).__init__(**kwargs)

        for key in name_and_image_dict.keys():
            image = ImageButton(
                source=name_and_image_dict[key]["image_path"],
                allow_stretch=True,
                size_hint_y=None,
                height=dp(75),
            )

            image.bind(on_press=self.dismiss)
            image.bind(on_press=lambda x, k=key: callback(k))
            self.add_widget(image)

    def set_options(self, name_and_image_dict):
        self.clear_widgets()
        for key in name_and_image_dict.keys():
            image = ImageButton(
                source=name_and_image_dict[key]["image_path"],
                allow_stretch=True,
                size_hint_y=None,
                height=dp(75),
            )

            image.bind(on_press=self.dismiss)
            image.bind(on_press=lambda x, k=key: self.callback(k))
            self.add_widget(image)


class DryWallImageDropDownButton(ButtonBehavior, Image):
    def __init__(self, name_and_image_dict, callback, **kwargs):
        super(DryWallImageDropDownButton, self).__init__(**kwargs)

        self.source = name_and_image_dict[list(name_and_image_dict.keys())[0]][
            "image_path"
        ]
        self.dropdown = DryWallImageDropDown(name_and_image_dict, callback)
        self.bind(on_release=self.dropdown.open)

    def set_options(self, name_and_image_dict):
        self.dropdown.set_options(name_and_image_dict)
