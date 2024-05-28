from kivy.core.window import Window
from kivy.metrics import dp

Width = Window.width if Window.width in [1280, 800] else 800
Height = Window.height - 32 if Window.height == 800 else 480


def is_screen_big():
    """
    Check whether the screen is Console XL (1280x768) or Console (800x480)

    :return: True if the screen is 1280x768, False if the screen is 800x480
    """
    return Height == 768


def get_scaled_width(width):
    """
    Returns the scaled width of the given width, relative to the current console screen size
    :param width: The width in pixels, based on a 800x480 screen
    :return: The scaled width
    """
    if width is None:
        return None
    if width is 0:
        return 0
    return float(width) / 800.0 * Width


def get_scaled_dp_width(width):
    return dp(get_scaled_width(width))


def get_scaled_height(height):
    """
    Returns the scaled height of the given height, relative to the current console screen size
    :param height: The height in pixels, based on a 800x480 screen
    :return: The scaled height
    """
    if height is None:
        return None
    if height is 0:
        return 0
    return float(height) / 480.0 * Height


def get_scaled_dp_height(height):
    return dp(get_scaled_height(height))


def get_scaled_tuple(tup, orientation="horizontal"):
    """
    Returns the scaled tuple of the given tuple, relative to the current console screen size
    This function is helpful for scaling the padding, margin, border, and pos properties of widgets

    :param tup: The tuple to be scaled
    :param orientation: The orientation of the layout (horizontal or vertical)
    :return: The scaled tuple
    """
    if tup is None:
        return None
    if type(tup) is not tuple:
        if type(tup) is int or type(tup) is float:
            return (
                get_scaled_width(tup)
                if orientation == "horizontal"
                else get_scaled_height(tup)
            )
    if len(tup) == 2:
        return get_scaled_width(tup[0]), get_scaled_height(tup[1])
    if len(tup) == 4:
        return (
            get_scaled_width(tup[0]),
            get_scaled_height(tup[1]),
            get_scaled_width(tup[2]),
            get_scaled_height(tup[3]),
        )


def get_scaled_sp(sp_str):
    """
    Takes a string of a sp font size, such as "20sp", and returns the scaled sp font size
    :param sp_str: The sp font size to be scaled
    :return: The scaled sp font size
    """
    if sp_str is None:
        return None
    return str(float(sp_str[:-2]) / 800.0 * Width) + "sp"
