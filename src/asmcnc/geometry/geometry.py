import math
from asmcnc.comms.logging_system.logging_system import Logger


def compute_polygon_points(sides, circumscribe_rad):
    polygon_vertices = []
    x0 = 350
    y0 = 200
    angle_delta_r = math.pi / 180 * 360.0 / sides
    Logger.debug("angle_delta_r ", angle_delta_r)
    angle_r = 0
    while angle_r < 2.0 * math.pi:
        x = x0 + circumscribe_rad * math.cos(angle_r)
        y = y0 + circumscribe_rad * math.sin(angle_r)
        Logger.debug("{} {}".format(x, y))
        polygon_vertices.append([x, y])
        angle_r += angle_delta_r
    Logger.debug(polygon_vertices)
    return polygon_vertices
