from asmcnc.comms.logging_system.logging_system import Logger

try:
    from typing import Dict, List
except ImportError:
    Logger.warning("Typing module not available.")
"""
A provider for colours that can be used in the application.
Note "Color(s)" spelling is used to keep the naming consistent with Kivy's Color class.

Usage:
-------
Python :
    from asmcnc.core_UI.utils import color_provider
    Label(color=color_provider.get_rgba("green"))

Kivy Builder :
    #:import color_provider asmcnc.core_UI.utils.color_provider
    Label:
        color: color_provider.get_rgba("green")

Functions
-------
get_rgba(color_name) -> List[float, float, float, float]
    Get the color by name in rgba format.
get_hex(color_name) -> str
    Get the color by name in hex format.
get_markup_string(text, color_name) -> str
    Get a markup string that can be used in labels.
    
Constants
-------
Colors : Dict[str, List[float, float, float, float]]
    A dictionary that contains the colors that can be used in the application.
    
Supporting Documentation
-------
Easycut software colour reference document:
https://docs.google.com/document/d/1bxCR3nOPByPlx_WBANi2rIB2xXZaYjnaPVMcbkC5j_0

Information on Kivy's Color class:
https://kivy.org/doc/stable/api-kivy.graphics.html
"""
Colors = {
    "white": [1.0, 1.0, 1.0, 1.0],
    "black": [0.0, 0.0, 0.0, 1.0],
    "green": [76 / 255.0, 175 / 255.0, 80 / 255.0, 1.0],
    "red": [230 / 255.0, 74 / 255.0, 25 / 255.0, 1.0],
    "primary": [13 / 255.0, 71 / 255.0, 161 / 255.0, 1.0],
    "primary_light": [84 / 255.0, 114 / 255.0, 211 / 255.0, 1.0],
    "primary_dark": [0 / 255.0, 33 / 255.0, 113 / 255.0, 1.0],
    "secondary": [255 / 255.0, 109 / 255.0, 0.0, 1.0],
    "secondary_light": [255 / 255.0, 158 / 255.0, 64 / 255.0, 1.0],
    "secondary_dark": [196 / 255.0, 60 / 255.0, 0.0, 1.0],
    "yellow": [240.0 / 255, 1, 0, 1],
    "grey": [229 / 255.0, 229 / 255.0, 229 / 255.0, 1.0],
    "blue": [25 / 255.0, 118 / 255.0, 210 / 255.0, 1.0],
    "dark_grey": [51 / 255.0, 51 / 255.0, 51 / 255.0, 1.0],
}


def get_rgba(color_name):
    """
    Get the color by name in rgba format. The color is represented as a list of floats [r, g, b, a].
    Use this method when making labels/widgets e.g. Label(color=color_provider.get_rgba("green")).

    :param color_name: The name of the color.
    :return: The color in rgba format.
    :raises KeyError: If the color name is not found in the color provider.
    """
    try:
        rgba = Colors[color_name.lower()]
    except KeyError:
        raise KeyError("Color name not found in the color provider.")
    return rgba


def get_hex(color_name):
    """
    Get the color by name in hex format.
    Avoid using this method if you don't need to. Use get_rgba or get_markup_color_string instead.

    :param color_name: The name of the color.
    :return: The color in hex format.
    :raises KeyError: If the color name is not found in the color provider.
    """
    color = get_rgba(color_name)
    return "#{:02x}{:02x}{:02x}".format(
        int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)
    )


def get_markup_string(text, color_name):
    """
    Get a markup string that can be used in labels. It is in the format [color=hex]text[/color].

    :param text: The text to be colored.
    :param color_name: The name of the color.
    :return: The markup string.
    :raises KeyError: If the color name is not found in the color provider.
    """
    color_hex = get_hex(color_name)
    return "[color={}]{}[/color]".format(color_hex, text)
