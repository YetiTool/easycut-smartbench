from kivy.core.window import Window


def get_scaled_width(width):
    return float(width) / Window.width * Window.width


def get_scaled_height(height):
    return float(height) / Window.height * Window.height
