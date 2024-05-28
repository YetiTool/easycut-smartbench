from asmcnc.comms.logging_system.logging_system import Logger

current_position = {"X": 10, "Y": 10, "Z": 10}


def if_less_than_coord(expected_pos):
    if current_position["X"] < expected_pos:
        return True
    else:
        return False


def if_more_than_coord(expected_pos):
    if current_position["X"] > expected_pos:
        return True
    else:
        return False


detection_too_late = {
    "X": if_more_than_coord,
    "Y": if_more_than_coord,
    "Z": if_less_than_coord,
}
if detection_too_late["X"](100):
    Logger.info("YES")
else:
    Logger.info("NO")
