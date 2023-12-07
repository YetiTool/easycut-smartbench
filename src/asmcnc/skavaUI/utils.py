from kivy.core.window import Window


def get_scaled_width(width):
    if width is None:
        return None
    return float(width) / 800.0 * Window.width


def get_scaled_height(height):
    if height is None:
        return None
    return float(height) / 480.0 * Window.height
