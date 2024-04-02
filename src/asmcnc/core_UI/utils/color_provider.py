
class ColorProvider(object):
    """Class for providing colors for the software. This class is a singleton.

    * Usage:
    color_provider = ColorProvider()
    color_provider.get_color("white")

    * Usage in Kivy Builder:
    background_color: app.color_provider.get_color("OK_GREEN")
    """

    _instance = None

    DEFINED_COLORS = {
        "white": [1, 1, 1, 1],
        "black": [0, 0, 0, 1],
        "button_green": [76 / 255., 175 / 255., 80 / 255., 1.0],
        "button_red": [230 / 255., 74 / 255., 25 / 255., 1.0],
    }  # STORE COLORS AS RGBA VALUES (0-1 range as per Kivy)

    def __new__(cls):
        """Create a new instance of the ColorProvider if one doesn't already exist."""
        if cls._instance is None:
            cls._instance = super(ColorProvider, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def get_color(self, color_name):
        """Get a color from the color provider.
        :param color_name: The name of the color to get.
        :return: The color as a list of RGBA values."""
        try:
            return self.DEFINED_COLORS[color_name.lower()]
        except KeyError:
            raise KeyError("Color name not found in the color provider.")

    def get_color_hex(self, color_name):
        """Get a color from the color provider as a hex string.
        :param color_name: The name of the color to get.
        :return: The color as a hex string."""
        color = self.get_color(color_name)
        return "#{:02x}{:02x}{:02x}".format(int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))

    def get_markup_color_string(self, color_name, text):
        """Get a markup string for a color.
        Format: [color=hex]text[/color]
        :param color_name: The name of the color to get.
        :param text: The text to apply the color to.
        :return: The text with the color applied."""
        return "[color={}]{}[/color]".format(self.get_color_hex(color_name), text)


if __name__ == "__main__":
    color_provider = ColorProvider()
    print(color_provider.get_color("button_green"))
    print(color_provider.get_color_hex("button_green"))
    print(color_provider.get_markup_color_string("button_green", "Hello, World!"))
