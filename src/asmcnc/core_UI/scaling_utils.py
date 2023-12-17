from kivy.core.window import Window


def is_screen_big():
    return Window.height == 800


def get_scaled_width(width):
    if width is None:
        return None
    if width is 0:
        return 0
    return float(width) / 800.0 * Window.width


def get_scaled_height(height):
    if height is None:
        return None
    if height is 0:
        return 0
    return float(height) / 480.0 * Window.height


def get_scaled_tuple(tup, orientation="horizontal"):
    if tup is None:
        return None

    if type(tup) is not tuple:
        if type(tup) is int or type(tup) is float:
            return get_scaled_width(tup) if orientation == "horizontal" else get_scaled_height(tup)

    if len(tup) == 2:
        return get_scaled_width(tup[0]), get_scaled_height(tup[1])

    if len(tup) == 4:
        return (get_scaled_width(tup[0]), get_scaled_height(tup[1]),
                get_scaled_width(tup[2]), get_scaled_height(tup[3]))


def get_scaled_sp(sp_str):
    if sp_str is None:
        return None
    return str(float(sp_str[:-2]) / 800.0 * Window.width) + "sp"
