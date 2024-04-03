from typing import Dict, Tuple

# A dictionary that contains the colors that can be used in the application.
# Add more colors where required.
Colours = {
    "white": (1.0, 1.0, 1.0, 1.0),
    "black": (0.0, 0.0, 0.0, 1.0),
    "green": (76 / 255., 175 / 255., 80 / 255., 1.0),
    "red": (230 / 255., 74 / 255., 25 / 255., 1.0),
}  # type: Dict[str, Tuple[float, float, float, float]]


class ColorProvider(object):
    """A provider for colors that can be used in the application.

    Methods
    -------
    get_rgba(color_name)
        Get the color by name in rgba format.
    get_color_hex(color_name)
        Get the color by name in hex format.
    get_color(color_name)
        Get the Color object by name.
    get_markup_color_string(text, color_name)
        Get a markup string that can be used in labels.
    """

    @staticmethod
    def get_rgba(color_name):
        """
        Get the color by name in rgba format. The color is represented as a tuple of floats (r, g, b, a).
        Use this method when making labels/widgets e.g. Label(color=ColorProvider.get_rgba("green")).

        :param color_name: The name of the color.
        :return: The color in rgba format.
        :raises KeyError: If the color name is not found in the color provider.
        """
        try:
            rgba = Colours[color_name.lower()]
        except KeyError:
            raise KeyError("Color name not found in the color provider.")

        return rgba

    @staticmethod
    def get_color_hex(color_name):
        """
        Get the color by name in hex format.
        Avoid using this method if you don't need to. Use get_rgba or get_markup_color_string instead.

        :param color_name: The name of the color.
        :return: The color in hex format.
        :raises KeyError: If the color name is not found in the color provider.
        """
        try:
            color = Colours[color_name.lower()]
        except KeyError:
            raise KeyError("Color name not found in the color provider.")

        return "#{:02x}{:02x}{:02x}".format(int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))

    @staticmethod
    def get_markup_color_string(text, color_name):
        """
        Get a markup string that can be used in labels. It is in the format [color=hex]text[/color].

        :param text: The text to be colored.
        :param color_name: The name of the color.
        :return: The markup string.
        :raises KeyError: If the color name is not found in the color provider.
        """
        try:
            color_hex = ColorProvider.get_color_hex(color_name)
        except KeyError:
            raise KeyError("Color name not found in the color provider.")

        return "[color={}]{}[/color]".format(color_hex, text)
