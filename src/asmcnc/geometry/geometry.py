import math

from asmcnc.comms.logging_system.logging_system import Logger


def compute_polygon_points(sides, circumscribe_rad):
    polygon_vertices = []
    # https://stackoverflow.com/questions/21690008/how-to-generate-random-vertices-to-form-a-convex-polygon-in-c
    x0 = 350
    y0 = 200
    angle_delta_r = (math.pi / 180) * 360.0 / sides
    print ("angle_delta_r ", angle_delta_r)

    angle_r = 0
    while angle_r < 2.0 * math.pi:
        x = x0 + (circumscribe_rad * math.cos(angle_r))
        y = y0 + (circumscribe_rad * math.sin(angle_r))
        Logger.info("{} {}".format(x, y))
        polygon_vertices.append([x, y])
        angle_r += angle_delta_r

    Logger.info(polygon_vertices)
    return polygon_vertices
