def get_hsl_by_percentage(percentage):
    return (120 * (1 - percentage)) / 360, 1, 1


def get_gradient(value, max_value, lower_boundary=15, upper_boundary=15, inverse=False):
    abs_percentage = abs(float(value) / float(max_value)) * 100

    if abs_percentage > 100 - upper_boundary:
        return (120 / 360, 1, 1) if inverse else (0, 1, 1)

    if abs_percentage < lower_boundary:
        return (0, 1, 1) if inverse else (120 / 360, 1, 1)

    percentage = float(value) / float(max_value)

    return get_hsl_by_percentage(percentage)


def calculate_width(value, max_value, factor, outer_box_width):
    if value == -999:
        return 0

    value = value / factor

    if value > max_value:
        return ((outer_box_width / max_value) * value) / 2

    return ((outer_box_width / max_value) * value) / 2
