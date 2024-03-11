import unittest
import sys

sys.path.append('./src')
from asmcnc.core_UI.path_utils import get_path

class TestPathUtils(unittest.TestCase):

    def test_get_path_files_only(self):
        target_dir = "router_machine.py"
        expected_result = "/easycut-smartbench/src/asmcnc/comms/router_machine.py"
        result = get_path(target_dir, files_only=True)
        self.assertIn(expected_result, result)

    def test_get_path_folders_only(self):
        target_dir = "skavaUI"
        expected_result = "/easycut-smartbench/src/asmcnc/skavaUI"
        result = get_path(target_dir, folders_only=True)
        self.assertIn(expected_result, result) 

    def test_get_path_first_result_only(self):
        target_dir = "img"
        expected_result = "easycut-smartbench/src/asmcnc/apps/drywall_cutter_app/img"
        result = get_path(target_dir, first_result_only=True)
        self.assertIn(expected_result, result) 

    def test_directory_in_target(self):
        target_dir = "skavaUI/img"
        expected_result = "easycut-smartbench/src/asmcnc/skavaUI/img"
        result = get_path(target_dir)
        self.assertIn(expected_result, result)

    def test_get_path_not_found(self):
        target_dir = "nonexistent_dir"
        result = get_path(target_dir)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()