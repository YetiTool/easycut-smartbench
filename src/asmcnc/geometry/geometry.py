import math


def compute_polygon_points(sides, circumscribe_rad):
    polygon_vertices = []
    x0 = 350
    y0 = 200
    angle_delta_r = math.pi / 180 * 360.0 / sides
    print(("angle_delta_r ", angle_delta_r))
    angle_r = 0
    while angle_r < 2.0 * math.pi:
        x = x0 + circumscribe_rad * math.cos(angle_r)
        y = y0 + circumscribe_rad * math.sin(angle_r)
        print("{} {}".format(x, y))
        polygon_vertices.append([x, y])
        angle_r += angle_delta_r
    print(polygon_vertices)
    return polygon_vertices
