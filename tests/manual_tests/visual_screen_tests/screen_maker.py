"""
@author archiejarvis on 05/07/2023
"""

import ast
import inspect


def get_required_parameters(clazz):
    file_path = inspect.getfile(clazz)

    # File path is ___.py, so ends at rightmost y, this fixes random funkiness
    file_path = file_path[: file_path.rfind("y") + 1]

    with open(file_path, "r") as f:
        tree = ast.parse(f.read())

    required_parameters = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "__init__":
            for statement in node.body:
                if (
                    isinstance(statement, ast.Assign)
                    and len(statement.targets) == 1
                    and isinstance(statement.targets[0], ast.Attribute)
                    and isinstance(statement.value, ast.Subscript)
                    and statement.targets[0].value.id == "self"
                    and statement.value.value.id == "kwargs"
                ):
                    required_parameters.append(statement.value.slice.value.s)

    return required_parameters


class ScreenMaker(object):
    param_map = {}

    def __init__(
        self, sm, l, kb, sett, jd, m, yp, db, am, sc, systemtools_sm, start_seq
    ):
        self.param_map["screen_manager"] = sm
        self.param_map["sm"] = sm
        self.param_map["localization"] = l
        self.param_map["keyboard"] = kb
        self.param_map["settings"] = sett
        self.param_map["job"] = jd
        self.param_map["machine"] = m
        self.param_map["m"] = m
        self.param_map["yetipilot"] = yp
        self.param_map["database"] = db
        self.param_map["calibration_db"] = db
        self.param_map["server_connection"] = sc
        self.param_map["app_manager"] = am
        self.param_map["systemtools"] = systemtools_sm
        self.param_map["start_sequence"] = start_seq
        self.param_map["consent_manager"] = self

    def create_screen(self, clazz, name):
        parameters = get_required_parameters(clazz)

        for parameter in parameters:
            if parameter not in self.param_map:
                raise Exception("Missing parameter: " + parameter)

        parameter_dict = {"name": name}

        for parameter in parameters:
            parameter_dict[parameter] = self.param_map[parameter]

        return clazz(**parameter_dict)
