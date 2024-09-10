import unittest
import json
import tempfile
import os
import copy
import sys

sys.path.append('./src')

from apps.drywall_cutter_app.config import config_loader


"""
RUN WITH
python tests/automated_unit_tests/apps/dwt/test_dwt_config_checking.py
FROM EASYCUT-SMARTBENCH DIR
"""


class TestDWTConfigChecking(unittest.TestCase):
    def setUp(self):
        self.valid_temp_json_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        self.invalid_temp_json_file = tempfile.NamedTemporaryFile(mode='w', delete=False)

        j_obj = {
            "cutting_depths": {
                "bottom_offset": 0.5,
                "auto_pass": True,
                "depth_per_pass": 1.0,
                "material_thickness": 3.0
            },
            "toolpath_offset": "in",
            "canvas_shape_dims": {
                "y": 20,
                "x": 10,
                "r": 5,
                "d": 15,
                "l": 30
            },
            "shape_type": "rectangle",
            "cutter_type": "tool_6mm.json",
            "units": "mm",
            "rotation": "horizontal",
            "datum_position": {
                "y": 5,
                "x": 5
            }
        }

        invalid_j_obj = copy.deepcopy(j_obj)
        invalid_j_obj.pop('rotation')

        self.valid_temp_json_file.write(json.dumps(
            j_obj,
            indent=4,
            sort_keys=True
        ))

        self.invalid_temp_json_file.write(json.dumps(
            invalid_j_obj,
            indent=4,
            sort_keys=True
        ))

        self.valid_temp_json_file.close()
        self.invalid_temp_json_file.close()

    def tearDown(self):
        os.remove(self.valid_temp_json_file.name)

    def test_check_valid_config(self):
        dwt_config = config_loader.DWTConfig()

        self.assertTrue(dwt_config.is_valid_configuration(self.valid_temp_json_file.name))

    def test_check_invalid_config(self):
        dwt_config = config_loader.DWTConfig()

        self.assertFalse(dwt_config.is_valid_configuration(self.invalid_temp_json_file.name))

    def test_fix_valid_config(self):
        dwt_config = config_loader.DWTConfig()

        dwt_config.fix_config(self.invalid_temp_json_file.name)

        self.assertTrue(dwt_config.is_valid_configuration(self.invalid_temp_json_file.name))

    def test_fix_already_valid_config(self):
        dwt_config = config_loader.DWTConfig()

        dwt_config.fix_config(self.valid_temp_json_file.name)

        self.assertTrue(dwt_config.is_valid_configuration(self.valid_temp_json_file.name))


if __name__ == '__main__':
    unittest.main()