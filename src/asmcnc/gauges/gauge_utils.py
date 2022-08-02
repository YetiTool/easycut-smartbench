def get_hsl_by_percentage(percentage):
    return (120 * (1-percentage)) / 360, 1, 1


def get_gradient(value, max_value, lower_boundary=15, upper_boundary=15, inverse=False):
    abs_percentage = abs(float(value) / float(max_value)) * 100

    if abs_percentage > 100 - upper_boundary:
        return (1/3, 1, 1) if inverse else (0, 1, 1)

    if abs_percentage < lower_boundary:
        return (0, 1, 1) if inverse else (1/3, 1, 1)

    return get_hsl_by_percentage(abs_percentage)


def calculate_width(value, max_value, factor):
    if value == -999:
        return 0

    value = value / factor

    if value > max_value:
        return max_value

    return value
