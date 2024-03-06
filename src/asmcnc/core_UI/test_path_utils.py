import unittest
from path_utils import get_path

class TestPathUtils(unittest.TestCase):

    def setUp(self):
        self.root = "/c:/Users/benji/Documents/"

    def test_get_path_files_only(self):
        target_dir = "router_machine.py"
        result = get_path(target_dir, files_only=True)
        self.assertEqual(result, self.root + "/easycut-smartbench/src/asmcnc/comms/router_machine.py")

    def test_get_path_folders_only(self):
        target_dir = "skavaUI"
        result = get_path(target_dir, folders_only=True)
        self.assertEqual(result, "/c:/Users/benji/Documents/easycut-smartbench/src/asmcnc/skavaUI")

    def test_get_path_first_result_only(self):
        target_dir = "test_dir"
        result = get_path(target_dir, first_result_only=True)
        self.assertEqual(result, "/c:/Users/benji/Documents/easycut-smartbench/src/asmcnc/core_UI/test_dir")

    def test_get_path_multiple_paths(self):
        target_dir = "test_dir"
        result = get_path(target_dir)
        self.assertIsInstance(result, list)
        self.assertIn("/c:/Users/benji/Documents/easycut-smartbench/src/asmcnc/core_UI/test_dir", result)

    def test_get_path_not_found(self):
        target_dir = "nonexistent_dir"
        result = get_path(target_dir)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()